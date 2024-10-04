# Debugging in Python

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->

**Table of Contents**

- [Debugging in Python ](#debugging-in-python)
  - [Introduction ](#introduction)
    - [1. **Using Print Statements (Quick and Simple Debugging)**](#1-using-print-statements-quick-and-simple-debugging)
      - [Example:](#example)
    - [2. **Using the Built-in `pdb` Module (Python Debugger)**](#2-using-the-built-in-pdb-module-python-debugger)
      - [Basic Commands:](#basic-commands)
      - [Example:](#example-1)
    - [3. **Using IDE Debuggers (Visual Studio Code, PyCharm, etc.)**](#3-using-ide-debuggers-visual-studio-code-pycharm-etc)
      - [Example: Debugging in **VS Code** using `debugpy`](#example-debugging-in-vs-code-using-debugpy)
    - [4. **Using `debugpy` for Remote Debugging**](#4-using-debugpy-for-remote-debugging)
      - [Example Setup for Remote Debugging:](#example-setup-for-remote-debugging)
    - [5. **Using `ipdb` (Enhanced `pdb`)**](#5-using-ipdb-enhanced-pdb)
      - [Installing `ipdb`:](#installing-ipdb)
      - [Example:](#example-2)
    - [6. **Logging for Persistent Debugging Information**](#6-logging-for-persistent-debugging-information)
      - [Example:](#example-3)
    - [7. **Test-Driven Debugging with Unit Tests**](#7-test-driven-debugging-with-unit-tests)
      - [Example with `pytest`:](#example-with-pytest)
    - [8. **Tracing Code Execution with `trace` Module**](#8-tracing-code-execution-with-trace-module)
      - [Example:](#example-4)
    - [Conclusion](#conclusion)

<!-- markdown-toc end -->

## Introduction

Debugging is an essential part of the development process, and Python offers
several tools and techniques to help you debug your code efficiently. The best
approach depends on the complexity of the project, personal preference, and the
tools you're using. Here’s a comprehensive guide on the best ways to debug in
Python, covering both built-in tools and third-party solutions.

### 1. **Using Print Statements (Quick and Simple Debugging)**

For small or straightforward problems, adding `print()` statements to your code
is the simplest and quickest debugging method. This technique helps you
understand the flow of your code and inspect variable values at different
stages.

#### Example:

```python
def calculate_sum(a, b):
    print(f"Calculating sum of {a} and {b}")
    return a + b

result = calculate_sum(5, 10)
print(f"Result is: {result}")
```

While this method is easy, it can clutter your code and is less efficient when
dealing with larger or more complex programs. It’s best suited for smaller, less
critical debugging tasks.

### 2. **Using the Built-in `pdb` Module (Python Debugger)**

Python’s built-in debugger, `pdb`, allows you to interactively debug your Python
code by setting breakpoints, stepping through code, inspecting variables, and
more.

#### Basic Commands:

- **`break` or `b`**: Set a breakpoint at a specified line or function.
- **`continue` or `c`**: Continue execution until the next breakpoint.
- **`step` or `s`**: Step into a function call.
- **`next` or `n`**: Step to the next line, but don’t step into function calls.
- **`list` or `l`**: List source code around the current line.
- **`print` or `p`**: Print the value of a variable.
- **`quit` or `q`**: Exit the debugger.

#### Example:

```python
import pdb

def buggy_function(a, b):
    pdb.set_trace()  # Set a breakpoint here
    result = a / b
    return result

buggy_function(10, 0)  # This will raise ZeroDivisionError
```

This code will pause at `pdb.set_trace()`, allowing you to interactively inspect
variables, step through lines, and figure out what’s going wrong.

### 3. **Using IDE Debuggers (Visual Studio Code, PyCharm, etc.)**

Integrated Development Environments (IDEs) like **PyCharm** and **Visual Studio
Code** have built-in debuggers that provide a graphical user interface (GUI) for
debugging. They allow you to:

- Set breakpoints by clicking next to the line number.
- Inspect variables and objects in real-time.
- Step through the code (`step over`, `step into`, `step out`).
- Continue execution until the next breakpoint.
- Watch expressions and interact with a debugging console.

These tools also support remote debugging, which is useful for debugging code
running on a different machine or in a production-like environment.

#### Example: Debugging in **VS Code** using `debugpy`

1. Install the Python extension and `debugpy` in your virtual environment.
2. Set breakpoints by clicking next to the line numbers.
3. Run the script using the debugger from VS Code’s debugging pane or add
   `debugpy` to your script for remote debugging.

### 4. **Using `debugpy` for Remote Debugging**

`debugpy` is a powerful debugging tool that allows you to debug Python code
remotely. It integrates with many IDEs (like Visual Studio Code) and allows you
to attach a debugger to a running Python process.

#### Example Setup for Remote Debugging:

1. Install `debugpy`:

   ```bash
   pip install debugpy
   ```

2. Add `debugpy` to your Python script:

   ```python
   import debugpy

   # Start the debugger, listening on localhost port 5678
   debugpy.listen(("localhost", 5678))
   print("Waiting for debugger to attach...")

   # Wait for a debugger to connect before continuing
   debugpy.wait_for_client()

   # Your code here
   def divide(a, b):
       return a / b

   divide(10, 0)
   ```

3. In your IDE (e.g., Visual Studio Code), configure a remote debug session to attach to `localhost:5678`.

This approach is great for debugging distributed systems, applications running
on servers, or Docker containers.

### 5. **Using `ipdb` (Enhanced `pdb`)**

`ipdb` is an enhanced version of `pdb` that integrates with `IPython`, providing
a richer experience with syntax highlighting, better tab completion, and command
history. It’s a great alternative if you’re familiar with IPython and want an
interactive debugging experience.

#### Installing `ipdb`:

```bash
pip install ipdb
```

#### Example:

```python
import ipdb

def buggy_function(a, b):
    ipdb.set_trace()  # Start an interactive debugging session
    result = a / b
    return result

buggy_function(10, 0)
```

### 6. **Logging for Persistent Debugging Information**

Instead of using `print()`, the **logging module** is a better approach for more
serious debugging and production-level code. Logging allows you to write
messages to files or streams and gives you control over the level of logging
(e.g., `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).

#### Example:

```python
import logging

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def divide(a, b):
    logging.debug(f"Dividing {a} by {b}")
    try:
        result = a / b
    except ZeroDivisionError:
        logging.error("Attempted to divide by zero")
        return None
    return result

divide(10, 0)
```

In this example, logging will provide detailed debug information about the
program’s flow and capture errors without interrupting the execution.

### 7. **Test-Driven Debugging with Unit Tests**

Unit testing frameworks like `unittest`, `pytest`, and `nose2` allow you to
write tests that validate individual units of functionality. Writing tests
before debugging helps isolate issues early.

With `pytest`, for example, you can run tests and get detailed failure reports,
which help identify issues. In combination with `pytest`’s `--pdb` flag, you can
drop into the debugger whenever a test fails.

#### Example with `pytest`:

```python
# test_math.py
import pytest

def divide(a, b):
    return a / b

def test_divide():
    assert divide(10, 2) == 5
    assert divide(10, 0) == None  # This will fail, allowing debugging

# Run pytest with --pdb to start debugging when the test fails
# $ pytest --pdb test_math.py
```

### 8. **Tracing Code Execution with `trace` Module**

Python’s `trace` module lets you trace the execution of a program, printing each
line of code as it's executed. This is useful for understanding the flow of
execution.

#### Example:

```bash
python -m trace --trace your_script.py
```

This command will print each line of code that is executed along with function
calls, making it easier to see where things might be going wrong.

### Conclusion

The best debugging method in Python depends on the complexity of your project
and personal preferences. Here's a quick summary:

- **Print Statements**: For simple, quick fixes.
- **`pdb`/`ipdb`**: For interactive debugging in the terminal.
- **IDE Debuggers (PyCharm, VS Code)**: For a powerful, GUI-driven debugging experience.
- **`debugpy`**: For remote debugging in distributed systems.
- **Logging**: For persistent debugging in production environments.
- **Unit Testing (`pytest`)**: For test-driven debugging and validation.
- **`trace` Module**: For detailed execution tracing.

Each of these tools has its place, and often the best approach is to use a
combination of them depending on the situation.
