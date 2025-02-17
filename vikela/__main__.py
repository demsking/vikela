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
import json
import logging

import uvicorn.config

from vikela import api
from vikela.utils.config import WORKERS
from vikela.utils.logger import logger
from vikela.utils.package import APP_NAME
from vikela.utils.package import APP_VERSION


def get_log_config():
  with open('log-config.json', 'r', encoding='utf-8') as file:
    return json.load(file)


def main():
  verbose = logger.isEnabledFor(logging.DEBUG)
  log_config = get_log_config() if not verbose else uvicorn.config.LOGGING_CONFIG

  logger.info(f'Starting {APP_NAME}/{APP_VERSION}')
  logger.info(f'Log level: {"DEBUG" if verbose else "INFO"}')

  uvicorn.run(
    app=api,
    host='0.0.0.0',
    port=6303,
    workers=WORKERS,
    server_header=False,
    use_colors=True,
    proxy_headers=True,
    log_level='info',
    log_config=log_config,
  )


if __name__ == '__main__':
  main()
