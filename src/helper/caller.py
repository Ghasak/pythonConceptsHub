__all__ = ["Employee"]

import random
from dataclasses import dataclass, field

from rich.console import Console

console = Console()


# @dataclass(order=True, repr=False)
@dataclass(order=True, repr=False)
class Employee:
    # instances attributes
    first_name: str = field(init=True, repr=True)
    last_name: str = field(init=True, repr=True)
    age: int = field(init=True, repr=True)
    salary: float = field(init=True, repr=True)
    gender: str = field(init=True, repr=True)  # Added the missing gender field
    emp_id: int = field(init=False, repr=True)

    # class attributes
    CONFIG = {"num_of_emp": 0}

    def __post_init__(self):
        # Correct the method name and increment the number of employees
        Employee.CONFIG["num_of_emp"] += 1
        self.emp_id = Employee.CONFIG["num_of_emp"]

    def __str__(self):
        # Use rich string formatting for better readability
        return f"[ INFO ] Employee: {self.first_name} {self.last_name}, Gender: {self.gender:<6}, Age: {self.age}, Salary: {self.salary:3.2f} "

    @classmethod
    def generate(cls):
        for _ in range(10):
            emp = Employee(
                first_name="Jack",
                last_name="Michael",
                age=random.randint(20, 55),
                salary=random.uniform(2000, 15000),
                gender=random.choice(["male", "female"]),
            )
            console.log(str(emp))
        console.log(f"Total number of employees generated: {cls.CONFIG['num_of_emp']}")


if __name__ == "__main__":
    Employee.generate()
