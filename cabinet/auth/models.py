from datetime import datetime, timedelta
from typing import Any, Dict

from sqlalchemy.event import listen
from sqlalchemy.orm import relationship

from cabinet.auth.permissions import all_permissions, all_roles
from cabinet.database import db, insert
from cabinet.models import role_permission_association, user_role_association


class Permission(db.Model):
    __tablename__ = "permission"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(32), nullable=False, unique=True)
    description = db.Column(db.String(64))

    object = db.Column(db.String(32), nullable=False)
    read = db.Column(db.Boolean(), nullable=False)
    write = db.Column(db.Boolean(), nullable=False)

    roles = relationship(
        "Role", secondary=role_permission_association, back_populates="permissions"
    )

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def __repr__(self) -> str:
        return f"Permission(name={self.name}, description={self.description}, object={self.object})"


class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(32), nullable=False, unique=True)
    description = db.Column(db.String(64))

    permissions = relationship("Permission", secondary=role_permission_association)
    users = relationship(
        "User", secondary=user_role_association, back_populates="roles"
    )

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def __repr__(self) -> str:
        return f"Role(name={self.name}, description={self.description})"


class Session(db.Model):
    # TODO: Cleanup expired sessions
    __tablename__ = "session"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = relationship("User", back_populates="sessions")

    ttl = db.Column(db.BigInteger)
    created_on = db.Column(db.DateTime, server_default=db.func.now())

    def is_expired(self) -> bool:
        if self.ttl == -1:
            return False

        now: datetime = datetime.now()
        expiration_time: datetime = self.created_on + timedelta(seconds=self.ttl)
        expired: bool = now > expiration_time

        return expired

    def __repr__(self) -> str:
        return f"Session(user_id={self.user_id}, ttl={self.ttl}, created_on={self.created_on})"


def init_roles_and_permissions(*args: Any, **kwargs: Any) -> None:
    created_permissions: Dict = {}
    for permission_spec in all_permissions:
        permission_model = insert(
            Permission(
                name=permission_spec.name,
                description=permission_spec.description,
                object=permission_spec.permission.object,
                read=permission_spec.permission.read,
                write=permission_spec.permission.write,
            )
        )
        created_permissions[permission_spec.name] = permission_model

    for role_spec in all_roles:
        role_model = Role(name=role_spec.name, description=role_spec.description)

        for permission_name in role_spec.permissions:
            role_model.permissions.append(created_permissions[permission_name])

        # Create the role
        insert(role_model)


listen(role_permission_association, "after_create", init_roles_and_permissions)
