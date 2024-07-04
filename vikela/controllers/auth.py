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
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from datetime import timedelta

import fastapi
import httpx
import pyotp
from dataclasses_json import DataClassJsonMixin
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from oremi_core.vars import getenv
from passlib.context import CryptContext

from vikela_core.controller import Controller
from vikela_core.couch import CouchDatabase
from vikela_core.geo import Geocode
from vikela_models.couch import GenericResponse
from vikela_models.document import Document
from vikela_models.location import ComputedLocation
from vikela_models.user import AccountMeta
from vikela_models.user import RegisterPayload
from vikela_models.user import UserData
from vikela_models.user import UserDocument

DEFAULT_USER_GROUPS = [
  item.strip() for item in getenv('DEFAULT_GROUPS', default='user').split(',')
]


@dataclass
class RegisterUserMeta(DataClassJsonMixin):
  hashed_password: str
  totp_secret: str | None = None
  created_at: str = field(default_factory=lambda: datetime.now().isoformat())
  updated_at: str | None = field(default=None)


UserDocumentType = Document[UserData, ComputedLocation, RegisterUserMeta]


@dataclass
class _UserDocumentInDB(UserDocumentType):
  name: str = field
  roles: list[str] = field


UserDocumentInDB = _UserDocumentInDB.create_alias_from_base_meta(
  data_cls=UserData,
  meta_cls=RegisterUserMeta,
  computed_cls=ComputedLocation,
)


class AuthController(
  Controller[RegisterPayload, UserData, ComputedLocation, RegisterUserMeta],
):
  coltype = 'user'
  Document = UserDocumentInDB
  PublicDocument = UserDocument

  ENDPOINT_TOKEN = '/token'
  ENDPOINT_USER_DOCUMENT = '/account/me'

  COOKIE_SESSION_NAME = getenv(
    name='COOKIE_SESSION_NAME',
    default='vikela-session',
  )

  COOKIE_SESSION_MAX_AGE = getenv(
    name='COOKIE_SESSION_MAX_AGE',
    default=0,
    expected_type=int,
  ) or None

  COOKIE_SESSION_EXPIRES = getenv(
    name='COOKIE_SESSION_EXPIRES',
    default=0,
    expected_type=int,
  ) or None

  COOKIE_SESSION_PATH = getenv(
    name='COOKIE_SESSION_PATH',
    default='/',
  )

  COOKIE_SESSION_DOMAIN = getenv(
    name='COOKIE_SESSION_DOMAIN',
    default='',
  ) or None

  COOKIE_SESSION_SECURE = getenv(
    name='COOKIE_SESSION_SECURE',
    default=False,
    expected_type=bool,
  )

  COOKIE_SESSION_HTTPONLY = getenv(
    name='COOKIE_SESSION_HTTPONLY',
    default=True,
    expected_type=bool,
  )

  COOKIE_SESSION_SAMESITE = getenv(
    name='COOKIE_SESSION_SAMESITE',
    default='lax',  # lax | strict | none
  )

  SECRET_KEY = getenv('JWT_SECRET_KEY')
  ALGORITHM = getenv('JWT_ALGORITHM', default='HS256')  # JWT signing algorithm
  ACCESS_TOKEN_EXPIRE_MINUTES = getenv(
    name='JWT_ACCESS_TOKEN_EXPIRE_MINUTES',
    default=30,
    expected_type=int,
  )

  # Crypt context for password hashing
  pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

  oauth2_token_scheme = OAuth2PasswordBearer(tokenUrl=ENDPOINT_TOKEN)

  vikela_auth_headers = Controller.parse_auth_headers(
    username=getenv('COUCHDB_AUTH_USERNAME'),
    token=getenv('COUCHDB_AUTH_TOKEN'),
  )

  def __init__(self, database: CouchDatabase, user_agent: str):
    super().__init__(database)

    self.geo = Geocode(useragent=user_agent)

  def parse_auth_request_headers(self, request: Request) -> dict:
    return self.vikela_auth_headers

  def verify_password(self, plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plaintext password against a hashed password.

    Args:
      plain_password: The plaintext password to verify.
      hashed_password: The hashed password to compare against.

    Returns:
      True if the password matches, False otherwise.
    """
    return self.pwd_context.verify(plain_password, hashed_password)

  def parse_password_hash(self, password: str) -> str:
    """
    Hashes a password (for demonstration purposes, returns the same password).

    Args:
      password: The plaintext password to hash.

    Returns:
      The hashed password.
    """
    return self.pwd_context.hash(password)

  def parse_document_id(self, docid: str | None = None) -> str:
    assert docid
    return f'org.couchdb.user:{docid}'

  def parse_public_document_id(self, docid: str | None = None) -> str:
    assert docid
    return docid.split(':')[1] if ':' in docid else docid

  async def authenticate_user(
    self,
    username: str,
    *,
    password: str,
  ) -> UserDocument | None:
    """
    Authenticates a user by username and password.

    Args:
      username: The username of the user to authenticate.
      password: The plaintext password of the user.

    Returns:
      The authenticated user object if credentials are correct, None otherwise.
    """
    try:
      user = await self.get_document(username)

      if not self.verify_password(password, user.meta.hashed_password):
        return None

      return user
    except httpx.HTTPStatusError as error:
      if error.response.status_code < 500:
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail='Incorrect username or password',
          headers={'WWW-Authenticate': 'Bearer'},
        ) from error

      raise error

  def create_access_token(
    self,
    data: dict,
    expires_delta: timedelta | None = None,
  ) -> str:
    """Creates a JWT token.

    Args:
        data: The data to encode in the token.
        expires_delta: The token expiry time delta.

    Returns:
        The encoded JWT token.
    """
    to_encode = data.copy()

    if expires_delta:
      expire = datetime.utcnow() + expires_delta
    else:
      expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({
      'exp': expire,
    })

    encoded_jwt = jwt.encode(
      claims=to_encode,
      key=AuthController.SECRET_KEY,
      algorithm=AuthController.ALGORITHM,
    )

    return encoded_jwt

  async def get_current_active_username(
    self,
    token: str = Depends(oauth2_token_scheme),
  ) -> str:
    """
    Retrieves the current username based on the JWT token.

    Args:
      token: The JWT token.

    Returns:
      The current username.

    Raises:
      HTTPException: If token validation fails or user not found.
    """
    credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail='Could not validate credentials',
      headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
      payload = jwt.decode(
        token,
        key=AuthController.SECRET_KEY,
        algorithms=[AuthController.ALGORITHM],
      )

      username: str | None = payload.get('sub', None)

      if username is None:
        raise credentials_exception

      return username
    except JWTError as error:
      raise credentials_exception from error

  async def get_current_active_user(
    self,
    token: str = Depends(oauth2_token_scheme),
  ) -> UserDocumentInDB:
    """
    Retrieves the current user based on the JWT token.

    Args:
      token: The JWT token.

    Returns:
      The current user object in database.

    Raises:
      HTTPException: If token validation fails or user not found.
    """
    username = await self.get_current_active_username(token)
    user = await self.get_document(username)

    return user

  async def get_current_active_public_user_document(
    self,
    token: str = Depends(oauth2_token_scheme),
  ) -> UserDocument:
    """
    Retrieves the current public user document based on the JWT token.

    Args:
      token: The JWT token.

    Returns:
      The current user public document object.

    Raises:
      HTTPException: If token validation fails or user not found.
    """
    username = await self.get_current_active_username(token)
    user = await self.get_public_document(username)

    return user

  def parse_document_data(self, payload: RegisterPayload) -> UserData:
    payload_dict = payload.to_dict()
    parsed_data = UserData.from_dict(payload_dict)

    return parsed_data

  def parse_computed_object(
    self,
    payload: RegisterPayload,
    data: UserData,
  ) -> DataClassJsonMixin | None:
    if data.address:
      results = self.geo.search(data.address, limit=1)

      if len(results) == 1:
        return ComputedLocation(location=results[0])

      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Unable to look up location "{data.address}"',
      )

    return None

  def parse_document_meta(
    self,
    payload: RegisterPayload,
    data: UserData,
    request: Request | None = None,
  ) -> RegisterUserMeta:
    return RegisterUserMeta(
      hashed_password=self.parse_password_hash(payload.password),
    )

  def parse_public_document_meta(
    self,
    raw_doc: dict,
    data: dict,
    request: Request | None = None,
  ) -> AccountMeta:
    return AccountMeta(
      username=raw_doc['name'],
      roles=raw_doc['roles'],
    )

  def create_raw_document(
    self,
    payload: RegisterPayload,
    *,
    docid: str | None = None,
    rev: str | None = None,
    request: Request | None = None,
  ) -> dict:
    raw_document = super().create_raw_document(
      payload=payload,
      docid=docid,
      rev=rev,
      request=request,
    )

    raw_document['name'] = payload.username
    raw_document['roles'] = DEFAULT_USER_GROUPS.copy()

    return raw_document

  async def register_user(
    self,
    payload: RegisterPayload,
    *,
    request: fastapi.Request,
  ) -> GenericResponse:
    user = self.create_document(payload, docid=payload.username)
    doc = user.to_dict()

    doc['name'] = payload.username
    doc['roles'] = DEFAULT_USER_GROUPS.copy()

    headers = AuthController.vikela_auth_headers
    result = await self.database.insert(doc, headers=headers)
    result.id = self.parse_public_document_id(result.id)

    return result

  async def setup_2fa(self, username: str, *, password: str):
    user = await self.authenticate_user(username, password=password)

    if not user:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
      )

    totp = pyotp.TOTP(pyotp.random_base32())
    user.meta.totp_secret = totp.secret

    # Save the TOTP secret to the user's record in CouchDB
    self.database.insert(user)

    return {'totp_secret': totp.secret}

  async def verify_2fa(self, username: str, *, token: str):
    user = await self.get_document(username)

    if not user or not user.meta.totp_secret:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid user or 2FA not set up',
      )

    totp = pyotp.TOTP(user.meta.totp_secret)

    if not totp.verify(token):
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid 2FA token',
      )

    return {'status': '2FA verified'}
