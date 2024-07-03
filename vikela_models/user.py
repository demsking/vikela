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
from dataclasses import field
from datetime import datetime
from typing import Literal

from dataclasses_json import dataclass_json
from dataclasses_json import DataClassJsonMixin
from dataclasses_json import Undefined

from .document import Document
from .location import ComputedLocation
from .model import Model


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class UserData(Model):
  email: str
  first_name: str
  last_name: str
  date_of_birth: str
  gender: Literal['male', 'female'] | None = None
  address: str | None = None
  phone_number: str | None = None
  interests: list[str] | None = None
  bio: str | None = None
  profile_picture_url: str | None = None
  social_links: dict | None = None

  @property
  def full_name(self) -> str:
    return f'{self.first_name} {self.last_name}'


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class RegisterPayload(Model):
  username: str
  password: str
  email: str
  first_name: str
  last_name: str
  date_of_birth: str
  gender: Literal['male', 'female'] | None = None
  address: str | None = None
  phone_number: str | None = None
  interests: list[str] | None = None
  bio: str | None = None
  profile_picture_url: str | None = None
  social_links: dict | None = None


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class GetAccessTokenResponse(Model):
  token_type: str
  access_token: str


@dataclass
class TokenData(Model):
  """Contains the username (sub) encoded in the JWT token."""
  sub: str


@dataclass
class AccountMeta(DataClassJsonMixin):
  username: str
  roles: list[str]
  created_at: str = field(default_factory=lambda: datetime.now().isoformat())
  updated_at: str | None = field(default=None)


UserDocumentType = Document[UserData, ComputedLocation, AccountMeta]
UserDocument = UserDocumentType.create_alias_from_base_meta(
  data_cls=UserData,
  meta_cls=AccountMeta,
)
