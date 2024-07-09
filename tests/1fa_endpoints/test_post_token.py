import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_get_access_token_token_post(client: TestClient):
  """Get Access Token"""
  path = '/token'
  payload = {}
  response = client.post(path, json=payload)
  assert response.status_code == 200

