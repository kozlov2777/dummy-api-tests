import json
from requests import Response
from pydantic import ValidationError
import pytest
import logging
from pydantic import BaseModel


def response_validator(model: BaseModel.__class__, response: Response, index_post_preview=None) -> None:
    if "data" in response.json():
        data_for_create_json = json.dumps(response.json()["data"][index_post_preview])
        try:
            model.model_validate_json(data_for_create_json)
        except ValidationError as err:
            logging.Logger.error(err)
            pytest.fail(err)
    else:
        data_for_create_json = json.dumps(response.json())
        try:
            model.model_validate_json(data_for_create_json)
        except ValidationError as err:
            logging.Logger.error(err)
            pytest.fail(err)
