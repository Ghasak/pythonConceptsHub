# Error Handling in Python
<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Error Handling in Python](#error-handling-in-python)
    - [What is Error Handling](#what-is-error-handling)
        - [What is Error Handling?](#what-is-error-handling)
        - [Why is Error Handling Needed?](#why-is-error-handling-needed)
        - [Types of Errors in Python](#types-of-errors-in-python)
        - [Basic Error Handling Example in Python](#basic-error-handling-example-in-python)
            - [Explanation:](#explanation)
        - [Importance of Catching Specific Exceptions](#importance-of-catching-specific-exceptions)
        - [Re-Raising Exceptions](#re-raising-exceptions)
        - [Advanced Example with `else` and `finally` Blocks](#advanced-example-with-else-and-finally-blocks)
            - [Explanation:](#explanation-1)
        - [Built-in Exceptions and Custom Exceptions](#built-in-exceptions-and-custom-exceptions)
            - [Example of a Custom Exception](#example-of-a-custom-exception)
        - [Conclusion](#conclusion)
        - [Latest Knowledge on Python Error Handling](#latest-knowledge-on-python-error-handling)
            - [Structured Exception Handling](#structured-exception-handling)
            - [Additional Features](#additional-features)
            - [Useful Built-in Functions and Methods for Error Handling](#useful-built-in-functions-and-methods-for-error-handling)
        - [Common Python Exceptions Overview](#common-python-exceptions-overview)
        - [Error Handling Techniques Table](#error-handling-techniques-table)

<!-- markdown-toc end -->

## What is Error Handling

### What is Error Handling?

**Error handling** refers to the process of anticipating, detecting, and
responding to programming errors. Errors in a program can occur due to a wide
range of reasons, including invalid input, external systems failing, or even
logical flaws in the code. Error handling ensures that a program behaves
predictably in the face of such errors, preventing the program from crashing or
producing unexpected results. Instead of the program halting abruptly, error
handling allows the program to gracefully manage issues, communicate the
problems clearly, and even recover from them in some cases.

In Python, errors are typically handled using exceptions. Exceptions are special
objects that represent an error and can be raised, caught, and processed in a
structured way. Python uses a `try-except` mechanism to handle exceptions,
allowing developers to write code that responds to errors without crashing the
entire program.

### Why is Error Handling Needed?

Error handling is essential for several reasons:

1. **Program Stability**: Without error handling, an error could cause an entire
   program to crash, losing valuable data or functionality. Error handling
   allows programs to continue running or shut down gracefully, giving
   developers or users the chance to recover.
2. **User Experience**: From the user's perspective, encountering a program
   crash can be frustrating. With error handling, users can be shown a clear
   error message explaining the issue instead of just a generic crash.

3. **Predictable Behavior**: Unchecked errors can result in unpredictable
   program behavior, making it hard to debug. Proper error handling ensures that
   the program behaves in a controlled and predictable way when errors arise.

4. **Error Logging and Debugging**: Error handling allows developers to log
   errors for later review. This is useful for identifying and resolving bugs,
   particularly in production environments where immediate debugging is not
   possible.

5. **Code Robustness**: Error handling encourages writing more resilient code,
   especially when dealing with external systems (like databases or APIs) where
   failures are likely to happen.

### Types of Errors in Python

In Python, errors can generally be classified into three types:

1. **Syntax Errors**: These occur when the Python interpreter detects an issue
   with the structure of the code. They are detected before the program runs.
   For example, forgetting a colon after a function definition or having
   unbalanced parentheses.

   ```python
   def my_function()  # SyntaxError: Missing colon
       print("Hello")
   ```

2. **Runtime Errors (Exceptions)**: These occur while the program is running,
   usually because of some operation that cannot be completed. Examples include
   dividing by zero, trying to access an invalid index in a list, or opening a
   file that doesn’t exist.

   ```python
   result = 10 / 0  # ZeroDivisionError: division by zero
   ```

3. **Logical Errors**: These are errors in the logic of the program that cause
   it to produce incorrect results, even though the program runs without
   crashing. Python cannot detect logical errors, and they need to be debugged
   manually through careful review and testing.

   ```python
   def calculate_area(radius):
       return 2 * 3.14 * radius  # Logic Error: formula for circumference instead of area
   ```

### Basic Error Handling Example in Python

The simplest form of error handling in Python uses the `try-except` block. Let's explore a basic example:

```python
try:
    # This block contains code that might raise an exception
    number = int(input("Enter a number: "))
    result = 10 / number
    print(f"Result is {result}")
except ZeroDivisionError:
    # This block handles the exception when division by zero occurs
    print("You can't divide by zero!")
except ValueError:
    # This block handles the exception when the input is not an integer
    print("Please enter a valid integer.")
```

#### Explanation:

1. **`try` block**: This block contains code that might throw an error.

   - If a user enters 0, Python raises a `ZeroDivisionError` because dividing by
     zero is undefined.
   - If a user enters a non-integer value like "abc", Python raises a
     `ValueError` because the input can't be converted to an integer.

2. **`except` blocks**: These blocks handle specific exceptions. In this
   example, one block handles division by zero, and another handles invalid
   integer input.

Without error handling, this program would crash if the user entered invalid
input. With proper handling, it gives useful feedback to the user and keeps
running.

### Importance of Catching Specific Exceptions

Catching specific exceptions instead of using a generic `except` block is
important because it allows the program to respond appropriately to different
kinds of errors. For example:

```python
try:
    number = int(input("Enter a number: "))
    result = 10 / number
    print(f"Result is {result}")
except Exception as e:
    print(f"An error occurred: {e}")
```

In this case, if any kind of error occurs, the program prints a general error
message. However, this approach might catch unexpected errors that you did not
anticipate. This can make debugging harder, as the actual error is masked by the
generic handling. By catching specific exceptions, you ensure that only expected
issues are handled, and unexpected issues raise more informative error messages.

### Re-Raising Exceptions

In some cases, you might want to handle an exception but still propagate it
upwards in the call stack so that other parts of the program or a logging system
can handle it. You can re-raise exceptions using the `raise` keyword:

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Handling error locally: {e}")
    raise  # Re-raises the original exception
```

Here, the exception is caught, a message is printed, and then the exception is
re-raised for higher-level handling.

### Advanced Example with `else` and `finally` Blocks

In some situations, you want to run certain code only if no exceptions occur
(using the `else` block), or always execute a block of code regardless of
exceptions (using `finally`). Here’s a more complex example:

```python
try:
    file = open('somefile.txt', 'r')
    data = file.read()
except FileNotFoundError:
    print("File not found!")
else:
    print("File read successfully.")
finally:
    if 'file' in locals() and not file.closed:
        file.close()
        print("File closed.")
```

#### Explanation:

1. **`try` block**: Attempts to open and read a file.
2. **`except` block**: Catches a `FileNotFoundError` if the file does not exist.
3. **`else` block**: Executes only if the `try` block succeeds without raising
   any exceptions.
4. **`finally` block**: Always runs, ensuring that the file is closed whether or
   not an exception occurs. This is critical for resource management, like
   closing files or network connections.

### Built-in Exceptions and Custom Exceptions

Python comes with many built-in exceptions, but sometimes you may want to define
your own. Custom exceptions can provide more meaningful error messages specific
to your application.

#### Example of a Custom Exception

```python
class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        super().__init__(f"Attempt to withdraw {amount} with only {balance} available.")
        self.balance = balance
        self.amount = amount

# Usage
def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount

try:
    new_balance = withdraw(100, 150)
except InsufficientFundsError as e:
    print(e)
```

In this example, the custom `InsufficientFundsError` exception provides more
context about why the error occurred, enhancing readability and making debugging
easier.

### Conclusion

Error handling is a crucial part of developing robust, reliable, and
maintainable software. It helps prevent programs from crashing due to unexpected
issues and ensures that users get meaningful feedback when things go wrong.
Python’s built-in exception handling mechanisms, combined with custom exceptions
and advanced features like `else` and `finally`, make it easy to handle errors
effectively while maintaining the clarity and readability of your code.

Here’s an enhanced explanation of error handling in Python, incorporating the
latest practices, tips, and features as of the most recent versions of Python.
I've also created a table that summarizes various topics related to error
handling.

### Latest Knowledge on Python Error Handling

Python's error handling model revolves around the use of exceptions. These allow
for cleaner code by separating error-checking logic from regular control flow.
Below is a more comprehensive breakdown of key components and best practices in
Python exception handling.

#### Structured Exception Handling

1. **`try-except` Block**:

   - `try`: Code that might raise an exception is placed here.
   - `except`: Handles specific exceptions. Can catch multiple exceptions in one
     block by providing a tuple of exception classes.
   - **Newer Practice**: Prefer catching specific exceptions rather than broad
     exception classes to avoid unintended behavior.

2. **`else` Block**:

   - Code in the `else` block executes only if no exceptions occur in the `try`
     block. This is useful for code that should only run when no errors are
     encountered.

3. **`finally` Block**:

   - The `finally` block is executed regardless of whether an exception
     occurred. It's commonly used for cleanup tasks like closing files or
     releasing resources.

4. **`except` as Alias**:
   - You can assign the exception to a variable and use it within the `except` block for further processing.
   - Example:
     ```python
     except ValueError as e:
         print(e)
     ```

#### Additional Features

1. **`raise from` Syntax**:

   - Python 3 introduces the `raise ... from` syntax, which provides better
     error chaining by preserving the original exception context when raising
     new exceptions.
   - Example:
     ```python
     try:
         func()
     except SomeError as e:
         raise AnotherError("Additional info") from e
     ```

2. **`Exception.__cause__` and `Exception.__context__`**:

   - You can use `__cause__` and `__context__` to inspect linked exceptions when using the `raise from` statement.

3. **Custom Exceptions**:

   - Always derive custom exceptions from `Exception` or a specific exception class (not `BaseException`).
   - Example:
     ```python
     class CustomError(Exception):
         pass
     ```

4. **Logging Exceptions**:

   - Use the `logging` module's `exception` method to log exceptions with the full traceback.
   - Example:
     ```python
     import logging
     logging.exception("An error occurred")
     ```

5. **Exception Groups** (Introduced in Python 3.11):
   - Python 3.11 introduced **Exception Groups** to handle multiple exceptions raised simultaneously.
   - Example:
     ```python
     try:
         raise ExceptionGroup("Multiple errors", [ValueError("Invalid value"), TypeError("Wrong type")])
     except* ValueError as eg:
         print("Caught ValueError from the group:", eg)
     ```

#### Useful Built-in Functions and Methods for Error Handling

- **`traceback.print_exc()`**: Prints the full traceback of the exception.
- **`sys.exc_info()`**: Returns a tuple of (exception type, exception value, traceback), useful for advanced exception handling.

### Common Python Exceptions Overview

Here’s a table with common exceptions and their associated collections or operations.

| Exception Type      | Description                                                                          | Common Use Cases                                                                   |
| ------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| `TypeError`         | Raised when an operation or function is applied to an object of inappropriate type.  | Passing an incorrect argument type to a function or method.                        |
| `ValueError`        | Raised when a function gets an argument of correct type but inappropriate value.     | Converting strings to numbers, invalid user input.                                 |
| `KeyError`          | Raised when a key is not found in a dictionary.                                      | Accessing dictionary keys.                                                         |
| `IndexError`        | Raised when a sequence (e.g., list, tuple) index is out of range.                    | Accessing elements of a list using an invalid index.                               |
| `AttributeError`    | Raised when an invalid attribute reference is made.                                  | Accessing non-existent attributes of an object.                                    |
| `ZeroDivisionError` | Raised when division by zero is attempted.                                           | Division operations.                                                               |
| `FileNotFoundError` | Raised when a file or directory is requested but doesn’t exist.                      | File handling, opening non-existent files.                                         |
| `OSError`           | Raised for system-related errors, such as file operations or process failures.       | General I/O errors, file operations, and process handling.                         |
| `MemoryError`       | Raised when an operation runs out of memory.                                         | Working with large data structures or intensive operations.                        |
| `RecursionError`    | Raised when the maximum recursion depth is exceeded.                                 | Recursive functions that do not have a base case or terminate improperly.          |
| `StopIteration`     | Raised when the `next()` function reaches the end of an iterator.                    | Iterating through a generator or custom iterator.                                  |
| `AssertionError`    | Raised by the `assert` statement when the condition is false.                        | Debugging, unit tests, ensuring conditions hold true.                              |
| `RuntimeError`      | Raised when an error does not fall under other built-in exceptions.                  | Used as a catch-all for errors not covered by other exceptions.                    |
| `ConnectionError`   | Raised for network-related errors (e.g., `ConnectionResetError`, `BrokenPipeError`). | Network operations, API calls.                                                     |
| `TimeoutError`      | Raised when a system operation times out.                                            | Network operations, file I/O with time constraints.                                |
| `CustomError`       | User-defined exceptions.                                                             | Defined for specific application errors that don't fall under standard exceptions. |

### Error Handling Techniques Table

| Technique                      | Description                                               | Example Code                                          |
| ------------------------------ | --------------------------------------------------------- | ----------------------------------------------------- |
| Basic `try-except`             | Handles exceptions in a controlled block of code.         | `try: code except: handle_error`                      |
| Multiple `except` Blocks       | Handle different exceptions in different ways.            | `except ValueError: code_a except KeyError: code_b`   |
| `else` Block                   | Executes if no exceptions are raised.                     | `else: code_if_no_exception`                          |
| `finally` Block                | Executes always, whether an exception occurs or not.      | `finally: cleanup_code`                               |
| `raise` Statement              | Raises an exception, optionally with arguments.           | `raise ValueError("Invalid input")`                   |
| `raise from`                   | Preserves the original exception when raising a new one.  | `raise CustomError() from original_exception`         |
| Custom Exception               | Define your own exceptions derived from `Exception`.      | `class CustomError(Exception): pass`                  |
| `logging.exception()`          | Logs the error with full traceback.                       | `logging.exception("An error occurred")`              |
| Exception Groups (Python 3.11) | Handle multiple exceptions raised at once.                | `except* ValueError: handle_value_errors`             |
| `traceback.print_exc()`        | Prints the full traceback for the caught exception.       | `traceback.print_exc()`                               |
| `sys.exc_info()`               | Returns type, value, and traceback of the last exception. | `exc_type, exc_value, exc_traceback = sys.exc_info()` |
| `assert`                       | Raises `AssertionError` if the condition is `False`.      | `assert condition, "Error message"`                   |

This table and enhanced knowledge should give you a comprehensive understanding of error handling techniques in Python, including newer features and best practices.


## Try/Excpet Blocks for Error Handling - More Explanation

