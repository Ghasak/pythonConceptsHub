import logging


class StdoutFilter1(logging.Filter):
    """Filter Number 1
    This filter will remove all messages
    like `warning` ,`error` and `critical` from my log record
    What will be print is only the
    `info` and `debug`
    """

    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        return record.levelno < logging.WARNING


class StdoutFilter2(logging.Filter):
    """Filter Number 2
    This filter will remove all messages
    like `debug` and `info` from my log record
    What will be print is only the
    warning, error, critical messages
    """

    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        return record.levelno >= logging.WARNING


class StderrFilter(logging.Filter):

    def filter(self, record):
        return record.levelno >= logging.WARNING  # Allow only WARNING and above


class QueueHandlerFilter(logging.Filter):
    """Filter for QueueHandler
    This filter will pass all log records to the queue,
    ensuring that all log levels are enqueued.
    """

    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        # Always return True to pass all log levels to the queue
        return True
