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
from dataclasses import dataclass
from typing import Any
from typing import Generic
from typing import TypeVar

from dataclasses_json import dataclass_json
from dataclasses_json import DataClassJsonMixin
from dataclasses_json import Undefined


DocumentViewValue = TypeVar('DocumentViewValue')
DocumentViewDoc = TypeVar('DocumentViewDoc', bound=dict)


@dataclass
class DocumentViewResponse(Generic[DocumentViewValue, DocumentViewDoc], DataClassJsonMixin):
  """
  View response.

  Docs: http://docs.couchdb.org/en/latest/api/ddoc/views.html#get--db-_design-ddoc-_view-view
  """
  rows: list[dict[str, Any]]  # List of view row objects
  offset: int | None = None
  total_rows: int | None = None
  update_seq: Any | None = None


@dataclass
class FindResponse(DataClassJsonMixin):
  docs: list[dict]
  warning: str | None = None
  execution_stats: dict | None = None
  bookmark: str | None = None


@dataclass
class GenericResponse(DataClassJsonMixin):
  ok: bool
  id: str
  rev: str


@dataclass
class OkResponse(DataClassJsonMixin):
  ok: bool


@dataclass
class GetNodeVersionResponse(DataClassJsonMixin):
  pass


@dataclass
class MaybeDocument(DataClassJsonMixin):
  _id: str | None = None
  _rev: str | None = None


@dataclass
class IdentifiedDocument(DataClassJsonMixin):
  _id: str


@dataclass
class RevisionedDocument(DataClassJsonMixin):
  _rev: str


@dataclass
class Document(IdentifiedDocument, RevisionedDocument, DataClassJsonMixin):
  pass


@dataclass
class FilterDocument(IdentifiedDocument, DataClassJsonMixin):
  filters: dict[str, str]
  language: str | None = None


@dataclass
class DesignDocumentView(dict[str, str]):
  pass


@dataclass
class DesignDocument(IdentifiedDocument, DataClassJsonMixin):
  views: dict[str, DesignDocumentView]
  language: str | None = None


@dataclass
class CreateSessionResponse(DataClassJsonMixin):
  ok: bool
  name: str
  roles: list[str]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SessionInfo(DataClassJsonMixin):
  authenticated: str
  authentication_handlers: list[str]
  authentication_db: str | None = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class UserCtx(DataClassJsonMixin):
  name: str
  roles: list[str]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetSessionResponse(DataClassJsonMixin):
  info: SessionInfo
  ok: bool
  userCtx: UserCtx
