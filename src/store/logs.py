"""Logging setup: every log line is structured data (JSON in production)."""

import logging

import structlog
from structlog.typing import Processor


def configure_logging(level: str, log_format: str) -> None:
    """Build the structlog pipeline once at startup. Every log call goes through these steps."""
    shared: list[Processor] = [
        structlog.contextvars.merge_contextvars,  # add fields bound for THIS request (request_id)
        structlog.processors.add_log_level,  # + "level": "info"
        structlog.processors.TimeStamper(fmt="iso", utc=True),  # + "timestamp" (UTC, sortable)
    ]
    renderer: list[Processor]
    if log_format == "json":
        # dict_tracebacks: an exception becomes structured fields, not 40 loose text lines
        renderer = [structlog.processors.dict_tracebacks, structlog.processors.JSONRenderer()]
    else:
        renderer = [structlog.dev.ConsoleRenderer()]  # colors + aligned columns for humans

    structlog.configure(
        processors=shared + renderer,
        # drop lines below the level BEFORE doing any work (DEBUG lines cost ~nothing in prod)
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelNamesMapping()[level]),
    )
