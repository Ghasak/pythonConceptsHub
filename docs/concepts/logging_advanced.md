# Logging Advanced

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


##  5. Modern Tip -5  Store config in json or yaml file



## Reference

- [python logging official website](https://docs.python.org/3/library/logging.html)
