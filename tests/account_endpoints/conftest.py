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
from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from vikela.controllers.auth import AuthController
from vikela.controllers.auth import UserDocument
from vikela.controllers.auth import UserDocumentInDB


@pytest.fixture
def username():
  return 'um.nyobe@example.com'


@pytest.fixture
def token():
  return 'token-xxx'


@pytest.fixture
def headers(token):
  return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def document_dict():
  return {
    '_id': 'org.couchdb.user:um.nyobe@example.com',
    '_rev': '10-85465b449abe13bfa9a1a314b34f247d',
    'type': 'user',
    'data': {
      'email': 'um.nyobe@example.com',
      'first_name': 'Um',
      'last_name': 'Nyobè',
      'date_of_birth': '200-12-12',
      'gender': 'male',
      'address': 'Douala, Cameroun',
      'phone_number': '+33 663 49 77 80',
      'interests': None,
      'bio': None,
      'profile_picture_url': None,
      'social_links': None
    },
    'computed': {
      'location': {
        'type': 'city',
        'name': 'Douala',
        'boundingbox': [
          3.8829389,
          4.2029389,
          9.5462018,
          9.8662018
        ],
        'lat': 4.0429389,
        'lon': 9.7062018,
        'addresstype': 'city',
        'display_name': 'Douala, Douala II, Communauté urbaine de Douala, Wouri, Littoral, Cameroon',
        'address': {
          'country': 'Cameroon',
          'country_code': 'cm',
          'region': None,
          'postcode': None,
          'road': None,
          'town': None,
          'municipality': 'Communauté urbaine de Douala',
          'county': 'Wouri',
          'state': 'Littoral',
          'city': 'Douala'
        }
      }
    },
    'meta': {
      'hashed_password': '$2b$12$Ocn.lKvR5e2YRNKVmz0.ZeQv/QyoY2NSJVD355ud6z2K8jL/8BW/a',
      'totp_secret': None,
      'created_at': '2024-07-03T22:43:21.783492',
      'updated_at': None
    },
    'name': 'um.nyobe@example.com',
    'roles': [
      'user'
    ],
    'updated_at': '2024-07-03T22:47:59.149132'
  }


@pytest.fixture
def document(document_dict):
  return UserDocumentInDB.from_dict(document_dict)


@pytest.fixture
def public_document_dict(document_dict):
  return {
    'type': 'user',
    'data': document_dict['data'],
    '_id': document_dict['_id'],
    '_rev': document_dict['_rev'],
    'computed': document_dict['computed'],
    'meta': {
      'username': document_dict['name'],
      'roles': [
        'user'
      ],
      'created_at': document_dict['meta']['created_at'],
      'updated_at': document_dict['meta']['updated_at'],
    },
  }


@pytest.fixture
def public_document(public_document_dict):
  return UserDocument.from_dict(public_document_dict)


@pytest.fixture
def auth_mocks(document, public_document, username, token):
  with patch.object(
    target=AuthController,
    attribute='get_current_active_username',
    new=AsyncMock(return_value=username),
  ) as mock_get_current_active_username:
    with patch.object(
      target=AuthController,
      attribute='get_document',
      new=AsyncMock(return_value=document),
    ) as mock_get_document:
      with patch.object(
        target=AuthController,
        attribute='get_public_document',
        new=AsyncMock(return_value=public_document),
      ) as mock_get_public_document:
        with patch.object(
          target=AuthController.oauth2_token_scheme,
          attribute='__call__',
          new=AsyncMock(return_value=token),
        ) as mock_scheme_call:
          yield {
            'mock_get_current_active_username': mock_get_current_active_username,
            'mock_get_document': mock_get_document,
            'mock_get_public_document': mock_get_public_document,
            'mock_scheme_call': mock_scheme_call,
          }
