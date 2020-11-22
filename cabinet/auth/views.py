from logging import getLogger as get_logger
from typing import Any

from flask import Blueprint

from flask_restful import Api

import cabinet.auth.controllers as auth_controller
from cabinet._types import ApiObject
from cabinet.api import CabinetResource
from cabinet.auth.controllers import permission_required
from cabinet.auth.schemas import (
    login_input_schema,
    login_output_schema,
    permission_list_schema,
    role_list_schema,
)
from cabinet.exceptions import IncorrectUsernameOrPassword
from cabinet.response import CabinetApiResponse
from cabinet.schema import validate_schema

PERMISSION_API_OBJECT = "Permission"
ROLE_API_OBJECT = "Role"

logger = get_logger(__name__)

bp = Blueprint("auth", __name__)
api = Api(bp)


class PermissionList(CabinetResource):
    @permission_required(PERMISSION_API_OBJECT)
    def get(self) -> Any:
        result = auth_controller.get_all_permissions()
        rendered_result = self.render(result, permission_list_schema)

        return rendered_result


class RoleList(CabinetResource):
    @permission_required(ROLE_API_OBJECT)
    def get(self) -> Any:
        result = auth_controller.get_all_roles()
        rendered_result = self.render(result, role_list_schema)

        return rendered_result


class Login(CabinetResource):
    @validate_schema(login_input_schema)
    def post(self, data: ApiObject) -> Any:
        username = data["username"]
        password = data["password"]

        try:
            token: auth_controller.AuthToken = auth_controller.create_login_token(
                username, password
            )
        except IncorrectUsernameOrPassword:
            return CabinetApiResponse.unauthorized()

        rendered_result = self.render(token, login_output_schema)
        return rendered_result


api.add_resource(PermissionList, "/permissions", endpoint="permissions")
api.add_resource(RoleList, "/roles", endpoint="roles")
api.add_resource(Login, "/login", endpoint="login")
