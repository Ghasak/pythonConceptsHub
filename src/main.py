# import csv
# import os
# import random
# import sys
# from collections import Counter, OrderedDict, defaultdict
# from pathlib import Path
# from tests.debugging_template import testing
# from src.helper.employee import Employee
# from lib.basics_of_python.syntax_and_structure import Employee, my_message
from rich.console import Console

# from src.logging.L01_myLoggerEngine import justLogging, logger
# from src.logging.L02_loading_config_from_outside import testing_loading_config
# from src.logging.L03_multi_config import testing_loading_config
from src.logging.L04_json_formatter_class import testing_loading_config

console = Console()

# justLogging()

testing_loading_config()

# def myFunction():
#     for _ in range(10):
#         logger.info("this is just a test happend on main module,")
#

if __name__ == "__main__":
    pass
