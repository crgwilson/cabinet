from datetime import datetime

import pytest

from cabinet import create_app
from cabinet.config import DevelopmentCabinetConfig
from cabinet.database import db as app_db

from tests.factories import (
    AdminUserFactory,
    SessionFactory,
    SessionTokenFactory,
    UserFactory,
)

test_config = DevelopmentCabinetConfig()


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
def token(session):
    admin_user_id = 1

    session_factory = SessionFactory()
    new_session = session_factory.new(admin_user_id)

    session.commit()

    token_factory = SessionTokenFactory()
    token = token_factory.new(new_session, test_config.CABINET_SECRET)

    yield token.decode("utf-8")


@pytest.yield_fixture
def expired_token(session):
    admin_user_id = 1

    session_factory = SessionFactory()
    new_session = session_factory.new(admin_user_id, ttl=0)

    session.commit()

    token_factory = SessionTokenFactory()
    token = token_factory.new(new_session, test_config.CABINET_SECRET)

    yield token.decode("utf-8")


@pytest.yield_fixture(scope="function")
def headers(token, expired_token) -> dict:
    headers = {
        "valid": {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        "expired": {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {expired_token}",
        },
        "invalid_auth_type": {
            "Content-Type": "application/json",
            "Authorization": f"Basic {token}",
        },
        "no_token": {"Content-Type": "application/json", "Authorization": "Bearer"},
        "no_auth": {"Content-Type": "application/json"},
    }

    yield headers


@pytest.fixture
def now() -> datetime:
    return datetime.now()
