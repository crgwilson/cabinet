from datetime import datetime
from functools import wraps
from logging import getLogger as get_logger
from typing import Any, Callable, List, Optional

from flask import current_app, request

import jwt

from sqlalchemy import or_

from cabinet import database
from cabinet._types import ApiObject, ApiObjectAttribute
from cabinet.auth.models import Permission, Role, Session
from cabinet.auth.permissions import ApiPermission
from cabinet.exceptions import InvalidToken, MalformedAuthHeader, UnsupportedAuthType
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
DELETE_METHODS = ["delete"]


def get_auth_token_from_header(header: str) -> AuthToken:
    try:
        split_header: List[str] = header.split()
        auth_type: str = split_header[0]
        auth_payload: str = split_header[1]
        auth_bytes: bytes = str.encode(auth_payload)
    except IndexError:
        logger.error("Received request with malformed 'Authorization' header")
        raise MalformedAuthHeader(header)

    if auth_type != "Bearer":
        raise UnsupportedAuthType(auth_type)

    try:
        token = AuthToken.decode(auth_bytes, current_app.config["CABINET_SECRET"])
    except jwt.DecodeError:
        logger.error("Received an auth token which could not be decoded")
        raise InvalidToken(auth_payload)

    return token


def permission_required(api_object: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def check_permissions(*args: Any, **kwargs: Any) -> Any:
            # TODO: Change the above return annotation
            if not api_object:
                # TODO: Raise an exception here because we need this variable
                return CabinetApiResponse.internal_server_error(
                    "Could not determine required permissions for this request"
                )

            auth_header: Optional[str] = request.headers.get("Authorization")
            if not auth_header:
                return CabinetApiResponse.unauthorized()

            try:
                token = get_auth_token_from_header(auth_header)
            except (InvalidToken, UnsupportedAuthType, MalformedAuthHeader):
                return CabinetApiResponse.unauthorized()

            # TODO: What happens if this raises an exception?
            session = get_session_with_token(token)

            if session.is_expired:
                # TODO: Session token has expired, return unauthorized
                return CabinetApiResponse.unauthorized()

            required_permission = ApiPermission(
                object=api_object,
                read=func.__name__ in READ_METHODS,
                write=func.__name__ in WRITE_METHODS,
                delete=func.__name__ in DELETE_METHODS,
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

    query_result: List[Permission] = query.all()
    return query_result


def has_permission(user_id: int, required_permission: ApiPermission) -> bool:
    # This could probably be better
    if required_permission.read:
        operation_type = Permission.read
    elif required_permission.write:
        operation_type = Permission.write
    else:
        operation_type = Permission.delete

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
