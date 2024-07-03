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
from vikela_models.error import ErrorResponse


FASTAPI_401_SCHEMA = {
  'model': ErrorResponse,
  'content': {
    'application/json': {
      'example': ErrorResponse(
        error='error_401',
        reason='Not authenticated',
      ),
    },
  },
}
