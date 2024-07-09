import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_get_server_info__get(client: TestClient):
  """Get Server Info"""
  path = '/'
  response = client.get(path)
  assert response.status_code == 200

