# Copyright 2024-2025 Sébastien Demanou. All Rights Reserved.
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
import multiprocessing

from oremi_core.vars import getenv

from .package import APP_NAME
from .package import APP_VERSION


ROOT_PATH = getenv('ROOT_PATH', default='/api')

CLIENT_USERAGENT = getenv(
  name='CLIENT_USERAGENT',
  default=f'{APP_NAME}/{APP_VERSION}',
)

COUCHDB_URL = getenv('COUCHDB_URL')
COUCHDB_AUTH_ROLES = getenv('COUCHDB_AUTH_ROLES', default='_admin')
COUCHDB_AUTH_USERNAME = getenv('COUCHDB_AUTH_USERNAME')
COUCHDB_AUTH_TOKEN = getenv('COUCHDB_AUTH_TOKEN')

WORKERS = getenv('WORKERS', default=multiprocessing.cpu_count(), expected_type=int)
"""The number of worker processes to run for handling incoming API requests. By default, it uses
the number of CPU cores available on the system."""

DEFAULT_USER_GROUPS = getenv(
  name='DEFAULT_USER_GROUPS',
  default='user',
  expected_type=list,
)

COOKIE_SESSION_NAME = getenv(
  name='COOKIE_SESSION_NAME',
  default='vikela-session',
)

COOKIE_SESSION_MAX_AGE = getenv(
  name='COOKIE_SESSION_MAX_AGE',
  default=None,
  expected_type=int,
)

COOKIE_SESSION_EXPIRES = getenv(
  name='COOKIE_SESSION_EXPIRES',
  default=None,
  expected_type=int,
)

COOKIE_SESSION_PATH = getenv(
  name='COOKIE_SESSION_PATH',
  default='/',
)

COOKIE_SESSION_DOMAIN = getenv(
  name='COOKIE_SESSION_DOMAIN',
  default=None,
)

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
  default='lax',
  choices=['lax', 'strict', 'none'],
)

JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = getenv('JWT_ALGORITHM', default='HS256')  # JWT signing algorithm
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = getenv(
  name='JWT_ACCESS_TOKEN_EXPIRE_MINUTES',
  default=30,
  expected_type=int,
)
