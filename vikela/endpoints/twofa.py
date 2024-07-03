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

from ..controllers.auth import AuthController


def create_2fa_endpoints(
  tag: str,
  api: FastAPI,
  auth_controller: AuthController,
) -> None:
  @api.post(
    path='/2fa/setup',
    tags=[tag],
    name='2FA Setup',
  )
  async def setup_2fa(username: str, password: str):
    """
    Endpoint to set up Two-Factor Authentication (2FA) for a user.
    """
    return auth_controller.setup_2fa(username, password=password)

  @api.post(
    path='/2fa/verify',
    tags=[tag],
    name='2FA Verification',
  )
  async def verify_2fa(username: str, token: str):
    """
    Endpoint to verify the Two-Factor Authentication (2FA) token for a user.
    """
    return auth_controller.verify_2fa(username, token=token)
