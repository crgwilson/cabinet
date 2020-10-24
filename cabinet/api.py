from logging import getLogger as get_logger
from typing import Any, Dict, List, Union

from flask_restful import Resource

from flask_sqlalchemy.model import DefaultMeta

from marshmallow import Schema

# from cabinet.response import CabinetApiResponse

QUERY_RESULT = Union[Dict[str, Any], List[DefaultMeta]]

logger = get_logger(__name__)


class CabinetResource(Resource):
    def __init__(self) -> None:
        super(CabinetResource, self).__init__()

    @staticmethod
    def render(result: QUERY_RESULT, schema: Schema) -> Any:
        return schema.dump(result)
