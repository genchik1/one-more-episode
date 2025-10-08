import logging
import sys
from datetime import datetime
from typing import Any

import orjson


class StructuredLogger:
    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger

    def debug(self, message: str, **kwargs) -> None:
        self._logger.debug(message, extra={"extra": kwargs})

    def info(self, message: str, **kwargs) -> None:
        self._logger.info(message, extra={"extra": kwargs})

    def warning(self, message: str, **kwargs) -> None:
        self._logger.warning(message, extra={"extra": kwargs})

    def error(self, message: str, **kwargs) -> None:
        self._logger.error(message, extra={"extra": kwargs})


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        if record.__getattribute__("extra"):
            log_entry.update(**record.extra)
        if record.args:
            if isinstance(record.args, dict):
                log_entry.update(record.args)
            else:
                log_entry["args"] = record.args

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        if record.stack_info:
            log_entry["stack_trace"] = self.formatStack(record.stack_info)

        return orjson.dumps(log_entry).decode("utf-8")


def setup_logging(level: str = "INFO", json_output: bool = True) -> logging.Logger:
    if json_output:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    root_logger.addHandler(console_handler)

    logging.getLogger("requests").setLevel(logging.WARNING)

    return root_logger
