from logging import getLogger as get_logger
from typing import Final, List, Optional

from flask import Blueprint, Flask

from cabinet.config import CabinetConfig
from cabinet.extensions import db, migrate

logger = get_logger(__name__)


class AppFactory(object):
    API_VERSION: Final[int] = 1
    DEFAULT_BLUEPRINTS: Final[List[Blueprint]] = []
    DEFAULT_CONFIG: Final[CabinetConfig] = CabinetConfig()

    def __init__(self) -> None:
        logger.debug("App factory created")

    def configure_app(self, config: CabinetConfig) -> None:
        self.app.config.from_object(config)

    def register_extensions(self) -> None:
        db.init_app(self.app)
        migrate.init_app(self.app)

    def register_blueprints(self, blueprints: List[Blueprint]) -> None:
        url_prefix = f"/api/v{self.API_VERSION}"
        for b in blueprints:
            logger.debug(f"Registering blueprint {b} with prefix {url_prefix}")
            self.app.register_blueprint(b, url_prefix=url_prefix)

    def create_app(
        self,
        app_name: Optional[str] = None,
        blueprints: Optional[List[Blueprint]] = None,
        config: Optional[CabinetConfig] = None,
    ) -> Flask:
        if not app_name:
            logger.debug(
                f"No app name was provided to the app factory, using default name {__name__}"
            )
            app_name = __name__

        if not blueprints:
            logger.debug(
                "No blueprints were provided, falling back to default blueprint list"
            )
            blueprints = self.DEFAULT_BLUEPRINTS

        if not config:
            config = self.DEFAULT_CONFIG

        self.app = Flask(app_name, static_folder=None)
        logger.debug("Instantiated Flask app...")

        logger.debug("Configuring Flask app with provided config object...")
        self.configure_app(config)
        logger.debug("Configured Flask app with provided config object...")

        logger.debug("Initializing Flask database...")
        self.register_extensions()

        logger.debug("Registering list of provided blueprints with Flask...")
        self.register_blueprints(blueprints)
        logger.debug("Blueprint registration done...")

        return self.app
