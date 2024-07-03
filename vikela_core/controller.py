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
import uuid
from datetime import datetime
from typing import Any
from typing import Generic
from typing import TypeVar

from dataclasses_json import DataClassJsonMixin
from fastapi import HTTPException
from fastapi import Request

from .couch import CouchDatabase
from .couch import GenericResponse
from vikela_models.document import BaseMeta
from vikela_models.document import Computed
from vikela_models.document import Data
from vikela_models.document import Document
from vikela_models.document import Meta
from vikela_models.document import UserMeta


Payload = TypeVar('Payload', bound=DataClassJsonMixin)


class Controller(Generic[Payload, Data, Computed, Meta]):
  coltype: str
  Document: Document[Data, Computed, Meta] = Document
  PublicDocument: Document[Data, Computed, Meta] | None = None

  def __init__(self, database: CouchDatabase):
    self.database = database
    self.public_document_class: Any = self.PublicDocument or self.Document

  @staticmethod
  def parse_auth_headers(*, username: str, token: str) -> dict:
    return {
      'X-Auth-CouchDB-UserName': username,
      'X-Auth-CouchDB-Token': token,
    }

  def parse_auth_request_headers(self, request: Request) -> dict:
    username = request.headers.get('X-Auth-UserName', '')
    token = request.headers.get('X-Auth-Secret', '')

    if username and token:
      return Controller.parse_auth_headers(username=username, token=token)

    return {}

  def parse_document_id(self, docid: str | None = None) -> str:
    return docid or str(uuid.uuid4())

  def parse_public_document_id(self, docid: str | None = None) -> str:
    return self.parse_document_id(docid)

  def parse_document_data(self, payload: Payload) -> Data:
    return payload

  def parse_public_document_data(self, raw_doc: dict) -> dict:
    return raw_doc['data']

  def parse_document_meta(
    self,
    payload: Payload,
    data: Data,
    request: Request | None = None,
  ) -> BaseMeta:
    return BaseMeta()

  def parse_public_document_meta(
    self,
    raw_doc: dict,
    data: dict,
    request: Request | None = None,
  ) -> BaseMeta:
    return BaseMeta()

  def parse_computed_object(
    self,
    payload: Payload,
    data: Data,
  ) -> DataClassJsonMixin | None:
    value = None  # avoid E1128
    return value

  def parse_public_raw_document(self, raw_doc: dict) -> dict:
    docid = raw_doc['_id']
    document_id = self.parse_public_document_id(docid)
    raw_document_data = self.parse_public_document_data(raw_doc)
    document_data = self.public_document_class.parse_data(
      raw_document_data,
    )

    document_meta = self.parse_public_document_meta(raw_doc, document_data)
    computed_object = self.parse_computed_object(raw_doc, document_data)

    return {
      '_id': document_id,
      '_rev': raw_doc['_rev'],
      'type': self.coltype,
      'data': document_data.to_dict(),
      'meta': document_meta.to_dict(),
      'computed': computed_object,
    }

  def parse_public_document(self, raw_doc: dict) -> Document:
    raw_document = self.parse_public_raw_document(raw_doc)
    public_document = self.public_document_class.from_dict(raw_document)

    return public_document

  def create_raw_document(
    self,
    payload: Payload,
    *,
    docid: str | None = None,
    rev: str | None = None,
    request: Request | None = None,
  ) -> dict:
    document_id = self.parse_document_id(docid)
    document_data = self.parse_document_data(payload)
    document_meta = self.parse_document_meta(payload, document_data, request)
    computed_object = self.parse_computed_object(payload, document_data)

    return {
      '_id': document_id,
      '_rev': rev,
      'type': self.coltype,
      'data': document_data.to_dict(),
      'meta': document_meta.to_dict(),
      'computed': computed_object.to_dict(),
    }

  def create_document(
    self,
    payload: Payload,
    *,
    docid: str | None = None,
    rev: str | None = None,
    request: Request | None = None,
  ) -> Document[Data, Computed, Meta]:
    raw_document = self.create_raw_document(
      payload=payload,
      docid=docid,
      rev=rev,
      request=request,
    )

    return self.Document.from_dict(raw_document)

  async def insert(
    self,
    docid: str | None = None,
    *,
    data: Data,
    request: Request,
  ) -> GenericResponse:
    headers = self.parse_auth_request_headers(request)
    doc = self.create_document(docid=docid, payload=data)

    result = await self.database.insert(doc, headers=headers)
    result.id = self.parse_public_document_id(result.id)

    return result

  async def revision(self, docid: str, request: Request) -> GenericResponse:
    headers = self.parse_auth_request_headers(request)
    docid = self.parse_document_id(docid)
    revision = await self.database.revision(docid, headers=headers)

    return GenericResponse(ok=True, id=docid, rev=revision)

  async def get_document(
    self,
    docid: str,
    *,
    rev: str | None = None,
    request: Request | None = None,
  ) -> Document[Data, Computed, Meta]:
    docid = self.parse_document_id(docid)
    headers = self.parse_auth_request_headers(request)
    raw_doc = await self.database.get(docid, rev=rev, headers=headers)

    return self.Document.from_dict(raw_doc)

  async def get_public_document(
    self,
    docid: str,
    *,
    rev: str | None = None,
    request: Request | None = None,
  ) -> Document[Data, Computed, Meta]:
    docid = self.parse_document_id(docid)
    headers = self.parse_auth_request_headers(request)
    raw_doc = await self.database.get(docid, rev=rev, headers=headers)
    public_doc = self.parse_public_document(raw_doc)

    return public_doc

  def validate_update_data(self, original_data: Data, new_data: Data) -> None:
    pass

  async def update_document_data(
    self,
    docid: str,
    *,
    rev: str | None = None,
    payload: Payload,
    current_doc: Document | None = None,
    request: Request,
  ) -> GenericResponse:
    headers = self.parse_auth_request_headers(request)

    if current_doc:
      doc = current_doc.to_dict()
    else:
      docid = self.parse_document_id(docid)
      doc = await self.database.get(
        docid,
        rev=rev,
        headers=headers,
      )

    previous_data = doc.get('data', {})
    self.validate_update_data(previous_data, payload)
    previous_data.update(payload.to_dict())
    doc_data = self.parse_document_data(payload)
    doc_computed = self.parse_computed_object(payload, doc_data)

    doc['data'] = doc_data.to_dict()
    doc['updated_at'] = datetime.now().isoformat()
    doc['computed'] = doc_computed.to_dict()

    result = await self.database.insert(doc, rev=doc['_rev'], headers=headers)
    result.id = self.parse_public_document_id(result.id)

    return result

  async def delete_document(
    self,
    docid: str,
    *,
    rev: str,
    request: Request,
  ) -> GenericResponse:
    headers = self.parse_auth_request_headers(request)
    docid = self.parse_document_id(docid)

    result = await self.database.delete(docid, rev=rev, headers=headers)
    result.id = self.parse_public_document_id(result.id)

    return result


class ControllerUserMeta(Generic[Payload, Data, Computed], Controller[Payload, Data, Computed, UserMeta]):
  Document: Document[Data, Computed, UserMeta] = Document

  def parse_document_meta_uid(self, request: Request | None = None) -> str:
    uid = None

    if request:
      uid = request.path_params.get('uid') or request.query_params.get('uid')

    if not uid:
      raise HTTPException(400, 'Missing required query param "uid"')

    return uid

  def parse_document_meta(
    self,
    payload: Payload,
    data: Data,
    request: Request | None = None,
  ) -> UserMeta:
    uid = self.parse_document_meta_uid(request)

    return UserMeta(uid=uid)

  def parse_public_document_meta(
    self,
    raw_doc: dict,
    data: dict,
    request: Request | None = None,
  ) -> UserMeta:
    uid = self.parse_document_meta_uid(request)

    return UserMeta(uid=uid)
