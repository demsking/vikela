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
from fastapi.testclient import TestClient

from vikela import api


client = TestClient(api, backend='asyncio')


def test_get_access_token_token_post(get_access_token_token_post_payload):
  """Get Access Token"""
  path = '/token'
  payload = get_access_token_token_post_payload
  response = client.post(path, json=payload)
  assert response.status_code == 200
