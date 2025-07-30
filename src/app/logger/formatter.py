import logging
from datetime import datetime, timezone
from typing import Any

from pythonjsonlogger.json import JsonFormatter


class CustomJsonFormatter(JsonFormatter):
    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


def get_formatter() -> CustomJsonFormatter:
    return CustomJsonFormatter(
        "%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s",
        json_ensure_ascii=False,
    )
