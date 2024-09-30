# OS Modules

## CheatSheet

Here's a table that summarizes various methods in the `os` module, mixed with magic methods like `__file__`, along with descriptions and syntax:

| **Method/Attribute**       | **Description**                                                                  | **Syntax**                                   |
| -------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------- |
| `os.getcwd()`              | Returns the current working directory.                                           | `cwd = os.getcwd()`                          |
| `os.chdir(path)`           | Changes the current working directory to the specified path.                     | `os.chdir('/path/to/directory')`             |
| `os.listdir(path)`         | Returns a list of file and directory names in the specified path.                | `files = os.listdir('/path')`                |
| `os.mkdir(path)`           | Creates a directory at the specified path.                                       | `os.mkdir('new_folder')`                     |
| `os.makedirs(path)`        | Recursively creates directories along the specified path.                        | `os.makedirs('/parent/child/new_folder')`    |
| `os.rmdir(path)`           | Removes a directory at the specified path.                                       | `os.rmdir('empty_folder')`                   |
| `os.remove(path)`          | Deletes a file at the specified path.                                            | `os.remove('file.txt')`                      |
| `os.rename(src, dst)`      | Renames or moves a file/directory from `src` to `dst`.                           | `os.rename('old.txt', 'new.txt')`            |
| `os.path.exists(path)`     | Checks whether a given path exists.                                              | `exists = os.path.exists('file.txt')`        |
| `os.path.join(*paths)`     | Joins one or more path components intelligently, cross-platform safe.            | `full_path = os.path.join('dir', 'file')`    |
| `os.path.dirname(path)`    | Returns the directory name of the given path.                                    | `dir_name = os.path.dirname('/a/b/file')`    |
| `os.path.basename(path)`   | Returns the base name of the given path.                                         | `file_name = os.path.basename('/a/b/file')`  |
| `os.path.abspath(path)`    | Returns the absolute version of the specified path.                              | `abs_path = os.path.abspath('file.txt')`     |
| `os.path.splitext(path)`   | Splits the file name and extension into a tuple.                                 | `name, ext = os.path.splitext('file.txt')`   |
| `os.environ`               | Provides access to the system environment variables.                             | `os.environ['HOME']`                         |
| `os.system(command)`       | Executes the command (string) in the system's shell.                             | `os.system('ls -l')`                         |
| `os.getlogin()`            | Returns the name of the user logged in on the terminal.                          | `user = os.getlogin()`                       |
| `os.getpid()`              | Returns the current process ID.                                                  | `pid = os.getpid()`                          |
| `os.fork()`                | Creates a child process (UNIX only).                                             | `pid = os.fork()`                            |
| `os.execv(path, args)`     | Replaces the current process with a new one at the given path.                   | `os.execv('/bin/ls', ['ls', '-l'])`          |
| `os.dup2(fd1, fd2)`        | Duplicates the file descriptor `fd1` to `fd2`.                                   | `os.dup2(new_fd, old_fd)`                    |
| `os.pipe()`                | Creates a pipe and returns a pair `(r, w)` file descriptors for reading/writing. | `r, w = os.pipe()`                           |
| `os.kill(pid, sig)`        | Sends a signal `sig` to the process `pid`.                                       | `os.kill(pid, signal.SIGTERM)`               |
| `os.stat(path)`            | Performs a stat system call on the given path, returning detailed metadata.      | `stats = os.stat('file.txt')`                |
| `os.walk(top, ...)`        | Generates file names in a directory tree by walking top-down or bottom-up.       | `for root, dirs, files in os.walk('/path'):` |
| `os.path.isabs(path)`      | Checks if the specified path is an absolute path.                                | `is_abs = os.path.isabs('/home/file')`       |
| `os.path.isfile(path)`     | Checks if the path points to a regular file.                                     | `is_file = os.path.isfile('file.txt')`       |
| `os.path.isdir(path)`      | Checks if the path points to a directory.                                        | `is_dir = os.path.isdir('/path')`            |
| `os.chmod(path, mode)`     | Changes the permissions of the file or directory at `path` to `mode`.            | `os.chmod('file.txt', 0o777)`                |
| `os.chown(path, uid, gid)` | Changes the owner and group of the file at `path`.                               | `os.chown('file.txt', 1000, 1000)`           |
| `__file__` (Magic method)  | Refers to the path of the currently executing file.                              | `print(__file__)`                            |
| `__dir__()` (Magic method) | Lists all valid attributes of an object.                                         | `dir(os)`                                    |
| `os.path.relpath(path)`    | Returns the relative path from the current working directory.                    | `rel_path = os.path.relpath('file.txt')`     |
| `os.urandom(n)`            | Returns a string of `n` random bytes, suitable for cryptographic use.            | `random_bytes = os.urandom(16)`              |
| `os.cpu_count()`           | Returns the number of CPUs available in the system.                              | `cpu_count = os.cpu_count()`                 |
| `os.getppid()`             | Returns the parent process ID of the current process.                            | `parent_pid = os.getppid()`                  |

## What is OS

The `os` module in Python provides a range of functionality to interact with the
operating system. Here are some complex syntaxes and patterns using the `os`
module, commonly practiced by Python developers:

### 1. **Dynamic Path Construction with `os.path`**

Python developers frequently use `os.path` to build paths dynamically across
different operating systems. This helps avoid issues with path separators (`/`
vs `\`) on different OSes.

```python
import os

# Join multiple directories dynamically
path = os.path.join(os.path.expanduser('~'), 'projects', 'my_project', 'data', 'file.txt')

# Further manipulate paths (e.g., get directory, basename)
directory = os.path.dirname(path)
filename = os.path.basename(path)
```

### 2. **Managing Processes and Subprocesses with `os.spawn` and `os.execv`**

Starting a new process or replacing the current process image using the `os`
module is less common but powerful.

```python
import os

# Example using `os.spawn` to run another program
pid = os.spawnl(os.P_NOWAIT, '/usr/bin/python3', 'python3', '-c', 'print("Hello from subprocess")')

# Example replacing the current process with another process using `os.execv`
os.execv('/usr/bin/python3', ['python3', '-c', 'print("This replaces the current process")'])
```

In this case, `os.execv` replaces the running process with the new process, so
no further code will execute after it.

### 3. **Environment Variables Handling**

Developers often manipulate environment variables with `os.environ` to manage
configuration, especially in environments like Docker or web applications.

```python
import os

# Access environment variables
database_url = os.environ.get('DATABASE_URL', 'sqlite:///:memory:')

# Set an environment variable
os.environ['NEW_VARIABLE'] = 'new_value'

# Deleting an environment variable
del os.environ['OLD_VARIABLE']
```

### 4. **Cross-Platform Handling of Signals and Process Control**

For advanced process control, you can send signals between processes or handle
them via the `os` module:

```python
import os
import signal
import time

# Signal handling
def handler(signum, frame):
    print(f"Signal {signum} received")

# Set a signal handler for SIGUSR1
signal.signal(signal.SIGUSR1, handler)

# Forking a process and sending a signal from the child process
pid = os.fork()
if pid == 0:
    # Child process
    os.kill(os.getppid(), signal.SIGUSR1)
    os._exit(0)
else:
    time.sleep(1)  # Wait for the signal
```

### 5. **File and Directory Permissions**

Managing file permissions (e.g., changing access rights) with `os.chmod` and
`os.chown` is essential for systems programming.

```python
import os
import stat

# Change permissions to read-write for user and group, and read-only for others
os.chmod('somefile.txt', stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

# Change ownership of the file (user_id, group_id)
os.chown('somefile.txt', 1000, 1000)
```

### 6. **Context Manager for `os.open`**

Though `open()` is typically used for file handling in Python, `os.open()`
provides low-level file operations, which is useful in some specific scenarios
(like controlling file flags). Using it with a context manager is less common
but powerful.

```python
import os

# Open file with low-level os.open for more control over flags
fd = os.open('somefile.txt', os.O_RDWR | os.O_CREAT)

# Use os.fdopen to create a higher-level file object for context management
with os.fdopen(fd, 'w') as file:
    file.write("Writing through os.open")
```

### 7. **Handling File Descriptors with `os.dup2`**

Redirecting standard input/output using `os.dup2` is an advanced use case in systems programming.

```python
import os
import sys

# Open a file and redirect stdout to the file
with open('output.log', 'w') as f:
    os.dup2(f.fileno(), sys.stdout.fileno())
    print("This will go to the file instead of stdout")
```

### 8. **Process Creation and Inter-Process Communication with `os.pipe` and `os.fork`**

Creating pipes for inter-process communication is a useful technique when working with multiple processes.

```python
import os

# Create a pipe (read_fd, write_fd)
read_fd, write_fd = os.pipe()

# Fork a child process
pid = os.fork()
if pid == 0:
    # Child process - write to the pipe
    os.write(write_fd, b"Hello from child process")
    os._exit(0)
else:
    # Parent process - read from the pipe
    os.close(write_fd)
    message = os.read(read_fd, 100)
    print(f"Received message: {message.decode()}")
```

These examples reflect some of the more complex and low-level capabilities
provided by the `os` module, frequently used in system administration, process
management, and low-level file operations. They offer deeper control compared to
the more abstracted high-level functions available in Python.

### Example mixing `os` module with `__file__`:

```python
import os

# Get the absolute path of the current script
current_script = os.path.abspath(__file__)

# Get the directory where the current script is located
script_dir = os.path.dirname(current_script)

# Create a new file in the same directory as the script
new_file_path = os.path.join(script_dir, 'new_file.txt')
with open(new_file_path, 'w') as f:
    f.write("Created by mixing __file__ with os module!")
```

This table and example show the diverse functionalities of the `os` module and
how to mix it with magic methods like `__file__` for dynamic and cross-platform
path management.
