from fastapi.testclient import TestClient


def test_verify_with_missing_x_original_url(client: TestClient):
  path = '/verify'
  response = client.get(path)

  assert response.status_code == 422


def test_verify_with_provided_rd(client: TestClient):
  path = '/verify?rd=http://vikela.example.com'
  headers = {'x-original-url': 'http://example.com'}
  response = client.get(path, headers=headers)

  assert response.status_code == 307
  assert 'location' in response.headers
  assert response.headers.get('location') == 'http://vikela.example.com?rd=http://testserver/verify'


def test_verify_with_missing_rd(client: TestClient):
  path = '/verify'
  headers = {'x-original-url': 'http://example.com'}
  response = client.get(path, headers=headers)

  assert response.status_code == 401


def test_verify_with_headers(client: TestClient, headers, auth_mocks):
  path = '/verify'
  x_original_url_header = {'x-original-url': 'https://example.com'}
  response = client.get(path, headers={**headers, **x_original_url_header})

  assert response.status_code == 200
