import logging

from src.domain.logger import ILogger


class TestLogger(ILogger):
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)

    def debug(self, message: str, **kwargs) -> None:
        self._logger.debug(message, extra={"extra_fields": kwargs})

    def info(self, message: str, **kwargs) -> None:
        self._logger.info(message, extra={"extra_fields": kwargs})

    def warning(self, message: str, **kwargs) -> None:
        self._logger.warning(message, extra={"extra_fields": kwargs})

    def error(self, message: str, **kwargs) -> None:
        self._logger.error(message, extra={"extra_fields": kwargs})
