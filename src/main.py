# import csv
import logging

# import os
# import random
# import sys
# from collections import Counter, OrderedDict, defaultdict
# from pathlib import Path
# from tests.debugging_template import testing
from src.helper.employee import Employee

# logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
stream_handler = logging.StreamHandler()

stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# from lib.basics_of_python.syntax_and_structure import Employee, my_message
from rich.console import Console

console = Console()


def my_logging_function():
    for i in range(10):
        logger.info(f"current value of i -> {i}")


# from src.helper.caller import Employee

if __name__ == "__main__":
    # testing()
    emp = Employee("Jack", "Michael")
    console.log("----------- EMPTY SPACE ---------------")
    my_logging_function()
    # print(emp)
