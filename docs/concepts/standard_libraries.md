# STANDARD LIBRARY IN PYTHON

## Intro

Here's a table summarizing some of the most common standard modules in Python,
along with their key functions or classes and brief descriptions. This list
covers many popular modules but isn't exhaustive, as the Python Standard Library
is quite extensive.

| **Module**        | **Description**                                | **Common Methods/Classes**                                     | **Usage/Description**                                                                   |
| ----------------- | ---------------------------------------------- | -------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `itertools`       | Iterators for efficient looping                | `count`, `cycle`, `repeat`, `chain`, `product`, `permutations` | Infinite and combinatorial iterators, useful in loops and functional programming.       |
| `collections`     | Specialized data structures                    | `namedtuple`, `deque`, `Counter`, `OrderedDict`, `defaultdict` | Data structures for efficient handling of data, like counting and ordered dictionaries. |
| `functools`       | Functional programming tools                   | `reduce`, `partial`, `lru_cache`, `cmp_to_key`                 | Tools for functional programming, such as caching and function composition.             |
| `hashlib`         | Secure hash functions                          | `md5`, `sha1`, `sha256`, `sha512`                              | Create secure hash values for data integrity checks.                                    |
| `pickle`          | Object serialization and deserialization       | `dump`, `dumps`, `load`, `loads`                               | Serialize Python objects to bytes for storage or network transfer.                      |
| `json`            | JSON encoding and decoding                     | `dump`, `dumps`, `load`, `loads`                               | Encode and decode JSON, a common data format in web applications.                       |
| `re`              | Regular expression operations                  | `search`, `match`, `findall`, `sub`, `compile`                 | Pattern matching and text processing using regular expressions.                         |
| `datetime`        | Date and time manipulation                     | `datetime`, `date`, `time`, `timedelta`, `strftime`            | Manipulate dates and times, format, parse, and perform arithmetic.                      |
| `time`            | Time-related functions                         | `time`, `sleep`, `ctime`, `perf_counter`                       | Time measurement, delays, and conversion to string formats.                             |
| `random`          | Random number generation                       | `random`, `randint`, `choice`, `shuffle`, `seed`               | Generate random numbers and make random selections.                                     |
| `math`            | Mathematical functions                         | `sqrt`, `pow`, `factorial`, `pi`, `sin`, `cos`                 | Basic and advanced mathematical functions and constants.                                |
| `statistics`      | Statistical calculations                       | `mean`, `median`, `mode`, `stdev`, `variance`                  | Perform basic statistics on datasets.                                                   |
| `os`              | OS-related operations                          | `getcwd`, `listdir`, `remove`, `mkdir`, `environ`, `path`      | Interact with the operating system for file and directory management.                   |
| `sys`             | System-specific parameters and functions       | `argv`, `exit`, `path`, `stdin`, `stdout`, `platform`          | Access system-level parameters and control program execution.                           |
| `argparse`        | Command-line argument parsing                  | `ArgumentParser`, `add_argument`, `parse_args`                 | Create command-line interfaces for Python programs.                                     |
| `subprocess`      | Spawn new processes and interact with them     | `run`, `Popen`, `call`, `check_output`                         | Execute shell commands and manage external processes.                                   |
| `logging`         | Logging facility                               | `basicConfig`, `getLogger`, `info`, `error`, `warning`         | Record log messages to track program execution and errors.                              |
| `pathlib`         | Object-oriented filesystem paths               | `Path`, `exists`, `mkdir`, `rmdir`, `glob`, `read_text`        | Manipulate file system paths in an object-oriented way.                                 |
| `fileinput`       | Iterating over lines in multiple input streams | `input`, `filelineno`, `filename`, `close`                     | Read lines from files, supporting multiple files and in-place editing.                  |
| `csv`             | CSV file reading and writing                   | `reader`, `writer`, `DictReader`, `DictWriter`                 | Parse and write CSV files commonly used for data exchange.                              |
| `sqlite3`         | DB-API 2.0 interface for SQLite databases      | `connect`, `cursor`, `execute`, `commit`, `close`              | Work with SQLite databases, creating and managing database tables.                      |
| `requests`        | HTTP library for sending requests              | `get`, `post`, `put`, `delete`, `head`                         | Send HTTP requests and handle responses; commonly used in web APIs.                     |
| `shutil`          | High-level file operations                     | `copy`, `copytree`, `move`, `rmtree`                           | Perform operations like copying, moving, and deleting files/directories.                |
| `socket`          | Low-level networking interface                 | `socket`, `connect`, `bind`, `send`, `recv`                    | Work with network connections, send and receive data over sockets.                      |
| `threading`       | Thread-based parallelism                       | `Thread`, `start`, `join`, `Lock`, `Event`, `Semaphore`        | Manage and create threads for concurrent program execution.                             |
| `multiprocessing` | Process-based parallelism                      | `Process`, `Queue`, `Pool`, `Pipe`, `Lock`                     | Parallel execution of functions using separate memory processes.                        |
| `queue`           | Synchronized queue classes                     | `Queue`, `LifoQueue`, `PriorityQueue`                          | Thread-safe data structures for passing data between threads.                           |
| `unittest`        | Unit testing framework                         | `TestCase`, `assertEqual`, `setUp`, `tearDown`                 | Write and run unit tests for code validation.                                           |
| `tkinter`         | Standard library for GUI development           | `Tk`, `Button`, `Label`, `Canvas`, `Entry`                     | Build simple GUI applications.                                                          |
| `uuid`            | Generate universally unique identifiers        | `uuid1`, `uuid4`, `UUID`                                       | Generate UUIDs for unique identifiers, often used in distributed systems.               |
| `base64`          | Base64 encoding and decoding                   | `b64encode`, `b64decode`                                       | Encode and decode data in base64 format, often for binary data in text formats.         |
| `struct`          | Interpret bytes as packed binary data          | `pack`, `unpack`, `calcsize`                                   | Handle binary data, useful for data interchange and network protocols.                  |
| `gzip`            | Support for Gzip files                         | `open`, `compress`, `decompress`                               | Read and write files in Gzip format for compression.                                    |
| `bz2`             | Support for Bzip2 compression                  | `compress`, `decompress`, `open`                               | Compress and decompress files using Bzip2 compression.                                  |
| `zipfile`         | ZIP archive handling                           | `ZipFile`, `open`, `extract`, `write`                          | Create, read, write, and extract files from ZIP archives.                               |
| `tarfile`         | Tar archive handling                           | `open`, `add`, `extract`, `list`                               | Read and write tar archives, including gzip and bzip2 compression.                      |

This table covers a selection of Python's built-in modules along with commonly
used methods and brief descriptions. Let me know if you’d like a deeper look at
any specific module or functionality!
