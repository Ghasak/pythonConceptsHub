import atexit
import json
import logging
import logging.config
import os
from queue import Queue

logger = logging.getLogger(__name__)  # Module-level logger
log_queue = Queue()  # Initialize the log queue


def setup_logging():
    # Load the logging configuration from the JSON file
    config_file = os.path.join(os.getcwd(), "src/logging/config05.json")

    with open(config_file) as f_in:
        config = json.load(f_in)

    # Inject the queue into the queue handler configuration
    config["handlers"]["queue_handler"]["queue"] = log_queue

    # Apply the logging configuration
    logging.config.dictConfig(config)

    # Verify that handlers are attached correctly
    handlers = logging.getLogger().handlers
    if not handlers:
        raise RuntimeError("No handlers were attached to the root logger.")
    # print(f"Attached Handlers: {[type(h).__name__ for h in handlers]}")  # Debug print

    # Ensure the queue handler is the first handler
    #queue_handler = handlers[0]

    # Use a try-except block to avoid IndexError
    try:
        queue_listener = logging.handlers.QueueListener(log_queue, *handlers[1:])  # Pass all remaining handlers to the listener
    except IndexError as e:
        raise RuntimeError("Not enough handlers attached to the root logger.") from e

    # Start the listener
    queue_listener.start()
    atexit.register(queue_listener.stop)


def testing_loading_config():
    setup_logging()  # Initialize logging with the config

    # Generate logs for testing
    logger.info("[INFO] This is just a test", extra={"x": "hello"})
    logger.debug("[DEBUG] This is just a test", extra={"y": "world"})
    logger.warning("[WARNING] This is a warning test")
    logger.error("[ERROR] This is an error test")


if __name__ == "__main__":
    testing_loading_config()
