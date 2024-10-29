import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
file_handler = logging.FileHandler("employee.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class Employee:
    "A sample Employee class"

    def __init__(self, first_name=None, last_name=None):
        self.first_name = first_name
        self.last_name = last_name
        logger.info(f"Created Employee: {self.first_name}-{self.last_name} using class : {self.__class__.__name__}")

    def __str__(self):
        return f"Created Employee: {self.first_name}-{self.last_name} using class : {self.__class__.__name__}"

    @property
    def email(self):
        return f"{self.first_name}_{self.last_name}@email.com"


if __name__ == "__main__":
    emp = Employee()
    logging.INFO("We have created an employee form the module itself. ")
