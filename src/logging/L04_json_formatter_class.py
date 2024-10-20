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
    logger.info(f"[INFO] this is just a test ")
    logger.debug(f"[DEBUG] this is just a test ")
    logger.warning(f"[WARNING] this is a warning test")
    logger.error(f"[ERROR] this is an error test")


if __name__ == "__main__":
    pass
