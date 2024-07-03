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
import json
from typing import Any

from fastapi import HTTPException
from fastapi import status
from jsonschema import SchemaError
from jsonschema import validate
from jsonschema import ValidationError


class Schema:
  def __init__(self, filename: str):
    self.filename = filename
    self.schema: dict[str, Any] = {}

  def load(self) -> None:
    """
    Load the JSON schema from the specified path.

    Raises:
      FileNotFoundError: If the schema file does not exist.
      json.JSONDecodeError: If the schema file is not a valid JSON.
    """
    try:
      with open(self.filename, 'r', encoding='utf-8') as schema_file:
        self.schema = json.load(schema_file)
    except FileNotFoundError as error:
      raise FileNotFoundError(
        f'Schema file not found at path: {self.filename}',
      ) from error
    except json.JSONDecodeError as error:
      raise json.JSONDecodeError(
        msg=f'Invalid JSON format in schema file at path: {self.filename}',
        doc=error.doc,
        pos=error.pos,
      ) from error

  def validate(self, data: dict[str, any]) -> None:
    """
    Validate the provided data against the loaded JSON schema.

    Parameters:
      data (dict[str, any]): The data to validate against the schema.

    Raises:
      HTTPException: If the data is not valid according to the schema or if there is an issue with the schema itself.
    """
    try:
      validate(instance=data, schema=self.schema)  # Validate the provided data against the schema
    except ValidationError as error:
      raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=f'Data validation error: {error.message}',
      ) from error
    except SchemaError as error:
      raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f'Schema error: {error.message}',
      ) from error
