from src.logging.L04_json_formatter_class import logger


def SuperMethodConcept():

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

    class Animal:

        def __init__(self, breed: str = None, sex: bool = 0):
            self.breed = breed
            self.sex = sex
            logger.info(f"the  Animal object is created using : {self.breed} with gender: {self.sex}")

        def __str__(self):
            return f"This is an Object created using {self.__class__.__name__}, with: {self.breed} with gender: {self.sex}"

    class Dog(Animal):

        def __init__(self, dog_name: str = None, dog_age: int = 0, breed: str = None, sex: bool = 0):
            self.dog_name = dog_name
            self.dog_age = dog_age
            super().__init__(breed, sex)

    return Employee, Animal, Dog


def testing_super_method_concept():
    _, _, Dog = SuperMethodConcept()
    my_dog = Dog("Jack", 12, "Bouldog", 1)
    logger.info(my_dog)


if __name__ == "__main__":
    pass
