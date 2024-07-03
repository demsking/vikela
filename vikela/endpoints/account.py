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
from fastapi import Body
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request

from ..controllers.auth import AuthController
from ..utils.openapi import FASTAPI_401_SCHEMA
from vikela_models.couch import GenericResponse
from vikela_models.error import ErrorResponse
from vikela_models.user import RegisterPayload
from vikela_models.user import UserData
from vikela_models.user import UserDocument
from vikela_models.user import UserDocumentType


def create_account_endpoints(
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

  example_update_payload = UserData(
    email='um.nyobe@example.com',
    first_name='Um',
    last_name='Nyobè',
    address='Yaoundé, Centre, Cameroun',
    gender='male',
    date_of_birth='200-12-12',
    phone_number='+237 675 63 21 78',
  )

  example_user_raw_document = auth_controller.create_raw_document(
    docid=example_register_payload.username,
    payload=example_register_payload,
  )

  example_public_user_document = auth_controller.parse_public_document(
    example_user_raw_document,
  )

  @api.post(
    path='/account',
    tags=[tag],
    status_code=201,
    responses={
      201: {
        'content': {
          'application/json': {
            'example': GenericResponse(
              id=example_register_payload.email,
              ok=True,
              rev='1-ad7a225ec95fc94892d6088465835810',
            ),
          },
        },
      },
      400: {'model': ErrorResponse},
      401: FASTAPI_401_SCHEMA,
      409: {'model': ErrorResponse},
    },
  )
  async def register_user(
    request: Request,
    payload: RegisterPayload = Body(..., examples=[example_register_payload]),
  ) -> GenericResponse:
    """
    Register a new user in the database.
    """
    return await auth_controller.register_user(payload, request=request)

  @api.get(
    path=AuthController.ENDPOINT_USER_DOCUMENT,
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
    current_user: UserDocument = Depends(
      dependency=auth_controller.get_current_active_public_user_document,
    ),
  ) -> UserDocumentType:
    """
    Retrieve the user document using a token.

    This endpoint retrieves the user document for the currently authenticated
    user based on the provided token.
    """
    return current_user

  @api.put(
    path='/account/profile',
    tags=[tag],
    responses={
      200: {
        'content': {
          'application/json': {
            'example': GenericResponse(
              id=example_register_payload.email,
              ok=True,
              rev='2-ad7a225ec95fc94892d6088465835810',
            ),
          },
        },
      },
      401: FASTAPI_401_SCHEMA,
      404: {'model': ErrorResponse},
      409: {'model': ErrorResponse},
    },
  )
  async def update_user_data(
    request: Request,
    current_user: UserDocument = Depends(
      dependency=auth_controller.get_current_active_user,
    ),
    payload: UserData = Body(..., examples=[example_update_payload]),
  ) -> GenericResponse:
    """
    Update the user profile data.

    This endpoint updates the user profile data for the currently authenticated
    user, using either an OAuth2 token or a session cookie for authentication.
    """
    return await auth_controller.update_document_data(
      docid=current_user.name,
      payload=payload,
      current_doc=current_user,
      request=request,
    )
