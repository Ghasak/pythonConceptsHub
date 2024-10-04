# Logging in Python

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->

**Table of Contents**

- [Logging in Python](#logging-in-python)
  - [Basics Logging](#basics-logging)
    - [Key Aspects of Modern Logging in Python](#key-aspects-of-modern-logging-in-python)
    - [Python Logging Flow](#python-logging-flow)
    - [Logging Formatter Options](#logging-formatter-options)
    - [Advanced Logging Features](#advanced-logging-features)
    - [Best Practices](#best-practices)
    - [What is a Handler in Python Logging?](#what-is-a-handler-in-python-logging)
    - [Why is a Handler Used?](#why-is-a-handler-used)
    - [Types of Handlers in Python](#types-of-handlers-in-python)
    - [What is a StreamHandler?](#what-is-a-streamhandler)
      - [Why Use `StreamHandler`?](#why-use-streamhandler)
    - [Example of Using `StreamHandler`](#example-of-using-streamhandler)
    - [Output in the Console:](#output-in-the-console)
    - [Conclusion](#conclusion)
  - [Q1: More about streamhandler](#q1-more-about-streamhandler)
    - [Key Differences and Benefits](#key-differences-and-benefits)
      - [1. **Separation of Concerns**](#1-separation-of-concerns)
      - [2. **Configurable Log Levels**](#2-configurable-log-levels)
      - [3. **Centralized Logging Configuration**](#3-centralized-logging-configuration)
      - [4. **Log Formatting**](#4-log-formatting)
      - [5. **Multiple Handlers and Output Destinations**](#5-multiple-handlers-and-output-destinations)
      - [6. **Thread-Safety and Performance**](#6-thread-safety-and-performance)
      - [7. **Log Propagation**](#7-log-propagation)
    - [Why Choose `StreamHandler` Over `sys.stdout`?](#why-choose-streamhandler-over-sysstdout)
    - [Example of Centralized Logging](#example-of-centralized-logging)
    - [Conclusion](#conclusion-1)
  - [Q1: More about benefits of Streamhandler](#q1-more-about-benefits-of-streamhandler)
    - [Scenario:](#scenario)
    - [Why `StreamHandler` is Better than `sys.stdout`:](#why-streamhandler-is-better-than-sysstdout)
    - [Example Code: Using `StreamHandler` and File Logging](#example-code-using-streamhandler-and-file-logging)
    - [What Happens Here:](#what-happens-here)
    - [Output:](#output)
    - [Why Using `StreamHandler` is Better in This Case:](#why-using-streamhandler-is-better-in-this-case)
    - [Conclusion:](#conclusion)
  - [Advanced Logging](#advanced-logging)

<!-- markdown-toc end -->

## Common Practices 



## Basics Logging

Modern logging in Python using the `logging` module is powerful, allowing for
comprehensive control over log formatting, handlers, log levels, and more. I'll
explain the key aspects of logging, along with the various bells and whistles
you can utilize.

### Key Aspects of Modern Logging in Python

1. **Loggers**: The core interface of the logging system. You can configure
   multiple loggers for different parts of your application.

   - `logger = logging.getLogger(__name__)` retrieves or creates a logger.

2. **Handlers**: Direct where the logs go, such as the console, files, or
   external systems.

   - Common handlers: `StreamHandler`, `FileHandler`, `RotatingFileHandler`,
     `TimedRotatingFileHandler`, `SMTPHandler`, `HTTPHandler`.

3. **Formatters**: Specify the layout of log messages.

   - You can include information like the time, log level, logger name, and more
     using format strings.

4. **Log Levels**: Different severity levels for logging messages. The standard
   levels are:

   - `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
   - You can also define custom levels.

5. **Configuration**: Logging can be configured using Python code or using
   configuration files in INI or JSON format.

6. **Filters**: Filters allow for fine-grained control over which log records to
   output.

7. **Asynchronous Logging**: For high-performance applications, you can
   configure logging to be asynchronous, using queue-based logging.

---

### Python Logging Flow

```python
import logging

# Step 1: Create or get a logger
logger = logging.getLogger(__name__)

# Step 2: Set log level (default is WARNING)
logger.setLevel(logging.DEBUG)

# Step 3: Create handlers (console, file, etc.)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('app.log')

# Step 4: Create formatters and add them to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Step 5: Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Example usage
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is critical')
```

---

### Logging Formatter Options

Below is a table showing all the available format types from the Python logging documentation:

| Format Symbol         | Description                                                                  |
| --------------------- | ---------------------------------------------------------------------------- |
| `%(asctime)s`         | The time the LogRecord was created. Format: `2003-07-08 16:49:45,896`.       |
| `%(created)f`         | Time when the LogRecord was created (float, seconds since the epoch).        |
| `%(relativeCreated)d` | Time in milliseconds since the logger was created until the log was emitted. |
| `%(msecs)d`           | Millisecond portion of the time when the LogRecord was created.              |
| `%(levelname)s`       | Text logging level (e.g., `DEBUG`, `INFO`).                                  |
| `%(levelno)s`         | Numeric logging level (e.g., `10` for `DEBUG`).                              |
| `%(message)s`         | The message passed in the logging call (or the result of `msg % args`).      |
| `%(name)s`            | The name of the logger (usually the module name).                            |
| `%(pathname)s`        | Full path of the source file where the log call was made.                    |
| `%(filename)s`        | The file name of the source file where the log call was made.                |
| `%(module)s`          | Module name of the source file.                                              |
| `%(funcName)s`        | Name of the function where the log call was made.                            |
| `%(lineno)d`          | Line number in the source file where the log call was made.                  |
| `%(thread)d`          | Thread ID where the log call was made.                                       |
| `%(threadName)s`      | Thread name where the log call was made.                                     |
| `%(process)d`         | Process ID where the log call was made.                                      |
| `%(processName)s`     | Process name where the log call was made.                                    |
| `%(stack_info)s`      | Stack trace information (if available).                                      |
| `%(exc_info)s`        | Exception information if `exc_info=True` is passed in the logging call.      |

---

### Advanced Logging Features

1. **Rotating Logs**: Useful for handling large logs by rotating log files when they reach a specific size.

   ```python
   from logging.handlers import RotatingFileHandler

   handler = RotatingFileHandler('app.log', maxBytes=2000, backupCount=5)
   ```

2. **Timed Rotation**: Logs rotate based on time (e.g., daily logs).

   ```python
   from logging.handlers import TimedRotatingFileHandler

   handler = TimedRotatingFileHandler('app.log', when='midnight', interval=1, backupCount=7)
   ```

3. **Logging to External Systems**:

   - **SMTPHandler**: Send logs via email.
   - **HTTPHandler**: Send logs to a web server.

4. **Configuring with Dictionaries**:
   You can also configure logging using dictionaries or external configuration files.

   Example of dict-based configuration:

   ```python
   import logging.config

   config = {
       'version': 1,
       'handlers': {
           'console': {
               'class': 'logging.StreamHandler',
               'level': 'DEBUG',
               'formatter': 'default',
           }
       },
       'formatters': {
           'default': {
               'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
           }
       },
       'loggers': {
           '': {  # root logger
               'handlers': ['console'],
               'level': 'DEBUG',
           },
       },
   }

   logging.config.dictConfig(config)
   logger = logging.getLogger(__name__)
   ```

---

### Best Practices

1. **Use different log levels** for different environments (e.g., `DEBUG` for development, `INFO` for production).
2. **Avoid excessive logging** to avoid performance overhead in high-traffic environments.
3. **Use contextual information** (like thread, process IDs) when dealing with multi-threaded or multi-process applications.
4. **Log asynchronously** when performance matters, especially in multi-threaded or multi-process applications (e.g., using `QueueHandler`).
5. **Secure your logging setup** if you're logging sensitive information, e.g., use secure transports for logging to external systems.

By using these modern logging features, you can create flexible, scalable, and efficient logging mechanisms in Python.

### What is a Handler in Python Logging?

In Python's `logging` module, a **handler** is responsible for directing the log
records (messages) to a particular destination. You can think of a handler as
the output channel for logs. It takes the log records generated by the logger
and outputs them to a specific destination, such as:

- Console/terminal (standard output)
- Files (log files)
- External systems (e.g., email, HTTP requests)
- Other destinations (e.g., memory buffers, queues)

### Why is a Handler Used?

Handlers provide **flexibility** in logging by allowing you to:

1. **Direct logs to multiple destinations**: For instance, you might want logs
   to go to both the console and a file at the same time.
2. **Filter logs**: Handlers can filter log records based on log level or other
   criteria, enabling more granular control over what gets logged where.
3. **Apply different formatting**: Different handlers can apply different
   formatters to the logs they process, ensuring that the logs appear with
   different formats depending on their destination.
4. **Manage log rotation**: Specialized handlers, such as `RotatingFileHandler`
   or `TimedRotatingFileHandler`, manage large logs by rotating them at specific
   file sizes or time intervals.

Without handlers, logs would have a single, rigid destination (e.g., only
printed to the console or stored in one log file), limiting how you handle
different log levels, formats, and destinations in a scalable way.

### Types of Handlers in Python

Python provides several built-in handlers:

- `StreamHandler`: Sends log output to streams such as `sys.stdout`, `sys.stderr`, or other file-like objects.
- `FileHandler`: Writes log records to a disk file.
- `RotatingFileHandler`: Writes to log files and manages rotation based on file size.
- `TimedRotatingFileHandler`: Rotates log files based on time intervals.
- `NullHandler`: A no-op handler that discards all log messages, commonly used in libraries.
- `HTTPHandler`: Sends log records to a web server via HTTP.
- `SMTPHandler`: Sends log records via email.
- `QueueHandler`: Sends log records to a queue (for asynchronous logging).

### What is a StreamHandler?

The `StreamHandler` is one of the most commonly used handlers in Python logging. It outputs log messages to a **stream**. A stream can be:

- `sys.stdout` (the default standard output where logs are usually printed)
- `sys.stderr` (standard error output, commonly used for error logs)
- Any other file-like object that behaves like a stream

#### Why Use `StreamHandler`?

- **Console logging**: It is typically used to display log messages in the
  console or terminal during the execution of a program.
- **Real-time monitoring**: If you need to see the logs as they happen (e.g.,
  for debugging), `StreamHandler` is the go-to solution because it outputs
  immediately to the terminal or another stream.
- **Quick setup**: Since most programs need some level of console output for
  logs, `StreamHandler` is the simplest and quickest way to set up logging.

### Example of Using `StreamHandler`

Here's a basic example that demonstrates how to use a `StreamHandler` to output logs to the console:

```python
import logging

# Step 1: Create or get a logger
logger = logging.getLogger('my_logger')

# Step 2: Set log level
logger.setLevel(logging.DEBUG)

# Step 3: Create a StreamHandler
stream_handler = logging.StreamHandler()

# Step 4: Optionally, create and set a formatter for the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)

# Step 5: Add the StreamHandler to the logger
logger.addHandler(stream_handler)

# Example log messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```

### Output in the Console:

```
2024-10-02 13:34:56,789 - my_logger - DEBUG - This is a debug message
2024-10-02 13:34:56,790 - my_logger - INFO - This is an info message
2024-10-02 13:34:56,790 - my_logger - WARNING - This is a warning message
2024-10-02 13:34:56,790 - my_logger - ERROR - This is an error message
2024-10-02 13:34:56,790 - my_logger - CRITICAL - This is a critical message
```

In this example:

- **`StreamHandler`** directs the logs to the console (by default, it sends logs
  to `sys.stdout`).
- **Formatter** specifies the format of the log message, including the time,
  logger name, log level, and the actual log message.
- **Logger** is responsible for managing the overall logging process and calling
  the handlers to output the logs.

### Conclusion

A `StreamHandler` is useful for sending log output to the console or any other
file-like stream, making it ideal for real-time monitoring and debugging.
Handlers in general allow flexible and configurable management of log
destinations, letting you direct different types of logs to various outputs.

## Q1: More about streamhandler

Sending logs to the **console** via `StreamHandler` vs directly using
`sys.stdout` or `sys.stderr` is about flexibility and control, not necessarily
performance. Let's break down the differences and explain why logging via a
`StreamHandler` is often preferred.

### Key Differences and Benefits

#### 1. **Separation of Concerns**

- **`StreamHandler`:** The logging system with a `StreamHandler` abstracts away
  the output destination, allowing you to change it easily (console, file, etc.)
  without modifying the core application logic.
- **`sys.stdout`:** If you print directly to `sys.stdout`, you are tightly
  coupling your output with the specific behavior of standard output. Changing
  where the output goes later becomes more difficult.

**Benefit:** Using a `StreamHandler` allows your log output to be flexible. You
can easily configure where the logs go, which can be particularly useful in
production systems where you may want to send logs to multiple destinations.

#### 2. **Configurable Log Levels**

- **`StreamHandler`:** You can define log levels (`DEBUG`, `INFO`, `WARNING`,
  `ERROR`, `CRITICAL`) and control which messages get output. For example, in a
  development environment, you might want `DEBUG` messages, but in production,
  you might only want `ERROR` and `CRITICAL` messages to appear.
- **`sys.stdout`:** If you print to `sys.stdout`, you don't have the ability to
  filter logs based on severity. Every log message will be output regardless of
  its importance.

**Benefit:** With `StreamHandler`, you can control log verbosity easily, making
the logging system more dynamic and adaptable based on the environment or
configuration.

#### 3. **Centralized Logging Configuration**

- **`StreamHandler`:** The `logging` module allows you to manage and configure
  multiple handlers, formatters, and loggers in a central location. You can
  define different handlers for different loggers and customize them for various
  parts of your application.
- **`sys.stdout`:** If you write directly to `sys.stdout`, you miss out on this
  centralized configuration. Each part of your code that wants to log something
  would have to handle its own output configuration manually.

**Benefit:** A logging system with handlers allows centralized control over all
logging behavior. This ensures consistent logging across the entire application,
with no need to modify each function that outputs logs individually.

#### 4. **Log Formatting**

- **`StreamHandler`:** The `StreamHandler` can apply formatting to log messages,
  such as adding timestamps, log levels, function names, line numbers, and more.
- **`sys.stdout`:** Direct printing to `sys.stdout` doesn't provide any built-in
  mechanism for formatting the log messages, so you'd have to manually format
  each print statement.

**Benefit:** With `StreamHandler`, you can define a `Formatter` that
automatically formats log messages, making them easier to read and more
informative.

#### 5. **Multiple Handlers and Output Destinations**

- **`StreamHandler`:** You can add multiple handlers to a logger, meaning that
  you can send logs to both the console (or `sys.stdout`) and other
  destinations, like files, external systems, etc., **simultaneously**.
- **`sys.stdout`:** If you print directly to `sys.stdout`, you're restricted to
  just that output. To output to multiple destinations, you'd have to manually
  implement that logic.

**Benefit:** The logging system allows you to route the same log messages to
multiple destinations in an organized and flexible way, without changing the
core code.

#### 6. **Thread-Safety and Performance**

- **`StreamHandler`:** The logging module is thread-safe by default, meaning
  multiple threads can log messages without conflicting with each other. While
  performance may not differ significantly, logging modules and handlers are
  optimized for safe concurrent logging.
- **`sys.stdout`:** Direct use of `sys.stdout` in a multi-threaded environment
  can lead to issues where log lines from different threads are interleaved or
  lost.

**Benefit:** Using `StreamHandler` ensures your logging system is safe to use in
multi-threaded or multi-process environments, reducing the risk of corrupt or
incomplete logs.

#### 7. **Log Propagation**

- **`StreamHandler`:** The logging system allows for log propagation. Loggers
  can pass log records to parent loggers, which can then pass them to their
  handlers. This means a child logger's messages can be caught and handled by a
  more general logger.
- **`sys.stdout`:** When printing directly to `sys.stdout`, there is no
  propagation of log records. Each message is an isolated event, and you would
  need to manually manage complex output flows.

**Benefit:** With `StreamHandler`, logs can propagate up to higher-level
loggers, giving you a more hierarchical and flexible logging structure.

### Why Choose `StreamHandler` Over `sys.stdout`?

- **Flexibility and Extensibility:** Using a `StreamHandler` gives you
  flexibility to later change or extend the output behavior. You might start by
  sending logs to the console but later decide to send logs to a file or
  external system (e.g., email alerts for critical errors).
- **Centralized Control:** You can configure all logging behavior in one place,
  applying different configurations (levels, formatters, filters) depending on
  the environment or requirements.
- **Cleaner Code:** Rather than cluttering your code with direct `print()`
  statements or calls to `sys.stdout`, you keep logging concerns separate from
  business logic. This makes your code easier to maintain and more modular.

- **Consistency and Scalability:** Using handlers ensures that log output
  remains consistent and scalable across different parts of your application, no
  matter where or how deep the log messages originate.

### Example of Centralized Logging

```python
import logging

# Centralized logger
logger = logging.getLogger('my_app')
logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# File handler
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.ERROR)  # Only log errors and above to file
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Log messages
logger.debug('This is a debug message')   # Goes to console only
logger.error('This is an error message')  # Goes to both console and file
```

In this example:

- Logs at all levels (`DEBUG`, `INFO`, etc.) go to the console.
- Only `ERROR` and `CRITICAL` logs are written to a file.
- This demonstrates the **flexibility** and **centralized control** that the
  `logging` module provides over simply printing to `sys.stdout`.

### Conclusion

Using a `StreamHandler` within Python's logging framework offers substantial
benefits over directly printing to `sys.stdout`. It provides **flexibility**,
**control**, and **configurability** for managing log output, enabling you to
manage complex logging requirements such as log formatting, filtering, and
multi-destination logging, all while keeping your code cleaner and easier to
maintain.

## Q1: More about benefits of Streamhandler

Let's look at a practical example where using `StreamHandler` in Python's
logging system is more beneficial than directly sending output to `sys.stdout`.
This scenario involves logging messages for both console and file output, with
different log levels and formatting.

### Scenario:

You have a Python application that runs in both **development** and
**production** environments. In development, you want to see detailed debug
messages printed to the console (`sys.stdout`), but in production, you want only
warnings and errors logged, and they should be logged both to the console and to
a file for future reference.

### Why `StreamHandler` is Better than `sys.stdout`:

- In production, you might want to log only warnings and errors to avoid
  cluttering the console with less critical information.
- You also want to simultaneously log these messages to a file, which requires
  additional flexibility.
- Directly printing to `sys.stdout` would not allow you to manage multiple log
  levels or easily change the log destination (console and file).

### Example Code: Using `StreamHandler` and File Logging

```python
import logging

# Step 1: Create or get a logger
logger = logging.getLogger('my_app')
logger.setLevel(logging.DEBUG)  # Log everything (DEBUG level and above)

# Step 2: Create a console handler (StreamHandler)
console_handler = logging.StreamHandler()  # Outputs to sys.stdout by default
console_handler.setLevel(logging.DEBUG)    # Log all levels to console (DEBUG and above)

# Step 3: Create a file handler
file_handler = logging.FileHandler('app.log')  # Outputs to a file
file_handler.setLevel(logging.WARNING)         # Only log WARNING and above to file

# Step 4: Create formatters and set them for both handlers
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

console_handler.setFormatter(console_formatter)
file_handler.setFormatter(file_formatter)

# Step 5: Add both handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Example log messages
logger.debug("This is a DEBUG message - only in console (for development)")
logger.info("This is an INFO message - only in console (for development)")
logger.warning("This is a WARNING message - both console and file")
logger.error("This is an ERROR message - both console and file")
logger.critical("This is a CRITICAL message - both console and file")
```

### What Happens Here:

1. **Development Logs (Console)**

   - All log messages, including `DEBUG`, `INFO`, `WARNING`, `ERROR`, and
     `CRITICAL`, are printed to the console via the `StreamHandler` because we
     set the console log level to `DEBUG`.

2. **Production Logs (File)**

   - Only `WARNING` and above messages (`WARNING`, `ERROR`, `CRITICAL`) are
     written to the `app.log` file because the file handler's log level is set
     to `WARNING`.

3. **Formatter Customization**
   - Console log messages include the logger name and detailed information
     (`%(asctime)s - %(name)s - %(levelname)s - %(message)s`).
   - File log messages have a simpler format (`%(asctime)s - %(levelname)s - %(message)s`), excluding the logger name.

### Output:

**Console (Development Environment):**

```
2024-10-02 14:10:22,123 - my_app - DEBUG - This is a DEBUG message - only in console (for development)
2024-10-02 14:10:22,124 - my_app - INFO - This is an INFO message - only in console (for development)
2024-10-02 14:10:22,125 - my_app - WARNING - This is a WARNING message - both console and file
2024-10-02 14:10:22,126 - my_app - ERROR - This is an ERROR message - both console and file
2024-10-02 14:10:22,127 - my_app - CRITICAL - This is a CRITICAL message - both console and file
```

**File (`app.log`) (Production Environment):**

```
2024-10-02 14:10:22,125 - WARNING - This is a WARNING message - both console and file
2024-10-02 14:10:22,126 - ERROR - This is an ERROR message - both console and file
2024-10-02 14:10:22,127 - CRITICAL - This is a CRITICAL message - both console and file
```

### Why Using `StreamHandler` is Better in This Case:

1. **Multiple Output Destinations:**
   - We are logging to both the console (via `StreamHandler`) and a file (via
     `FileHandler`) simultaneously with different log levels, which wouldn't be
     possible if you simply used `sys.stdout` for console output.
2. **Log Level Filtering:**

   - You can easily filter which messages go to which destination (e.g., all
     messages to the console but only warnings and errors to the file). If you
     used `sys.stdout`, you wouldn't have the built-in filtering of messages by
     log level.

3. **Flexible Configuration:**

   - Handlers allow us to modify the logging behavior for each environment
     without changing the core logging logic. For instance, in production, you
     might switch to a different log file or suppress debug messages. This is
     not as easy when using direct `sys.stdout` output.

4. **Formatted Output:**

   - Using `StreamHandler`, we can apply a custom format for the logs, including
     timestamps and log levels. With `sys.stdout`, you would have to manually
     create these formats for every log statement, leading to redundant code.

5. **Cleaner and Scalable Code:**
   - The logging framework with handlers provides a more scalable and cleaner
     approach to logging. If you decide to add more destinations (e.g., logging
     to a remote server or sending critical logs via email), you can easily do
     so by adding new handlers.

### Conclusion:

In this example, using `StreamHandler` offers much more flexibility, control,
and configurability than simply printing logs to `sys.stdout`. It enables
multiple output destinations, filtering by log levels, customizable formatting,
and overall a more maintainable logging system—features critical in larger and
more complex applications.

## Advanced Logging - Logger Root vs Specific

In Python’s `logging` module, the **root logger** and **specific loggers** are
critical concepts for organizing your logging infrastructure. Using specific
loggers instead of the root logger provides better control, modularity, and
flexibility, especially in larger applications.

### Root Logger vs. Specific Logger

#### **Root Logger:**

The **root logger** is the default logger provided by Python's `logging` module.
If you don’t explicitly create a logger, the root logger is used. This logger is
a global logger, which means all logging calls without a specific logger
reference will be handled by the root logger.

#### **Specific Logger:**

A **specific logger** is any logger created with a custom name using
`logging.getLogger(name)`. These loggers are hierarchically organized and allow
you to separate logging behavior for different parts of your application,
libraries, or modules.

### Benefits of Using Specific Loggers Over the Root Logger

1. **Modularity and Separation of Concerns:**

   - Specific loggers allow different parts of your application to log messages
     independently. This enables separate configuration for different modules,
     making the code cleaner and more maintainable.
   - Example: `auth_logger`, `db_logger`, `api_logger`, etc.

2. **Fine-Grained Control:**

   - With specific loggers, you can configure log levels, handlers, and formats
     for different loggers. This provides more control over what gets logged and
     where.
   - You can log `DEBUG` messages in one part of your application (e.g.,
     `database` module) while logging only `ERROR` messages in another (e.g.,
     `api` module).

3. **Log Hierarchy:**

   - Specific loggers follow a hierarchical structure. Loggers have a
     parent-child relationship, allowing log messages to propagate up the
     hierarchy. This means you can apply configurations to a parent logger that
     will be inherited by its children.

4. **Avoid Global Configuration:**

   - Relying on the root logger can result in conflicts and unintended behavior,
     especially when integrating third-party libraries that also use logging.
     Using specific loggers avoids these issues.

5. **Multiple Logging Configurations:**
   - With specific loggers, you can define multiple handlers (console, file,
     etc.) and formatters for different parts of the application, making your
     logging infrastructure more versatile.

---

### Common Syntax for Root Logger and Specific Logger

#### Using the Root Logger:

The root logger is created automatically when you use `logging.basicConfig()`. Here's how to use it:

```python
import logging

# Configure the root logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Log messages using the root logger
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
```

#### Using Specific Logger:

You can create a specific logger for different modules or parts of your application:

```python
import logging

# Create a logger for the 'database' module
db_logger = logging.getLogger('database')
db_logger.setLevel(logging.DEBUG)

# Create a logger for the 'api' module
api_logger = logging.getLogger('api')
api_logger.setLevel(logging.WARNING)

# Create a console handler and set the format
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to both loggers
db_logger.addHandler(console_handler)
api_logger.addHandler(console_handler)

# Log messages using the specific loggers
db_logger.debug('This is a debug message from the database module')
db_logger.info('This is an info message from the database module')
api_logger.warning('This is a warning message from the api module')
api_logger.error('This is an error message from the api module')
```

### Output:

```
2024-10-02 14:20:56,789 - database - DEBUG - This is a debug message from the database module
2024-10-02 14:20:56,790 - database - INFO - This is an info message from the database module
2024-10-02 14:20:56,791 - api - WARNING - This is a warning message from the api module
2024-10-02 14:20:56,792 - api - ERROR - This is an error message from the api module
```

---

### Logger Hierarchy

Loggers are hierarchical. For instance, a logger named `app.database` is
considered a child of the logger `app`. Log messages propagate up this hierarchy
unless explicitly stopped.

#### Example of Logger Hierarchy:

```python
import logging

# Parent logger (app)
app_logger = logging.getLogger('app')
app_logger.setLevel(logging.DEBUG)

# Child logger (app.database)
db_logger = logging.getLogger('app.database')

# Create a handler for app logger
app_handler = logging.StreamHandler()
app_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
app_handler.setFormatter(app_formatter)
app_logger.addHandler(app_handler)

# Log messages from both app and app.database
app_logger.debug('This is a debug message from the app')
db_logger.info('This is an info message from the app.database')
```

### Output:

```
2024-10-02 14:30:22,123 - app - DEBUG - This is a debug message from the app
2024-10-02 14:30:22,124 - app.database - INFO - This is an info message from the app.database
```

Here, `db_logger` inherits the handler from `app_logger` because `app.database` is a child of `app`.

---

### Preventing Log Propagation

By default, log messages propagate up to the root logger. You can stop this by
setting `propagate = False` on a specific logger.

#### Example:

```python
import logging

# Parent logger
app_logger = logging.getLogger('app')
app_logger.setLevel(logging.DEBUG)

# Child logger (app.database) that does not propagate logs to the parent
db_logger = logging.getLogger('app.database')
db_logger.propagate = False  # Prevent log propagation

# Handler for the parent logger
app_handler = logging.StreamHandler()
app_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
app_handler.setFormatter(app_formatter)
app_logger.addHandler(app_handler)

# Handler for the child logger
db_handler = logging.StreamHandler()
db_formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
db_handler.setFormatter(db_formatter)
db_logger.addHandler(db_handler)

# Log messages from both loggers
app_logger.debug('This is a debug message from the app')
db_logger.info('This is an info message from the app.database')
```

### Output:

```
2024-10-02 14:35:22,123 - app - DEBUG - This is a debug message from the app
app.database - This is an info message from the app.database
```

Here, the `db_logger` logs directly using its own handler without propagating to
the `app_logger`. This is useful when you want to prevent certain logs from
appearing in the parent loggers.

---

### Using Configuration Files for Loggers

You can configure logging using a configuration file (e.g., INI, JSON, YAML) for
more complex applications. This separates logging configuration from the code,
making it easier to manage and modify.

#### Example INI Configuration (`logging.conf`):

```ini
[loggers]
keys=root,app,app.database

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=defaultFormatter

[logger_root]
level=WARNING
handlers=consoleHandler

[logger_app]
level=DEBUG
handlers=consoleHandler
qualname=app

[logger_app.database]
level=INFO
handlers=fileHandler
qualname=app.database
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=defaultFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=INFO
formatter=defaultFormatter
args=('app.log', 'a')

[formatter_defaultFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

#### Loading the Configuration:

```python
import logging
import logging.config

logging.config.fileConfig('logging.conf')

# Get loggers
app_logger = logging.getLogger('app')
db_logger = logging.getLogger('app.database')

# Log messages
app_logger.debug('This is a debug message from the app')
db_logger.info('This is an info message from the app.database')
```

---

### Key Takeaways

1. **Root Logger**:

   - Quick setup using `logging.basicConfig()`.
   - Global logger used by default if no specific logger is created.
   - Limited control in larger applications.

2. **Specific Logger**:

   - Modular logging for different components of an application.
   - Allows hierarchical organization and log message propagation.
   - Provides fine-grained control over log levels, handlers, and formatting.
   - Prevents conflicts with third-party libraries that use the root logger.

3. **Logger Hierarchy**:

   - Loggers inherit handlers and configurations from parent loggers.
   - Propagation can be controlled to allow or prevent messages from being passed up the hierarchy.

4. **Configuration Flexibility**:
   - You can configure loggers programmatically or via configuration files.
   - Centralized control of logging behavior helps to separate logging configuration from application logic

## References

- [x] [log record attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes)
