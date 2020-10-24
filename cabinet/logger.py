import logging
from sys import stdout

from cabinet.config import CabinetConfig


def logger_init(config: CabinetConfig, logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(config.LOG_LEVEL)

    handler = logging.StreamHandler(stdout)
    formatter = logging.Formatter(config.LOG_FORMAT)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
