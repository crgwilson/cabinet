from datetime import datetime
from typing import Dict, List

import pytest

from cabinet import create_app
from cabinet.config import DevelopmentCabinetConfig
from cabinet.database import db as app_db
from cabinet.nfsganesha.constants import nfs_ganesha_constants

from tests.dbus import MockDbus, MockDbusObject, MockDbusService, mock_show_exports
from tests.factories import (
    AdminUserFactory,
    SessionFactory,
    SessionTokenFactory,
    UserFactory,
)

test_config = DevelopmentCabinetConfig()


class SpyLogger(object):
    def __init__(self) -> None:
        self.logs: Dict[str, List[str]] = {
            "debug": [],
            "info": [],
            "warn": [],
            "error": [],
            "exception": [],
        }

    def debug(self, message: str) -> None:
        self.logs["debug"].append(message)

    def info(self, message: str) -> None:
        self.logs["info"].append(message)

    def warn(self, message: str) -> None:
        self.logs["warn"].append(message)

    def error(self, message: str) -> None:
        self.logs["error"].append(message)

    def exception(self, message: str) -> None:
        self.logs["exception"].append(message)

    def get_logs_by_level(self, log_level: str) -> List[str]:
        return self.logs[log_level]


@pytest.fixture(scope="session")
def app(request):
    flask_app = create_app(test_config)
    ctx = flask_app.app_context()
    ctx.push()

    yield flask_app

    ctx.pop()


@pytest.fixture(scope="session")
def db(app, request):
    app_db.drop_all()
    app_db.create_all()

    app_db.app = app
    yield app_db

    app_db.drop_all()


@pytest.fixture(scope="function")
def session(db, request):
    db.session.begin_nested()
    yield db.session
    db.session.rollback()


@pytest.fixture(scope="function")
def client(app, session):
    with app.test_client() as c:
        yield c


@pytest.fixture
def user(session):
    user_factory = UserFactory()
    user = user_factory.new()

    session.commit()
    return user


@pytest.fixture
def admin_user(session):
    admin_user_factory = AdminUserFactory()
    admin_user = admin_user_factory.new()

    session.commit()
    return admin_user


@pytest.fixture
def user_predictable_password(session):
    user_factory = AdminUserFactory()
    user = user_factory.new(password="password")  # noqa: S106

    session.commit()
    return user


@pytest.fixture
def token(session):
    admin_user_id = 1

    session_factory = SessionFactory()
    new_session = session_factory.new(admin_user_id)

    session.commit()

    token_factory = SessionTokenFactory()
    token = token_factory.new(new_session, test_config.CABINET_SECRET)

    yield token.decode("utf-8")


@pytest.fixture
def expired_token(session):
    admin_user_id = 1

    session_factory = SessionFactory()
    new_session = session_factory.new(admin_user_id, ttl=0)

    session.commit()

    token_factory = SessionTokenFactory()
    token = token_factory.new(new_session, test_config.CABINET_SECRET)

    yield token.decode("utf-8")


@pytest.fixture
def tokens(session, user) -> dict:
    admin_user_id = 1
    tokens_to_return = {}

    session_factory = SessionFactory()
    privileged_session = session_factory.new(admin_user_id)
    expired_session = session_factory.new(admin_user_id, ttl=0)
    unprivileged_session = session_factory.new(user.id)

    session.commit()

    token_factory = SessionTokenFactory()
    privileged_token = token_factory.new(privileged_session, test_config.CABINET_SECRET)
    expired_token = token_factory.new(expired_session, test_config.CABINET_SECRET)
    unprivileged_token = token_factory.new(
        unprivileged_session, test_config.CABINET_SECRET
    )

    tokens_to_return["privileged"] = privileged_token.decode("utf-8")
    tokens_to_return["expired"] = expired_token.decode("utf-8")
    tokens_to_return["unprivileged"] = unprivileged_token.decode("utf-8")

    yield tokens_to_return


@pytest.fixture(scope="function")
def headers(tokens) -> dict:
    headers = {
        "valid": {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + tokens["privileged"],
        },
        "expired": {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + tokens["expired"],
        },
        "no_permissions": {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + tokens["unprivileged"],
        },
        "invalid_auth_type": {
            "Content-Type": "application/json",
            "Authorization": "Basic " + tokens["unprivileged"],
        },
        "invalid_token": {
            "Content-Type": "application/json",
            "Authorization": "Bearer thisisatest",
        },
        "no_token": {"Content-Type": "application/json", "Authorization": "Bearer"},
        "no_auth": {"Content-Type": "application/json"},
    }

    yield headers


@pytest.fixture(scope="function")
def logger() -> SpyLogger:
    return SpyLogger()


@pytest.fixture(scope="function")
def dbus() -> MockDbus:
    export_manager_methods = {}
    for method in nfs_ganesha_constants.EXPORT_MANAGER_METHODS:
        export_manager_methods[method] = mock_show_exports

    mock_export_manager = MockDbusObject(
        nfs_ganesha_constants.EXPORT_MANAGER_OBJECT, export_manager_methods
    )

    mock_dbus_service = MockDbusService(
        nfs_ganesha_constants.SERVICE, [mock_export_manager]
    )
    mock_dbus = MockDbus([mock_dbus_service])

    return mock_dbus


@pytest.fixture
def now() -> datetime:
    return datetime.now()
