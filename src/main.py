import random
from collections import Counter, OrderedDict, defaultdict

# from lib.basics_of_python.syntax_and_structure import Employee, my_message
from rich.console import Console

from src.helper.caller import Employee

console = Console()

Employee.generate()


class Vector2d:
    CONFIG = {'num_of_vec': 0}

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


# console.log(my_message)
if __name__ == "__main__":
    pass
