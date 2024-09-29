# Data Classes in Action

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Data Classes in Action](#data-classes-in-action)
    - [Introduction](#introduction)
        - [Table 1: Attributes for the `@dataclass` Decorator](#table-1-attributes-for-the-dataclass-decorator)
        - [Table 2: Keywords and Options in the `field()` Function](#table-2-keywords-and-options-in-the-field-function)
        - [Dataclass Template with All Features](#dataclass-template-with-all-features)
        - [What Are Python Dataclasses?](#what-are-python-dataclasses)
        - [Why Do We Need Dataclasses?](#why-do-we-need-dataclasses)
        - [How to Use Dataclasses?](#how-to-use-dataclasses)
        - [Syntax of a Modern Python Dataclass](#syntax-of-a-modern-python-dataclass)
        - [Explanation of Key Features](#explanation-of-key-features)
        - [Dataclass Example vs. Regular Class Example](#dataclass-example-vs-regular-class-example)
            - [Regular Class Example](#regular-class-example)
            - [Dataclass Example](#dataclass-example)
        - [Summary Table](#summary-table)
        - [Why Do We Need `default_factory`?](#why-do-we-need-default_factory)
        - [When to Use `default_factory`?](#when-to-use-default_factory)
        - [How to Use `default_factory`?](#how-to-use-default_factory)
        - [Examples of `default_factory` Usage](#examples-of-default_factory-usage)
            - [1. **Using `default_factory` for Mutable Data Containers (List)**](#1-using-default_factory-for-mutable-data-containers-list)
            - [2. **Using `default_factory` with a Function**](#2-using-default_factory-with-a-function)
            - [3. **Using `default_factory` for Complex Nested Structures**](#3-using-default_factory-for-complex-nested-structures)
            - [4. **Using `default_factory` for Lazy Initialization**](#4-using-default_factory-for-lazy-initialization)
        - [Summary Table for `default_factory`](#summary-table-for-default_factory)
        - [Why Do We Need `__post_init__()`?](#why-do-we-need-__post_init__)
        - [When to Use `__post_init__()`?](#when-to-use-__post_init__)
        - [How to Use `__post_init__()`?](#how-to-use-__post_init__)
        - [Examples of `__post_init__()` Usage](#examples-of-__post_init__-usage)
            - [1. **Basic Usage of `__post_init__()`**](#1-basic-usage-of-__post_init__)
            - [2. **Using `InitVar` with `__post_init__()`**](#2-using-initvar-with-__post_init__)
            - [3. **Handling Field Validation in `__post_init__()`**](#3-handling-field-validation-in-__post_init__)
            - [4. **Using `__post_init__()` for Dependent Initialization**](#4-using-__post_init__-for-dependent-initialization)
        - [Summary Table for `__post_init__()`](#summary-table-for-__post_init__)
        - [1. `init`: Add `__init__()` Method?](#1-init-add-__init__-method)
            - [What It Is:](#what-it-is)
            - [Why We Need It:](#why-we-need-it)
            - [Example:](#example)
        - [2. `repr`: Add `__repr__()` Method?](#2-repr-add-__repr__-method)
            - [What It Is:](#what-it-is-1)
            - [Why We Need It:](#why-we-need-it-1)
            - [Example:](#example-1)
        - [3. `eq`: Add `__eq__()` Method?](#3-eq-add-__eq__-method)
            - [What It Is:](#what-it-is-2)
            - [Why We Need It:](#why-we-need-it-2)
            - [Example:](#example-2)
        - [4. `order`: Add Ordering Methods?](#4-order-add-ordering-methods)
            - [What It Is:](#what-it-is-3)
            - [Why We Need It:](#why-we-need-it-3)
            - [Example:](#example-3)
        - [5. `unsafe_hash`: Force the Addition of a `__hash__()` Method?](#5-unsafe_hash-force-the-addition-of-a-__hash__-method)
            - [What It Is:](#what-it-is-4)
            - [Why We Need It:](#why-we-need-it-4)
            - [Example:](#example-4)
        - [6. `frozen`: Make the Instance Immutable?](#6-frozen-make-the-instance-immutable)
            - [What It Is:](#what-it-is-5)
            - [Why We Need It:](#why-we-need-it-5)
            - [Example:](#example-5)
        - [Summary Table for `@dataclass()` Parameters](#summary-table-for-dataclass-parameters)
        - [Workaround to Make Some Fields Immutable](#workaround-to-make-some-fields-immutable)
        - [Example of Partially Immutable Dataclass](#example-of-partially-immutable-dataclass)
        - [Another Approach: Customizing `__setattr__()`](#another-approach-customizing-__setattr__)
        - [Summary](#summary)
        - [Why You Can't Combine `frozen=True` and `property`/`__setattr__()`:](#why-you-cant-combine-frozentrue-and-property__setattr__)
        - [Alternative Approach](#alternative-approach)
        - [Example:](#example-6)
        - [Conclusion:](#conclusion)
        - [Explanation and Examples of Using `slots` in Dataclasses](#explanation-and-examples-of-using-slots-in-dataclasses)
            - [What are slots?](#what-are-slots)
            - [Using `slots=True` in Dataclasses](#using-slotstrue-in-dataclasses)
        - [Explanation of Dataclass Field Arguments](#explanation-of-dataclass-field-arguments)
            - [1. `init=True/False`](#1-inittruefalse)
            - [2. `repr=True/False`](#2-reprtruefalse)
            - [3. `default=None`](#3-defaultnone)
            - [4. `default_factory`](#4-default_factory)
        - [Summary Table](#summary-table-1)
        - [Definitions and Differences](#definitions-and-differences)
        - [Example Demonstrating the Differences](#example-demonstrating-the-differences)
        - [Key Differences Highlighted:](#key-differences-highlighted)
        - [Conclusion](#conclusion)
        - [Definitions and Differences](#definitions-and-differences-1)
        - [Example Demonstrating the Differences](#example-demonstrating-the-differences-1)
        - [Key Differences Highlighted:](#key-differences-highlighted-1)
        - [Conclusion](#conclusion-1)
    - [What is InitVar](#what-is-initvar)
        - [Understanding `InitVar`](#understanding-initvar)
        - [How to Use `InitVar`](#how-to-use-initvar)
        - [Example](#example)
        - [Summary of `InitVar`](#summary-of-initvar)
    - [Hash in dataclasses](#hash-in-dataclasses)
        - [Example of Using `hash` in Dataclasses](#example-of-using-hash-in-dataclasses)
        - [Explanation](#explanation)
        - [Example 1: Using `hash=True`](#example-1-using-hashtrue)
        - [Example 2: Using `hash=False`](#example-2-using-hashfalse)
        - [Explanation and Effects:](#explanation-and-effects)
        - [Example Dataclass Definitions and Usage](#example-dataclass-definitions-and-usage)
            - [Dataclass with `hash=True`](#dataclass-with-hashtrue)
            - [Dataclass with `hash=False`](#dataclass-with-hashfalse)
        - [Expected Outputs](#expected-outputs)
        - [Table 1: Attributes for the `@dataclass` Decorator](#table-1-attributes-for-the-dataclass-decorator-1)
        - [Table 2: Keywords and Options in the `field()` Function](#table-2-keywords-and-options-in-the-field-function-1)
        - [Dataclass Template with All Features](#dataclass-template-with-all-features-1)
    - [Template - Boilerplate](#template---boilerplate)
        - [Updated Dataclass with `InitVar`](#updated-dataclass-with-initvar)
        - [Explanation of Changes](#explanation-of-changes)
        - [1. **Dataclass Decorators**](#1-dataclass-decorators)
        - [2. **Field Specifications**](#2-field-specifications)
        - [3. **Automatic and Custom Initialization**](#3-automatic-and-custom-initialization)
        - [4. **Property Decorators**](#4-property-decorators)
        - [5. **Immutability with Mutation Methods**](#5-immutability-with-mutation-methods)
        - [6. **Serialization and Factory Methods**](#6-serialization-and-factory-methods)
        - [7. **Rich Output and String Representation**](#7-rich-output-and-string-representation)
        - [8. **Enhanced Usability**](#8-enhanced-usability)
        - [Summary](#summary-1)
    - [Notes during dev.](#notes-during-dev)

<!-- markdown-toc end -->

## Introduction

A comprehensive overview of key concepts and attributes
associated with Python dataclasses, including those used within the `field()`
function and others that are essential for defining and customizing dataclasses.

- Below are two comprehensive tables detailing the attributes available in the
  Python `@dataclass` decorator and the `field()` function for dataclass fields.
  These tables include descriptions, benefits, and typical use cases to help you
  integrate these features effectively in your development work.

### Table 1: Attributes for the `@dataclass` Decorator

| Attribute     | Description                                                                       | Benefits                                                                                         | Use Cases                                                            |
| ------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| `init`        | Automatically generate an `__init__()` method.                                    | Simplifies initialization of dataclasses.                                                        | When you need an automatic constructor.                              |
| `repr`        | Automatically generate a `__repr__()` method.                                     | Eases debugging by providing a readable string representation.                                   | When you need a simple way to print dataclass objects for debugging. |
| `eq`          | Automatically generate an `__eq__()` method.                                      | Allows object comparison using `==`.                                                             | When you need to compare dataclass instances.                        |
| `order`       | Automatically generate ordering methods (`__lt__`, `__le__`, `__gt__`, `__ge__`). | Enables object ordering and comparisons.                                                         | When objects need to be sortable or compared.                        |
| `unsafe_hash` | Force the generation of a `__hash__()` method even if `__eq__` is defined.        | Enables objects to be used as dictionary keys or set members, even when custom equality is used. | When `eq` is True but you still need a hash method.                  |
| `frozen`      | Make instances immutable after creation.                                          | Prevents modification after initialization, ensuring hash consistency.                           | When object immutability is needed (similar to tuples).              |

### Table 2: Keywords and Options in the `field()` Function

| Field Attribute   | Description                                                                                                      | Benefits                                                                  | When It's Used                                                                  |
| ----------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `default`         | Sets a default value for the field, which is used if no value is provided during instantiation.                  | Provides a convenient way to set a default without using `__post_init__`. | When a field should have a default value.                                       |
| `default_factory` | Accepts a callable that returns the default value for the field; called for each new instance.                   | Ensures unique default values for mutable types like lists or dicts.      | When default needs to be a mutable type like a list or a dictionary.            |
| `init`            | If `True`, include the field as a parameter in the `__init__()` method; if `False`, exclude it.                  | Allows exclusion of fields from the initialization method.                | To exclude fields from the automatic constructor.                               |
| `repr`            | If `True`, include the field in the string returned by the `__repr__()` method; if `False`, exclude it.          | Controls visibility in the object's representation.                       | To customize the object’s official string representation.                       |
| `compare`         | If `True`, include the field in comparisons of the object; if `False`, exclude it.                               | Controls which fields affect object comparison.                           | To include/exclude fields from being used in comparison operations.             |
| `hash`            | If `True`, include the field in the hash value; if `False`, exclude it; if `None`, use the setting of `compare`. | Determines field inclusion in hash calculations.                          | To control which fields contribute to the object's hash value.                  |
| `metadata`        | A mapping that stores arbitrary information about the field. Does not affect the field’s behavior directly.      | Useful for storing extra information about the field.                     | For annotations or additional metadata that does not affect dataclass behavior. |

### Dataclass Template with All Features

This template includes use of various `@dataclass` and `field()` attributes for
a hypothetical `Employee` class, demonstrating a possible configuration you can
start from and adapt based on your specific requirements.

```python
from dataclasses import dataclass, field
from typing import List

def default_id():
    return 1

@dataclass(order=True, frozen=True)
class Employee:
    id: int = field(default_factory=default_id, init=True, repr=True, compare=True, hash=True)
    name: str = field(init=True, repr=True, compare=False, hash=False)
    skills: List[str] = field(default_factory=list, repr=True, compare=False, hash=False)
    age: int = field(default=None, repr=True, compare=True, hash=True, metadata={'unit': 'years'})

# Example usage
if __name__ == "__main__":
    emp1 = Employee(name="Alice")
    emp2 = Employee(id=2, name="Bob", skills=["Python", "Data Analysis"])
    print(emp1)
    print(emp2)
    print(emp1 == emp2)
```

This template effectively utilizes the `dataclass` and `field` features,
providing a robust starting point for defining classes with various custom
behaviors in terms of initialization, representation, comparison, and
immutability. Adjust the attributes and methods as needed for your application.

### What Are Python Dataclasses?

Dataclasses in Python are a way to simplify the process of creating classes that
store data. They automatically generate special methods like `__init__()`,
`__repr__()`, `__eq__()`, and others, based on the class attributes. Introduced
in Python 3.7, dataclasses reduce boilerplate code when you primarily need a
class to manage data.

---

### Why Do We Need Dataclasses?

- **Reduces boilerplate**: No need to manually write the `__init__()`,
  `__repr__()`, `__eq__()` methods.
- **Readability**: Code is cleaner and easier to maintain.
- **Customizability**: Dataclasses are still regular Python classes, so you can
  add additional methods and functionality.

---

### How to Use Dataclasses?

You use the `@dataclass` decorator from the `dataclasses` module to define a
dataclass. The decorator automatically generates special methods based on the
class attributes.

---

### Syntax of a Modern Python Dataclass

Below is the exhaustive syntax for a Python dataclass covering all related concepts:

```python
from dataclasses import dataclass, field, InitVar
from typing import List, Optional

@dataclass(order=True, frozen=False, slots=True)
class Employee:
    # Basic fields with default values
    id: int
    name: str = "Unknown"

    # Optional fields with default factories (lists, dictionaries, etc.)
    skills: List[str] = field(default_factory=list)

    # Init-only variables (not stored as attributes)
    experience: InitVar[int] = 0

    # Private fields with custom metadata
    _salary: float = field(repr=False, compare=False, metadata={"unit": "USD"})

    # Post-init method for further processing after the object is created
    def __post_init__(self, experience: int):
        if experience < 5:
            self._salary = 50000
        else:
            self._salary = 70000

    # Example method
    def give_raise(self, amount: float):
        self._salary += amount

# Usage
emp = Employee(id=1, name="Alice", experience=3)
print(emp)  # Output: Employee(id=1, name='Alice', skills=[])
print(emp._salary)  # Output: 50000

emp.give_raise(5000)
print(emp._salary)  # Output: 55000
```

---

### Explanation of Key Features

| **Feature**       | **Meaning**                                                                                                                                      | **Usage**                                                                                                          |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| `@dataclass`      | The decorator that makes the class a dataclass, auto-generating methods like `__init__()`.                                                       | `@dataclass` above the class definition.                                                                           |
| `order=True`      | Generates comparison methods (`<`, `<=`, `>`, `>=`) for the class.                                                                               | `@dataclass(order=True)` to enable ordering.                                                                       |
| `frozen=False`    | Makes the instance immutable (if set to `True`).                                                                                                 | `@dataclass(frozen=True)` to make the class immutable.                                                             |
| `slots=True`      | Optimizes memory usage by not storing attributes in the usual `__dict__` but in a static structure (Python 3.10+).                               | `@dataclass(slots=True)` for memory efficiency.                                                                    |
| `field()`         | Fine-tunes the behavior of individual fields (e.g., default values, whether to include in `repr`, comparison, etc.).                             | `field(default=..., repr=False, compare=False)` to customize field behavior.                                       |
| `InitVar`         | Defines init-only variables, used during initialization but not stored as instance attributes.                                                   | `experience: InitVar[int] = 0` — this variable is only available in the constructor and is not an attribute.       |
| `__post_init__()` | A special method that runs after the `__init__` method. It’s useful when you want to process fields after initialization or work with `InitVar`. | Custom logic such as setting `_salary` based on experience inside `__post_init__`.                                 |
| `default_factory` | Used to set default values for mutable types like lists or dictionaries.                                                                         | `skills: List[str] = field(default_factory=list)` to initialize a list.                                            |
| `metadata`        | Allows storing additional metadata for a field, useful for validation or documentation.                                                          | `_salary: float = field(metadata={"unit": "USD"})` — metadata is just extra information associated with the field. |

---

### Dataclass Example vs. Regular Class Example

#### Regular Class Example

```python
class Employee:
    def __init__(self, id, name="Unknown", skills=None, experience=0):
        self.id = id
        self.name = name
        self.skills = skills if skills is not None else []
        self.experience = experience
        self._salary = 50000 if experience < 5 else 70000

    def give_raise(self, amount):
        self._salary += amount

    def __repr__(self):
        return f"Employee(id={self.id}, name={self.name}, skills={self.skills})"

# Usage
emp = Employee(id=1, name="Alice", experience=3)
print(emp)  # Output: Employee(id=1, name='Alice', skills=[])
print(emp._salary)  # Output: 50000

emp.give_raise(5000)
print(emp._salary)  # Output: 55000
```

#### Dataclass Example

```python
from dataclasses import dataclass, field

@dataclass
class Employee:
    id: int
    name: str = "Unknown"
    skills: list = field(default_factory=list)
    experience: int = 0
    _salary: float = field(init=False, repr=False)

    def __post_init__(self):
        self._salary = 50000 if self.experience < 5 else 70000

    def give_raise(self, amount: float):
        self._salary += amount

# Usage
emp = Employee(id=1, name="Alice", experience=3)
print(emp)  # Output: Employee(id=1, name='Alice', skills=[])
print(emp._salary)  # Output: 50000

emp.give_raise(5000)
print(emp._salary)  # Output: 55000
```

---

### Summary Table

| **Concept**               | **Description**                                                                            | **Example**                                                                      |
| ------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| **What are Dataclasses?** | Simplified way to create classes focused on storing data, reducing boilerplate.            | `@dataclass` decorator on a class.                                               |
| **Why Dataclasses?**      | To automatically generate methods like `__init__()`, `__repr__()`, and `__eq__()`.         | Less manual code needed.                                                         |
| **Usage**                 | Add `@dataclass` decorator and define class attributes like regular class fields.          | `@dataclass` and define fields like `id: int`, `name: str`.                      |
| **Field**                 | Customizes individual fields with defaults, whether they should be compared, etc.          | `field(default_factory=list, repr=False)` for a list field.                      |
| \***\*post_init\*\***     | Allows post-initialization processing, useful for logic that depends on other fields.      | Initialize `_salary` after setting `experience` in the constructor.              |
| **InitVar**               | Init-only variables that aren't stored as attributes, available only in `__post_init__()`. | `experience: InitVar[int] = 0` can be passed but isn’t stored.                   |
| **Slots**                 | Optimizes memory usage by reducing overhead from `__dict__`.                               | `@dataclass(slots=True)` to use memory-efficient attribute storage.              |
| **Order**                 | Generates ordering methods (`<`, `>`, `<=`, `>=`).                                         | `@dataclass(order=True)` allows comparisons between instances.                   |
| **Frozen**                | Makes the class immutable (frozen instances cannot be modified).                           | `@dataclass(frozen=True)` prevents any modification of instance attributes.      |
| **Default Factories**     | Assign default values for mutable types such as lists or dictionaries.                     | `field(default_factory=list)` initializes an empty list if no value is provided. |

This summary should give you a comprehensive understanding of Python's dataclasses and how to use them effectively!

### Why Do We Need `default_factory`?

In Python, mutable default arguments (like lists, dictionaries, sets, etc.) can
lead to unexpected behavior. If a mutable default argument is shared across
instances of a class, modifying it in one instance can affect other instances.

To avoid this issue, `default_factory` in Python dataclasses is used to create
default values for fields that need mutable data types or for dynamically
computed values. It ensures each instance gets a fresh, independent object
rather than sharing one.

---

### When to Use `default_factory`?

- **Mutable default values**: For fields that need mutable types (lists,
  dictionaries), using a factory function ensures that each instance has its own
  independent copy.
- **Dynamic defaults**: When the default value of a field depends on some logic,
  and you want that logic to run when the class is instantiated (instead of at
  the time of definition).
- **Lazy initialization**: When an object or value should only be created at
  runtime.

---

### How to Use `default_factory`?

You use the `field()` function with the `default_factory` argument, passing a
callable (usually a function or class) that generates the default value. Here
are some examples:

---

### Examples of `default_factory` Usage

#### 1. **Using `default_factory` for Mutable Data Containers (List)**

```python
from dataclasses import dataclass, field

@dataclass
class Team:
    members: list = field(default_factory=list)

# Each Team instance gets a new empty list for members
team1 = Team()
team2 = Team()

team1.members.append("Alice")
print(team1.members)  # Output: ['Alice']
print(team2.members)  # Output: [] (Not affected by team1)
```

In this example, without `default_factory`, using a default argument like
`members: list = []` would result in both `team1` and `team2` sharing the same
list.

---

#### 2. **Using `default_factory` with a Function**

```python
from dataclasses import dataclass, field
import random

def generate_id():
    return random.randint(1000, 9999)

@dataclass
class Employee:
    id: int = field(default_factory=generate_id)
    name: str = "Unknown"

# Each Employee gets a random ID at instantiation
emp1 = Employee(name="Alice")
emp2 = Employee(name="Bob")

print(emp1.id)  # Output: Random ID, e.g., 1203
print(emp2.id)  # Output: Different random ID, e.g., 4537
```

Here, `generate_id()` is a function that provides a dynamic default value, ensuring each employee gets a unique ID.

---

#### 3. **Using `default_factory` for Complex Nested Structures**

```python
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Inventory:
    stock: Dict[str, int] = field(default_factory=lambda: {'apple': 0, 'banana': 0})

# Each Inventory instance gets its own dictionary
inv1 = Inventory()
inv2 = Inventory()

inv1.stock['apple'] += 10
print(inv1.stock)  # Output: {'apple': 10, 'banana': 0}
print(inv2.stock)  # Output: {'apple': 0, 'banana': 0} (Not affected by inv1)
```

This example shows how `default_factory` can be used to initialize nested data structures, like a dictionary.

---

#### 4. **Using `default_factory` for Lazy Initialization**

Sometimes, you might want a field to be initialized only when the class is instantiated, which is especially useful for expensive computations.

```python
@dataclass
class DatabaseConnection:
    conn: str = field(default_factory=lambda: "Connected to DB")

@dataclass
class Application:
    db_connection: DatabaseConnection = field(default_factory=DatabaseConnection)

app = Application()
print(app.db_connection.conn)  # Output: Connected to DB
```

In this example, the `DatabaseConnection` object is only created when the `Application` class is instantiated.

---

### Summary Table for `default_factory`

| **Use Case**                | **Description**                                                                               | **Example**                                                                                          |
| --------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Mutable Defaults**        | Use `default_factory` to avoid shared mutable default arguments.                              | `field(default_factory=list)` for a list.                                                            |
| **Dynamic Default Values**  | Use it to generate dynamic values at runtime, e.g., random IDs or values based on logic.      | `field(default_factory=generate_id)` where `generate_id()` returns a unique value for each instance. |
| **Complex Data Structures** | Use it for initializing fields with complex types like dictionaries or other data containers. | `field(default_factory=lambda: {'key': 0})` for initializing a dictionary.                           |
| **Lazy Initialization**     | Create expensive or delayed objects only at the time of instantiation.                        | `field(default_factory=DatabaseConnection)` ensures a connection object is created when needed.      |

---

### Why Do We Need `__post_init__()`?

In Python dataclasses, `__post_init__()` is a special method that gets called
after the dataclass `__init__()` method completes. This is useful when you need
to perform some additional logic after the object is initialized, especially
when you have fields like `InitVar` that are not stored as attributes or when
you need to perform computations that depend on multiple fields.

---

### When to Use `__post_init__()`?

- **Post-constructor initialization**: When additional initialization or
  validation is required after the default `__init__()` is run.
- **Working with `InitVar`**: You can handle `InitVar` variables (those that are
  passed during initialization but are not stored as attributes) in
  `__post_init__()`.
- **Dependent computations**: If certain attributes need to be set or computed
  based on the values of other fields, `__post_init__()` is a good place to do
  that.

---

### How to Use `__post_init__()`?

You define a `__post_init__()` method within your dataclass. This method is
automatically called right after the `__init__()` method, allowing you to add
any logic you want.

---

### Examples of `__post_init__()` Usage

#### 1. **Basic Usage of `__post_init__()`**

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    status: str = "Unknown"

    def __post_init__(self):
        if self.age >= 18:
            self.status = "Adult"
        else:
            self.status = "Minor"

# Usage
person1 = Person(name="Alice", age=20)
person2 = Person(name="Bob", age=15)

print(person1)  # Output: Person(name='Alice', age=20, status='Adult')
print(person2)  # Output: Person(name='Bob', age=15, status='Minor')
```

In this example, `__post_init__()` is used to set the `status` field based on the `age` value after initialization.

---

#### 2. **Using `InitVar` with `__post_init__()`**

`InitVar` allows you to pass values during initialization but not store them as attributes. You can process them in `__post_init__()`.

```python
from dataclasses import dataclass, field, InitVar

@dataclass
class Product:
    name: str
    price: float
    discount: InitVar[float] = 0.0  # Passed during init, not stored as an attribute
    final_price: float = field(init=False)

    def __post_init__(self, discount: float):
        self.final_price = self.price - (self.price * discount)

# Usage
product = Product(name="Laptop", price=1000, discount=0.1)
print(product)  # Output: Product(name='Laptop', price=1000, final_price=900.0)
```

In this case, the `discount` is an `InitVar` that is passed during initialization but is only used inside `__post_init__()` to compute the `final_price`.

---

#### 3. **Handling Field Validation in `__post_init__()`**

You can use `__post_init__()` to validate fields after initialization.

```python
from dataclasses import dataclass

@dataclass
class BankAccount:
    account_number: str
    balance: float

    def __post_init__(self):
        if self.balance < 0:
            raise ValueError("Balance cannot be negative!")

# Usage
try:
    account = BankAccount(account_number="123ABC", balance=-100)
except ValueError as e:
    print(e)  # Output: Balance cannot be negative!
```

Here, `__post_init__()` checks whether the `balance` is negative and raises an error if it is.

---

#### 4. **Using `__post_init__()` for Dependent Initialization**

When one field’s initialization depends on another, `__post_init__()` can help handle that.

```python
from dataclasses import dataclass, field

@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)

    def __post_init__(self):
        self.area = self.width * self.height

# Usage
rect = Rectangle(width=5, height=10)
print(rect.area)  # Output: 50
```

Here, the `area` field is computed based on the `width` and `height` fields during `__post_init__()`.

---

### Summary Table for `__post_init__()`

| **Use Case**                        | **Description**                                                                                                                                  | **Example**                                                           |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------- |
| **Post-constructor initialization** | Allows further processing after `__init__()`, particularly when the class's default constructor isn't enough to initialize all values correctly. | Set `status` based on `age` after the object is initialized.          |
| **Working with `InitVar`**          | Enables processing of variables passed during initialization but not stored as attributes.                                                       | Use `discount` to calculate `final_price` without storing `discount`. |
| **Dependent computations**          | Useful for fields that depend on the values of other fields, especially when computed dynamically.                                               | Compute `area` after initializing `width` and `height`.               |
| **Field validation**                | Allows validation of fields after the object is constructed, ensuring valid values (e.g., checking for negative balances).                       | Raise an error if the `balance` is negative in a `BankAccount` class. |

---

Let me know if you'd like more detailed examples or have other questions about dataclasses!

### 1. `init`: Add `__init__()` Method?

#### What It Is:

The `init` parameter controls whether the `__init__()` method should be
auto-generated for your dataclass. If set to `True` (the default), the dataclass
will generate an `__init__()` method based on the fields defined in the class.

#### Why We Need It:

In most cases, we want dataclasses to auto-generate the `__init__()` method,
saving us the trouble of manually writing it. However, there are cases where you
may want to manage the initialization yourself (e.g., when more complex logic is
required or when using another design pattern).

#### Example:

```python
from dataclasses import dataclass

@dataclass(init=True)
class Car:
    make: str
    model: str

car = Car(make="Toyota", model="Corolla")
print(car)  # Output: Car(make='Toyota', model='Corolla')

# If init=False, you must provide your own constructor.
@dataclass(init=False)
class CarManualInit:
    make: str
    model: str

    def __init__(self, make, model):
        self.make = make
        self.model = model

car_manual = CarManualInit(make="Toyota", model="Corolla")
print(car_manual)  # Output: CarManualInit(make='Toyota', model='Corolla')
```

---

### 2. `repr`: Add `__repr__()` Method?

#### What It Is:

The `repr` parameter controls whether a `__repr__()` method should be
auto-generated for your dataclass. This method returns a string that represents
the object in a readable way, useful for debugging or logging.

#### Why We Need It:

Having a good `__repr__()` method makes it easier to inspect and debug objects.
However, in cases where you want to hide certain fields or provide a custom
representation, you can set `repr=False` or manually define your own
`__repr__()` method.

#### Example:

```python
@dataclass(repr=True)
class Employee:
    name: str
    position: str

emp = Employee(name="Alice", position="Engineer")
print(emp)  # Output: Employee(name='Alice', position='Engineer')

# Custom repr or hiding field from repr:
@dataclass(repr=False)
class ConfidentialEmployee:
    name: str
    position: str

emp_conf = ConfidentialEmployee(name="Bob", position="Manager")
print(emp_conf)  # Output: <__main__.ConfidentialEmployee object at 0x...>
```

---

### 3. `eq`: Add `__eq__()` Method?

#### What It Is:

The `eq` parameter controls whether the dataclass should auto-generate the
`__eq__()` method, which compares two objects for equality. By default, it
checks whether the values of all the fields are the same between two instances.

#### Why We Need It:

The `__eq__()` method is useful for checking equality between instances. In
certain cases, you may not want equality to depend on all fields, or you may
want to implement a custom equality method.

#### Example:

```python
@dataclass(eq=True)
class Product:
    name: str
    price: float

prod1 = Product(name="Phone", price=699.99)
prod2 = Product(name="Phone", price=699.99)
print(prod1 == prod2)  # Output: True

# eq=False disables the automatic equality check:
@dataclass(eq=False)
class ManualProduct:
    name: str
    price: float

prod_manual = ManualProduct(name="Phone", price=699.99)
prod_manual2 = ManualProduct(name="Phone", price=699.99)
print(prod_manual == prod_manual2)  # Output: False (No equality check)
```

---

### 4. `order`: Add Ordering Methods?

#### What It Is:

The `order` parameter controls whether comparison methods (`<`, `<=`, `>`, `>=`)
are auto-generated. If `order=True`, the dataclass will add ordering methods
based on the field values.

#### Why We Need It:

If you want to compare instances of a dataclass (e.g., sorting employees by
salary), you can set `order=True` to auto-generate the comparison methods.

#### Example:

```python
@dataclass(order=True)
class Employee:
    name: str
    salary: float

emp1 = Employee(name="Alice", salary=50000)
emp2 = Employee(name="Bob", salary=60000)

print(emp1 < emp2)  # Output: True (because 50000 < 60000)

# order=False by default, so no ordering methods are generated.
@dataclass(order=False)
class UnorderedEmployee:
    name: str
    salary: float

# This will raise an error if you try to compare instances
# unordered_emp1 < unordered_emp2  -> TypeError: '<' not supported
```

---

### 5. `unsafe_hash`: Force the Addition of a `__hash__()` Method?

#### What It Is:

The `unsafe_hash` parameter forces the generation of a `__hash__()` method, even
when the class is mutable. Normally, mutable classes (which can change their
values) should not be hashable because their hash might change when fields
change.

#### Why We Need It:

Use `unsafe_hash=True` if you need instances of your dataclass to be hashable
(e.g., to be used in sets or as dictionary keys), but be careful—changing a
field after hashing can lead to inconsistent results.

#### Example:

```python
@dataclass(unsafe_hash=True)
class Product:
    name: str
    price: float

prod = Product(name="Laptop", price=1000)
print(hash(prod))  # Hash is generated and can be used as a key in dictionaries

# unsafe_hash=False (default), so normally this would raise an error if you try to hash
@dataclass(unsafe_hash=False)
class UnhashableProduct:
    name: str
    price: float

# unhashable_prod = UnhashableProduct(name="Phone", price=699)
# hash(unhashable_prod) -> TypeError: unhashable type: 'UnhashableProduct'
```

---

### 6. `frozen`: Make the Instance Immutable?

#### What It Is:

The `frozen` parameter makes a dataclass immutable. If `frozen=True`, the fields
cannot be changed after initialization, and attempts to modify them will raise
an exception.

#### Why We Need It:

If you need your dataclass to be immutable (like a tuple), use `frozen=True`.
This is especially useful when you want instances to be hashable, as
immutability guarantees consistent hash values.

#### Example:

```python
@dataclass(frozen=True)
class ImmutableEmployee:
    name: str
    position: str

emp = ImmutableEmployee(name="Alice", position="Engineer")
# emp.name = "Bob"  # Raises: FrozenInstanceError: cannot assign to field 'name'

# frozen=False (default), allows field modification
@dataclass(frozen=False)
class MutableEmployee:
    name: str
    position: str

emp_mutable = MutableEmployee(name="Alice", position="Engineer")
emp_mutable.name = "Bob"  # Works because the instance is mutable
print(emp_mutable.name)  # Output: Bob
```

---

### Summary Table for `@dataclass()` Parameters

| **Parameter** | **Description**                                                                                                                                            | **Default** | **Example**                                                                              |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ---------------------------------------------------------------------------------------- |
| `init`        | Automatically adds an `__init__()` method that initializes the fields.                                                                                     | `True`      | `@dataclass(init=False)` if you want to manually define the constructor.                 |
| `repr`        | Automatically adds a `__repr__()` method for a readable string representation.                                                                             | `True`      | `@dataclass(repr=False)` if you don't want the default string representation.            |
| `eq`          | Automatically adds an `__eq__()` method for checking equality between instances.                                                                           | `True`      | `@dataclass(eq=False)` if you want to disable automatic equality checks.                 |
| `order`       | Automatically adds ordering methods (`<`, `<=`, `>`, `>=`) for comparing instances.                                                                        | `False`     | `@dataclass(order=True)` if you want to enable instance comparison.                      |
| `unsafe_hash` | Forces the addition of a `__hash__()` method, even for mutable instances. Use with caution, as it can lead to inconsistent behavior if fields are changed. | `False`     | `@dataclass(unsafe_hash=True)` to make instances hashable, even if the class is mutable. |
| `frozen`      | Makes the dataclass immutable (fields cannot be modified after initialization).                                                                            | `False`     | `@dataclass(frozen=True)` if you want to make the instance immutable like a tuple.       |

This breakdown covers each parameter with explanations and examples, showing how
they can customize the behavior of dataclasses. Let me know if you'd like more
details!

In Python, if you use `frozen=True` with a dataclass, it makes **all fields
immutable**. However, if you want to achieve partial immutability (i.e., make
some fields immutable while allowing others to be mutable), there isn't a direct
way to do it just with `frozen=True`.

### Workaround to Make Some Fields Immutable

You can manually control immutability by using the `property` decorator in
combination with `@dataclass` to control the mutability of specific fields. This
approach allows you to make some fields immutable by only providing a getter
(read-only property), while other fields remain mutable.

---

### Example of Partially Immutable Dataclass

In the example below, the `id` field is immutable (read-only), while the `name`
field remains mutable.

```python
from dataclasses import dataclass, field

@dataclass
class Person:
    _id: int
    name: str

    # Property to make 'id' immutable (read-only)
    @property
    def id(self):
        return self._id

# Usage
p = Person(_id=123, name="Alice")
print(p.id)  # Output: 123
p.name = "Bob"  # Works, as 'name' is mutable
print(p.name)  # Output: Bob

# p.id = 456  # Raises an AttributeError: can't set attribute, since 'id' is read-only
```

Here, `id` is a read-only property, so trying to set it after initialization
raises an `AttributeError`, while the `name` field is mutable and can be
changed.

---

### Another Approach: Customizing `__setattr__()`

If you want more control and flexibility, you can override the `__setattr__()`
method to enforce immutability only for specific fields.

```python
from dataclasses import dataclass

@dataclass
class Employee:
    id: int
    name: str
    salary: float

    def __setattr__(self, name, value):
        # Enforce immutability for 'id' field
        if name == "id" and hasattr(self, name):
            raise AttributeError(f"{name} is immutable.")
        else:
            super().__setattr__(name, value)

# Usage
emp = Employee(id=1, name="Alice", salary=50000)
emp.name = "Bob"  # Works, as 'name' is mutable
print(emp.name)  # Output: Bob

# emp.id = 2  # Raises: AttributeError: id is immutable.
```

This approach allows you to enforce immutability selectively by intercepting
assignments to specific fields.

---

### Summary

- **Frozen Dataclass**: If you use `frozen=True`, **all fields** are immutable.
- **Custom Properties**: Use the `property` decorator to make some fields
  immutable while others remain mutable.
- **Override `__setattr__()`**: Customize the behavior by overriding the
  `__setattr__()` method to control which fields can or cannot be changed after
  initialization.

Yes, you're correct. You **cannot** combine the `frozen=True` option with the
manual `property` workaround or `__setattr__()` override. When you use
`frozen=True` in a dataclass, **all fields become immutable**, and Python
prevents any modification of instance attributes entirely.

In a `frozen=True` dataclass, trying to modify any attribute raises a
`FrozenInstanceError`. Since frozen dataclasses are implemented by making the
class `__setattr__()` and `__delattr__()` methods raise exceptions, you can't
override these methods to customize immutability for specific fields.

### Why You Can't Combine `frozen=True` and `property`/`__setattr__()`:

- **With `frozen=True`**, Python injects restrictions on **all fields** by
  overriding `__setattr__()` and making it impossible to selectively modify
  fields or implement custom logic for immutability.
- When the dataclass is frozen, it is a global lock on mutability for the entire
  instance.

### Alternative Approach

If you need selective immutability, you must skip using `frozen=True` and
instead manage immutability yourself through custom logic, such as:

1. **Using `property` for read-only fields.**
2. **Overriding `__setattr__()`** to selectively control which fields are
   modifiable.

### Example:

Here’s an alternative without `frozen=True` but achieving selective immutability:

```python
from dataclasses import dataclass, field

@dataclass
class Employee:
    id: int  # Immutable field
    name: str  # Mutable field

    # Property to make 'id' immutable
    @property
    def id(self):
        return self._id

    # Override __setattr__ to enforce immutability for 'id'
    def __setattr__(self, name, value):
        if name == "_id" and hasattr(self, "_id"):
            raise AttributeError(f"'{name}' is immutable.")
        super().__setattr__(name, value)

    def __post_init__(self):
        # Initialize _id privately, because 'id' is a read-only property
        self._id = self.id
        del self.id  # Remove the public attribute to force property access

# Usage
emp = Employee(id=1, name="Alice")
print(emp.id)  # Output: 1
emp.name = "Bob"  # This works because 'name' is mutable
# emp.id = 2  # Raises: AttributeError: '_id' is immutable.
```

### Conclusion:

- You **cannot** selectively apply immutability while using `frozen=True` in
  dataclasses.
- You can achieve partial immutability using custom logic, like `property` or
  `__setattr__()`, without using `frozen=True`.

---

### Explanation and Examples of Using `slots` in Dataclasses

#### What are slots?

Python classes by default use a dictionary to store their attributes, which
allows for dynamic attribute bindings and modification. However, this
flexibility comes at the cost of higher memory usage. The `__slots__` attribute
changes the behavior by defining a static structure which significantly reduces
the memory overhead.

#### Using `slots=True` in Dataclasses

In Python's dataclasses, the `slots=True` argument can be used to automatically
generate the `__slots__` attribute, limiting the instance to only the fields
defined and potentially improving memory usage and attribute access speed.

**Example:**

```python
from dataclasses import dataclass

@dataclass(slots=True)
class InventoryItem:
    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand
```

In this example, an `InventoryItem` class is defined with slots, restricting
instances to the specified attributes only, potentially reducing memory usage.

### Explanation of Dataclass Field Arguments

#### 1. `init=True/False`

This argument in a dataclass field specifies whether the field should be
included as a parameter in the generated `__init__()` method of the dataclass.

- `init=True`: The field is included in the `__init__()` method.
- `init=False`: The field is not included in the `__init__()` method.

**Example:**

```python
from dataclasses import dataclass, field

@dataclass
class Employee:
    name: str
    id: int = field(init=False, default=999)
```

Here, `id` is not included as a parameter in the `__init__()` method and defaults to `999`.

#### 2. `repr=True/False`

This argument controls whether the field should be included in the autogenerated `__repr__()` method.

- `repr=True`: Includes the field in the string returned by `__repr__()`.
- `repr=False`: Excludes the field from the `__repr__()` output.

**Example:**

```python
from dataclasses import dataclass, field

@dataclass
class Employee:
    name: str
    id: int = field(repr=False)
```

The `id` will not be included in the `__repr__()` output for instances of `Employee`.

#### 3. `default=None`

This sets a default value for the field if no value is provided during instantiation.

**Example:**

```python
from dataclasses import dataclass

@dataclass
class Employee:
    name: str
    id: int = field(default=None)
```

If `id` is not provided during instantiation, it defaults to `None`.

#### 4. `default_factory`

Used when the default value needs to be a dynamically created object, like a
list or a dictionary, which should not be shared between instances.

**Example:**

```python
from dataclasses import dataclass, field

@dataclass
class Employee:
    skills: list = field(default_factory=list)
```

Each `Employee` instance gets its own list for `skills`.

### Summary Table

| Keyword           | Use Cases                         | Description                                                                  | When It's Used                                     |
| ----------------- | --------------------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------- |
| `slots=True`      | Optimizing memory usage           | Uses static structure to store attributes, reducing per-instance memory cost | Dataclasses with many instances                    |
| `init=True/False` | Control `__init__()` parameters   | Include/exclude fields in the autogenerated constructor                      | Customizing constructor parameters                 |
| `repr=True/False` | Customizing object representation | Determine if a field should be included in `__repr__()` output               | Adjusting how objects are represented              |
| `default=None`    | Setting default field values      | Provide a default value for a field if none is given during instantiation    | Fields that should have a default value            |
| `default_factory` | Default value for mutable types   | Generate a default value for each instance independently                     | When default values need to be unique per instance |

This table outlines the use cases and descriptions of various dataclass field
configurations, helping to choose the right configuration depending on the
specific needs of your application.

---

The two field configurations you mentioned in the context of Python dataclasses
do seem similar at first glance, but they have distinct behaviors:

### Definitions and Differences

1. **`some_value : str = field(init=False, repr=False)`**

   - **`init=False`** means that `some_value` is not included as a parameter in
     the `__init__()` method of the dataclass. This implies that you cannot set
     it directly at instantiation.
   - **`repr=False`** means that `some_value` will not be included in the
     autogenerated `__repr__()` output of the dataclass.
   - **Default value** is not specified, which means Python will raise an error
     if you try to access `some_value` without setting it first.

2. **`some_value : str = field(default=None, repr=False)`**
   - **`default=None`** explicitly sets the default value of `some_value` to
     `None`. This allows `some_value` to be accessed immediately after
     instantiation, even if no value is provided during instantiation.
   - **`repr=False`** has the same effect as in the first case, excluding
     `some_value` from the `__repr__()` output.
   - This field is included in the `__init__()` method by default because `init`
     is not specified (defaults to `True`), allowing the value to be set at
     object creation.

### Example Demonstrating the Differences

Let's define two classes with these fields and see how object creation differs:

```python
from dataclasses import dataclass, field

@dataclass
class ExampleA:
    some_value: str = field(init=False, repr=False)

@dataclass
class ExampleB:
    some_value: str = field(default=None, repr=False)

# Creating objects
try:
    obj_a = ExampleA()
    print("ExampleA created")
    print(f"Value of some_value in ExampleA: {obj_a.some_value}")
except AttributeError as e:
    print(f"Error when accessing uninitialized some_value in ExampleA: {e}")

obj_b = ExampleB()
print("ExampleB created")
print(f"Value of some_value in ExampleB: {obj_b.some_value}")

# Attempt to set some_value directly at instantiation (should fail for ExampleA)
try:
    obj_a = ExampleA(some_value="Test")
except TypeError as e:
    print(f"Error when initializing ExampleA with some_value: {e}")

obj_b = ExampleB(some_value="Test")
print(f"ExampleB created with some_value set at instantiation: {obj_b.some_value}")
```

### Key Differences Highlighted:

- **Initialization**: `ExampleA` does not allow setting `some_value` at
  instantiation due to `init=False`. Trying to do so will result in a
  `TypeError`.
- **Default Value**: `ExampleA` will raise an error if `some_value` is accessed
  without being explicitly set after object creation, while `ExampleB` will not
  because it defaults to `None`.
- **Instantiation**: You can pass `some_value` directly when creating an
  instance of `ExampleB`, but not for `ExampleA`.

### Conclusion

- They are not the same because `ExampleA` requires you to set `some_value`
  manually after creating an instance (and does not accept it as an `__init__`
  argument), whereas `ExampleB` allows you to set it either during instantiation
  or use the default value. This makes `ExampleB` more flexible and
  user-friendly in scenarios where you want a default value that can optionally
  be overridden.

---

The two field configurations you mentioned in the context of Python dataclasses
do seem similar at first glance, but they have distinct behaviors:

### Definitions and Differences

1. **`some_value : str = field(init=False, repr=False)`**

   - **`init=False`** means that `some_value` is not included as a parameter in
     the `__init__()` method of the dataclass. This implies that you cannot set
     it directly at instantiation.
   - **`repr=False`** means that `some_value` will not be included in the
     autogenerated `__repr__()` output of the dataclass.
   - **Default value** is not specified, which means Python will raise an error
     if you try to access `some_value` without setting it first.

2. **`some_value : str = field(default=None, repr=False)`**
   - **`default=None`** explicitly sets the default value of `some_value` to
     `None`. This allows `some_value` to be accessed immediately after
     instantiation, even if no value is provided during instantiation.
   - **`repr=False`** has the same effect as in the first case, excluding
     `some_value` from the `__repr__()` output.
   - This field is included in the `__init__()` method by default because `init`
     is not specified (defaults to `True`), allowing the value to be set at
     object creation.

### Example Demonstrating the Differences

Let's define two classes with these fields and see how object creation differs:

```python
from dataclasses import dataclass, field

@dataclass
class ExampleA:
    some_value: str = field(init=False, repr=False)

@dataclass
class ExampleB:
    some_value: str = field(default=None, repr=False)

# Creating objects
try:
    obj_a = ExampleA()
    print("ExampleA created")
    print(f"Value of some_value in ExampleA: {obj_a.some_value}")
except AttributeError as e:
    print(f"Error when accessing uninitialized some_value in ExampleA: {e}")

obj_b = ExampleB()
print("ExampleB created")
print(f"Value of some_value in ExampleB: {obj_b.some_value}")

# Attempt to set some_value directly at instantiation (should fail for ExampleA)
try:
    obj_a = ExampleA(some_value="Test")
except TypeError as e:
    print(f"Error when initializing ExampleA with some_value: {e}")

obj_b = ExampleB(some_value="Test")
print(f"ExampleB created with some_value set at instantiation: {obj_b.some_value}")
```

### Key Differences Highlighted:

- **Initialization**: `ExampleA` does not allow setting `some_value` at
  instantiation due to `init=False`. Trying to do so will result in a
  `TypeError`.
- **Default Value**: `ExampleA` will raise an error if `some_value` is accessed
  without being explicitly set after object creation, while `ExampleB` will not
  because it defaults to `None`.
- **Instantiation**: You can pass `some_value` directly when creating an
  instance of `ExampleB`, but not for `ExampleA`.

### Conclusion

- They are not the same because `ExampleA` requires you to set `some_value`
  manually after creating an instance (and does not accept it as an `__init__`
  argument), whereas `ExampleB` allows you to set it either during instantiation
  or use the default value. This makes `ExampleB` more flexible and
  user-friendly in scenarios where you want a default value that can optionally
  be overridden.

Below is a table summarizing the differences between the two field configurations in dataclasses:

| **Aspect**                      | **ExampleA: `some_value: str = field(init=False, repr=False)`**                            | **ExampleB: `some_value: str = field(default=None, repr=False)`**  |
| ------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| **Included in `__init__()`**    | No, cannot be set during instantiation.                                                    | Yes, can be set during instantiation or will use default (`None`). |
| **Default Value Provision**     | No default value, must be set manually after instantiation.                                | Default value is `None`, automatically set.                        |
| **Access Post-Instantiation**   | Raises error if accessed before being explicitly set.                                      | Can be accessed immediately with default or set value.             |
| **Error on Unset Access**       | Will raise an `AttributeError` if accessed before setting.                                 | No error, returns `None` if not set during instantiation.          |
| **Representation (`__repr__`)** | Excluded due to `repr=False`.                                                              | Excluded due to `repr=False`.                                      |
| **Flexibility**                 | Less flexible, requires manual setting post-creation.                                      | More flexible, supports immediate use and default initialization.  |
| **Usage Scenario**              | Suitable when post-creation initialization is needed or for attributes managed internally. | Suitable for optional attributes with a sensible default.          |

This table highlights the operational differences and typical usage scenarios,
helping you to decide which configuration might be better suited to your
specific needs in Python applications.

## What is InitVar

Ah, `InitVar` in Python dataclasses is a type specifically meant for fields that
are needed during the initialization process but are not intended to be stored
as part of the object's attributes after initialization is complete.
Essentially, `InitVar` fields are used for providing temporary data that is used
to compute or set other fields within the dataclass during the `__post_init__`
method.

### Understanding `InitVar`

`InitVar` is used for initialization variables that are not part of the actual
data record (or persistent state) of the dataclass. This is particularly useful
for parameters that are needed for the initialization but should not be part of
the object's state after initialization.

### How to Use `InitVar`

Here's a step-by-step explanation on how to use `InitVar`:

1. **Import `InitVar`:** First, you need to import `InitVar` from the
   `dataclasses` module.
2. **Define `InitVar` Fields:** In the dataclass, declare fields as
   `InitVar[type]` where `type` is the expected type of the initialization
   variable.
3. **Use in `__post_init__`:** These variables can then be used in the
   `__post_init__` method to perform additional initializations or to compute
   values for the actual fields of the dataclass.

### Example

Here's an example to demonstrate how `InitVar` might be used:

```python
from dataclasses import dataclass, field, InitVar

@dataclass
class Student:
    name: str
    graduating: bool = field(init=False)
    age: int
    graduation_year: InitVar[int]  # This is used to compute `graduating`

    def __post_init__(self, graduation_year: int):
        current_year = 2021
        self.graduating = (graduation_year == current_year)

# Example usage
student = Student(name="John Doe", age=21, graduation_year=2021)
print(student)  # Output will not include graduation_year, but will show graduating status
```

In this example:

- `graduation_year` is provided during instantiation but isn't stored as part of
  the object. It's only used to compute whether the student is graduating this
  year.
- The `graduating` attribute is then computed based on the `graduation_year`
  passed during initialization.

### Summary of `InitVar`

| Aspect     | Description                                                                                                                                                         |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Purpose    | To provide additional data needed during initialization but not meant to be part of the object’s permanent state.                                                   |
| Usage      | It is declared as `field_name: InitVar[type]` and used within the `__post_init__` method.                                                                           |
| Common Use | Initialization parameters that are needed to compute the actual attributes of a dataclass but do not need to be stored as part of the dataclass's persistent state. |

Using `InitVar` can help make your dataclass definitions clearer by separating
temporary initialization data from the persistent state of objects, enhancing
the maintainability and readability of your code.

## Hash in dataclasses

Here we will provide an example of a dataclass where the `hash` attribute is
explicitly used, and demonstrate how it impacts the behavior of the class in
hashed collections like sets and dictionaries.

### Example of Using `hash` in Dataclasses

We will create a dataclass for `Person` where each person has a unique
identifier (`id`). We'll use this `id` for hashing and comparisons, but other
fields like `name` will be excluded from these operations.

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Person:
    id: int
    name: str = field(compare=False, hash=False, repr=True)

# Creating a set of Person objects
if __name__ == "__main__":
    person1 = Person(id=1, name="Alice")
    person2 = Person(id=1, name="Alice")
    person3 = Person(id=2, name="Bob")

    # Adding to a set to see hash and equality behavior
    people_set = {person1, person2, person3}
    print(people_set)  # Expected: {Person(id=1, name='Alice'), Person(id=2, name='Bob')}

    # Creating a dictionary to use persons as keys
    person_dict = {person1: "Data for Alice", person3: "Data for Bob"}
    print(person_dict[person1])  # Output: "Data for Alice"
    print(person_dict[person2])  # Output: "Data for Alice" since person1 and person2 are considered the same based on id
```

### Explanation

1. **Dataclass Definition**:

   - `Person` is defined with `id` as a field that participates in hashing and
     equality checks (by default, as we haven't specified otherwise).
   - The `name` field has `compare=False` and `hash=False`, meaning it doesn't
     affect the equality comparisons or the hash value of the instances.

2. **Set Behavior**:

   - `person1` and `person2` are considered the same in the set because they
     have the same `id`, even though all other attributes are the same too. If
     you change the `id`, you'll see different behavior.
   - `person3` is different due to a different `id`.

3. **Dictionary Key Usage**:
   - Persons are used as keys in a dictionary. Because `person1` and `person2`
     have the same `id` and thus the same hash value, they are treated as the
     same key, so `person_dict[person2]` accesses the same item as
     `person_dict[person1]`.

This example illustrates how the `hash` setting can be used to control which
fields contribute to the object's identity in contexts where hashing is
relevant, such as sets and dictionaries. This is crucial for ensuring correct
and expected behaviors in data structures relying on hash-based mechanisms.

Let's create two examples where we explicitly set `hash=True` and `hash=False`
for specific fields in a dataclass, and then observe how these settings affect
behavior when objects are used in sets and dictionaries.

### Example 1: Using `hash=True`

In this example, we will define a dataclass where a specific field contributes to the hash value.

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Product:
    id: int
    name: str
    price: float = field(compare=False, hash=True)  # Using hash=True explicitly

# Testing in main
if __name__ == "__main__":
    product1 = Product(id=101, name="Coffee", price=15.99)
    product2 = Product(id=101, name="Coffee", price=15.99)
    product3 = Product(id=102, name="Tea", price=10.99)

    # Adding to a set
    product_set = {product1, product2, product3}
    print(product_set)  # Should print both products as the 'id' and 'price' are the same for product1 and product2

    # Using as dictionary keys
    product_dict = {product1: "Available", product3: "Out of stock"}
    print(product_dict[product2])  # Should output 'Available' as product2 is considered the same as product1
```

### Example 2: Using `hash=False`

In this next example, we'll define a dataclass where a field is explicitly excluded from contributing to the hash.

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Employee:
    id: int
    name: str = field(compare=True, hash=False)  # hash=False to exclude from hash computations

# Testing in main
if __name__ == "__main__":
    employee1 = Employee(id=1, name="Alice")
    employee2 = Employee(id=1, name="Alice")
    employee3 = Employee(id=2, name="Bob")

    # Adding to a set
    employee_set = {employee1, employee2, employee3}
    print(employee_set)  # Should show Alice once and Bob once, even though name does not affect the hash

    # Using as dictionary keys
    employee_dict = {employee1: "Developer", employee3: "Manager"}
    print(employee_dict[employee2])  # Outputs 'Developer' since employee1 and employee2 have the same ID
```

### Explanation and Effects:

- **Example 1 (`hash=True`)**: The `price` field, although typically not used
  for identity, is included in hash computations. Both `product1` and `product2`
  are treated as the same in sets and dictionaries due to having identical `id`
  and `price`.
- **Example 2 (`hash=False`)**: The `name` field in `Employee` does not affect
  the hash value, so even if two employees have the same name but different IDs,
  they would be treated as different objects. However, in this example, because
  we haven't altered the ID and it is the only attribute contributing to the
  hash, `employee1` and `employee2` are still treated as identical.

These examples demonstrate the flexibility you have with Python's dataclasses to
tailor the behavior of objects concerning how they are stored and retrieved from
data structures that depend on hashing, like sets and dictionaries.

Absolutely, let's clarify and unify the example with two similar dataclass
definitions, where one uses `hash=True` and the other uses `hash=False`. We will
then observe the effects when these objects are placed in sets and dictionaries.

### Example Dataclass Definitions and Usage

#### Dataclass with `hash=True`

In this example, a field contributes to the hash value explicitly.

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Item:
    id: int
    name: str = field(compare=False, hash=True)  # Hash explicitly included for `name`

# Testing in main
if __name__ == "__main__":
    item1 = Item(id=1, name="Pen")
    item2 = Item(id=1, name="Pen")
    item3 = Item(id=1, name="Pencil")

    # Adding to a set
    item_set = {item1, item2, item3}
    print(item_set)  # Output will show 'Pen' once and 'Pencil' once because name affects hash

    # Using as dictionary keys
    item_dict = {item1: "Stationery", item3: "Art Supplies"}
    print(item_dict[item2])  # Outputs 'Stationery' because item2 is considered the same as item1
```

#### Dataclass with `hash=False`

In the next example, the field is excluded from contributing to the hash.

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Item:
    id: int
    name: str = field(compare=False, hash=False)  # Hash explicitly excluded for `name`

# Testing in main
if __name__ == "__main__":
    item1 = Item(id=1, name="Pen")
    item2 = Item(id=1, name="Pen")
    item3 = Item(id=1, name="Pencil")

    # Adding to a set
    item_set = {item1, item2, item3}
    print(item_set)  # Output will show 'Pen' twice and 'Pencil' once because name does not affect hash

    # Using as dictionary keys
    item_dict = {item1: "Stationery", item3: "Art Supplies"}
    print(item_dict[item2])  # Outputs 'Stationery' because item2 is considered the same as item1 by ID
```

### Expected Outputs

- **First Example (`hash=True`)**:

  - The output for the set will be something like `{Item(id=1, name='Pen'), Item(id=1, name='Pencil')}`, as `name` contributes to the hash and `Pencil`
    is treated as a different entry despite the same `id`.
  - The dictionary access `print(item_dict[item2])` will output `'Stationery'`
    because `item2` is identical to `item1` based on both `id` and `name`.

- **Second Example (`hash=False`)**:
  - The output for the set will show something like `{Item(id=1, name='Pen'), Item(id=1, name='Pen'), Item(id=1, name='Pencil')}`, displaying multiple
    entries for 'Pen' because `name` does not contribute to the hash.
  - The dictionary access will still treat `item2` as identical to `item1`, as
    hashing defaults to using `id` only.

This illustration should clearly demonstrate how the `hash` attribute affects
the behavior of dataclass objects when used in hashed data structures.

---

Below are two comprehensive tables detailing the attributes available in the
Python `@dataclass` decorator and the `field()` function for dataclass fields.
These tables include descriptions, benefits, and typical use cases to help you
integrate these features effectively in your development work.

### Table 1: Attributes for the `@dataclass` Decorator

| Attribute     | Description                                                                       | Benefits                                                                                         | Use Cases                                                            |
| ------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| `init`        | Automatically generate an `__init__()` method.                                    | Simplifies initialization of dataclasses.                                                        | When you need an automatic constructor.                              |
| `repr`        | Automatically generate a `__repr__()` method.                                     | Eases debugging by providing a readable string representation.                                   | When you need a simple way to print dataclass objects for debugging. |
| `eq`          | Automatically generate an `__eq__()` method.                                      | Allows object comparison using `==`.                                                             | When you need to compare dataclass instances.                        |
| `order`       | Automatically generate ordering methods (`__lt__`, `__le__`, `__gt__`, `__ge__`). | Enables object ordering and comparisons.                                                         | When objects need to be sortable or compared.                        |
| `unsafe_hash` | Force the generation of a `__hash__()` method even if `__eq__` is defined.        | Enables objects to be used as dictionary keys or set members, even when custom equality is used. | When `eq` is True but you still need a hash method.                  |
| `frozen`      | Make instances immutable after creation.                                          | Prevents modification after initialization, ensuring hash consistency.                           | When object immutability is needed (similar to tuples).              |

### Table 2: Keywords and Options in the `field()` Function

| Field Attribute   | Description                                                                                                      | Benefits                                                                  | When It's Used                                                                  |
| ----------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `default`         | Sets a default value for the field, which is used if no value is provided during instantiation.                  | Provides a convenient way to set a default without using `__post_init__`. | When a field should have a default value.                                       |
| `default_factory` | Accepts a callable that returns the default value for the field; called for each new instance.                   | Ensures unique default values for mutable types like lists or dicts.      | When default needs to be a mutable type like a list or a dictionary.            |
| `init`            | If `True`, include the field as a parameter in the `__init__()` method; if `False`, exclude it.                  | Allows exclusion of fields from the initialization method.                | To exclude fields from the automatic constructor.                               |
| `repr`            | If `True`, include the field in the string returned by the `__repr__()` method; if `False`, exclude it.          | Controls visibility in the object's representation.                       | To customize the object’s official string representation.                       |
| `compare`         | If `True`, include the field in comparisons of the object; if `False`, exclude it.                               | Controls which fields affect object comparison.                           | To include/exclude fields from being used in comparison operations.             |
| `hash`            | If `True`, include the field in the hash value; if `False`, exclude it; if `None`, use the setting of `compare`. | Determines field inclusion in hash calculations.                          | To control which fields contribute to the object's hash value.                  |
| `metadata`        | A mapping that stores arbitrary information about the field. Does not affect the field’s behavior directly.      | Useful for storing extra information about the field.                     | For annotations or additional metadata that does not affect dataclass behavior. |

### Dataclass Template with All Features

This template includes use of various `@dataclass` and `field()` attributes for
a hypothetical `Employee` class, demonstrating a possible configuration you can
start from and adapt based on your specific requirements.

```python
from dataclasses import dataclass, field
from typing import List

def default_id():
    return 1

@dataclass(order=True, frozen=True)
class Employee:
    id: int = field(default_factory=default_id, init=True, repr=True, compare=True, hash=True)
    name: str = field(init=True, repr=True, compare=False, hash=False)
    skills: List[str] = field(default_factory=list, repr=True, compare=False, hash=False)
    age: int = field(default=None, repr=True, compare=True, hash=True, metadata={'unit': 'years'})

# Example usage
if __name__ == "__main__":
    emp1 = Employee(name="Alice")
    emp2 = Employee(id=2, name="Bob", skills=["Python", "Data Analysis"])
    print(emp1)
    print(emp2)
    print(emp1 == emp2)
```

This template effectively utilizes the `dataclass` and `field` features,
providing a robust starting point for defining classes with various custom
behaviors in terms of initialization, representation, comparison, and
immutability. Adjust the attributes and methods as needed for your application.

---

## Template - Boilerplate

Let's integrate `InitVar` into the `Employee`
dataclass. `InitVar` fields are typically used for initialization purposes and
do not become part of the object's state. This can be useful for input
validation, computing derived properties, or other setup tasks that should not
impact the serialized or compared state of the instance.

### Updated Dataclass with `InitVar`

Here, we'll use `InitVar` to provide an optional initialization message or
configuration detail that can be logged or processed during instantiation but
won't be stored with the object.

```python
from dataclasses import dataclass, field, InitVar, asdict, astuple
from typing import List, Optional

def default_id():
    return 1

@dataclass(order=True, frozen=True)
class Employee:
    id: int = field(default_factory=default_id, init=True, repr=True, compare=True, hash=True)
    name: str = field(init=True, repr=True, compare=False, hash=False)
    skills: List[str] = field(default_factory=list, repr=True, compare=False, hash=False)
    age: Optional[int] = field(default=None, repr=True, compare=True, hash=True, metadata={'unit': 'years'})
    initialization_log: InitVar[Optional[str]] = None  # This will not be part of the persistent state

    def __post_init__(self, initialization_log: Optional[str]):
        object.__setattr__(self, 'name', self.name.title())  # Enforce name to be title case
        if self.age is not None and (self.age < 0 or self.age > 120):
            raise ValueError("Invalid age value: Age must be between 0 and 120.")

        # Log the initialization detail if provided
        if initialization_log:
            print(f"Initializing Employee: {initialization_log}")

    @property
    def info(self):
        return f"{self.name}, {self.age} years old, working with skills: {', '.join(self.skills)}"

    def add_skill(self, skill: str):
        if isinstance(skill, str) and skill not in self.skills:
            new_skills = self.skills + [skill]
            object.__setattr__(self, 'skills', new_skills)

    def __str__(self):
        return f"Employee {self.id}: {self.info}"

    @staticmethod
    def from_dict(data):
        return Employee(**data)

    @classmethod
    def from_employee(cls, employee):
        return cls(id=employee.id, name=employee.name, skills=employee.skills.copy(), age=employee.age)

# Example usage
if __name__ == "__main__":
    emp1 = Employee(name="alice", age=30, initialization_log="Created for project A")
    emp2 = Employee(id=2, name="bob", skills=["Python", "Data Analysis"], age=25)
    print(emp1)
    print(emp2)

    emp1.add_skill("Leadership")
    print(emp1)

    emp3 = Employee.from_dict({'name': 'Carol', 'age': 32})
    print(emp3)

    emp4 = Employee.from_employee(emp1)
    print(emp4)
```

### Explanation of Changes

- **`initialization_log: InitVar[Optional[str]]`**: This field is declared as an
  `InitVar`, which means it can be passed to the constructor but does not become
  part of the instance's field data. It's a transient parameter used for
  additional logging or setup during instantiation.
- **Updated `__post_init__`**: Now accepts `initialization_log` as a parameter
  and logs this during object creation if provided. This allows for dynamic
  handling of initialization context or messaging.

This modification makes the `Employee` class even more versatile by allowing for
contextual initialization while keeping the internal state clean of any
temporary or setup-specific data.

The enhanced `Employee` dataclass integrates several advanced programming
concepts and Python features. Here are the key features of the class:

### 1. **Dataclass Decorators**

- **Frozen**: The `frozen=True` parameter makes instances of the class immutable
  after creation. This immutability is essential for ensuring objects are
  hashable and can be safely used as keys in dictionaries or elements in sets.

### 2. **Field Specifications**

- **Custom Fields**: Fields are customized with parameters like `init`, `repr`,
  `compare`, and `hash` to precisely control their behavior in object lifecycle
  operations—construction, representation, comparison, and hashing.
- **InitVar**: Utilizes `InitVar` for the `initialization_log`, which allows
  passing additional initialization data that does not persist as part of the
  object's state, used primarily for logging or initialization checks.

### 3. **Automatic and Custom Initialization**

- **`__post_init__` Method**: Automates post-initialization processes like input
  validation and setting properties that require custom logic, such as
  capitalizing names and validating age constraints.
- **Temporary Initialization Data**: Handles non-persistent data for
  initialization which is not stored with the object, demonstrating how to
  manage temporary context data.

### 4. **Property Decorators**

- **Computed Properties**: Implements the `info` property to provide a formatted
  description of the employee, combining multiple fields into a readable string.
  This method showcases how to use `@property` to create read-only properties
  that compute their values dynamically.

### 5. **Immutability with Mutation Methods**

- **Controlled Mutation**: Despite the class being frozen, it provides a method
  `add_skill` to append skills to the employee. This method circumvents
  immutability constraints by creating a new list and setting it, demonstrating
  a pattern to modify `frozen` dataclass fields.

### 6. **Serialization and Factory Methods**

- **Conversion Utilities**: Implements methods like `from_dict` and
  `from_employee` to facilitate creating instances from different data sources
  (dictionaries or other instances), enhancing the dataclass’s flexibility and
  usability in various contexts.

### 7. **Rich Output and String Representation**

- **Custom String Representation**: Overridden `__str__` method to provide a
  meaningful string output that uses the computed `info` property, making the
  class more informative and easier to debug.

### 8. **Enhanced Usability**

- **Error Handling**: Incorporates error checks within `__post_init__` to ensure
  that the employee's age is within a realistic range, preventing invalid data
  at the point of object creation.

### Summary

The `Employee` dataclass effectively demonstrates advanced usage of Python's
dataclass features to create a robust, immutable, and well-encapsulated class.
It's designed to handle complex initialization, ensure data integrity, and
provide convenient methods for object management and interaction, making it
suitable for sophisticated software systems where such behaviors are beneficial.

## Notes during dev.

1. Do you know that you can add both the `init` and `default` to the dataclasses
   for example check the example below

```python
# src/lib/caller.py

from dataclasses import dataclass, field

__all__ = [
    "caller_var",
    "CallerClass",
]  # This makes only caller_var available for import from src.lib


@dataclass(order=False, slots=True, repr=True)
class CallerClass:
    user_name: str = field(
        init=True,
        default=None,
        metadata={"user_name": "user name for the first entry "},
        repr=True,
    )
    emp_email:str = field(init=False, default=None, repr=True)

    def __post_init__(self):
        self.emp_email = f"{self.user_name} created using {self.__class__.__name__}"



```
