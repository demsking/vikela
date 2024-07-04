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
import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_update_user_data_account_profile_put(
  client: TestClient,
  update_user_data_account_profile_put_payload,
  auth_mocks,
  headers,
):
  """Update User Data"""
  path = '/account/profile'
  payload = update_user_data_account_profile_put_payload
  response = client.put(path, json=payload, headers=headers)

  assert response.status_code in (200, 409)
