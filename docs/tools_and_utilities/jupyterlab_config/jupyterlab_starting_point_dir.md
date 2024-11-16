# Methods for chaning the notebook Dir

**NOTE**:

- Once you change the dir, it will run to the end of session, so you must
  restart the session `kernal` to get the next effect.

In Jupyter Notebook, there are several ways to change the working directory to
a specific directory, such as the root directory. Here are various methods:

### Method 1: Use `os.chdir()` in a Code Cell

The `os` library in Python provides a straightforward way to change the working directory.

```python
import os

# Change to root directory
os.chdir('/')
print("Current Working Directory:", os.getcwd())
```

### Method 2: Modify the Notebook's Startup Directory in the Jupyter Config File

If you want to set the default working directory for Jupyter Notebooks (so
every notebook opens in a specific directory), you can edit the Jupyter
configuration file:

1. Open your terminal and run:

   ```bash
   jupyter notebook --generate-config
   ```

   This will generate a `.jupyter/jupyter_notebook_config.py` file in your home directory if it doesn’t already exist.

2. Open `.jupyter/jupyter_notebook_config.py` and find the line that starts with `c.NotebookApp.notebook_dir`.

3. Set it to your desired path, such as root (`/`) or any other directory:

   ```python
   c.NotebookApp.notebook_dir = '/'
   ```

4. Save and restart Jupyter Notebook.

### Method 3: Change Directory Using `%cd` Magic Command

You can use Jupyter’s magic command `%cd` to change the working directory
temporarily for the session:

```python
# Change to root directory
%cd /
```

### Method 4: Update the Notebook File Path with `sys.path`

If you’re importing modules and want to ensure they load from the specified
directory, you can append the path to `sys.path`:

```python
import sys
sys.path.insert(0, '/')
print("Current Working Directory:", sys.path[0])
```

### Method 5: Run Jupyter Notebook from the Desired Directory (Terminal)

You can also start Jupyter Notebook from the desired directory directly:

1. Open your terminal.
2. Navigate to the desired directory (e.g., root):
   ```bash
   cd /
   ```
3. Start Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

This way, the working directory will be set to the directory where Jupyter Notebook was launched.

---

These methods give you flexibility depending on whether you want a temporary
session change, a persistent change across all notebooks, or a one-time setup.
Let me know if you'd like further details on any method!

## I use method -1 advanced

```py
import os
from pathlib import Path

# Store the initial working directory
initial_dir = os.getcwd()

# Set the working directory to the project root based on the notebook location
project_root = Path().resolve().parent.parent
os.chdir(project_root)

print("Changed to Project Root Directory:", os.getcwd())

# ... Run your code with the root directory as the working directory ...

# When done, you can change back to the initial directory if needed
# os.chdir(initial_dir)
# print("Reverted to Initial Directory:", os.getcwd())
```
