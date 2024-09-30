from pathlib import Path
import sys
import os
import csv
import random
from collections import Counter, OrderedDict, defaultdict

# from lib.basics_of_python.syntax_and_structure import Employee, my_message
from rich.console import Console

from src.helper.caller import Employee

console = Console()

console.log(os.path.abspath(__file__))


data_path = "/Users/gmbp/Desktop/devCode/pythonHub/pythonCheatSheet/src/data/famous_women_in_science.csv"
full_path = os.path.join(os.getcwd(), "src/data/famous_women_in_science.csv")


# Assume you're in the project root, this will always point to the correct path
full_path = Path("src/data/famous_women_in_science.csv").resolve()

# You can then use full_path directly
print(full_path)


def my_context_manager(data_path:str)->None:
    with open(file = data_path, mode = "r",newline="",  encoding = "utf-8") as file:
        lines = file.readlines()
        for line in lines:
            print(line, end = "")


my_context_manager(full_path)

# with open(file = data_path, mode = 'r', newline='', encoding='utf-8') as file:
#     csv_reader = csv.reader(file)
#
#     for row in csv_reader:
#         print(row)


# console.log(my_message)
if __name__ == "__main__":
    pass
