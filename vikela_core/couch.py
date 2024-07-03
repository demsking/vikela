# Copyright 2024 Sébastien Demanou. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import json
import logging
from typing import Any
from typing import Literal

import httpx

from .client import HttpClient
from vikela_models.couch import CreateSessionResponse
from vikela_models.couch import DesignDocument
from vikela_models.couch import Document
from vikela_models.couch import DocumentViewResponse
from vikela_models.couch import FilterDocument
from vikela_models.couch import FindResponse
from vikela_models.couch import GenericResponse
from vikela_models.couch import GetNodeVersionResponse
from vikela_models.couch import GetSessionResponse
from vikela_models.couch import IdentifiedDocument
from vikela_models.couch import MaybeDocument
from vikela_models.couch import OkResponse


Headers = httpx.Headers


class CouchServer:
  def __init__(
    self,
    url: str,
    *,
    useragent: str,
    dbuser: str | None = None,
    roles: str | None = None,
    authtoken: str | None = None,
    logger: logging.Logger | None = None,
  ) -> None:
    headers = {
      'User-Agent': useragent,
    }

    if dbuser:
      headers['X-Auth-CouchDB-UserName'] = dbuser

    if roles:
      headers['X-Auth-CouchDB-Roles'] = roles

    if authtoken:
      headers['X-Auth-CouchDB-Token'] = authtoken

    self.client = HttpClient(
      base_url=url,
      headers=headers,
      logger=logger,
    )

    self.session = CouchSessionDatabase(self)

  @property
  def url(self) -> str:
    return self.client.base_url

  async def exists(self, dbname: str, headers: Headers | None = None) -> bool:
    try:
      await self.client.get(f'/{dbname}', headers=headers)
      return True
    except httpx.HTTPStatusError:
      return False

  async def create(self, dbname: str, headers: Headers | None = None) -> OkResponse:
    response = await self.client.put(f'/{dbname}', headers=headers)

    return OkResponse.from_json(response.text)

  async def destroy(self, dbname: str, headers: Headers | None = None) -> OkResponse:
    response = await self.client.delete(f'/{dbname}', headers=headers)

    return OkResponse.from_json(response.text)

  async def version(self, headers: Headers | None = None) -> GetNodeVersionResponse:
    response = await self.client.get('/_node/_local/_versions', headers=headers)

    return GetNodeVersionResponse.from_json(response.text)

  def use(self, dbname: str) -> 'CouchDatabase':
    return CouchDatabase(dbname, self)

  async def terminate(self) -> None:
    await self.client.aclose()


class CouchSessionDatabase:
  def __init__(
    self,
    server: CouchServer,
  ) -> None:
    self.name = '_session'
    self.server = server

  async def create_session(
    self,
    *,
    username: str,
    password: str,
    headers: Headers | None = None,
  ) -> tuple[CreateSessionResponse, str]:
    """
    Initiates new session for specified user credentials by providing Cookie
    value.

    See https://docs.couchdb.org/en/stable/api/server/authn.html#post--_session
    """
    response = await self.server.client.post(
      f'/{self.name}',
      headers=headers,
      json={
        'name': username,
        'password': password,
      },
    )

    set_cookie = response.headers.get('Set-Cookie')

    return CreateSessionResponse.from_json(response.text), set_cookie

  async def get_session(
    self,
    *,
    headers: Headers | None = None,
  ) -> GetSessionResponse:
    """
    Returns information about the authenticated user, including a
    [User Context Object](https://docs.couchdb.org/en/stable/json-structure.html#userctx-object),
    the authentication method and database that were used, and a list of
    configured authentication handlers on the server.

    See https://docs.couchdb.org/en/stable/api/server/authn.html#get--_session
    """
    response = await self.server.client.get(
      f'/{self.name}',
      headers=headers,
    )

    return GetSessionResponse.from_json(response.text)

  async def delete_session(
    self,
    *,
    headers: Headers | None = None,
  ) -> OkResponse:
    """
    Closes user's session by instructing the browser to clear the cookie. This
    does not invalidate the session from the server's perspective, as there is
    no way to do this because CouchDB cookies are stateless. This means calling
    this endpoint is purely optional from a client perspective, and it does not
    protect against theft of a session cookie.

    See https://docs.couchdb.org/en/stable/api/server/authn.html#delete--_session
    """
    response = await self.server.client.delete(
      f'/{self.name}',
      headers=headers,
      params={},
    )

    return OkResponse.from_json(response.text)


class CouchDatabase:
  def __init__(
    self,
    dbname: str,
    server: CouchServer,
  ) -> None:
    self.name = dbname
    self.server = server

  async def delete(
    self,
    docid: str,
    *,
    rev: str | None = None,
    batch: str | None = None,
    headers: Headers | None = None,
  ) -> GenericResponse:
    response = await self.server.client.delete(
      f'/{self.name}/{docid}',
      headers=headers,
      params={
        'rev': rev,
        'batch': batch,
      },
    )

    return GenericResponse.from_json(response.text)

  async def bulk(
    self,
    docs: list[dict[str, Any]],
    new_edits=False,
    headers: Headers | None = None,
  ) -> list:
    """
    Insert multiple documents in a single.

    Args:
      docs: A list of documents to be inserted into the database.
      new_edits: Whether to create new revisions of the documents or use the existing ones.
        If True, the server will create a new revision for each document in the list of documents.
        If False, the server will use the existing revision of each document in the list of documents.
        If the server does not have a revision for each document in the list of documents, it will return an error.
        If the server does not have a revision for each document in the list of documents and new_edits is True, it will return an error.
        If the server does not have a revision for each document in the list of documents and new_edits is False, it will return an error.
    """
    response = await self.server.client.post(f'/{self.name}/_bulk_docs', headers=headers, json={
      'docs': docs,
      'new_edits': new_edits,
    })

    return response.json()

  async def insert(
    self,
    document: Document | IdentifiedDocument | MaybeDocument | DesignDocument | FilterDocument | dict,
    *,
    rev: str | None = None,
    headers: Headers | None = None,
  ) -> GenericResponse:
    """
    Insert a new document into the database.

    Args:
      document: The document to be inserted into the database.
      rev: The revision of the document to be inserted into the database.
    """
    path = f'/{self.name}'
    method = 'POST'

    if hasattr(document, 'to_dict'):
      data = document.to_dict()
    else:
      data = document

    if '_rev' in data:
      del data['_rev']

    if isinstance(document, dict):
      if document.get('_id'):
        path += f'/{document["_id"]}'
        method = 'PUT'
    elif isinstance(document, IdentifiedDocument):
      if hasattr(document, '_id') and document._id:
        path += f'/{document._id}'  # pylint: disable=protected-access
        method = 'PUT'

    response = await self.server.client.request(
      method=method,
      url=path,
      json=data,
      headers=headers,
      params={'rev': rev} if rev else {},
    )

    return GenericResponse.from_json(response.text)

  async def insert_att(
    self,
    docid: str,
    *,
    attname: str,
    rev: str,
    data: Any,
    content_type: str = 'application/octet-stream',
    headers: Headers | None = None,
  ) -> GenericResponse:
    """
    Insert an attachment into the database.

    Args:
      docid: The document id of the attachment to be inserted into the database.
      attname: The name of the attachment to be inserted into the database.
      rev: The revision of the attachment to be inserted into the database.
      data: The attachment to be inserted into the database.
      content_type: The content type of the attachment to be inserted into the database.
        Defaults to 'application/octet-stream'.

    Documentation: https://docs.couchdb.org/en/latest/api/document/attachments.html#put--db-docid-attname
    """
    _headers = headers or {}
    _headers.update({
      'Content-Type': content_type,
    })

    response = await self.server.client.put(
      f'/{self.name}/{docid}/{attname}',
      data=data,
      params={'rev': rev} if rev else {},
      headers=_headers,
    )

    return GenericResponse.from_json(response.text)

  async def delete_att(
    self,
    docid: str,
    *,
    attname: str,
    rev: str,
    headers: Headers | None = None,
  ) -> GenericResponse:
    """
    Insert an attachment into the database.

    Args:
      docid: The document id of the attachment to be inserted into the database.
      attname: The name of the attachment to be inserted into the database.
      rev: The revision of the attachment to be inserted into the database.

    Documentation: https://docs.couchdb.org/en/latest/api/document/attachments.html#delete--db-docid-attname
    """
    response = await self.server.client.delete(
      f'/{self.name}/{docid}/{attname}',
      params={'rev': rev} if rev else {},
      headers=headers,
    )

    return GenericResponse.from_json(response.text)

  async def fetch(
    self,
    docids: list[str],
    headers: Headers | None = None,
  ) -> DocumentViewResponse:
    response = await self.server.client.post(f'/{self.name}/_all_docs', headers=headers, json={
      'keys': docids,
    })

    return DocumentViewResponse.from_json(response.text)

  async def find(
    self,
    selector: dict[str, Any],
    *,
    fields: list[str] | None = None,
    limit=25,
    skip=0,
    sort: list[str] | None = None,
    use_index: str | list[str] | None = None,
    conflicts=False,
    r=1,
    bookmark: str | None = None,
    update=True,
    stable=True,
    stale: Literal['ok', False] = False,
    execution_stats=False,
    headers: Headers | None = None,
  ) -> FindResponse:
    """
    Find documents using a declarative JSON querying syntax. Queries will use custom indexes,
    specified using the _index endpoint, if available. Otherwise, they use the built-in _all_docs
    index, which can be arbitrarily slow.

    Documentation: https://docs.couchdb.org/en/latest/api/database/find.html#post--db-_find
    """
    query = {
      'selector': selector,
      'fields': fields,
      'limit': limit,
      'skip': skip,
      'sort': sort,
      'use_index': use_index,
      'conflicts': conflicts,
      'r': r,
      'bookmark': bookmark,
      'update': update,
      'stable': stable,
      'stale': stale,
      'execution_stats': execution_stats,
    }
    query = dict(filter(lambda item: item[1] is not None, query.items()))
    response = await self.server.client.post(f'/{self.name}/_find', json=query, headers=headers)
    response_dict: dict = response.json()

    find_response = FindResponse(
      docs=response_dict.get('docs', []),
      bookmark=response_dict.get('bookmark', None),
      warning=response_dict.get('warning', None),
      execution_stats=response_dict.get('execution_stats', None),
    )

    return find_response

  async def revision(self, docid: str, headers: Headers | None = None) -> str:
    """
    Documentation: https://docs.couchdb.org/en/latest/api/document/common.html#head--db-docid
    """
    response = await self.server.client.head(f'/{self.name}/{docid}', headers=headers)

    return json.loads(response.headers['Etag'])

  async def get(
    self,
    docid: str,
    *,
    rev: str | None = None,
    headers: Headers | None = None,
  ) -> dict:
    response = await self.server.client.get(
      f'/{self.name}/{docid}',
      params={'rev': rev} if rev else {},
      headers=headers,
    )

    return response.json()

  async def view(
    self,
    designname: str,
    viewname: str,
    headers: Headers | None = None,
    **kwargs,
  ) -> DocumentViewResponse:
    response = await self.server.client.get(
      f'/{self.name}/_design/{designname}/_view/{viewname}',
      headers=headers,
      **kwargs,
    )

    return DocumentViewResponse.from_json(response.text)

  async def get_ddoc_info(
    self,
    designname: str,
    viewname: str,
    headers: Headers | None = None,
    **kwargs,
  ) -> httpx.Response:
    """
    Returns the HTTP Headers containing a minimal amount of information about
    the specified design document.

    Documentation: https://docs.couchdb.org/en/latest/api/ddoc/common.html#head--db-_design-ddoc
    """
    return await self.server.client.head(
      f'/{self.name}/_design/{designname}',
      headers=headers,
      **kwargs,
    )
