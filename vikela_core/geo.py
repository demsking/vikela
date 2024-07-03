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
import httpx

from vikela_models.location import Location


class Geocode:
  def __init__(self, useragent: str):
    self.useragent = useragent

  def search(
    self,
    query: str,
    *,
    limit: int = 10,
    country_codes: list[str] | str | None = None,
    language_result: str = 'en',
  ) -> list[Location]:
    params = {
      'q': query,
      'limit': limit,
      'format': 'json',
      'addressdetails': 1,
    }

    if isinstance(country_codes, list) and len(country_codes) > 0:
      params['countrycodes'] = ','.join(country_codes)

    # See https://nominatim.org/release-docs/develop/api/Search
    response = httpx.get(
      url='https://nominatim.openstreetmap.org/search',
      params=params,
      headers={
        'User-Agent': self.useragent,
        'Accept-Language': language_result,
      },
    )

    response.raise_for_status()

    return Location.schema().loads(response.text, many=True)
