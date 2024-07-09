import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_2FA_Verification_2fa_verify_post(client: TestClient):
  """2Fa Verification"""
  path = '/2fa/verify'
  payload = {}
  response = client.post(path, json=payload)
  assert response.status_code == 200

