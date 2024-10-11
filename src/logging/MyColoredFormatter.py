import logging
import datetime as dt
from src.logging.constants import *



class MyColoredFormatter(logging.Formatter):
    """
    Custom log formatter to add colors to log messages based on the log level
    and other attributes such as timestamp, filename, function name, and line number.
    """

    def format(self, record):
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
        log_line = f"{asctime}: {filename}: {funcName}: L{lineno}: {levelname}: {message}"
        return log_line

