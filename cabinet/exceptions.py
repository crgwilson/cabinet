from logging import getLogger as get_logger
from typing import Any

logger = get_logger(__name__)


class CabinetException(Exception):
    def __init__(self, *args: Any, **kwargs: Any):
        logger.exception(self)


class MalformedAuthHeader(CabinetException):
    def __init__(self, header: str) -> None:
        self.header = header
        super().__init__()


class UnsupportedAuthType(CabinetException):
    def __init__(self, auth_type: str) -> None:
        self.auth_type = auth_type
        super().__init__()


class InvalidToken(CabinetException):
    def __init__(self, token: str) -> None:
        self.token = token
        super().__init__()
