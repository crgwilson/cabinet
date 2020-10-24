from typing import Literal, NamedTuple

LOG_LEVEL = Literal["DEBUG", "INFO", "WARN", "ERROR"]


class CabinetConfig(NamedTuple):
    DEBUG: bool = False
    TESTING: bool = False
    SERVER_NAME: str = "0.0.0.0"
    APPLICATION_ROOT: str = "/"

    LOG_LEVEL: LOG_LEVEL = "INFO"
    LOG_FORMAT: str = "[%(asctime)s] %(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"

    DB_ADDR: str = ":memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"sqlite:///{self.DB_ADDR}"


class DevelopmentCabinetConfig(CabinetConfig):
    DEBUG = True
    TESTING = True
