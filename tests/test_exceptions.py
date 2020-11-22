import pytest

from cabinet import exceptions


def patch_logger(monkeypatch, mock_logger) -> None:
    monkeypatch.setattr(exceptions, "logger", mock_logger)


def test_cls_base_exception(monkeypatch, logger) -> None:
    patch_logger(monkeypatch, logger)

    with pytest.raises(exceptions.CabinetException):
        raise exceptions.CabinetException()

    captured_logs = logger.get_logs_by_level("exception")
    assert len(captured_logs) == 1


def test_cls_malformed_auth_header_exception(monkeypatch, logger) -> None:
    patch_logger(monkeypatch, logger)

    with pytest.raises(exceptions.MalformedAuthHeader):
        raise exceptions.MalformedAuthHeader(header="test")

    captured_logs = logger.get_logs_by_level("exception")
    assert len(captured_logs) == 1
    assert captured_logs[0] == "Received request with malformed auth header test"


def test_cls_unsupported_auth_type_exception(monkeypatch, logger) -> None:
    patch_logger(monkeypatch, logger)

    with pytest.raises(exceptions.UnsupportedAuthType):
        raise exceptions.UnsupportedAuthType(auth_type="Basic")

    captured_logs = logger.get_logs_by_level("exception")
    assert len(captured_logs) == 1
    assert captured_logs[0] == "Received request with unsupported auth type Basic"


def test_cls_missing_configuration_exception(monkeypatch, logger) -> None:
    patch_logger(monkeypatch, logger)

    with pytest.raises(exceptions.MissingConfiguration):
        raise exceptions.MissingConfiguration(key="test")

    captured_logs = logger.get_logs_by_level("exception")
    assert len(captured_logs) == 1
    assert (
        captured_logs[0] == "Required key test not found in cabinet app configuration"
    )


def test_cls_invalid_token_exception(monkeypatch, logger) -> None:
    patch_logger(monkeypatch, logger)

    with pytest.raises(exceptions.InvalidToken):
        raise exceptions.InvalidToken(token="test")  # noqa: S106

    captured_logs = logger.get_logs_by_level("exception")
    assert len(captured_logs) == 1
    assert captured_logs[0] == "Received request with invalid auth token test"


def test_cls_incorrect_username_or_password(monkeypatch, logger) -> None:
    patch_logger(monkeypatch, logger)

    with pytest.raises(exceptions.IncorrectUsernameOrPassword):
        raise exceptions.IncorrectUsernameOrPassword(username="test")

    captured_logs = logger.get_logs_by_level("exception")
    assert len(captured_logs) == 1
    assert (
        captured_logs[0]
        == "Failed login attempt for user test - Incorrect Username or Password"
    )
