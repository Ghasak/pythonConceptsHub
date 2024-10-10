# Define ANSI escape codes for colors
RESET = "\033[0m"
COLORS = {
    "DEBUG": "\033[36m",  # Cyan for DEBUG level
    "INFO": "\033[95m",  # light magenta
    "WARNING": "\033[33m",  # Yellow for WARNING level
    "ERROR": "\033[31m",  # Red for ERROR level
    "CRITICAL": "\033[1;31m",  # Bold Red for CRITICAL level
}

# Additional colors for log fields
FILENAME_COLOR = "\033[35m"  # Magenta for filename
FUNCNAME_COLOR = "\033[34m"  # Blue for function name
LINENO_COLOR = "\033[36m"  # Cyan for line number
TIME_COLOR = "\033[90m"  # Light gray for timestamp

if __name__ == "__main__":
    pass
