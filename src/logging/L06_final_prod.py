import atexit
import json
import logging
import logging.config
import os
from queue import Queue

logger = logging.getLogger(__name__)  # Module-level logger
log_queue = Queue()  # Initialize the queue

def setup_logging():
    # Load the logging configuration from the JSON file
    config_file = os.path.join(os.getcwd(), "src/logging/config06.json")
    with open(config_file) as f_in:
        config = json.load(f_in)

    # Inject the queue into the queue handler configuration
    config["handlers"]["queue_handler"]["queue"] = log_queue

    # Apply the logging configuration
    logging.config.dictConfig(config)

    # Retrieve individual handlers from the global handler registry
    stdout_handler = logging._handlers.get('stdout')
    stderr_handler = logging._handlers.get('stderr')
    file_json_handler = logging._handlers.get('file_json')

    # Ensure all handlers are correctly attached
    if not all([stdout_handler, stderr_handler, file_json_handler]):
        raise RuntimeError("Handlers not correctly attached.")

    # Create and start the QueueListener with the handlers
    queue_listener = logging.handlers.QueueListener(
        log_queue, stdout_handler, stderr_handler, file_json_handler
    )
    queue_listener.start()

    # Ensure the listener stops gracefully on exit
    atexit.register(queue_listener.stop)

def testing_loading_config():
    setup_logging()  # Initialize logging

    # Generate some test logs
    logger.debug("debug message", extra={"x": "hello"})
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("exception message")

if __name__ == "__main__":
    testing_loading_config()

