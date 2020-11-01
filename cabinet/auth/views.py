from logging import getLogger as get_logger
from typing import Any

from flask import Blueprint

from flask_restful import Api

import cabinet.auth.controllers as auth_controller
from cabinet._types import ApiResponse
from cabinet.api import CabinetResource
from cabinet.auth.controllers import permission_required
from cabinet.auth.schemas import (
    login_input_schema,
    permission_list_schema,
    role_list_schema,
)
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


# TODO
class Login(CabinetResource):
    @validate_schema(login_input_schema)
    def post(self) -> ApiResponse:
        ...


# TODO
class Logout(CabinetResource):
    def post(self) -> ApiResponse:
        ...


api.add_resource(PermissionList, "/permissions", endpoint="permissions")
api.add_resource(RoleList, "/roles", endpoint="roles")
