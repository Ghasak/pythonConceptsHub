import logging
import logging.config
import time
from datetime import datetime

from src.logging.constants import *


class CustomColoredFormatter(logging.Formatter):
    """
    Custom log formatter to add colors to log messages based on the log level
    and other attributes such as timestamp, filename, function name, and line number.
    Inherits:
        logging.Formatter: A standard logging Formatter that formats log records.
    Methods:
        formatTime(record, datefmt=None): Formats the creation time of the log record, including timezone.
        format(record): Returns the formatted string for the log message, applying color to various fields.
    """

    def formatTime(self, record, datefmt=None):
        """
        Formats the time of the log record, including timezone.
        Args:
            record (LogRecord): The log record containing all the information to be logged.
            datefmt (str, optional): A format string for the date and time.
        Returns:
            str: The formatted time string, including the timezone.
        This method uses the `datetime.fromtimestamp()` function to convert the creation timestamp
        to a datetime object and then formats it. The timezone is appended to the formatted time.
        """
        dt = datetime.fromtimestamp(
            record.created, tz=datetime.now().astimezone().tzinfo
        )
        if datefmt:
            formatted_time = dt.strftime(datefmt)
        else:
            formatted_time = dt.isoformat()
        # Append the timezone name
        timezone = time.tzname[0]
        return f"{formatted_time} {timezone}"

    def format(self, record):
        """
        Formats the log record by adding color to different
        components of the log message.
        Args:
            record (LogRecord): The log record containing all
                                the information to be logged.
        Returns:
            str: The complete formatted log message
                 as a string, including colors for different fields.
        """
        # Generate timestamp with formatTime method including timezone
        asctime = f"{TIME_COLOR}{self.formatTime(record, self.datefmt)}{RESET}"

        # Add color to different fields
        log_color = COLORS.get(record.levelname, RESET)
        filename = f"{FILENAME_COLOR}{record.filename}{RESET}"
        funcName = f"{FUNCNAME_COLOR}{record.funcName}{RESET}"
        lineno = f"{LINENO_COLOR}{record.lineno}{RESET}"
        levelname = f"{log_color}{record.levelname}{RESET}"
        message = f"{log_color}{record.getMessage()}{RESET}"

        # Construct formatted log line
        log_line = (
            f"{asctime}: {filename}: {funcName}: L{lineno}: {levelname}: {message}"
        )
        return log_line


# Logging configuration dictionary
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": CustomColoredFormatter,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        "root": {
            "level": "DEBUG",
            "handlers": ["stdout"],
        }
    },
}

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


def justLogging():
    """
    Test function that generates log messages at various log levels.

    Logs messages at the INFO, DEBUG, WARNING, ERROR, and CRITICAL levels to demonstrate
    the colored output from the custom formatter.

    The different log levels include:
    - INFO: A general message, indicating normal operation.
    - DEBUG: A debug-level message, useful for diagnostic purposes.
    - WARNING: A message indicating a potential issue.
    - ERROR: A message indicating a more serious problem.
    - CRITICAL: A message indicating a severe error that needs immediate attention.
    """
    logger.info("Hello, this is a message from God!!")
    logger.debug("Debugging the message from God!!")
    logger.warning("This is a warning message!!")
    logger.error("An error occurred!!")
    logger.critical("Critical issue!!")

    try:
        # Variables for division
        a = 10
        b = 0

        # Raise ZeroDivisionError if b is zero
        if b == 0:
            raise ZeroDivisionError(
                "Attempted to divide by zero, which is not allowed."
            )

        # Division operation
        c = a / b
    except ZeroDivisionError as e:
        # Handle specific ZeroDivisionError
        logger.error(f"ZeroDivisionError occurred: {e}")
    except Exception as e:
        # Handle any other unexpected exceptions
        logger.exception(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Test the logging function
    justLogging()
