from typing import List

from cabinet import database
from cabinet.auth.models import Permission, Role


def get_all_permissions() -> List[Permission]:
    return database.get_all(Permission)


def get_permission(permission_id: int) -> Permission:
    return database.get(Permission, permission_id)


def get_all_roles() -> List[Role]:
    return database.get_all(Role)


def get_role(role_id: int) -> Role:
    return database.get(role_id)
