import logging


class StdoutFilter(logging.Filter):
    """Allow only DEBUG and INFO messages for stdout."""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno <= logging.INFO


class StderrFilter(logging.Filter):
    """Allow only WARNING, ERROR, and CRITICAL messages for stderr."""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno >= logging.WARNING
