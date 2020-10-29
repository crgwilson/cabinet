from logging import getLogger as get_logger
from typing import Any

from flask import Blueprint

from flask_restful import Api

import cabinet.auth.controllers as auth_controller
from cabinet.api import CabinetResource
from cabinet.auth.schemas import permission_list_schema, role_list_schema

# from cabinet.auth.schemas import permission_list_schema, permission_schema, role_list_schema, role_schema
# from cabinet.schema import validate_schema

logger = get_logger(__name__)

bp = Blueprint("auth", __name__)
api = Api(bp)


class PermissionList(CabinetResource):
    def get(self) -> Any:
        result = auth_controller.get_all_permissions()
        rendered_result = self.render(result, permission_list_schema)

        return rendered_result


class RoleList(CabinetResource):
    def get(self) -> Any:
        result = auth_controller.get_all_roles()
        rendered_result = self.render(result, role_list_schema)

        return rendered_result


api.add_resource(PermissionList, "/permissions", endpoint="permissions")
api.add_resource(RoleList, "/roles", endpoint="roles")
