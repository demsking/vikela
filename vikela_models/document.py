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
import uuid
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Any
from typing import Generic
from typing import Literal
from typing import TypeVar

from dataclasses_json import dataclass_json
from dataclasses_json import DataClassJsonMixin
from dataclasses_json import Undefined


@dataclass
class BaseMeta(DataClassJsonMixin):
  created_at: str = field(default_factory=lambda: datetime.now().isoformat())
  updated_at: str | None = field(default=None)


@dataclass
class UserMeta(DataClassJsonMixin):
  uid: str
  created_at: str = field(default_factory=lambda: datetime.now().isoformat())
  updated_at: str | None = field(default=None)


Data = TypeVar('Data', bound=DataClassJsonMixin)
Computed = TypeVar('Computed', bound=DataClassJsonMixin)
Meta = TypeVar('Meta', bound=Literal[BaseMeta, UserMeta])


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Document(Generic[Data, Computed, Meta], DataClassJsonMixin):
  type: str
  data: Data
  _id: str = field(default_factory=lambda: str(uuid.uuid4()))
  _rev: str | None = None
  computed: Computed | None = None
  meta: Meta = field

  @classmethod
  def create_alias_from_user_meta(
    cls: type['Document[Data, Computed, Meta]'],
    data_cls: type[Data],
    computed_cls: type[Computed] | None = None,
    meta_cls: type[BaseMeta] = BaseMeta,
  ) -> 'Document[Data, Computed, UserMeta]':
    return cls.create_alias_from_base_meta(
      data_cls=data_cls,
      computed_cls=computed_cls,
      meta_cls=UserMeta,
    )

  @classmethod
  def create_alias_from_base_meta(
    cls: type['Document[Data, Computed, Meta]'],
    data_cls: type[Data],
    computed_cls: type[Computed] | None = None,
    meta_cls: type[BaseMeta] = BaseMeta,
  ) -> 'Document[Data, Computed, Meta]':
    # pylint: disable=arguments-renamed
    # pylint: disable=arguments-differ
    base_cls = cls

    @dataclass
    class WrappedDocument(base_cls):
      @staticmethod
      def parse_data(raw_data: dict[str, Any] | data_cls):
        if isinstance(raw_data, dict):
          document_data = data_cls.from_dict(raw_data)
        else:
          document_data = raw_data

        return document_data

      @staticmethod
      def parse_meta(raw_meta: dict[str, Any] | meta_cls):
        if isinstance(raw_meta, dict):
          document_meta = meta_cls.from_dict(raw_meta)
        else:
          document_meta = raw_meta

        return document_meta

      @staticmethod
      def parse_computed(raw_computed: dict[str, Any] | computed_cls):
        if isinstance(raw_computed, dict):
          computed_object = computed_cls.from_dict(raw_computed)
        else:
          computed_object = raw_computed

        return computed_object

      @classmethod
      def from_dict(cls, raw: dict[str, Any]):
        doc = base_cls.from_dict({
          **raw,
          'data': {},
          'meta': {},
          'computed': None,
        })

        doc.data = cls.parse_data(raw['data'])
        doc.meta = cls.parse_meta(raw['meta'])

        if computed_cls and 'computed' in raw:
          doc.computed = cls.parse_computed(raw['computed'])

        return doc

      @classmethod
      def from_json(cls, raw: str):
        data_dict = json.loads(raw)
        return cls.from_dict(data_dict)

      @staticmethod
      def to_dict():
        return cls.to_dict()  # pylint: disable=no-value-for-parameter

      @staticmethod
      def to_json():
        return cls.to_json()  # pylint: disable=no-value-for-parameter

    return WrappedDocument


GenericDocument = Document[dict, None, BaseMeta]
GenericUserDocument = Document[dict, None, UserMeta]
