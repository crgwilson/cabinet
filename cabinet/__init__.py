from typing import Any, Final, List

from flask import Blueprint

from cabinet.config import CabinetConfig
from cabinet.factory import AppFactory
from cabinet.health.views import bp as health_bp

APP_BLUEPRINTS: Final[List[Blueprint]] = [health_bp]


def create_app(config: CabinetConfig) -> Any:
    factory = AppFactory()
    app = factory.create_app(
        app_name=__name__, blueprints=APP_BLUEPRINTS, config=config,
    )

    return app
