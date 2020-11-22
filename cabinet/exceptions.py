from logging import getLogger as get_logger
from typing import Any

logger = get_logger(__name__)


class CabinetException(Exception):
    def __init__(self, *args: Any, **kwargs: Any):
        logger.exception(str(self))


class MalformedAuthHeader(CabinetException):
    def __init__(self, header: str) -> None:
        self.header = header
        super().__init__()

    def __str__(self) -> str:
        return f"Received request with malformed auth header {self.header}"


class UnsupportedAuthType(CabinetException):
    def __init__(self, auth_type: str) -> None:
        self.auth_type = auth_type
        super().__init__()

    def __str__(self) -> str:
        return f"Received request with unsupported auth type {self.auth_type}"


class MissingConfiguration(CabinetException):
    def __init__(self, key: str) -> None:
        self.key = key
        super().__init__()

    def __str__(self) -> str:
        return f"Required key {self.key} not found in cabinet app configuration"


class InvalidToken(CabinetException):
    def __init__(self, token: str) -> None:
        self.token = token
        super().__init__()

    def __str__(self) -> str:
        return f"Received request with invalid auth token {self.token}"


class IncorrectUsernameOrPassword(CabinetException):
    def __init__(self, username: str) -> None:
        self.username = username
        super().__init__()

    def __str__(self) -> str:
        return f"Failed login attempt for user {self.username} - Incorrect Username or Password"
