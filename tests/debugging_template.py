import logging
import os

# import pdb
# import sys
from pathlib import Path

# import debugpy
# import ipdb
from rich.console import Console

logging.basicConfig(level=logging.INFO)

console = Console()


def testing():
    """
    The functionality being tested solely demonstrates the implementation
    of debugging alongside logging. It should be utilized only for basic
    testing purposes and must not be implemented in production environments
    due to its limited capabilities.

    """

    # pdb.set_trace()  # Set a breakpoint here

    console.log(os.path.abspath(__file__))

    data_path = "/Users/gmbp/Desktop/devCode/pythonHub/pythonCheatSheet/src/data/famous_women_in_science.csv"
    full_path = os.path.join(os.getcwd(), "src/data/famous_women_in_science.csv")

    list_directories = [data_path, full_path]
    for p in list_directories:
        console.log(p)

    # Assume you're in the project root, this will always point to the correct path
    full_path = Path("src/data/famous_women_in_science.csv").resolve()

    # You can then use full_path directly
    print(full_path)

    def my_context_manager(data_path: str) -> None:
        try:
            with open(file=data_path, mode="r", newline="", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    # ipdb.set_trace()
                    logging.info(line.strip())
        except Exception as e:
            logging.info(f"[ MY INFO ]: {e}")

    for i in range(10):
        console.log(f"[INFO] value of i -> {i}")

    my_context_manager(full_path)


# with open(file = data_path, mode = 'r', newline='', encoding='utf-8') as file:
#     csv_reader = csv.reader(file)
#
#     for row in csv_reader:
#         print(row)

# console.log(my_message)

if __name__ == "__main__":
    pass
