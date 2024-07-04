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
async def test_get_user_document_account_me_get(
  client: TestClient,
  auth_mocks,
  headers,
  public_document_dict,
):
  """Get User Document"""
  path = '/account/me'
  response = client.get(path, headers=headers)

  assert response.status_code == 200
  assert response.json() == public_document_dict
