from typing import List, NamedTuple


class PermissionSpec(NamedTuple):
    name: str
    description: str
    object: str
    allow_read: bool
    allow_write: bool


class RoleSpec(NamedTuple):
    name: str
    description: str
    permissions: List[PermissionSpec]


allow_read_write_all = PermissionSpec(
    name="AllReadWrite",
    description="Provide full access to all API endpoints",
    object="All",
    allow_read=True,
    allow_write=True,
)
allow_read_all = PermissionSpec(
    name="AllRead",
    description="Provide read-only access to all API endpoints",
    object="All",
    allow_read=True,
    allow_write=False,
)
allow_write_all = PermissionSpec(
    name="AllWrite",
    description="Provide write access to all API endpoints",
    object="All",
    allow_read=False,
    allow_write=True,
)

admin_role = RoleSpec(
    name="Administrator",
    description="Server administrators with full access to all API endpoints",
    permissions=[allow_read_write_all],
)
all_roles: List[RoleSpec] = [admin_role]
