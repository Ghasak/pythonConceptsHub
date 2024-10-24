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
from src.logging.L04_json_formatter_class import logger, testing_loading_config

console = Console()

# justLogging()

testing_loading_config()

# def myFunction():
#     for _ in range(10):
#         logger.info("this is just a test happend on main module,")
#


class Employee:

    CONFIG = {"num_of_emp": 0}

    def __init__(
        self,
        first_name: str = None,
        last_name: str = None,
        age: int = 0,
        salary: float = 0.0,
    ) -> None:
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.age: int = age
        self.salary: float = salary


def my_function_for_parsing(param1: str, param2: str):
    if param1.isdigit() or param2.isdigit():
        logger.info("yes both are digits")


class Animal:

    def __init__(self, breed: str = None, sex: bool = 0):
        self.breed = breed
        self.sex = sex
        console.log(f"the  Animal object is created using : {self.breed} with gender: {self.sex}")

    def __str__(self):
        return f"This is an Object created using {self.__class__.__name__}, with: {self.breed} with gender: {self.sex}"


class Dog(Animal):

    def __init__(self, dog_name: str = None, dog_age: int = 0, breed: str = None, sex: bool = 0):
        self.dog_name = dog_name
        self.dog_age = dog_age
        super().__init__(breed, sex)


if __name__ == "__main__":
    my_dog = Dog("Jack", 12, "Bouldog", 1)
    logger.info(my_dog)

    # my_function_for_parsing("1212", "12213")
