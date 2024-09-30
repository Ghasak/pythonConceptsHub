# Magic Method and Objects

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->

**Table of Contents**

- [Magic Method and Objects](#magic-method-and-objects)
  - [Introduction ](#introduction)
    - [How to Use These `__objects__`:](#how-to-use-these-__objects__)
    - [When `__file__` is available:](#when-__file__-is-available)
    - [When `__file__` is not available:](#when-__file__-is-not-available)
    - [Key Points:](#key-points)

<!-- markdown-toc end -->

## Introduction

Here is a comprehensive table of important Python `__objects__` (often referred to as "dunder" or "magic" attributes and methods) with their explanations, usage, and examples:

| **`__Object__`**   | **Explanation**                                                                            | **Usage**                                                                           | **Example**                                                               |
| ------------------ | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `__file__`         | Path to the current file.                                                                  | Used to dynamically get the path of the current script.                             | `print(__file__)`                                                         |
| `__name__`         | The name of the module or `__main__` if the module is being run as a script.               | Helps differentiate between running a file as a script or importing it as a module. | `if __name__ == "__main__": print("Run as script")`                       |
| `__all__`          | A list defining the public symbols in a module when using `from module import *`.          | Defines what is imported when `from module import *` is used.                       | `__all__ = ['func1', 'Class1']`                                           |
| `__init__`         | The constructor method in a class, called when an instance is created.                     | Defines initialization behavior for a class.                                        | `class MyClass: def __init__(self): self.value = 10`                      |
| `__repr__`         | Official string representation of an object, used for debugging.                           | Overrides the behavior of `repr()` and debugging printouts.                         | `def __repr__(self): return f'MyClass({self.value})'`                     |
| `__str__`          | Human-readable string representation of an object, used by `str()` or `print()`.           | Customizes the string representation for an object.                                 | `def __str__(self): return f'MyClass value: {self.value}'`                |
| `__doc__`          | Documentation string for a module, class, method, or function.                             | Automatically stores docstrings.                                                    | `class MyClass: """This is a sample class."""; print(MyClass.__doc__)`    |
| `__call__`         | Allows an instance of a class to be called like a function.                                | Enables the instance to act like a callable object.                                 | `class CallableClass: def __call__(self): print("Called")`                |
| `__dict__`         | A dictionary containing the writable attributes of an object.                              | Used to inspect or modify object attributes.                                        | `print(MyClass.__dict__)`                                                 |
| `__class__`        | The class to which an instance belongs.                                                    | Used to find out the class type of an object.                                       | `obj.__class__`                                                           |
| `__module__`       | The name of the module in which a class was defined.                                       | Identifies the module where the class is defined.                                   | `MyClass.__module__`                                                      |
| `__bases__`        | Tuple of base classes from which a class is derived.                                       | Used to inspect inheritance hierarchies.                                            | `print(MyClass.__bases__)`                                                |
| `__new__`          | A special method that creates a new instance of a class.                                   | Allows control over instance creation before `__init__`.                            | `def __new__(cls): instance = super().__new__(cls); return instance`      |
| `__len__`          | Defines behavior for `len()` function for a class.                                         | Enables custom classes to work with `len()`.                                        | `def __len__(self): return len(self.data)`                                |
| `__getitem__`      | Defines behavior for getting an item using indexing.                                       | Enables `obj[key]` syntax for custom classes.                                       | `def __getitem__(self, index): return self.data[index]`                   |
| `__setitem__`      | Defines behavior for setting an item using indexing.                                       | Enables `obj[key] = value` syntax for custom classes.                               | `def __setitem__(self, index, value): self.data[index] = value`           |
| `__delitem__`      | Defines behavior for deleting an item using indexing.                                      | Enables `del obj[key]` syntax for custom classes.                                   | `def __delitem__(self, index): del self.data[index]`                      |
| `__iter__`         | Defines behavior for iteration over an object.                                             | Enables an object to be iterable.                                                   | `def __iter__(self): return iter(self.data)`                              |
| `__next__`         | Defines behavior for the next item in an iteration.                                        | Implements the behavior of the `next()` function.                                   | `def __next__(self): return next(self.iterator)`                          |
| `__enter__`        | Defines behavior when entering a `with` block.                                             | Implements context manager functionality.                                           | `def __enter__(self): return self`                                        |
| `__exit__`         | Defines behavior when exiting a `with` block.                                              | Implements cleanup behavior for a context manager.                                  | `def __exit__(self, exc_type, exc_value, traceback): print("Exit")`       |
| `__contains__`     | Defines behavior for the `in` operator.                                                    | Enables `in` operator for custom classes.                                           | `def __contains__(self, item): return item in self.data`                  |
| `__hash__`         | Defines behavior for the `hash()` function.                                                | Enables custom hash values for objects.                                             | `def __hash__(self): return hash(self.value)`                             |
| `__eq__`           | Defines behavior for equality comparison `==`.                                             | Enables custom equality checks.                                                     | `def __eq__(self, other): return self.value == other.value`               |
| `__lt__`, `__gt__` | Define behavior for `<` and `>` comparisons.                                               | Enables custom less-than and greater-than operations.                               | `def __lt__(self, other): return self.value < other.value`                |
| `__del__`          | Destructor method, called when an object is about to be destroyed.                         | Enables cleanup before object is deleted.                                           | `def __del__(self): print("Object deleted")`                              |
| `__slots__`        | Limits the attributes that instances of a class can have, improving memory usage.          | Reduces memory overhead in large classes.                                           | `class MyClass: __slots__ = ['value']`                                    |
| `__annotations__`  | Stores type annotations of a class, method, or function.                                   | Allows access to type hints.                                                        | `def my_func(x: int) -> str: pass; print(my_func.__annotations__)`        |
| `__mro__`          | Method Resolution Order for a class, showing the order in which base classes are resolved. | Useful for understanding inheritance chains.                                        | `print(MyClass.__mro__)`                                                  |
| `__subclasses__()` | Returns a list of immediate subclasses of a class.                                         | Allows introspection of subclass hierarchy.                                         | `print(BaseClass.__subclasses__())`                                       |
| `__format__`       | Defines custom string formatting behavior for an object.                                   | Implements behavior for `format()` function.                                        | `def __format__(self, format_spec): return f'{self.value:{format_spec}}'` |
| `__bool__`         | Defines behavior for `bool()` on an object.                                                | Customizes truthiness of an object.                                                 | `def __bool__(self): return bool(self.value)`                             |

### How to Use These `__objects__`:

- **`__file__`**: Use to dynamically determine the script location or path during runtime.

  ```python
  print(f"This script is running from: {__file__}")
  ```

- **`__name__`**: Use in a script to check whether it is being run directly or imported as a module.

  ```python
  if __name__ == "__main__":
      print("Running this script directly.")
  ```

- **`__all__`**: Define it in a module to control what gets exported when using `from module import *`.

  ```python
  __all__ = ['function1', 'Class1']
  ```

- **`__call__`**: Use when you want an object to be callable, like a function.
  ```python
  class CallableObject:
      def __call__(self):
          print("Object called")
  obj = CallableObject()
  obj()  # Outputs: "Object called"
  ```

This table includes a wide range of dunder methods and attributes that provide
special behavior to classes, functions, and modules, making Python more flexible
and powerful.

Actually, `__file__` **is** a part of the Python language, but it behaves in a
specific context. It is an attribute of a module and is automatically created
when a Python script is executed from a file. However, it does not exist in
interactive environments like the Python REPL, Jupyter notebooks, or
environments where the code isn't being executed from a file.

### When `__file__` is available:

- **Python scripts**: When a Python file (e.g., `script.py`) is executed,
  `__file__` contains the path to that file.
- **Imported modules**: When a module is imported, `__file__` contains the path
  to the module file.

### When `__file__` is not available:

- **Interactive environments**: If you're using the Python interpreter
  interactively (e.g., in a REPL, Jupyter notebook, or some IDE consoles), the
  `__file__` attribute is not defined because there is no "file" associated with
  the running code.

### Key Points:

- **`__file__` is part of the Python language**, but it depends on the execution
  environment. It's not always defined in interactive sessions, but it is
  defined when a script is executed from a file.

For example, in a Python script (`example.py`):

```python
print(__file__)
```

Running this script would output the path to `example.py` when executed from the
command line or via an IDE.

In a Jupyter notebook or Python REPL:

```python
print(__file__)
```

This would throw the error `NameError: name '__file__' is not defined` because there is no file being executed.

So, `__file__` is a valid part of Python, but its availability depends on
whether the code is being executed from a script or interactively.

## More dunder methods

In Python Object-Oriented Programming (OOP), "dunder" (double underscore) or
"magic" methods like `__getattr__`, `__setattr__`, and many others, allow
developers to define custom behavior for basic operations. Here's a
comprehensive table of Python's key magic methods related to attribute access,
setting, deletion, and more, along with syntax and usage examples.

### Table of Python Attribute-Related Magic Methods

| **Magic Method**                                 | **Description**                                                                                                     | **Syntax**                                            | **Example Usage**                                                                                                                        |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `__getattr__(self, name)`                        | Called when an attribute lookup has not found the attribute in the usual places.                                    | `def __getattr__(self, name):`                        | `class MyClass: def __getattr__(self, name): return f"{name} attribute not found" obj = MyClass(); print(obj.some_attr)`                 |
| `__getattribute__(self, name)`                   | Called unconditionally to get an attribute, even if it exists. Use `super()` to avoid recursion.                    | `def __getattribute__(self, name):`                   | `class MyClass: def __getattribute__(self, name): return f"Getting {name}" obj = MyClass(); print(obj.any_attr)`                         |
| `__setattr__(self, name, value)`                 | Called when an attribute assignment is attempted.                                                                   | `def __setattr__(self, name, value):`                 | `class MyClass: def __setattr__(self, name, value): self.__dict__[name] = value obj = MyClass(); obj.some_attr = "value"`                |
| `__delattr__(self, name)`                        | Called when an attribute is deleted.                                                                                | `def __delattr__(self, name):`                        | `class MyClass: def __delattr__(self, name): print(f"Deleting {name}") del obj.some_attr`                                                |
| `__dir__(self)`                                  | Called by `dir()` to list the attributes of an object.                                                              | `def __dir__(self):`                                  | `class MyClass: def __dir__(self): return ['custom_attr'] print(dir(MyClass()))`                                                         |
| `__slots__`                                      | Limits the attributes an object can have, saving memory.                                                            | `__slots__ = ('attr1', 'attr2')`                      | `class MyClass: __slots__ = ('name', 'age') obj = MyClass(); obj.name = "John"`                                                          |
| `__call__(self, *args, **kwargs)`                | Makes an instance callable like a function.                                                                         | `def __call__(self, *args, **kwargs):`                | `class MyClass: def __call__(self, x): return x**2 obj = MyClass(); print(obj(5))`                                                       |
| `__len__(self)`                                  | Called by `len()` to return the number of items in an object.                                                       | `def __len__(self):`                                  | `class MyClass: def __len__(self): return 10 obj = MyClass(); print(len(obj))`                                                           |
| `__getitem__(self, key)`                         | Defines behavior for element access (e.g., `obj[key]`).                                                             | `def __getitem__(self, key):`                         | `class MyClass: def __getitem__(self, key): return f"Item {key}" obj = MyClass(); print(obj[1])`                                         |
| `__setitem__(self, key, value)`                  | Defines behavior for setting an item (e.g., `obj[key] = value`).                                                    | `def __setitem__(self, key, value):`                  | `class MyClass: def __setitem__(self, key, value): self.__dict__[key] = value obj = MyClass(); obj[1] = "new value"`                     |
| `__delitem__(self, key)`                         | Defines behavior for deleting an item (e.g., `del obj[key]`).                                                       | `def __delitem__(self, key):`                         | `class MyClass: def __delitem__(self, key): print(f"Deleting item {key}") del obj[1]`                                                    |
| `__contains__(self, item)`                       | Defines behavior for the `in` operator.                                                                             | `def __contains__(self, item):`                       | `class MyClass: def __contains__(self, item): return item == "target" obj = MyClass(); print("target" in obj)`                           |
| `__iter__(self)`                                 | Called to get an iterator from an object.                                                                           | `def __iter__(self):`                                 | `class MyClass: def __iter__(self): return iter([1, 2, 3]) obj = MyClass(); for i in obj: print(i)`                                      |
| `__next__(self)`                                 | Defines the behavior of the `next()` function for iteration.                                                        | `def __next__(self):`                                 | `class MyClass: def __init__(self): self.val = 0; def __next__(self): self.val += 1; return self.val obj = MyClass(); print(next(obj))`  |
| `__repr__(self)`                                 | Defines the “official” string representation of an object, used for debugging.                                      | `def __repr__(self):`                                 | `class MyClass: def __repr__(self): return "MyClass() instance" obj = MyClass(); print(repr(obj))`                                       |
| `__str__(self)`                                  | Defines the “informal” string representation of an object, used by `str()` and `print()`.                           | `def __str__(self):`                                  | `class MyClass: def __str__(self): return "MyClass instance" obj = MyClass(); print(str(obj))`                                           |
| `__format__(self, format_spec)`                  | Defines behavior for custom string formatting using the `format()` function.                                        | `def __format__(self, format_spec):`                  | `class MyClass: def __format__(self, format_spec): return f"Formatted {format_spec}" obj = MyClass(); print(format(obj, 'format_spec'))` |
| `__hash__(self)`                                 | Defines behavior for the `hash()` function, allowing an object to be used in hashed collections like sets or dicts. | `def __hash__(self):`                                 | `class MyClass: def __hash__(self): return hash(self.__str__()) obj = MyClass(); print(hash(obj))`                                       |
| `__eq__(self, other)`                            | Defines behavior for equality comparison (`==`).                                                                    | `def __eq__(self, other):`                            | `class MyClass: def __eq__(self, other): return self.value == other.value obj1, obj2 = MyClass(), MyClass(); print(obj1 == obj2)`        |
| `__lt__(self, other)`                            | Defines behavior for the less-than comparison (`<`).                                                                | `def __lt__(self, other):`                            | `class MyClass: def __lt__(self, other): return self.value < other.value obj1, obj2 = MyClass(), MyClass(); print(obj1 < obj2)`          |
| `__gt__(self, other)`                            | Defines behavior for the greater-than comparison (`>`).                                                             | `def __gt__(self, other):`                            | `class MyClass: def __gt__(self, other): return self.value > other.value obj1, obj2 = MyClass(), MyClass(); print(obj1 > obj2)`          |
| `__del__(self)`                                  | Destructor method called when an object is about to be garbage collected.                                           | `def __del__(self):`                                  | `class MyClass: def __del__(self): print("Deleting instance") obj = MyClass(); del obj`                                                  |
| `__enter__(self)`                                | Defines the behavior when entering a `with` block (for context managers).                                           | `def __enter__(self):`                                | `class MyClass: def __enter__(self): return self with MyClass() as obj: print("Entered")`                                                |
| `__exit__(self, exc_type, exc_value, traceback)` | Defines the behavior when exiting a `with` block (for context managers).                                            | `def __exit__(self, exc_type, exc_value, traceback):` | `class MyClass: def __exit__(self, exc_type, exc_value, traceback): print("Exiting") with MyClass(): pass`                               |
| `__copy__(self)`                                 | Defines shallow copy behavior for an object (used by `copy.copy()`).                                                | `def __copy__(self):`                                 | `import copy class MyClass: def __copy__(self): return MyClass() obj = MyClass(); copy.copy(obj)`                                        |
| `__deepcopy__(self, memo)`                       | Defines deep copy behavior for an object (used by `copy.deepcopy()`).                                               | `def __deepcopy__(self, memo):`                       | `import copy class MyClass: def __deepcopy__(self, memo): return MyClass() obj = MyClass(); copy.deepcopy(obj)`                          |

### Example: Using `__getattr__`, `__setattr__`, and `__delattr__`

```python
class MyClass:
    def __init__(self):
        self.existing_attr = 10

    # Called when an attribute is accessed but not found
```
