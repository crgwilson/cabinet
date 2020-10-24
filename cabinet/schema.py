from functools import wraps
from logging import getLogger as get_logger
from typing import Any, Callable

from flask import request

from marshmallow import Schema

from cabinet.response import CabinetApiResponse

logger = get_logger(__name__)


def validate_schema(schema: Schema) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def decorated_function(*args: Any, **kwargs: Any) -> Any:
            if schema:
                request_json = request.get_json()

                errors = schema.validate(request_json)

                if errors:
                    error_str = str(errors)
                    return CabinetApiResponse.bad_request(error_str)
                else:
                    data = schema.load(request_json)
                    kwargs["data"] = data

            try:
                results = func(*args, **kwargs)
            except Exception as err:
                err_str = str(err)
                logger.error(f"Error occured while processing request {err_str}")
                return CabinetApiResponse.internal_server_error(err_str)

            return results

        return decorated_function

    return decorator
