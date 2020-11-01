from datetime import datetime
from functools import wraps
from logging import getLogger as get_logger
from typing import Any, Callable, List

from flask import current_app, request

import jwt

from sqlalchemy import or_

from cabinet import database
from cabinet._types import ApiObject, ApiObjectAttribute
from cabinet.auth.models import Permission, Role, Session
from cabinet.auth.permissions import ApiPermission
from cabinet.response import CabinetApiResponse
from cabinet.user.models import User

logger = get_logger(__name__)


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
            "created_on": self.created_on.isoformat(),
            "ttl": self.ttl,
        }

    def encode(self) -> bytes:
        return jwt.encode(
            self.payload,
            self.secret,
            algorithm=self.ALGO,
        )

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


def create_role(**kwargs: ApiObjectAttribute) -> Role:
    role = Role(
        name=kwargs["name"],
        description=kwargs["name"],
    )
    return database.update(role)


def get_all_sessions() -> List[Session]:
    return database.get_all(Session)


def get_session(session_id: int) -> Session:
    return database.get(Session, session_id)


def get_session_with_token(token: AuthToken) -> Session:
    s = database.session()
    query = s.query(Session).filter(
        Session.user_id == token.user_id,
        Session.created_on == str(token.created_on),
        Session.ttl == token.ttl,
    )
    return query.first()


def create_session(**kwargs: ApiObjectAttribute) -> Session:
    session = Session(**kwargs)
    return database.insert(session)


def delete_session(session_id: int) -> None:
    session = get_session(session_id)
    database.delete(session)


READ_METHODS = ["get"]
WRITE_METHODS = ["put", "post", "patch"]


def permission_required(api_object: str):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def check_permissions(*args: Any, **kwargs: Any):
            if not api_object:
                # TODO: Raise an exception here because we need this variable
                return CabinetApiResponse.internal_server_error(
                    "Could not determine required permissions for this request"
                )

            if not request.headers.get("Authorization"):
                # TODO: Error here - Missing auth header
                return CabinetApiResponse.unauthorized()

            try:
                auth_header: str = request.headers.get("Authorization")
                split_header: List[str] = auth_header.split()
                auth_type: str = split_header[0]
                auth_payload: bytes = str.encode(split_header[1])
            except IndexError:
                logger.error("Received request with malformed 'Authorization' header")
                return CabinetApiResponse.unauthorized()

            if auth_type != "Bearer":
                # TODO: Error here - unsupported auth type
                return CabinetApiResponse.unauthorized()

            # Wrap this in a try and error properly if theres a problem
            token = AuthToken.decode(auth_payload, current_app.config["CABINET_SECRET"])
            # Might error here too
            session = get_session_with_token(token)

            if session.is_expired:
                # TODO: Session token has expired, return unauthorized
                return CabinetApiResponse.unauthorized()

            is_write_operation = func.__name__ in WRITE_METHODS
            required_permission = ApiPermission(
                object=api_object,
                read=not is_write_operation,
                write=is_write_operation,
            )

            if not has_permission(session.user_id, required_permission):
                return CabinetApiResponse.forbidden()

            return func(*args, **kwargs)

        return check_permissions

    return decorator


def get_all_user_permissions(user_id: int) -> List[Permission]:
    # session.query(Permission).join(
    #   Role, Permission.roles
    # ).join(
    #   User, Role.users
    # ).filter(
    #   User.username=="admin"
    # ).distinct().all()
    s = database.session()
    query = (
        s.query(Permission)
        .join(Role, Permission.roles)
        .join(User, Role.users)
        .filter(User.id == user_id)
        .distinct()
    )

    return query.all()


def has_permission(user_id: int, required_permission: ApiPermission) -> bool:
    # This could probably be better
    if required_permission.read:
        operation_type = Permission.read
    else:
        operation_type = Permission.write

    s = database.session()
    query = (
        s.query(Permission)
        .join(Role, Permission.roles)
        .join(User, Role.users)
        .filter(
            User.id == user_id,
            or_(
                Permission.object == "All",
                Permission.object == required_permission.object,
            ),
            operation_type == True,  # noqa E720
        )
        .distinct()
    )

    results: List[Permission] = query.all()

    return len(results) > 0
