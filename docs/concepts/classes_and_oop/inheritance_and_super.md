# INHERITANCE and SUPER in Python

To fully understand inheritance and the use of `super()` in Python, let’s break
down the concept with a detailed example, covering **inheritance** across
classes, the role of `super()`, and how the variables are handled when you
create an object from a child class.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [INHERITANCE and SUPER in Python](#inheritance-and-super-in-python)
    - [Concept](#concept)
        - [Inheritance and `super()` explained:](#inheritance-and-super-explained)
        - [Code Example](#code-example)
- [Parent class](#parent-class)
- [Child class inheriting from Animal](#child-class-inheriting-from-animal)
- [Another child class inheriting from Animal](#another-child-class-inheriting-from-animal)
- [Creating objects from the child classes](#creating-objects-from-the-child-classes)
- [Calling methods on the objects](#calling-methods-on-the-objects)
    - [-](#-)
        - [1. **Creating the Parent Class (Animal)**](#1-creating-the-parent-class-animal)
        - [2. **Creating a Child Class (Dog)**](#2-creating-a-child-class-dog)
        - [3. **Creating Another Child Class (Cat)**](#3-creating-another-child-class-cat)
        - [Output of the Program:](#output-of-the-program)
        - [What Happens When You Create a Dog or Cat Object?](#what-happens-when-you-create-a-dog-or-cat-object)
        - [Accessing Variables from Parent and Child Classes:](#accessing-variables-from-parent-and-child-classes)
        - [Key Points to Understand:](#key-points-to-understand)
        - [**Rules of Inheritance, Variables, and `super()`**](#rules-of-inheritance-variables-and-super)
        - [Summary](#summary)
        - [**What `super()` Represents in Python?**](#what-super-represents-in-python)
        - [**Basic Concept: What Does `super()` Replace?**](#basic-concept-what-does-super-replace)
        - [**Example: Usage of `super()` vs Manual Parent Class Call**](#example-usage-of-super-vs-manual-parent-class-call)
        - [**Explanation of the Example:**](#explanation-of-the-example)
        - [**Output of the Example:**](#output-of-the-example)
        - [**Key Differences between `super()` and Manual Parent Calls:**](#key-differences-between-super-and-manual-parent-calls)
        - [**What Happens Internally with `super()`?**](#what-happens-internally-with-super)
        - [**Summary**](#summary)

<!-- markdown-toc end -->


---

## Concept

### Inheritance and `super()` explained:

1. **Parent class (Base class)**: The class that provides attributes and methods
   to other classes.
2. **Child class (Subclass)**: The class that inherits from the parent class and
   can add or override attributes and methods.
3. **`super()`**: It allows a child class to call methods or access variables
   from the parent class.

Let’s walk through the code example in a step-by-step manner.

---

### Code Example

```python
# Parent class
class Animal:
    def __init__(self, name, age):
        self.name = name  # Instance variable
        self.age = age    # Instance variable
        print(f"Animal {self.name} is created, age: {self.age}")

    def sound(self):
        print("Animals make different sounds.")

# Child class inheriting from Animal
class Dog(Animal):
    def __init__(self, name, age, breed):
        # Use super() to call the parent class's __init__
        super().__init__(name, age)  # Initialize inherited variables (name, age)
        self.breed = breed  # New variable specific to Dog class
        print(f"Dog {self.name} is a {self.breed}.")

    # Overriding the sound() method from the parent class
    def sound(self):
        super().sound()  # Optionally call the parent method
        print(f"{self.name} barks!")

# Another child class inheriting from Animal
class Cat(Animal):
    def __init__(self, name, age, fur_color):
        # Using super() to initialize the inherited attributes
        super().__init__(name, age)
        self.fur_color = fur_color  # New variable specific to Cat class
        print(f"Cat {self.name} has {self.fur_color} fur.")

    # Overriding the sound() method
    def sound(self):
        print(f"{self.name} meows!")

# Creating objects from the child classes
print("Creating a dog object...")
dog = Dog("Buddy", 5, "Golden Retriever")

print("\nCreating a cat object...")
cat = Cat("Whiskers", 3, "white")

# Calling methods on the objects
print("\nDog sounds:")
dog.sound()

print("\nCat sounds:")
cat.sound()

# Accessing variables
print(f"\nThe dog's name is {dog.name} and breed is {dog.breed}.")
print(f"The cat's name is {cat.name} with {cat.fur_color} fur.")
```

---

### Explanation of the Example:

#### 1. **Creating the Parent Class (Animal)**

- The `Animal` class has two instance variables: `name` and `age`.
- The `__init__()` method initializes these variables, and it prints when an animal is created.
- It also has a method called `sound()` which prints a generic message.

#### 2. **Creating a Child Class (Dog)**

- The `Dog` class **inherits from the `Animal` class**.
- It has an extra instance variable called `breed`.
- In the `__init__()` method of `Dog`, we use `super().__init__(name, age)` to call the `Animal` class's `__init__()` and **initialize the inherited variables** (`name` and `age`).
- It overrides the `sound()` method but still calls the parent class’s `sound()` method using `super().sound()`.

#### 3. **Creating Another Child Class (Cat)**

- Similarly, the `Cat` class inherits from `Animal` and adds a `fur_color` variable.
- It overrides the `sound()` method to print a cat-specific sound.

---

### Output of the Program:

```sh
Creating a dog object...
Animal Buddy is created, age: 5
Dog Buddy is a Golden Retriever.

Creating a cat object...
Animal Whiskers is created, age: 3
Cat Whiskers has white fur.

Dog sounds:
Animals make different sounds.
Buddy barks!

Cat sounds:
Whiskers meows!

The dog's name is Buddy and breed is Golden Retriever.
The cat's name is Whiskers with white fur.
```

---

### What Happens When You Create a Dog or Cat Object?

1. **Dog object (`dog = Dog(...)`)**:

   - When the `Dog` object is created, Python:
     - Calls the `Dog` class's `__init__()`.
     - Inside the `Dog`'s `__init__()`, the `super()` function calls the `Animal` class’s `__init__()` to initialize the inherited attributes `name` and `age`.
     - Then, the `breed` attribute is initialized, and a message is printed.

2. **Cat object (`cat = Cat(...)`)**:
   - The same process occurs for the `Cat` class.
   - Python initializes the parent attributes and the child-specific attribute (`fur_color`).

---

### Accessing Variables from Parent and Child Classes:

- When you access `dog.name` or `cat.name`, you are accessing variables defined in the **parent class**.
- When you access `dog.breed` or `cat.fur_color`, you are accessing **child-specific variables**.

---

### Key Points to Understand:

1. **Inheritance allows code reuse**: You only define common variables and
   methods once in the parent class.
2. **`super()` initializes inherited variables**: Without calling
   `super().__init__()`, the `name` and `age` wouldn’t be initialized for `Dog`
   and `Cat`.
3. **Overriding methods**: A child class can override a parent class's method to
   provide more specific behavior.
4. **Creating objects from child classes**: When you create a child class object
   (e.g., `dog = Dog(...)`), both the child and parent class constructors are
   called.

---

This example covers **everything you need to understand about inheritance** and
`super()` usage, along with what happens when creating objects from child
classes. Let me know if anything is unclear or if you have further questions!

Below is a detailed breakdown of the rules regarding inheritance, `super()`, and
variable handling between parent and child classes, formatted into a table for
clarity.

---

### **Rules of Inheritance, Variables, and `super()`**

| **Rule**                                                                   | **Explanation**                                                                                                                                                                                       | **Example / Behavior**                                                                                                                                    |
| -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Child Class Inherits Variables from Parent**                          | All variables (attributes) defined in the parent class are accessible in the child class, either directly or via `super()`.                                                                           | If the parent class defines `name` and `age`, the child class can access them directly or by calling `super().__init__()`.                                |
| **2. Variables with Same Name in Parent and Child (Overriding Variables)** | If a child class defines a variable with the **same name** as the parent class, the child’s version will **override** the parent’s version.                                                           | `class Parent: self.name = "Parent Name"` <br> `class Child(Parent): self.name = "Child Name"` <br> **Accessing `child.name` will print `"Child Name"`**. |
| **3. `super()` to Call Parent’s Constructor**                              | The child class uses `super()` to call the parent class’s `__init__()` method to initialize variables defined in the parent. Without calling `super()`, the inherited variables won’t be initialized. | `class Parent: def __init__(self): self.age = 10` <br> **Child must use `super().__init__()` to initialize `age`.**                                       |
| **4. New Variables in Child Class**                                        | The child class can introduce new variables that the parent class doesn’t have. These variables are specific to the child class.                                                                      | A `Dog` class adds a `breed` variable that doesn’t exist in the `Animal` class.                                                                           |
| **5. Accessing Parent’s Methods via `super()`**                            | A child class can use `super()` to call a method from the parent class, even if it overrides that method.                                                                                             | `def sound(self): super().sound()` <br> Calls the parent’s `sound()` method before adding child-specific behavior.                                        |
| **6. Child Class Must Explicitly Call Parent’s Constructor if Needed**     | Python **does not automatically call the parent’s constructor (`__init__()`)**. If the child class has its own `__init__()`, the parent constructor must be called explicitly using `super()`.        | Without `super().__init__()`, inherited variables will not be initialized.                                                                                |
| **7. Child Class Can Override Parent Methods**                             | A child class can override a parent class’s method with its own implementation, completely replacing the parent’s version.                                                                            | `def sound(self): print("Dog barks!")` <br> This replaces the parent class’s `sound()` method.                                                            |
| **8. Accessing Parent Variables from Child Class**                         | Variables initialized by the parent class can be accessed in the child class unless explicitly overridden.                                                                                            | If `name` is initialized by the parent, you can access it with `self.name` in the child.                                                                  |
| **9. Order of Constructor Execution**                                      | If `super()` is called, the **parent constructor** (`__init__()`) executes first, followed by the child class’s constructor code.                                                                     | Parent variables are initialized first, ensuring all inherited attributes are set before adding new ones.                                                 |
| **10. Private Variables (Name Mangling)**                                  | Variables prefixed with `__` (double underscore) in the parent class are **not directly accessible** in the child class. Python uses name mangling to prevent direct access.                          | `class Parent: __secret = 42` <br> The child class cannot access `__secret` directly; it becomes `_Parent__secret`.                                       |
| **11. Using `super()` with Multiple Inheritance**                          | In multiple inheritance, `super()` ensures the **next class in the method resolution order (MRO)** is called, preventing repeated constructor calls.                                                  | If `class C(A, B):`, `super().__init__()` will follow the MRO and call `A` and `B` constructors correctly.                                                |
| **12. `super()` Works with Non-`__init__` Methods**                        | `super()` can be used not only with constructors (`__init__`) but also with other methods in the parent class.                                                                                        | `def sound(self): super().sound()` <br> This works with any method, not just `__init__`.                                                                  |

---

### Summary

- **Variables in Parent and Child**: If the same variable exists in both parent
  and child, the **child’s version overrides** the parent’s.
- **New Variables**: The child class can introduce its own variables that do not
  exist in the parent.
- **Using `super()`**: It ensures that parent class methods, especially the
  constructor, are properly called to initialize inherited attributes.
- **Private Variables**: Variables with `__` in the parent class cannot be
  accessed directly by the child.

This table should provide a clear and comprehensive guide on inheritance,
variable handling, and the role of `super()`! Let me know if you have any
follow-up questions or need further clarification.

### **What `super()` Represents in Python?**

In Python, **`super()`** is a built-in function that provides access to
**methods or variables from the parent class** (or superclass). It helps ensure
that the **parent class’s methods or constructor** are correctly called,
especially in cases of method overriding and multiple inheritance.

If you **don’t use `super()`**, you would need to **manually call the parent
class** methods by referring to the class name directly. However, `super()` is
cleaner and avoids potential errors, especially in **multiple inheritance
scenarios**.

---

### **Basic Concept: What Does `super()` Replace?**

If you **don’t use `super()`**, the child class would need to call methods like this:

```python
ParentClassName.method(self, ...)
```

With **`super()`**, you don’t need to know the parent class name or hard-code
it—this helps when your code needs to evolve (e.g., if class names change or in
multiple inheritance).

---

### **Example: Usage of `super()` vs Manual Parent Class Call**

```python
# Parent Class
class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        print(f"Vehicle {self.brand} {self.model} is created.")

    def start(self):
        print(f"{self.brand} {self.model} is starting.")

# Child Class without using super()
class Car(Vehicle):
    def __init__(self, brand, model, doors):
        # Manually calling the parent constructor
        Vehicle.__init__(self, brand, model)  # Without super()
        self.doors = doors
        print(f"This car has {self.doors} doors.")

    def start(self):
        # Manually calling the parent method
        Vehicle.start(self)  # Without super()
        print(f"{self.brand} {self.model} is now in car mode.")

# Child Class using super()
class Bike(Vehicle):
    def __init__(self, brand, model, type_of_bike):
        # Using super() to call the parent constructor
        super().__init__(brand, model)
        self.type_of_bike = type_of_bike
        print(f"This is a {self.type_of_bike} bike.")

    def start(self):
        # Using super() to call the parent method
        super().start()
        print(f"{self.brand} {self.model} is ready to ride!")
```

---

### **Explanation of the Example:**

1. **Manual Parent Class Call (Without `super()`):**

   - In the `Car` class, we manually call the parent class’s `__init__()` and
     `start()` methods.
   - This approach works but has some downsides:
     - If the parent class name changes, the code needs to be updated.
     - It’s not optimal when dealing with multiple inheritance (where you need
       to carefully control the method resolution order).

2. **Using `super()` in the `Bike` Class:**
   - The `super().__init__()` call in the `Bike` class initializes the inherited
     variables from the `Vehicle` class without needing to mention the class
     name.
   - The `super().start()` method call ensures that the `start()` method from
     the parent class is invoked before adding bike-specific behavior.

---

### **Output of the Example:**

```plaintext
Vehicle Toyota Corolla is created.
This car has 4 doors.
Toyota Corolla is starting.
Toyota Corolla is now in car mode.

Vehicle Yamaha R15 is created.
This is a sport bike.
Yamaha R15 is starting.
Yamaha R15 is ready to ride!
```

---

### **Key Differences between `super()` and Manual Parent Calls:**

| **Aspect**                | **Using `super()`**                                 | **Without `super()`**                              |
| ------------------------- | --------------------------------------------------- | -------------------------------------------------- |
| **Code Simplicity**       | Cleaner and more maintainable                       | Harder to maintain if parent changes               |
| **Multiple Inheritance**  | Handles method resolution order (MRO) automatically | Needs manual control over MRO                      |
| **Class Name Dependency** | Independent of the parent class name                | Requires hard-coding parent class name             |
| **Error Prone**           | Less error-prone                                    | More likely to cause errors in complex hierarchies |

---

### **What Happens Internally with `super()`?**

In a simple inheritance like the one above:

- `super()` refers to the **immediate parent class** based on the **method
  resolution order (MRO)**.
- In **multiple inheritance**, `super()` ensures that the **next class in the
  MRO** gets called, avoiding duplicate calls to the same class's methods.

---

### **Summary**

- **`super()`** is a cleaner, safer way to call parent class methods or
  constructors.
- It avoids **hard-coding class names**, reduces errors in complex hierarchies,
  and handles **method resolution order (MRO)** automatically.
- **Without `super()`**, you’d need to call parent methods directly using the
  parent class name, which can be error-prone and less maintainable.

This example and explanation should give you a complete understanding of what
`super()` does, how it’s used, and what it replaces! Let me know if anything is
unclear or if you need more examples.


