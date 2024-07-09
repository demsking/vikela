import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_2FA_Setup_2fa_setup_post(client: TestClient):
  """2Fa Setup"""
  path = '/2fa/setup'
  payload = {}
  response = client.post(path, json=payload)
  assert response.status_code == 200

