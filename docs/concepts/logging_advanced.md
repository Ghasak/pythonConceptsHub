# Logging Advanced

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->

**Table of Contents**

- [Logging Advanced](#logging-advanced)
  - [01 Intro](#01-intro)
  - [1. Modern tip -1 Use dictConfig](#1-modern-tip--1-use-dictconfig)
    - [Diagram for logging frame](#diagram-for-logging-frame)
    - [Notes on logger tree](#notes-on-logger-tree)
  - [2. Modern Tip -2 Put all handlers/filters on the root](#2-modern-tip--2-put-all-handlersfilters-on-the-root)
  - [3. Modern tip -3 Don't use the root logger](#3-modern-tip--3-dont-use-the-root-logger)
  - [4. Modern tip -4 One Logger per major-subcomponet](#4-modern-tip--4-one-logger-per-major-subcomponet)
  - [Using dicConfig](#using-dicconfig)
  - [Example setup: everything to stdout](#example-setup-everything-to-stdout)
  - [5. Modern Tip -5 Store config in json or yaml file](#5-modern-tip--5-store-config-in-json-or-yaml-file)
    - [5.1 Using JSON](#51-using-json)
      - [5.5.1 JSON config file](#551-json-config-file)
      - [5.1.2 JSON file loader](#512-json-file-loader)
    - [5.2 Using Yaml](#52-using-yaml)
      - [5.2.1 Yaml file config](#521-yaml-file-config)
      - [5.2.2 Yaml config](#522-yaml-config)
  - [Reference](#reference)

<!-- markdown-toc end -->

## 01 Intro

The needs for a full understanding the logging in python given all the
necessary aspects on how to create a logging with the following features:

1. High Quality
2. Parsable
3. Multi-destination
4. Non-Blocking

## 1. Modern tip -1 Use dictConfig

For some reason, `dictConfig` is not prominently mentioned in the main logging
documents but rather hidden away in the logging.config submodule in Python. As
the name suggests, this allows you to configure logging through a dictionary
that explicitly lists all of the necessary components of your logging setup,
providing greater control and flexibility over your application's logging
behavior. It will allow us to configure namely the filters, formatters,
handlers, and loggers.

```python
import  logging.config

logger = logging.getLogger(__name__) # OR give it a name

logging_config = {
    "version":1,
    "disable_existing_loggers": False,
    "filters": {...},
    "handlers":{...} ,
    "loggers":{...} ,
}

```

### Diagram for logging frame

- Understanding the Python logger:
  - The following diagram represents the root logger.
  - Any logger you will create will be identical to the root logger unless you
    alter their components.
  - For example, the `A` logger will be exactly the same, and everything will
    be propagated to the parent logger in the tree of loggers.

```sh
                                     ┌──────────────────────────────────────────────┐
                         ┌──────┐    │                   LOGGER                     │
                         │.info │    │    ┌───────────────────────────────────┐     │
                         └──────┘    │    │        LEVEL: DEBUG/INFO/WARN/ ...│     │
                        ┌──────────┐ │    └───────────────────────────────────┘     │
                        │LOG RECORD│ │    ┌───────────────────────────────────┐     │
                        │ message  │ │    │        FILTER                     │     │
                        │ level    │ │    └───────────────────────────────────┘     │
                        │ created  │ │    ┌───────────────────────────────────┐     │
                        │ thread   │ │    │        ...                        │     │
                        │ ...      │ │    └───────────────────────────────────┘     │
                        └──────────┘ │ ┌────────────┐ ┌────────────┐ ┌────────────┐ │
                                     │ │  HANDLER   │ │  HANDLER   │ │  ........  │ │
                                     │ │┌──────────┐│ │┌──────────┐│ │┌──────────┐│ │
                                     │ ││  LEVEL   ││ ││  LEVEL   ││ ││  .....   ││ │
                                     │ │└──────────┘│ │└──────────┘│ │└──────────┘│ │
                                     │ │┌──────────┐│ │┌──────────┐│ │┌──────────┐│ │
                                     │ ││  FILTER  ││ ││  FILTER  ││ ││  ......  ││ │
                                     │ │└──────────┘│ │└──────────┘│ │└──────────┘│ │
                                     │ │┌──────────┐│ │┌──────────┐│ │┌──────────┐│ │
                                     │ ││  ...     ││ ││  ...     ││ ││  ......  ││ │
                                     │ │└──────────┘│ │└──────────┘│ │└──────────┘│ │
                                     │ │┌──────────┐│ │┌──────────┐│ │┌──────────┐│ │
                                     │ ││ FORMATTER││ ││ FORMATTER││ ││ .......  ││ │
                                     │ │└──────────┘│ │└──────────┘│ │└──────────┘│ │
                                     │ └─────┬──────┘ └─────┬──────┘ └─────┬──────┘ │
                                     └───────┼──────────────┼──────────────┼────────┘
┌──────────────────────────────────┐         │              │              │
│{"message": "THE ACTUAL MESSAGE"}`│         │              │              │
│INFO: THE ACTUAL MESSAGE`         │         │              │              │
└──────────────────────────────────┘         ▼              ▼              ▼
                                       ┌─────────┐    ┌─────────┐    ┌─────────┐
                                       │ STDOUT  │    │  FILE   │    │  EMAIL  │
                                       └─────────┘    └─────────┘    └─────────┘
```

### Notes on logger tree

1. The log record will be passed to each `handler` which has all information for
   the logger.
2. Each `handler` will recieve the `log record` and can alter the message along
   the way.
3. If a record dropped by a `handler` it is still passed to other `handlers`,
   but if its dropped by the logger itself, then it dropped for good.

4. The `log record` is a python object which the `handler` has a `formatter` to
   convert it to a `string`.

5. The formatter is what lets you customize what an individual message looks
   like.
6. The mental image above is for the `root` logger, as in the root of the tree
   of loggers (the root of the tree of loggers).
   - Loggers can be named by dots then you end up with tree of loggers.
   - `A.x` logger is a child of `A` logger which is a child of `root` logger as shown below:

```sh

             ┌─────────────┐
      ┌──────┤ root logger │───────────────┐
      │      └─────────────┘               │
      ▼                                    ▼
┌─────────┐                           ┌───────────┐
│logger A │                           │  logger B │
└─────┬───┘                           └───────────┘
      ▼
┌──────────┐
│logger A.x│
└──────────┘

```

7. The `log record` will be a python object which will run and propagate to the
   `logger A` then to the `Root` logger.

   - It would prepoagate up to the root and al of the roots handlers would run

8. This is done to make it easier for users to disable messages from while
   subsystems, just by disabling certian loggers.
9. Once again, if a record is dropped by a handler it will continue moving on,
   to include propagating up to the parent. But, if it's dropped by a logger, then
   it stops and doesn't propagate.

## 2. Modern Tip -2 Put all handlers/filters on the root

Put all handlers on the root logger. That any messages generated by
third-party libraries get logged and formatted as the same way as messages
generated by your won application.

## 3. Modern tip -3 Don't use the root logger

Using any top level logging function like `info`, `debug` such as

```python
logging.info("uses root logger") # BAD dont do that
```

- Instead, use your own logger (the one that has no formatter, filters,
  logging, handlers ...), and keep these up to the root to control them all. As
  we stated, We're depending on propgatio to send all events up to the root
  logger.

- If you have a small to medium-sized application, a single non-root logger is
  all you need.
- If you have a very large application then, you should make one non-root
  logger for each major subcomponent of your application.

## 4. Modern tip -4 One Logger per major-subcomponet

- Don't get Logger(`__name__`) in every file, because these are globals that
  live for the entire life of the program.

## Using dicConfig

```python

import logging.config
logger = loggng.getLogger("__name__")
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {},
    "handlers": {},
    "loggers": {},
}


def main():
    logging.cofnig.dictConfig(config= logging_config)
    logger.addHandler(logging.StreamHandler(...))
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")

```

## Example setup: everything to stdout

Use the following digram to understand that we will create a logger to `stdout`.

```sh
logging_config = {
    "version":1,                                             ┌──────────────────────┐
    "disable_existing_loggers":False,                        │   LOGGER "ROOT"      │
    "filters":1,                                             └──────────────────────┘
    "formatters":{                                           ┌──────────────────────┐
        "simple":{                                           │   level: DEBUG       │
            "format": "%(levelname)s: %(message)s"           ├──────────────────────┤
        }                                                    │   HANDLER "STDOUT"   │
    },                                                       ├──────────────────────┤
    "handlers":{                                             │   Formatter: "Simple"│
        "stdout":{                                           ├──────────────────────┤
            "class": "logging.StreamHandler",                │   level : msg        │ ◀──┐
            "formatter": "simple",                           └──────────┬───────────┘    │
            "strea":"ext://sys.stdout",                                 ▼                │
        }                                                          ┌────────┐       ┌────┴─────┐
    },                                                             │ STDOUT │       │PROPAGATE!│
    "loggers":{                                                    └────────┘       └──────────┘
        "root": {"level": "DEBUG", "handlers": ["stdout"]}                               ▲
    },                                                         ┌─────────────────┐       │
}                                                              │ LOGGER "MY_APP" ├───────┘
                                                               └─────────────────┘
```

- `version` : To maintain compatibility,
- `disable_existing_loggers`: It disalbesanything that's not explicitly listed in this config.
- `filters` : No filter for now in the root logger.
- `formatters` : What we will display in the message from the `logging record object`.
- `handlers` : to print the message on `stdout`.

## 5. Modern Tip -5 Store config in json or yaml file

### 5.1 Using JSON

#### 5.5.1 JSON config file

- We can use the `JSON` module to load the configurations outside the python moduler

```json
{
  "version": 1,
  "disable_existing_loggers": false,
  "formatters": {
    "simple": {
      "format": "%(asctime)s:%(filename)s:%(funcName)s: %(lineno)d: %(levelname)s: %(message)s"
    }
  },

  "handlers": {
    "stdout": {
      "class": "logging.StreamHandler",
      "formatter": "simple",
      "stream": "ext://sys.stdout"
    }
  },
  "loggers": {
    "root": {
      "level": "DEBUG",
      "handlers": ["stdout"]
    }
  }
}
```

#### 5.1.2 JSON file loader

```python
import json
import logging.config
import logging.handlers
import pathlib

logger = logging.getlogger("my_app")

def setup_logging():
    config_file = pathlib.Path("logging_configs/config.json")
    with open(config_file) as f_in:
        config = json.load(f_in)
    logging.config.dictConfig(config)

```

### 5.2 Using Yaml

For `yaml` file there is no native parser for it in python,
instead we rely on a dependency. `pyyaml` is a popular choice.

```sh
pip install pyyaml
```

#### 5.2.1 Yaml file config

- The config is stored as

```yml
version: 1
disable_existing_logger: false
formatters:
  simple:
    format: "%(levelname)s: %(message)s"
  handler:
    stdout:
      class: logging.StreamHandler
      formatter: simple
      stream: ext://sys.stdout
```

#### 5.2.2 Yaml config

- Then you can use the function here to load it

```python
import yaml
import logging.config
import logging.handlers
import pathlib


logger = logging.getlogger(__name__)

def setup_logging():
     config_file = pathlib.Path("logging_configs/config.json")
     with open(config_file) as f_in:
         config = yaml.safe_load(f_in)
     logging.config.dictConfig(config)

```

## Example Setup - Errors to STDERR - All to FILE

- We store all configurations in the `json` file similar to the one below

```json
{
  "version": 1,
  "disable_existing_loggers": false,
  "formatters": {
    "simple": {
      "format": "%(asctime)s:%(filename)s:%(funcName)s: %(lineno)d: %(levelname)s: %(message)s"
    }
  },
  "handlers": {
    "stdout": {
      "class": "logging.StreamHandler",
      "level": "DEBUG",
      "formatter": "simple",
      "stream": "ext://sys.stdout"
    },
    "stderr": {
      "class": "logging.StreamHandler",
      "level": "WARNING",
      "formatter": "simple",
      "stream": "ext://sys.stderr"
    },
    "file": {
      "class": "logging.handlers.RotatingFileHandler",
      "level": "DEBUG",
      "formatter": "simple",
      "filename": "src/logging/my_app.log",
      "maxBytes": 10000,
      "backupCount": 3
    }
  },
  "loggers": {
    "root": {
      "level": "DEBUG",
      "handlers": ["stdout", "file", "stderr"]
    }
  }
}
```

- We load the configurations similar to before.

```py
import json
import logging.config
import logging.handlers
import os

logger = logging.getLogger(__name__)


def setup_logging():
    config_file = os.path.join(os.getcwd(), "src/logging/config02.json")

    with open(config_file) as f_in:
        config = json.load(f_in)
    logging.config.dictConfig(config)


def testing_loading_config():
    setup_logging()
    for i in range(10):
        logger.info(f"this is just a test {i}")
        logger.warning(f"this is a warning test {i}")
        logger.error(f"this is an error test {i}")


if __name__ == "__main__":
    pass




```

- To visulaize the logger that we created we can see the diagram below:

```
  ┌──────────────────────────────────────────────┐
  │                LOGGER "ROOT"                 │
  │             ┌───────────────┐                │
  │             │ LEVEL DEBUG   │                │
  │             └───────────────┘                │
  │ ┌──────────────────┐   ┌────────────────┐    │
  │ │ HANDLER "STDERR" │   │ HANDLER "FILE" │    │
  │ └──────────────────┘   └────────────────┘    │
  │ ┌──────────────────┐   ┌────────────────┐    │
  │ │  LEVEL WARNING   │   │ LEVEL DEBUG    │    │
  │ └──────────────────┘   └────────────────┘    │
  │ ┌──────────────────┐   ┌──────────────────┐  │
  │ │FORMATTER "SIMPLE"│   │FORMATTER "SIMPLE"│  │
  │ └──────────────────┘   └──────────────────┘  │
  └──────────────────────────────────────────────┘
              │                       │
              ▼                       ▼
          ┌──────┐                ┌──────┐
          │STDERR│                │ FILE │
          └──────┘                └──────┘

```

## 7. Modern Tip -7 Store persistent logs in JSON Line file

There is a need for a better logging file formattng, as we need to explore the
file of the logging and filter it easily and isolate the `trace` and other
messages or a logging with two line messages.

- We can achieve this by creating our logging file as a `json` file , i.e.,
  each line is a json object that can be load easily line by line.

### 7.1 logging config

You will need to care about the following directorires:

1. `src.logging.MyColoredFormatter.MyColoredFormatter`: Here is the color scheme that we will use for the logging.
2. `src.logging.myCustomJsonClass01.MyJSONFormatter`: Here is the jsonline exporting using the file handler.
3. `src/logging/my_app.jsonl`: Here, we store the logging file.
4. `src.logging.myFilters.StdoutFilter1`: the filter for stdout.
5. `src.logging.myFilters.StderrFilter` : the filter for stderror

```json
{
  "version": 1,
  "disable_existing_loggers": false,
  "formatters": {
    "simple": {
      "format": "%(asctime)s:%(filename)s:%(funcName)s: %(lineno)d: %(levelname)s: %(message)s",
      "datefmt": "%Y-%m-%dT%H:%M:%S%z"
    },
    "colored": {
      "()": "src.logging.MyColoredFormatter.MyColoredFormatter",
      "format": "%(asctime)s: %(filename)s: %(funcName)s: L%(lineno)d: %(levelname)s: %(message)s",
      "datefmt": "%Y-%m-%dT%H:%M:%S%z"
    },
    "json": {
      "()": "src.logging.myCustomJsonClass01.MyJSONFormatter",
      "fmt_keys": {
        "level": "levelname",
        "message": "message",
        "timestamp": "timestamp",
        "logger": "name",
        "module": "module",
        "function": "funcName",
        "line": "lineno",
        "thread_name": "threadName"
      }
    }
  },
  "handlers": {
    "stdout": {
      "class": "logging.StreamHandler",
      "level": "DEBUG",
      "formatter": "colored",
      "stream": "ext://sys.stdout",
      "filters": ["stdout_filter"]
    },

    "stderr": {
      "class": "logging.StreamHandler",
      "level": "DEBUG",
      "formatter": "colored",
      "stream": "ext://sys.stderr",
      "filters": ["stderr_filter"]
    },
    "file": {
      "class": "logging.handlers.RotatingFileHandler",
      "level": "DEBUG",
      "formatter": "json",
      "filename": "src/logging/my_app.jsonl",
      "maxBytes": 10000,
      "backupCount": 3
    }
  },
  "filters": {
    "stdout_filter": {
      "()": "src.logging.myFilters.StdoutFilter1"
    },
    "stderr_filter": {
      "()": "src.logging.myFilters.StderrFilter"
    }
  },
  "loggers": {
    "root": {
      "level": "DEBUG",
      "handlers": ["stdout", "stderr", "file"]
    }
  }
}
```

It's completely normal and often quite practical to have separate handlers for
`stdout` and `stderr` in your logging configuration. Let me explain why this
setup is beneficial and what you gain from it.

### 7.2 **Why Separate Handlers for `stdout` and `stderr`?**

1. **Separation of Log Levels**:

   - The main reason to have separate handlers for `stdout` and `stderr` is to
     **separate log messages based on their severity**.
   - Generally, messages like `INFO` and `DEBUG` indicate normal operation,
     which can be redirected to `stdout`. These are messages that are
     informative, but not indicative of any problem.
   - On the other hand, messages like `WARNING`, `ERROR`, and `CRITICAL`
     indicate something problematic or unexpected, so it makes sense to redirect
     them to `stderr`.

2. **Improved Log Management**:

   - Separating `stdout` and `stderr` helps with **log management** and
     **troubleshooting**. This is particularly important when working with
     Unix-based systems or in the context of automation scripts, logging
     pipelines, or containerized environments.
   - For instance, if you're running a container or a script that outputs logs,
     `stdout` might be used to communicate regular progress, whereas `stderr` can
     be used to signal that an issue needs attention. This is helpful when
     redirecting output to different files or when filtering logs.

3. **Log Parsing and Monitoring Tools**:
   - **Log monitoring tools** and log parsers, such as `Logstash`, `Fluentd`,
     or even custom scripts, can easily distinguish between `stdout` and `stderr`
     to **route** messages appropriately for further action.
   - Sending errors and warnings (`stderr`) separately allows for specific
     alerts or escalations to be triggered based on those messages, while
     `stdout` logs can be used for less critical purposes like performance
     metrics or debugging.

### 7.3 **How Your Filters and Handlers Work Together**

With your current configuration:

1. **`stdout` Handler with `StdoutFilter1`**:

   - This handler will **only output messages with level `INFO` and `DEBUG`**.
   - `StdoutFilter1` filters out everything from `WARNING` and above. This
     means that regular operation details and debug information are sent to the
     standard output (`stdout`), but no higher-severity messages.

2. **`stderr` Handler with `StderrFilter`**:

   - This handler will **only output messages with level `WARNING` and above**.
   - This ensures that all messages indicating problems are directed to
     `stderr`. This distinction allows the critical errors to be separated from
     the normal log flow, making them easier to spot.

3. **File Handler (`file`) with JSON Formatter**:
   - This handler writes all logs (`DEBUG` level and above) to a file in JSON
     format.
   - This is a convenient way to retain a complete record of all log messages,
     making it easier to trace an application's behavior over time.

### 7.4 **Benefits of This Configuration**

1. **Clarity in Logging Output**:

   - By splitting the log outputs, it's much easier to **differentiate between
     normal operational logs and issues** that require attention.
   - Developers, support engineers, and DevOps professionals can focus on
     `stderr` logs for problem analysis and refer to `stdout` for understanding
     the general flow.

2. **Flexible Log Redirection**:

   - When running scripts or services, **redirecting logs** can be essential.
     You can redirect `stdout` to one location (e.g., `/var/log/app_info.log`)
     and `stderr` to another (e.g., `/var/log/app_errors.log`).
   - You can achieve this on the command line like this:

     ```bash
     python my_app.py > app_info.log 2> app_errors.log
     ```

   - This ensures that normal messages don’t mix with error logs, which makes
     troubleshooting easier.

3. **Automation, Pipelining, and CI/CD Environments**:

   - In many CI/CD environments, handling `stdout` and `stderr` separately can
     be important for **automated alerting** or **pipeline scripts**.
   - `stderr` logs can trigger an alert or an error handler in the pipeline,
     while `stdout` logs might just be archived for reference.

4. **Containerized and Cloud Environments**:
   - For applications running inside **containers** (e.g., Docker), it is a
     common practice to rely on `stdout` and `stderr` for logging.
   - Cloud-native logging solutions often aggregate logs from containers, and
     separating `stdout` and `stderr` makes it easier to **implement log
     routing**, monitor health, and trigger alerts based on critical log
     messages.

### **Summary**

- Having separate `stdout` and `stderr` handlers is **normal** and
  **recommended** for most use cases, especially in environments where logs need
  to be processed, redirected, or monitored closely.
- This setup provides better control over how different types of logs are
  handled and enables more effective troubleshooting and monitoring.
- `stdout` is typically used for **informational and debug logs**, while
  `stderr` is used for **warnings and errors**. This distinction can help you
  streamline log analysis, troubleshooting, and monitoring.

Your current configuration is well-structured and follows best practices by
keeping the logs separated logically. It allows you to efficiently manage both
routine information and issues, making your system easier to observe and
maintain.

If you need further assistance or have more questions on how to extend this
setup or implement other logging best practices, let me know!

## Extra with logging

- Given the configurations we have already written, we can always add
  additional pieces of information using the `extra` parameter.

```py
logger.debug("debug message", extra = {"x":"Hello"})

```

## MODERN TIP - 9 LOG OFF TH EMAIN THREAD

Due to its inherent characteristic, invoking a log function involves
input/output operations. If a user initiates a request to my web application
and this results in ten log messages being generated, I do not want to
introduce a delay of ten round-trip times in my logging service before
responding to the user. Currently, this is what will take place as all logging
calls are synchronous and blocking.

The solution is to use a `QueueHanlder` to log-off the main thread,

```sh

   ┌──────────────────────────────┐                     ┌────────────────────────────────────────────────────┐
   │     ┌───────────────┐        │                     │              ┌─────────────────┐                   │
   │     │ LOGGER "ROOT" │        │                     │              │  QUEUE LISTNER  │                   │
   │     └───────────────┘        │                     │              └─────────────────┘                   │
   │       LEVEL: DEBUG           │                     │   ┌──────────────────┐       ┌────────────────┐    │
   │                              │                     │   │ HANDLER "STDERR" │       │ HANDLER "FILE" │    │
   │ ┌─────────────────────────┐  │                     │   └──────────────────┘       └────────────────┘    │
   │ │ HANDLER "QUEUE_HANDLER" │  │                     │  ┌────────────────────┐     ┌───────────────────┐  │
   │ └───────────┬─────────────┘  │                     │  │ LEVEL: WARNING     │     │  LEVEL: DEBUG     │  │
   │             │                │                     │  │ FORMATTER "SIMPLE" │     │ FORMATTER: "JSON" │  │
   └─────────────┼────────────────┘                     │  └────────┬───────────┘     └─────────┬─────────┘  │
    ▲        ┌───┴───┐                                  │           ▼                           ▼            │
    │        │ QUEUE │─────────────▶ OTHER THREAD ─────▶│        STDERR                       FILE           │
    │        └───────┘                                  └────────────────────────────────────────────────────┘
    │┌─────────────┐
    └┤ PROPAGATE! ┌────────────────────┐
     └────────────│┘  LOGGER "MY_APP"  │
                  └────────────────────┘
```

- A queue handler stores your log recors in a queue without blocking, while an
  associated queue listener accepts those messages.

Here’s a breakdown and explanation of your **logging configuration** and
**Python script**. I’ll explain what each part of the configuration does, how
it interacts with your code, and what you should expect when using it in your
project.

---

## **Configuration Explanation (`config05.json`)**

### 1. **Formatters**

These define how the log messages will be formatted when they are output by the handlers.

- **`simple`**:

  ```json
  "format": "%(asctime)s:%(filename)s:%(funcName)s: %(lineno)d: %(levelname)s: %(message)s"
  ```

  This will display log messages with the timestamp, filename, function name,
  line number, log level, and message.

- **`colored`**:
  Uses a **custom formatter** from your code: `MyColoredFormatter`. It’s
  designed to print log messages with colors, making them easier to read on the
  console.

- **`json`**:
  Uses another **custom JSON formatter** (`MyJSONFormatter`). Instead of plain
  text, logs are structured in JSON format with specific keys like `level`,
  `message`, `timestamp`, etc., which is useful for machine-readable logs.

### 2. **Handlers**

Handlers define **where the logs go** (console, file, etc.) and how they are
formatted.

- **`queue_handler`**:
  Uses a **`QueueHandler`** that sends log records to a queue (defined later in
  the code with `Queue`). This enables asynchronous logging by passing log
  records from different threads to a single listener.

- **`stdout`**:
  Sends **DEBUG-level logs** or higher to the **standard output
  (`sys.stdout`)** with the `colored` formatter.

- **`stderr`**:
  Sends **ERROR-level logs** to **`sys.stderr`**, also using the `colored`
  formatter.

- **`file`**:
  A **rotating file handler** that writes logs to `my_app.jsonl`. It keeps log
  file sizes manageable (with `maxBytes=10000` and `backupCount=3`).

### 3. **Filters**

Filters allow you to selectively process log messages based on custom logic.

- **`stdout_filter`** and **`stderr_filter`**:
  Custom filters (from `myFilters` module) likely control what gets logged to
  `stdout` and `stderr`. These could filter logs based on conditions, such as
  message content or context.

### 4. **Loggers**

- **`root`** logger:
  The `root` logger is the **default logger** used in your code. It’s
  configured to:
  - Accept **DEBUG-level logs** and higher.
  - Use the following handlers: `queue_handler`, `stdout`, `stderr`, and
    `file`.

---

## **What to Expect from the Configuration in Your Code**

1. **Queue-based Asynchronous Logging**:

   - Your `QueueHandler` sends all log records to a **`Queue`**.
   - A **`QueueListener`** processes records asynchronously, passing them to
     the other handlers (`stdout`, `stderr`, `file`).
   - This setup ensures that logging is **non-blocking**, meaning log messages
     won’t slow down your code even under heavy logging loads.

2. **Logs Sent to Different Destinations**:

   - **DEBUG** and **INFO** logs appear in **`stdout`** with colors (via
     `MyColoredFormatter`).
   - **ERROR** logs are sent to **`stderr`**.
   - All logs are saved in a **rotating JSON log file** (`my_app.jsonl`),
     ensuring that logs are structured and easy to parse.

3. **Graceful Shutdown**:

   - When your application exits, the `QueueListener` is **stopped gracefully**
     using `atexit`. This ensures that all pending log messages in the queue are
     processed before the program terminates.

4. **Custom Filters**:
   - The `stdout` and `stderr` filters allow you to **control what gets
     logged** to the respective streams (e.g., filtering based on log content).

---

## **Python Code Explanation**

### Key Parts

1. **Setting up Logging (`setup_logging`)**:

   - The `setup_logging()` function loads the configuration from
     `config05.json`.
   - It **injects the queue** into the `queue_handler` dynamically.
   - It **verifies** that at least one handler is attached to the root logger.
   - It **creates and starts a `QueueListener`**, passing all handlers except
     the `queue_handler` (which only sends logs to the queue).

2. **Generating Logs (`testing_loading_config`)**:

   - This function generates several log messages with different levels:
     `INFO`, `DEBUG`, `WARNING`, and `ERROR`.
   - It also passes **extra context** with some logs (e.g., `extra={"x": "hello"}`), which could be used by your custom formatters.

3. **Starting the Program**:
   - If the script is executed directly (`if __name__ == "__main__":`), it
     calls `testing_loading_config()` to **initialize logging and generate test
     logs**.

---

## **Expected Output**

When you run your code, you should see the following behavior:

- **On `stdout` (standard output)**:
  Colored **DEBUG and INFO logs** will be printed, formatted by `MyColoredFormatter`.

- **On `stderr` (standard error)**:
  **ERROR logs** will be printed, also using `MyColoredFormatter`.

- **In the file `my_app.jsonl`**:
  All logs will be saved in **JSON format**, structured for easy parsing.

Example log in `stdout`:

```
DATE: 2024-10-29 TIME:14:35:52 [+0000]: L05_queue_handler.py: testing_loading_config: L30: INFO: [INFO] This is just a test
```

Example log in `my_app.jsonl`:

```json
{
  "level": "INFO",
  "message": "[INFO] This is just a test",
  "timestamp": "2024-10-29T14:35:52+0000",
  "logger": "__main__",
  "module": "L05_queue_handler",
  "function": "testing_loading_config",
  "line": 30,
  "thread_name": "MainThread"
}
```

---

## **Potential Issues to Watch For**

1. **Filters**:

   - If the filters aren’t correctly implemented, some logs might not appear
     where expected (e.g., logs not showing up in `stdout` or `stderr`).

2. **Handler Errors**:

   - If any handler (like `file` or `stdout`) fails, it could cause logging to
     break. Make sure the log file path (`src/logging/my_app.jsonl`) is writable.

3. **Performance**:
   - Queue-based logging is efficient, but if the queue isn’t drained quickly enough (e.g., under heavy load), it could grow large. Adjust the `QueueListener` if needed.

---

## **Summary**

This setup provides a **robust, asynchronous logging system** with multiple handlers for different outputs:

- **Console output** (with colors for readability).
- **JSON-formatted log files** for structured logging.
- **Filters** to control what goes to `stdout` and `stderr`.
- **Asynchronous logging** using a queue to avoid blocking the main thread.

It ensures your logs are easy to read during development (via colored output) and easy to analyze in production (via structured JSON logs).

## How about jsonl file?

Yes, based on your configuration, the **JSONL file** (`my_app.jsonl`) will
capture **all log messages** from your application. Here’s a detailed
explanation of how it works and why all messages will end up in the JSONL file.

---

### **How the JSONL File (`my_app.jsonl`) Works in Your Setup**

In your configuration:

```json
"handlers": {
  "file": {
    "class": "logging.handlers.RotatingFileHandler",
    "level": "DEBUG",
    "formatter": "json",
    "filename": "src/logging/my_app.jsonl",
    "maxBytes": 10000,
    "backupCount": 3
  }
}
```

- **`level`: `"DEBUG"`** – This means the `file` handler will capture **all
  logs** from **DEBUG** level and above (i.e., `DEBUG`, `INFO`, `WARNING`,
  `ERROR`, `CRITICAL`).
- **`formatter`: `"json"`** – Logs will be formatted as JSON objects, making
  them suitable for **structured logging**.
- **`RotatingFileHandler`** – The log file will rotate when it reaches **10,000
  bytes**, keeping **up to 3 backups**.

Since the **root logger** has `"file"` in its handlers list, **every log
message** processed by the logger will also be sent to the JSONL file.

---

### **Expected Behavior**

1. **All log messages will be written to `my_app.jsonl`**:

   - Since the `file` handler has a **DEBUG** level, it will capture **all log
     levels**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.

2. **Log file format**:

   - Each log entry will be formatted as a **JSON object**, and **each line in
     the file will contain a single log message** (hence the `.jsonl` extension,
     meaning JSON Lines).

   Example JSONL file content:

   ```json
        {
          "level": "INFO",
          "message": "[INFO] This is just a test",
          "timestamp": "2024-10-29T14:35:52+0000",
          "logger": "__main__",
          "module": "L05_queue_handler",
          "function": "testing_loading_config",
          "line": 30,
          "thread_name": "MainThread"
        }
        {
          "level": "DEBUG",
          "message": "[DEBUG] This is just a test",
          "timestamp": "2024-10-29T14:35:53+0000",
          "logger": "__main__",
          "module": "L05_queue_handler",
          "function": "testing_loading_config",
          "line": 31,
          "thread_name": "MainThread"
        }
        {
          "level": "WARNING",
          "message": "[WARNING] This is a warning test",
          "timestamp": "2024-10-29T14:35:54+0000",
          "logger": "__main__",
          "module": "L05_queue_handler",
          "function": "testing_loading_config",
          "line": 32,
          "thread_name": "MainThread"
        }
        {
          "level": "ERROR",
          "message": "[ERROR] This is an error test",
          "timestamp": "2024-10-29T14:35:55+0000",
          "logger": "__main__",
          "module": "L05_queue_handler",
          "function": "testing_loading_config",
          "line": 33,
          "thread_name": "MainThread"
        }
   ```

3. **Handling Multiple Threads**:
   - Since the `QueueHandler` sends logs to a **queue** and the `QueueListener`
     processes them, the JSONL file will capture **logs from multiple threads**
     correctly in the order they are processed.

---

### **Verifying the JSONL File**

After running your script, you can check the content of `my_app.jsonl` by printing the file:

```bash
cat src/logging/my_app.jsonl
```

You should see all the log messages (in JSON format) from the test function `testing_loading_config()`.

---

### **Summary**

Yes, the **JSONL file will capture all log messages** at or above the `DEBUG`
level. Since your `root` logger sends logs to the `file` handler with a `DEBUG`
level, **every log message from your application will be saved in the JSONL
file**, including those sent to `stdout` and `stderr`.

This setup ensures:

- **Comprehensive logging** to the JSONL file.
- **Asynchronous handling** of logs via the `QueueListener`.
- **Structured logs** for easier analysis and post-processing.

## Perforamnce and efficiency

Is there a bad code practice of using logger = logging.getLogger(**name**) # Module-level logger instead passing a hard coded single name like "my_app".
Using `logging.getLogger(__name__)` is generally considered a **good practice** and has several advantages over hard-coding a logger name like `"my_app"`. However, there are a few situations where using a **hard-coded logger name** might be preferable. Let’s go over the pros and cons of each approach and when to use them.

---

## **Using `__name__` (Recommended Practice)**

### **Advantages**:

1. **Contextual Logging**:

   - `__name__` will automatically use the **name of the current module**, which makes it easier to identify **where the log messages are coming from** in large applications.
   - For example:
     - If the module is `src.logging.L05_queue_handler`, the logger’s name will be `src.logging.L05_queue_handler`.
     - This is especially useful when logs come from different parts of your application.

2. **Consistent and Flexible**:

   - You don’t need to manually change the logger name in every module.
   - If the module name changes, the logger name will **automatically reflect the new module name**.

3. **Easier Filtering and Control**:

   - You can control logging behavior by **module**. For example, you can set log levels per module (`logging.getLogger("src.logging").setLevel(logging.WARNING)`).

4. **Integration with External Tools**:
   - Many logging tools (e.g., **Sentry** or **ELK stack**) benefit from having detailed, module-level logger names for filtering and diagnostics.

### **Disadvantages**:

1. **Less Control Over Global Logging Settings**:

   - If you want all modules to use **exactly the same logger name** (like `"my_app"`), this approach can make it harder to ensure consistency across modules.

2. **Verbose Logger Names**:
   - In some cases, module names can get very long (e.g., `src.logging.L05_queue_handler`), which might clutter your logs. However, this can be mitigated by configuring how logger names are displayed in your log format.

---

## **Using a Hard-Coded Logger Name (e.g., `"my_app"`)**

### **Advantages**:

1. **Simple and Consistent Logger Name**:

   - If you want **all log messages to use the same logger name**, hard-coding `"my_app"` ensures that every part of your application will log to the same place.

2. **Easier Setup for Small Applications**:

   - In smaller applications, where logs don't need to be differentiated by module, a single hard-coded logger name might make things simpler.

3. **Fewer Configuration Challenges**:
   - If your logging system expects **one logger name** (e.g., `"my_app"`), using `__name__` might complicate the setup, and a hard-coded name might be more practical.

### **Disadvantages**:

1. **Loses Context**:

   - You lose the ability to know **which module generated the log message**. All logs will appear as if they came from the `"my_app"` logger, making it harder to debug large applications.

2. **More Manual Work**:

   - You need to ensure every module uses the same logger name, which is prone to human error (e.g., accidentally using `"my-app"` in one module and `"my_app"` in another).

3. **Less Granular Control**:
   - You can't easily adjust the log level or behavior **per module** because everything logs under the same name.

---

## **Which Approach Should You Use?**

- **For Larger Projects**:
  Use `logging.getLogger(__name__)` so you get **contextual logging** per module, making it easier to debug and trace logs.

- **For Smaller Projects** or **Highly Centralized Logging Needs**:
  Use a **hard-coded name** like `"my_app"` if you want **one consistent logger** across the entire project.

---

## **Example Comparison**

### Using `__name__` (Recommended for Large Projects):

```python
# In src/logging/L05_queue_handler.py
logger = logging.getLogger(__name__)  # Logger name: 'src.logging.L05_queue_handler'

logger.info("This is an info log.")
```

Log Output:

```
2024-10-29 14:35:52,001 src.logging.L05_queue_handler: This is an info log.
```

---

### Using Hard-Coded Logger Name (Suitable for Small Projects):

```python
# In src/logging/L05_queue_handler.py
logger = logging.getLogger("my_app")

logger.info("This is an info log.")
```

Log Output:

```
2024-10-29 14:35:52,001 my_app: This is an info log.
```

---

## **Conclusion**

In most cases, **`logging.getLogger(__name__)` is the better practice**, especially for larger projects, as it offers **contextual information** and flexibility. It also makes it easier to maintain and debug your code by showing exactly which module produced the log message.

However, for **simple applications** or when you want **a unified logging experience** across all modules, using a **single hard-coded name** like `"my_app"` can be a valid approach.

Choose the method based on the complexity and size of your project:

- **Large projects** → Use `__name__` for context-aware logging.
- **Small, single-module apps** → Use `"my_app"` for simplicity.

## Reference

- [python logging official website](https://docs.python.org/3/library/logging.html)
