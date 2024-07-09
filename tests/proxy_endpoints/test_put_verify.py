import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_verify_verify_options(client: TestClient):
  """Verify"""
  path = '/verify'
  payload = {}
  response = client.put(path, json=payload)
  assert response.status_code == 422

