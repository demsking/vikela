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
from datetime import timedelta

from fastapi import Cookie
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query
from fastapi import Response
from fastapi import status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from ..controllers.auth import AuthController
from ..controllers.auth import UserDocumentInDB
from ..utils.config import COOKIE_SESSION_DOMAIN
from ..utils.config import COOKIE_SESSION_EXPIRES
from ..utils.config import COOKIE_SESSION_HTTPONLY
from ..utils.config import COOKIE_SESSION_MAX_AGE
from ..utils.config import COOKIE_SESSION_NAME
from ..utils.config import COOKIE_SESSION_PATH
from ..utils.config import COOKIE_SESSION_SAMESITE
from ..utils.config import COOKIE_SESSION_SECURE
from ..utils.config import JWT_ACCESS_TOKEN_EXPIRE_MINUTES
from ..utils.openapi import FASTAPI_401_SCHEMA
from vikela_models.couch import OkResponse
from vikela_models.error import ErrorResponse
from vikela_models.user import GetAccessTokenResponse
from vikela_models.user import RegisterPayload
from vikela_models.user import UserDocumentType


def create_1fa_endpoints(
  tag: str,
  api: FastAPI,
  auth_controller: AuthController,
) -> None:
  example_register_payload = RegisterPayload(
    username='um.nyobe',
    email='um.nyobe@example.com',
    first_name='Um',
    last_name='Nyobè',
    address='Douala, Cameroun',
    password='mypwd',
    gender='male',
    date_of_birth='200-12-12',
    phone_number='+237 663 49 77 80',
  )

  example_user_raw_document = auth_controller.create_raw_document(
    docid=example_register_payload.username,
    payload=example_register_payload,
  )

  example_public_user_document = auth_controller.parse_public_document(
    example_user_raw_document,
  )

  async def get_user_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
  ) -> tuple[UserDocumentInDB, str]:
    """
    Generates an access token for a user.
    """
    user = await auth_controller.authenticate_user(
      username=form_data.username,
      password=form_data.password,
    )

    if not user:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={'WWW-Authenticate': 'Bearer'},
      )

    access_token_expires = timedelta(
      minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    return user, auth_controller.create_access_token(
      data={'sub': form_data.username, **user.data.to_dict()},
      expires_delta=access_token_expires,
    )

  @api.post(
    path=AuthController.ENDPOINT_TOKEN,  # POST /token
    tags=[tag],
    responses={
      200: {
        'content': {
          'application/json': {
            'example': GetAccessTokenResponse(
              access_token='XXX',
              token_type='bearer',
            ),
          },
        },
      },
      401: {
        'model': ErrorResponse,
        'content': {
          'application/json': {
            'example': {
              'error': 'unauthorized',
              'reason': 'Name or password is incorrect.',
            },
          },
        },
      },
    },
  )
  async def get_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
  ) -> GetAccessTokenResponse:
    """
    Generates an access token for a user.
    """
    _, access_token = await get_user_access_token(form_data)

    return GetAccessTokenResponse(
      token_type='bearer',
      access_token=access_token,
    )

  @api.post('/session', tags=[tag])
  async def create_user_session(
    response: Response,
    rd: str | None = Query(
      default=None,
      description='The optional redirection URL',
      json_schema_extra={'format': 'uri'},
    ),
    form_data: OAuth2PasswordRequestForm = Depends(),
  ):
    """
    Endpoint to log in a user and set the session cookie.
    """
    user, access_token = await get_user_access_token(form_data)

    response.set_cookie(
      key=COOKIE_SESSION_NAME,
      value=access_token,
      expires=COOKIE_SESSION_EXPIRES,
      httponly=COOKIE_SESSION_HTTPONLY,
      domain=COOKIE_SESSION_DOMAIN,
      max_age=COOKIE_SESSION_MAX_AGE,
      path=COOKIE_SESSION_PATH,
      samesite=COOKIE_SESSION_SAMESITE,
      secure=COOKIE_SESSION_SECURE,
    )

    if rd:
      return RedirectResponse(url=rd)

    return user.data

  @api.get(
    path='/session/me',
    tags=[tag],
    responses={
      200: {
        'content': {
          'application/json': {
            'example': example_public_user_document,
          },
        },
      },
      401: FASTAPI_401_SCHEMA,
    },
  )
  async def get_user_document(
    session: str | None = Cookie(None),
  ) -> UserDocumentType:
    """
    Retrieve the user document using session cookie.

    This endpoint retrieves the user document for the currently authenticated
    user based on the provided session cookie.
    """
    if session:
      return await auth_controller.get_current_active_public_user_document(
        token=session,
      )

    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail='Invalid session or not logged in'
    )

  # TODO See how to implement cookie auth
  @api.delete('/session', tags=[tag], include_in_schema=False)
  async def delete_user_session(response: Response) -> OkResponse:
    """
    Endpoint to log out a user by deleting the session cookie.
    """
    response.delete_cookie(COOKIE_SESSION_NAME)

    return OkResponse(ok=True)
