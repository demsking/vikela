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
# pylint: disable=wildcard-import,unused-wildcard-import,invalid-name,line-too-long
import pytest
from fastapi.testclient import TestClient

from vikela import api


@pytest.fixture
def client():
  return TestClient(api, backend='asyncio', root_path='', follow_redirects=False)


@pytest.fixture
def register_user_account_post_payload():
  return {
    'username': 'um.nyobe',
    'password': 'mypwd',
    'email': 'um.nyobe@example.com',
    'first_name': 'Um',
    'last_name': 'Nyob\u00e8',
    'date_of_birth': '200-12-12',
    'gender': 'male',
    'address': 'Douala, Cameroun',
    'phone_number': '+237 663 49 77 80'
  }


@pytest.fixture
def update_user_data_account_profile_put_payload():
  return {
    'email': 'um.nyobe@example.com',
    'first_name': 'Um',
    'last_name': 'Nyob\u00e8',
    'date_of_birth': '200-12-12',
    'gender': 'male',
    'address': 'Yaound\u00e9, Centre, Cameroun',
    'phone_number': '+237 675 63 21 78'
  }


@pytest.fixture
def get_access_token_token_post_payload():
  return None


@pytest.fixture
def _2FA_Setup_2fa_setup_post_payload():
  return None


@pytest.fixture
def username():
  return None


@pytest.fixture
def password():
  return None


@pytest.fixture
def _2FA_Verification_2fa_verify_post_payload():
  return None


@pytest.fixture
def token():
  return None
