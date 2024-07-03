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
import os

import fastapi
import httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from oremi_core.vars import getenv

from .controllers.auth import AuthController
from .endpoints.account import create_account_endpoints
from .endpoints.onefa import create_1fa_endpoints
from .endpoints.proxy import create_proxy_endpoints
from .endpoints.twofa import create_2fa_endpoints
from .endpoints.version import create_version_endpoints
from .utils.logger import logger
from .utils.package import APP_NAME
from .utils.package import APP_VERSION
from vikela_core.couch import CouchServer
from vikela_models.document import DataClassJsonMixin
from vikela_models.error import ErrorResponse


HTTP_AGENT = f'{APP_NAME}/{APP_VERSION}'
SERVICE_TITLE = 'Vikela'

_current_dir = os.path.dirname(os.path.abspath(__file__))
_readme_path = os.path.realpath(
  os.path.join(_current_dir, '..', 'OPENAPI-DESCRIPTION.md'),
)

with open(_readme_path, 'r', encoding='utf-8') as file:
  SERVICE_DESCRIPTION = file.read()

tag_version = {
  'name': 'Server Endpoints',
  'description': 'Endpoints to retrieve server information including name and version.',
}

tag_account = {
  'name': 'Account Endpoints',
  'description': 'Endpoints related to user account management, including registration, account details, and updates.'
}

tag_1fa = {
  'name': '1FA Endpoints',
  'description': 'Endpoints related to One Time Passwords authentication.'
}

tag_2fa = {
  'name': '2FA Endpoints',
  'description': 'Endpoints related to two-factor authentication (2FA) setup and verification.'
}

tag_proxy = {
  'name': 'Proxy Endpoints',
  'description': """
  Endpoints that serve as proxies for authentication and authorization, providing access token verification and user information retrieval. These endpoints manage user sessions and set custom headers based on authenticated user data.

  <style>
    .method {
      font-size: 0.929em;
      line-height: 20px;
      color: rgb(255, 255, 255);
      padding: 3px 10px;
      text-transform: uppercase;
      font-family: Montserrat, sans-serif;
      margin: 0px;
    }

    .method.get {
      background-color: rgb(47, 129, 50);
    }

    .method.post {
      background-color: rgb(24, 111, 175);
    }

    .method.put {
      background-color: rgb(149, 80, 124);
    }

    .method.delete {
      background-color: rgb(204, 51, 51);
    }

    .method.patch {
      background-color: rgb(191, 88, 29);
    }
  </style>

  <div style="border-radius:4px;margin-bottom:3px"><div style="cursor:default;background-color: rgb(17, 23, 26);padding:10px 20px 7px;width:100%"><span type="get" class="method get">get</span><span class="sc-jXcxbT hVdkvA" style="color:#fff">/proxy/verify</span></div></div>

  <div style="border-radius:4px;margin-bottom:3px"><div style="cursor:default;background-color: rgb(17, 23, 26);padding:10px 20px 7px;width:100%"><span type="post" class="method post">post</span><span class="sc-jXcxbT hVdkvA" style="color:#fff">/proxy/verify</span></div></div>

  <div style="border-radius:4px;margin-bottom:3px"><div style="cursor:default;background-color: rgb(17, 23, 26);padding:10px 20px 7px;width:100%"><span type="put" class="method put">put</span><span class="sc-jXcxbT hVdkvA" style="color:#fff">/proxy/verify</span></div></div>

  <div style="border-radius:4px;margin-bottom:3px"><div style="cursor:default;background-color: rgb(17, 23, 26);padding:10px 20px 7px;width:100%"><span type="delete" class="method delete">delete</span><span class="sc-jXcxbT hVdkvA" style="color:#fff">/proxy/verify</span></div></div>

  <div style="border-radius:4px;margin-bottom:3px"><div style="cursor:default;background-color: rgb(17, 23, 26);padding:10px 20px 7px;width:100%"><span type="patch" class="method patch">patch</span><span class="sc-jXcxbT hVdkvA" style="color:#fff">/proxy/verify</span></div></div>

  Verify user and set custom headers or redirect to login.

  This endpoint verifies the user using an OAuth2 token or session cookie. If
  the user is authenticated, it sets custom headers with user information. If
  not, it redirects to the login URL.
  """
}

api = FastAPI(
  docs_url=None,
  redoc_url='/docs',
  title=SERVICE_TITLE,
  version=APP_VERSION,
  # summary=APP_DESCRIPTION,
  description=SERVICE_DESCRIPTION,
  root_path=getenv('BASEURL', default='/api'),
  license_info={
    'name': 'Apache 2.0',
    'url': 'http://www.apache.org/licenses/LICENSE-2.0.html',
  },
  openapi_tags=[
    tag_version,
    tag_account,
    tag_1fa,
    tag_2fa,
    tag_proxy,
  ],
)

user_agent = getenv(
  name='CLIENT_USERAGENT',
  default=f'{APP_NAME}/{APP_VERSION}',
)

couch = CouchServer(
  url=getenv('COUCHDB_URL'),
  useragent=user_agent,
  roles=getenv('COUCHDB_AUTH_ROLES', default='_admin'),
  logger=logger,
)

database = couch.use('_users')
auth_controller = AuthController(database, user_agent)

create_version_endpoints(tag_version['name'], api)
create_account_endpoints(tag_account['name'], api, auth_controller)
create_1fa_endpoints(tag_1fa['name'], api, auth_controller)
create_2fa_endpoints(tag_2fa['name'], api, auth_controller)
create_proxy_endpoints(tag_proxy['name'], api, auth_controller)


@api.exception_handler(fastapi.exceptions.ResponseValidationError)
async def handle_response_validation_error(
  request: fastapi.Request,
  error: fastapi.exceptions.ResponseValidationError,
) -> JSONResponse:
  validation_error = error.errors()[0]

  if isinstance(validation_error['input'], DataClassJsonMixin):
    if isinstance(error.body, list):
      data = [item.to_dict() for item in error.body]
    else:
      data = error.body.to_dict()

    return JSONResponse(content=data)

  return JSONResponse(
    status_code=500,
    content={
      'error': 'invalid_response',
      'reason': validation_error['msg'],
    },
  )


@api.exception_handler(fastapi.HTTPException)
async def transform_fastapi_error(
  request: fastapi.Request,
  error: fastapi.HTTPException,
) -> JSONResponse:
  response = ErrorResponse(
    error=f'error_{error.status_code}',
    reason=error.detail,
  )

  return JSONResponse(
    status_code=error.status_code,
    content=response.to_dict(),
  )


@api.exception_handler(httpx.HTTPStatusError)
async def httpx_http_status_error_handler(
  request: fastapi.Request,
  error: httpx.HTTPStatusError,
) -> JSONResponse:
  try:
    detail = error.response.json()
  except Exception:
    detail = str(error)

  return JSONResponse(
    status_code=error.response.status_code,
    content=detail if 'error' in detail and 'reason' in detail else {
      'error': f'error_{error.response.status_code}',
      'reason': str(error),
    },
  )


@api.exception_handler(httpx.InvalidURL)
async def httpx_invalid_error_handler(
  request: fastapi.Request,
  error: httpx.InvalidURL,
) -> JSONResponse:
  return JSONResponse(
    status_code=400,
    content={
      'error': 'bad_request',
      'reason': str(error),
    },
  )
