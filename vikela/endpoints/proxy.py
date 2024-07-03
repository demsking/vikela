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
from fastapi import FastAPI
from fastapi import Header
from fastapi import Request
from fastapi import Response
from fastapi.responses import RedirectResponse

from ..controllers.auth import AuthController


def create_proxy_endpoints(
  tag: str,
  api: FastAPI,
  auth_controller: AuthController,
) -> None:
  @api.api_route(
    tags=[tag],
    path='/proxy/verify',
    methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
    status_code=204,
    include_in_schema=False,
    responses={
      307: {},
    },
  )
  async def verify(
    request: Request,
    response: Response,
    rd: str,
    authorization: str | None = Header(None),
  ):
    """
    Verify user and set custom headers or redirect to login.

    This endpoint verifies the user using an OAuth2 token or session cookie. If
    the user is authenticated, it sets custom headers with user information. If
    not, it redirects to the login URL.
    """
    token: str | None = None

    # Extract token from the Authorization header
    if authorization:
      scheme, _, credentials = authorization.partition(' ')
      if scheme.lower() == 'bearer':
        token = credentials

    if token:
      try:
        user = await auth_controller.get_current_active_user(
          token=token,
        )

        # Set custom headers
        response.headers['Remote-User'] = user.name
        response.headers['Remote-Name'] = user.data.full_name
        response.headers['Remote-Email'] = user.data.email
        response.headers['Remote-Groups'] = ','.join(user.roles)

        return
      except Exception as _exception:
        ...

    # If no valid session, redirect to login URL with the provided `rd`
    # parameter
    return RedirectResponse(url=f'{rd}?rd={request.url}')
