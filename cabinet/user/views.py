from logging import getLogger as get_logger
from typing import Any

from flask import Blueprint

from flask_restful import Api

import cabinet.user.controllers as user_controller
from cabinet._types import ApiObject
from cabinet.api import CabinetResource
from cabinet.schema import validate_schema
from cabinet.user.schemas import user_input_schema, user_list_schema, user_schema

# from cabinet.response import CabinetApiResponse

logger = get_logger(__name__)

bp = Blueprint("users", __name__)
api = Api(bp)


class UsersList(CabinetResource):
    def get(self) -> Any:
        result = user_controller.get_all_users()
        rendered_result = self.render(result, user_list_schema)

        return rendered_result

    @validate_schema(user_input_schema)
    def post(self, data: ApiObject) -> Any:
        result = user_controller.create_user(
            username=data["username"], password=data["password"]
        )
        rendered_result = self.render(result, user_schema)

        return rendered_result


api.add_resource(UsersList, "/users", endpoint="users")
