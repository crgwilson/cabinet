from logging import getLogger as get_logger
from typing import Any

from flask_restful import Resource

from marshmallow import Schema

from cabinet._types import QueryResult

logger = get_logger(__name__)


class CabinetResource(Resource):
    def __init__(self) -> None:
        super(CabinetResource, self).__init__()

    @staticmethod
    def render(result: QueryResult, schema: Schema) -> Any:
        return schema.dump(result)
