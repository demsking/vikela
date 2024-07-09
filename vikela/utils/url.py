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
from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urlunparse


def remove_param(url: str, *, param: str) -> str:
  # Parse the URL
  parsed_url = urlparse(url)
  # Extract query parameters
  query_params = parse_qs(parsed_url.query)

  # Remove param parameter if it exists
  if param in query_params:
    del query_params[param]

  # Reconstruct the query string without param
  new_query = urlencode(query_params, doseq=True)

  # Reconstruct the full URL without param parameter
  new_url = urlunparse(parsed_url._replace(query=new_query))
  return new_url
