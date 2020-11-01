from typing import List, NamedTuple


class ApiPermission(NamedTuple):
    object: str
    read: bool
    write: bool

    def __str__(self) -> str:
        permission_string: str = ""

        if self.read:
            permission_string += "r"

        if self.write:
            permission_string += "w"

        return f"{self.object}: {permission_string}"


class PermissionSpec(NamedTuple):
    name: str
    description: str
    permission: ApiPermission


class RoleSpec(NamedTuple):
    name: str
    description: str
    permissions: List[PermissionSpec]


allow_read_write_all = PermissionSpec(
    name="AllReadWrite",
    description="Provide full access to all API endpoints",
    permission=ApiPermission(
        object="All",
        read=True,
        write=True,
    ),
)
allow_read_all = PermissionSpec(
    name="AllRead",
    description="Provide read-only access to all API endpoints",
    permission=ApiPermission(
        object="All",
        read=True,
        write=False,
    ),
)
allow_write_all = PermissionSpec(
    name="AllWrite",
    description="Provide write access to all API endpoints",
    permission=ApiPermission(
        object="All",
        read=False,
        write=True,
    ),
)
allow_read_write_user = PermissionSpec(
    name="UserReadWrite",
    description="Provide full access to the user management API endpoints",
    permission=ApiPermission(
        object="User",
        read=True,
        write=True,
    ),
)

admin_role = RoleSpec(
    name="Administrator",
    description="Server administrators with full access to all API endpoints",
    permissions=[allow_read_write_all.name],
)

all_permissions: List[PermissionSpec] = [
    allow_read_write_all,
    allow_read_all,
    allow_write_all,
    allow_read_write_user,
]
all_roles: List[RoleSpec] = [admin_role]
