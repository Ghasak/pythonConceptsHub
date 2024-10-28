# SUPER METHOD EXPLAINED

## Question

Help me to understand more about the super should I pass all variables similar to the parent variables?
or I can skip them? if I skip them how I can provide them to the dog
Class If I don't know them in the parent class which is Animal

```py
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

```

explain this to me and correct my understanding.

## Starting from a question

The code you provided demonstrates the use of inheritance in Python,
specifically how the `super()` function works to pass variables from a subclass
(`Dog`) to its parent class (`Animal`). Let me walk you through it step-by-step:

### Key Points About the Code:

1. **Inheritance:**

   - The `Dog` class inherits from the `Animal` class, meaning it will have access to the attributes and methods of `Animal`.

2. **`super()` usage:**

   - `super().__init__(...)` calls the parent class (`Animal`)'s `__init__` method from within the `Dog` class’s constructor. This ensures that the attributes of `Animal` (`breed` and `sex`) are properly initialized when creating a `Dog` object.

3. **Argument Passing:**
   - In the `Dog` class’s `__init__` method, you pass the `breed` and `sex` arguments to the parent `Animal` class using `super().__init__(breed, sex)`.
   - **Yes**, you must pass the appropriate arguments to the parent class if they are needed there. This is to ensure the `Animal` class's attributes are properly set.

---

### Detailed Walkthrough:

1. **The `Animal` Class:**

   ```python
   class Animal:
       def __init__(self, breed: str = None, sex: bool = 0):
           self.breed = breed
           self.sex = sex
           console.log(f"the  Animal object is created using : {self.breed} with gender: {self.sex}")
   ```

   - `Animal` is the parent class.
   - It has two attributes: `breed` and `sex`.
   - The constructor (`__init__`) sets the values of these attributes when the object is created.
   - You're trying to log details using `console.log()`, but this is **JavaScript syntax** and will throw an error in Python. You should use Python’s logging or `print()` instead.

2. **The `Dog` Class:**

   ```python
   class Dog(Animal):
       def __init__(self, dog_name: str = None, dog_age: int = 0, breed: str = None, sex: bool = 0):
           self.dog_name = dog_name
           self.dog_age = dog_age
           super().__init__(breed, sex)
   ```

   - `Dog` is the subclass, inheriting from `Animal`.
   - The `Dog` class introduces two new attributes: `dog_name` and `dog_age`.
   - In the `Dog` class's `__init__`, you initialize these attributes and use `super()` to call the parent class's `__init__` method to initialize the `breed` and `sex` attributes from `Animal`.

3. **Main Code Block:**

   ```python
   if __name__ == "__main__":
       my_dog = Dog("Jack", 12, "Bouldog", 1)
       logger.info(my_dog)
   ```

   - Here, a `Dog` object is created with the name `"Jack"`, age `12`, breed `"Bouldog"`, and sex `1` (likely indicating male).
   - Then, you try to log the `Dog` object using `logger.info()`. This will call the `__str__()` method defined in the `Animal` class (since `Dog` inherits it), and display a string representation of the object.

---

### Explanation of `super()` and Variable Passing:

1. **Why Use `super()`?**

   - When a subclass (like `Dog`) extends a parent class (like `Animal`), the parent class still needs to initialize its own attributes. `super()` allows you to reuse the parent class’s constructor without repeating the same code.

2. **Do You Need to Pass All Parent Variables to `super()`?**

   - Yes, if the parent class requires certain variables to initialize its attributes (like `breed` and `sex` here), you need to pass those when calling `super()`.
   - If you don't know the values of these attributes upfront, you can pass default or placeholder values, or gather them from user input later.

3. **Skipping Variables?**
   - You cannot skip required variables in the parent class's `__init__`. If `Animal`'s `__init__` expects `breed` and `sex`, you must provide them when calling `super()`. Otherwise, Python will raise a `TypeError`.

---

### Fixed Code with Improvements:

```python
class Animal:
    def __init__(self, breed: str = None, sex: bool = 0):
        self.breed = breed
        self.sex = sex
        print(f"The Animal object is created using: {self.breed} with gender: {self.sex}")

    def __str__(self):
        return f"This is an Object created using {self.__class__.__name__}, with: {self.breed} with gender: {self.sex}"


class Dog(Animal):
    def __init__(self, dog_name: str = None, dog_age: int = 0, breed: str = None, sex: bool = 0):
        self.dog_name = dog_name
        self.dog_age = dog_age
        super().__init__(breed, sex)


if __name__ == "__main__":
    my_dog = Dog("Jack", 12, "Bulldog", 1)
    print(my_dog)
```

---

### Output:

```sh
The Animal object is created using: Bulldog with gender: 1
This is an Object created using Dog, with: Bulldog with gender: 1
```

---

### Summary:

- Use `super()` to call the parent class's constructor.
- Pass all required variables from the subclass to the parent class via `super()`.
- If a parent class needs specific arguments, they must be passed from the subclass. Alternatively, you can provide default values or input from other sources.
