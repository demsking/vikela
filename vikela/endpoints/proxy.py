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
from typing import Literal

import httpx
from fastapi import FastAPI
from fastapi import Header
from fastapi import Query
from fastapi import Request
from fastapi import Response
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from ..controllers.auth import AuthController
from ..utils.logger import logger
from ..utils.url import remove_param


HTTP_METHODS = Literal[
  'GET',
  'HEAD',
  'POST',
  'PUT',
  'PATCH',
  'DELETE',
  'TRACE',
  'CONNECT',
  'OPTIONS',
  'COPY',
  'LOCK',
  'MKCOL',
  'MOVE',
  'PROPFIND',
  'PROPPATCH',
  'UNLOCK',
  'TRACE',
]


def create_proxy_endpoints(
  tag: str,
  api: FastAPI,
  auth_controller: AuthController,
) -> None:
  @api.api_route(
    tags=[tag],
    path='/verify',
    methods=[
      'GET',
      'HEAD',
      'POST',
      'PUT',
      'PATCH',
      'DELETE',
      'OPTIONS',
      'TRACE',
    ],
    responses={
      200: {
        'headers': {
          'Remote-User': {
            'description': 'The username of the authenticated user',
            'schema': {
              'type': 'string',
              'example': 'um.nyobe',
            },
          },
          'Remote-Name': {
            'description': 'The full name of the authenticated user',
            'schema': {
              'type': 'string',
              'example': 'Um Nyobè',
            }
          },
          'Remote-Email': {
            'description': 'The email address of the authenticated user',
            'schema': {
              'type': 'string',
              'example': 'um.nyobe@example.com',
            }
          },
          'Remote-Groups': {
            'description': 'Comma-separated list of groups the user belongs to',
            'schema': {
              'type': 'string',
              'example': 'admin,user',
            },
          },
        },
      },
      401: {
        'description': 'Unauthorized - User not authenticated',
      },
      307: {
        'description': 'Temporary Redirect - User not authenticated, redirecting to login',
      },
    },
  )
  async def verify(
    request: Request,
    response: Response,
    rd: str | None = Query(
      default=None,
      description='The optional redirection URL of the login page'
    ),
    authorization: str | None = Header(
      alias='Authorization',
      default=None,
      description='Authorization token for the request, usually a Bearer token'
    ),
    x_original_url: str = Header(
      alias='X-Original-URL',
      description='The original URL of the request, required for verification',
      json_schema_extra={'format': 'uri'}
    ),
    x_forwarded_method: HTTP_METHODS | None = Header(
      alias='X-Forwarded-Method',
      default=None,
      description='The original HTTP method of the request if it was forwarded'
    ),
  ) -> Response:
    """
    Verify user and set custom headers or redirect to login.

    This endpoint verifies the user using an OAuth2 token. If the user is
    authenticated, it sets custom headers with user information. If not, it
    redirects to the login URL.
    """
    # Extract token from the Authorization header
    if authorization:
      scheme, _, credentials = authorization.partition(' ')

      if scheme.lower() == 'bearer':
        proxy_method = x_forwarded_method or request.method
        proxy_url = x_original_url or str(request.url)

        try:
          logger.info('Authorization header found. Attempting to verify token.')
          user = await auth_controller.get_current_active_user(
            token=credentials,
          )

          logger.info(f'Authenticated user: {user.name}')

          # Set custom headers
          custom_headers = {
            'Remote-User': user.name.encode('utf-8'),
            'Remote-Name': user.data.full_name.encode('utf-8'),
            'Remote-Email': user.data.email.encode('utf-8'),
            'Remote-Groups': ','.join(user.roles).encode('utf-8'),
          }

          logger.info(f'Setting custom headers for user {user.name}: {custom_headers}')

          # Make a proxy request using httpx
          headers = dict(request.headers)

          # Remove 'host' header to avoid conflicts with the target server
          headers.pop('host', None)

          logger.info(f'Proxing request to {proxy_url} with method {proxy_method}')
          async with httpx.AsyncClient() as client:
            proxy_response = await client.request(
              method=proxy_method,
              url=proxy_url,
              content=await request.body(),
              headers={**headers, **custom_headers},
            )

          # Ensure 'Content-Encoding' header is handled properly
          content_encoding = proxy_response.headers.get('content-encoding', '').lower()
          if content_encoding in ['gzip', 'deflate', 'br']:
            logger.info(f'Content-Encoding detected: {content_encoding}. Decoding response body.')
            decoded_content = proxy_response.read()
            proxy_response.headers.pop('content-encoding', None)
          else:
            decoded_content = proxy_response.content

          # Return the response to the client
          logger.info('Returning proxied response content.')

          # Forward the external response to the FastAPI response
          response.status_code = proxy_response.status_code
          response.headers.update(proxy_response.headers)
          response.body = decoded_content

          return response
        except HTTPException as exception:
          logger.error(f'Authentication failed - {exception}')
        except httpx.ConnectError as error:
          logger.error(f'Error during proxing to {proxy_url} with method {proxy_method}: {error}')
          response.status_code = status.HTTP_404_NOT_FOUND
          return response
        except Exception as exception:
          logger.error(f'Error during verification: {exception}')
          raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error',
          ) from exception

    # If no valid session, redirect to login URL with the provided `rd`
    # parameter
    if rd:
      url = remove_param(str(request.url), param='rd')
      return RedirectResponse(url=f'{rd}?rd={url}')

    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail='Unauthorized access',
      headers={'WWW-Authenticate': 'Bearer'},
    )
