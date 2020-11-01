from datetime import datetime
from typing import Optional

from flask.wrappers import Response

import pytest

from cabinet import create_app
from cabinet.config import DevelopmentCabinetConfig
from cabinet.database import db as app_db
from cabinet.response import HTTPResponseMessages, HTTPStatusCodes

from tests.factories import (
    AdminUserFactory,
    SessionFactory,
    SessionTokenFactory,
    UserFactory,
)


test_config = DevelopmentCabinetConfig()


class Helpers:
    SUCCESS_CODE = HTTPStatusCodes.OK.value
    NOT_FOUND_CODE = HTTPStatusCodes.NOT_FOUND.value
    ERROR_CODE = HTTPStatusCodes.INTERNAL_SERVER_ERROR.value

    SUCCESS_MESSAGE = HTTPResponseMessages.OK.value
    NOT_FOUND_MESSAGE = HTTPResponseMessages.NOT_FOUND.value

    SUCCESS_JSON = {"message": SUCCESS_MESSAGE}
    NOT_FOUND_JSON = {"message": NOT_FOUND_MESSAGE}

    CONTENT_TYPE = "application/json"
    AUTH_TYPE = "Bearer"

    def headers(self, token: Optional[str] = None) -> dict:
        headers = {}
        headers["Content-Type"] = self.CONTENT_TYPE
        if token:
            headers["Authorization"] = f"{self.AUTH_TYPE} {token}"

        return headers

    def assert_valid(self, response: Response) -> None:
        assert response.is_json
        assert response.content_type == self.CONTENT_TYPE

    def assert_success(self, response: Response) -> None:
        self.assert_valid(response)
        assert response.status_code == self.SUCCESS_CODE

    def assert_not_found(self, response: Response) -> None:
        self.assert_valid(response)
        assert response.status_code == self.NOT_FOUND_CODE
        assert response.json == self.NOT_FOUND_JSON

    def assert_failure(self, response: Response) -> None:
        self.assert_valid(response)
        assert response.status_code == self.ERROR_CODE


@pytest.yield_fixture(scope="session")
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


@pytest.yield_fixture(scope="function")
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


@pytest.yield_fixture
def session_token(session):
    admin_user_id = 1

    session_factory = SessionFactory()
    new_session = session_factory.new(admin_user_id)

    session.commit()

    token_factory = SessionTokenFactory()
    token = token_factory.new(new_session, test_config.CABINET_SECRET)

    return token.decode("utf-8")


@pytest.fixture
def now() -> datetime:
    return datetime.now()


@pytest.fixture
def helpers() -> Helpers:
    return Helpers()
