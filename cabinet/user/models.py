from typing import Any

import bcrypt

from sqlalchemy.event import listen
from sqlalchemy.orm import relationship

from cabinet.database import db
from cabinet.models import user_role_association


def hash_password(mapper: Any, connection: Any, target: Any) -> None:
    target.hash_password()


def insert_admin_user(*args: Any, **kwargs: Any) -> None:
    db.session.add(User(id=1, username="admin", password="admin"))  # noqa S106


def give_admin_access(*args: Any, **kwargs: Any) -> None:
    admin_user_insert = user_role_association.insert().values(user_id=1, role_id=1)
    db.session.execute(admin_user_insert)
    db.session.commit()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    roles = relationship("Role", secondary=user_role_association)
    sessions = relationship("Session", cascade="all, delete", passive_deletes=True)

    # TODO add roles
    # TODO add api keys

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def hash_password(self) -> None:
        pw_bytes = str.encode(self.password)
        hashed_password = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
        self.password = hashed_password.decode("utf-8")

    def check_password(self, password: str) -> bool:
        param_bytes = str.encode(password)
        pw_bytes = str.encode(self.password)

        return bcrypt.checkpw(param_bytes, pw_bytes)

    def __repr__(self) -> str:
        return f"User(username={self.username})"


listen(User, "before_insert", hash_password)
listen(User.__table__, "after_create", insert_admin_user)
listen(user_role_association, "after_create", give_admin_access)
