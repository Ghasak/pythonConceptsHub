import json
import logging.config
import logging.handlers
import os

logger = logging.getLogger(__name__)


def setup_logging():
    config_file = os.path.join(os.getcwd(), "src/logging/config03.json")

    with open(config_file) as f_in:
        config = json.load(f_in)
    logging.config.dictConfig(config)


def testing_loading_config():
    setup_logging()
    for i in range(10):
        logger.info(f"this is just a test {i}")
        logger.warning(f"this is a warning test {i}")
        logger.error(f"this is an error test {i}")


if __name__ == "__main__":
    pass
