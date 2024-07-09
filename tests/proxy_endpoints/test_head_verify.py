import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_verify_verify_options(client: TestClient):
  """Verify"""
  path = '/verify'
  response = client.head(path)
  assert response.status_code == 422

