from datetime import datetime
from typing import List

import jwt

from cabinet import database
from cabinet._types import ApiObject, ApiObjectAttribute
from cabinet.auth.models import Permission, Role, Session


class AuthToken(object):
    ALGO = "HS256"

    def __init__(
        self, user_id: int, created_on: datetime, ttl: int, secret: str
    ) -> None:
        self.user_id: int = user_id
        self.created_on: datetime = created_on
        self.ttl: int = ttl
        self.secret: str = secret

    @property
    def payload(self) -> ApiObject:
        return {
            "user_id": self.user_id,
            "created_on": str(self.created_on),
            "ttl": self.ttl,
        }

    def encode(self) -> bytes:
        return jwt.encode(self.payload, self.secret, algorithm=self.ALGO,)

    @classmethod
    def decode(cls, token: bytes, secret: str) -> "AuthToken":
        decoded = jwt.decode(token, secret, algorithms=cls.ALGO)

        return cls(
            user_id=decoded["user_id"],
            created_on=datetime.fromisoformat(decoded["created_on"]),
            ttl=decoded["ttl"],
            secret=secret,
        )


def get_all_permissions() -> List[Permission]:
    return database.get_all(Permission)


def get_permission(permission_id: int) -> Permission:
    return database.get(Permission, permission_id)


def get_all_roles() -> List[Role]:
    return database.get_all(Role)


def get_role(role_id: int) -> Role:
    return database.get(Role, role_id)


def get_all_sessions() -> List[Session]:
    return database.get_all(Session)


def get_session(session_id: int) -> Session:
    return database.get(Session, session_id)


def get_session_with_attrs(user_id: int, created_on: datetime, ttl: int) -> Session:
    s = database.session()
    query = s.query(Session).filter(
        Session.user_id == user_id, Session.created_on == created_on, Session.ttl == ttl
    )
    return query.first()


def create_session(**kwargs: ApiObjectAttribute) -> Session:
    session = Session(**kwargs)
    return database.insert(session)


def delete_session(session_id: int) -> None:
    session = get_session(session_id)
    database.delete(session)
