from logging import getLogger as get_logger
from typing import Any

from flask import Blueprint

from flask_restful import Api

import cabinet.user.controllers as user_controller
from cabinet._types import ApiObject
from cabinet.api import CabinetResource
from cabinet.auth.controllers import permission_required
from cabinet.response import CabinetApiResponse
from cabinet.schema import validate_schema
from cabinet.user.schemas import user_input_schema, user_list_schema, user_schema

# from cabinet.response import CabinetApiResponse

API_OBJECT = "User"

logger = get_logger(__name__)

bp = Blueprint("users", __name__)
api = Api(bp)


class UsersList(CabinetResource):
    # TODO: The gets shouldn't say they return Any
    @permission_required(API_OBJECT)
    def get(self) -> Any:
        result = user_controller.get_all_users()
        rendered_result = self.render(result, user_list_schema)

        return rendered_result

    @permission_required(API_OBJECT)
    @validate_schema(user_input_schema)
    def post(self, data: ApiObject) -> Any:
        result = user_controller.create_user(
            username=data["username"], password=data["password"]
        )
        rendered_result = self.render(result, user_schema)

        return rendered_result


class Users(CabinetResource):
    @permission_required(API_OBJECT)
    def get(self, user_id: int) -> Any:
        result = user_controller.get_user(user_id)
        if not result:
            rendered_result = CabinetApiResponse.not_found()
        else:
            rendered_result = self.render(result, user_schema)

        return rendered_result

    @permission_required(API_OBJECT)
    @validate_schema(user_input_schema)
    def put(self, user_id: int, data: ApiObject) -> Any:
        target_user = user_controller.get_user(user_id)
        if not target_user:
            return CabinetApiResponse.not_found()

        result = user_controller.update_user(
            user_id, username=data["username"], password=data["password"]
        )

        rendered_result = self.render(result, user_schema)

        return rendered_result

    @permission_required(API_OBJECT)
    def delete(self, user_id: int) -> Any:
        target_user = user_controller.get_user(user_id)
        if not target_user:
            return CabinetApiResponse.not_found()

        user_controller.delete_user(user_id)
        return CabinetApiResponse.ok()


api.add_resource(UsersList, "/users", endpoint="users")
api.add_resource(Users, "/users/<int:user_id>", endpoint="user")
