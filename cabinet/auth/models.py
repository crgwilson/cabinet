from typing import Any, Dict

from sqlalchemy.event import listen
from sqlalchemy.orm import relationship

from cabinet.auth.permissions import all_roles
from cabinet.database import db, insert

role_permission_association = db.Table(
    "role_permission_association",
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
    db.Column("permission_id", db.Integer, db.ForeignKey("permission.id")),
)


class Permission(db.Model):
    __tablename__ = "permission"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(32), nullable=False, unique=True)
    description = db.Column(db.String(64))

    object = db.Column(db.String(32), nullable=False)
    allow_read = db.Column(db.Boolean(), nullable=False)
    allow_write = db.Column(db.Boolean(), nullable=False)

    roles = relationship(
        "Role", secondary=role_permission_association, back_populates="permissions"
    )

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )


class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(32), nullable=False, unique=True)
    description = db.Column(db.String(64))

    permissions = relationship("Permission", secondary=role_permission_association)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )


def init_roles_and_permissions(*args: Any, **kwargs: Any) -> None:
    created_permissions: Dict = {}
    for role in all_roles:
        role_model = Role(name=role.name, description=role.description)

        # Ensure all the necessary permissions exist for each role
        for permission_spec in role.permissions:
            if permission_spec.name not in created_permissions.keys():
                # If the permission does not exist already, create it
                permission_model = insert(
                    Permission(
                        name=permission_spec.name,
                        description=permission_spec.description,
                        object=permission_spec.object,
                        allow_read=permission_spec.allow_read,
                        allow_write=permission_spec.allow_write,
                    )
                )
                created_permissions[permission_spec.name] = permission_model

            # Add the existing permission to the role
            role_model.permissions.append(created_permissions[permission_spec.name])

        # Create the role
        insert(role_model)


listen(role_permission_association, "after_create", init_roles_and_permissions)