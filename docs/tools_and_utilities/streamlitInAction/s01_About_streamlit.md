# About Streamlit

If you're looking for dashboarding tools similar to Streamlit for Python, here
are some popular options:

1. **Dash by Plotly**: A powerful and versatile framework for building
   dashboards and web applications. Dash is highly customizable and works well
   for creating interactive data visualizations.

2. **Panel**: Part of the HoloViz ecosystem, Panel allows for creating powerful
   dashboards with various plotting libraries like Matplotlib, Bokeh, Plotly,
   and others. It supports widgets and can be deployed as a web app.

3. **Voila**: Converts Jupyter notebooks into interactive dashboards. It’s
   straightforward to use if you’re already working within the Jupyter ecosystem
   and want to add interactivity without much additional code.

4. **Gradio**: Known for rapid prototyping, especially with machine learning
   models. Gradio allows users to build simple web interfaces for their models
   and code. It’s intuitive and requires minimal code to set up.

5. **Bokeh**: While primarily a plotting library, Bokeh allows for building
   standalone interactive dashboards. It has widgets and interactions and can be
   integrated into larger applications.

6. **Flask or Django with Plotly Dash or Bokeh**: For more customized
   applications, combining Flask or Django with visualization tools like Plotly
   or Bokeh can allow for flexible dashboarding and integration with a backend.

7. **Shiny for Python**: Inspired by R's Shiny framework, it recently added
   support for Python. Shiny is known for its reactive programming model, making
   it great for dynamic and interactive web applications.

Each of these tools has its strengths depending on your project requirements,
such as customization, ease of use, or specific visualization needs.

## If i have a binary complied in cpp for computing some task?

- Is there a way to trigger it using streamlit by clicking a button Yes, you can
  trigger a binary compiled in C++ from a Streamlit app by using Python’s
  `subprocess` module. This module allows you to run external commands, so you can
  call your binary directly when a button in Streamlit is clicked. Here’s how you
  can do it:

1. **Import the necessary modules**: Use `subprocess` to handle the binary
   execution and `streamlit` to build the app interface.

2. **Define a function**: Create a function that will be called when the button
   is clicked. This function should use `subprocess.run()` or
   `subprocess.call()` to execute the binary.

3. **Trigger the function with a button**: Use `st.button()` to create a button
   in Streamlit, which calls your function when clicked.

Here’s an example:

```python
import subprocess
import streamlit as st

# Define a function to execute the binary
def run_cpp_binary():
    # Replace './my_cpp_binary' with the path to your binary
    result = subprocess.run(['./my_cpp_binary'], capture_output=True, text=True)
    return result.stdout  # Return the output from the binary

# Streamlit app
st.title("Run C++ Binary from Streamlit")

if st.button("Run Task"):
    output = run_cpp_binary()
    st.write("Output from C++ Binary:")
    st.code(output)
```

### Key Points:

- **`capture_output=True`**: Captures the output, so you can display it in Streamlit.
- **Error Handling**: Consider adding error handling to check for any issues when running the binary.
- **Permissions**: Ensure the binary has execution permissions (`chmod +x my_cpp_binary` on Unix-like systems).
- **Path to Binary**: Use the correct path to your binary. For relative paths, make sure the Streamlit app runs in the same directory or provide an absolute path.

This setup allows users to trigger the C++ binary by clicking a button in the
Streamlit app, with the output shown directly in the Streamlit interface.

## Having tasks

If you have multiple individual Python scripts (e.g., `task1.py`, `task2.py`, etc.) and want to trigger each one from a button in a Streamlit app, you can follow a similar approach. Here’s how to set it up:

1. **Define Functions for Each Script**: Create a function in Streamlit to trigger each script, using the `subprocess` module to run them.

2. **Add Buttons for Each Task**: Use `st.button()` to create separate buttons for each script. When a button is clicked, the corresponding script is executed.

3. **Display Output**: Capture and display the output of each script in Streamlit.

Here’s a code example:

```python
import subprocess
import streamlit as st

# Function to run each script
def run_task(script_name):
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    return result.stdout

# Streamlit app
st.title("Run Python Scripts from Streamlit")

# Button to run task1.py
if st.button("Run Task 1"):
    output = run_task('task1.py')
    st.write("Output from task1.py:")
    st.code(output)

# Button to run task2.py
if st.button("Run Task 2"):
    output = run_task('task2.py')
    st.write("Output from task2.py:")
    st.code(output)

# Add additional buttons for other tasks as needed
```

### Notes

- **`capture_output=True`**: Captures the script's standard output so you can
  display it in the Streamlit interface.
- **Error Handling**: Consider adding error handling to display any errors if a
  script fails to run.
- **Python Path**: The `python` command in `subprocess.run(['python', 'task1.py'])` assumes Python is accessible through this alias. If you have
  specific Python versions, use `python3` or an absolute path to the Python
  executable.

This setup allows each button to trigger an individual script and display its
output in the Streamlit app.

## Is there a way to measure when the task will finish like a progress bar?

- And how to make it work for my task1.py for example
  Yes, you can add a progress bar in Streamlit to give users an indication of the task's progress. However, since `task1.py` is a separate script, measuring its progress can be challenging if it doesn’t inherently provide status updates.

Here are a few ways to approach this:

### 1. **Using Estimated Time (Simplified Progress Bar)**

If you have an approximate idea of how long `task1.py` typically takes, you can use a simulated progress bar based on estimated time. This is not precise but gives users an indication that the task is running.

```python
import subprocess
import streamlit as st
import time

def run_task_with_progress(script_name, estimated_time=10):
    # Start the task in a subprocess
    process = subprocess.Popen(['python', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Simulated progress bar
    progress_bar = st.progress(0)
    for i in range(estimated_time):
        time.sleep(1)
        progress_bar.progress((i + 1) / estimated_time)

    # Wait for the process to complete and get output
    stdout, stderr = process.communicate()

    return stdout if stdout else stderr  # Return output or error message

# Streamlit app
st.title("Run Python Scripts with Progress Bar")

if st.button("Run Task 1 with Progress Bar"):
    output = run_task_with_progress('task1.py', estimated_time=10)
    st.write("Output from task1.py:")
    st.code(output)
```

This approach uses `estimated_time` to control the progress bar’s duration.
Adjust `estimated_time` to match the typical runtime of `task1.py`.

### 2. **Using Real-Time Updates from the Script (If Modifiable)**

If you can modify `task1.py`, you could add progress output from the script
itself (such as writing to a temporary file or emitting progress messages). The
Streamlit app can then read this file or listen to these messages to update the
progress bar.

For example, update `task1.py` to periodically write its progress (e.g., “10%”, “20%”, etc.) to a file:

**task1.py:**

```python
import time

for i in range(1, 11):
    with open("progress.txt", "w") as f:
        f.write(f"{i * 10}")
    time.sleep(1)  # Simulate work
```

Then, in the Streamlit app, read the `progress.txt` file to update the progress bar:

```python
import subprocess
import streamlit as st
import time

def run_task_with_real_progress(script_name):
    # Start the task in a subprocess
    process = subprocess.Popen(['python', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    progress_bar = st.progress(0)

    while process.poll() is None:  # Process is still running
        try:
            with open("progress.txt", "r") as f:
                progress = int(f.read().strip())
                progress_bar.progress(progress / 100)
        except:
            pass  # Handle cases where progress.txt isn't yet available
        time.sleep(1)  # Adjust as needed

    stdout, stderr = process.communicate()
    return stdout if stdout else stderr

# Streamlit app
st.title("Run Python Script with Real-Time Progress")

if st.button("Run Task 1 with Real-Time Progress"):
    output = run_task_with_real_progress('task1.py')
    st.write("Output from task1.py:")
    st.code(output)
```

### Explanation:

- **task1.py** writes progress updates to `progress.txt`.
- The Streamlit app reads `progress.txt` and updates the progress bar.
- This approach provides real-time feedback based on the script’s actual
  progress, making it more accurate than an estimated time.

This setup allows you to display a dynamic progress bar while the task is
running, giving users real-time feedback on the script's progress.

## What if?

- What if i want to run a function with already tqdm progress bar and make it
  sync with streamlit progress bar show also how we call this function from
  task1.py for example

---

If you have a function with a `tqdm` progress bar, you can sync it with
Streamlit’s progress bar by updating the Streamlit progress bar within the loop
that `tqdm` iterates over. To do this, you'll need to modify the function to
accept an external Streamlit progress handler that will update the Streamlit
interface each time `tqdm` makes progress.

Here’s how to set it up:

1. **Define the function in `task1.py`**: Use `tqdm` within the function,
   passing an external Streamlit progress bar to update in real-time.

2. **Call the function in Streamlit**: Import and run the function from
   `task1.py` within your Streamlit app, updating the Streamlit progress bar
   alongside `tqdm`.

### Step 1: Modify `task1.py` to Include a Function with TQDM and Streamlit Sync

In `task1.py`, define the function, and pass in an optional `progress_bar` argument from Streamlit.

**task1.py:**

```python
from tqdm import tqdm
import time

def task_with_tqdm(iterations=100, progress_bar=None):
    for i in tqdm(range(iterations), desc="Processing"):
        # Simulate some work
        time.sleep(0.1)

        # Update Streamlit progress bar if provided
        if progress_bar:
            progress_bar.progress((i + 1) / iterations)

# This function can be called directly from Streamlit
```

In this example, `progress_bar.progress((i + 1) / iterations)` syncs the `tqdm`
progress with Streamlit’s progress bar if `progress_bar` is provided.

### Step 2: Call `task_with_tqdm` from Streamlit and Sync with Streamlit Progress Bar

In your Streamlit app, you can import `task_with_tqdm` from `task1.py`, create a
Streamlit progress bar, and pass it to `task_with_tqdm`.

**Streamlit app:**

```python
import streamlit as st
from task1 import task_with_tqdm  # Import the function from task1.py

# Streamlit app setup
st.title("Run Task with TQDM and Streamlit Progress Bar")

# Button to run the task
if st.button("Run Task 1"):
    # Create a Streamlit progress bar
    streamlit_progress_bar = st.progress(0)

    # Call the function, passing the Streamlit progress bar
    task_with_tqdm(iterations=100, progress_bar=streamlit_progress_bar)

    st.write("Task completed!")
```

### Explanation

- **Streamlit Progress Bar**: `st.progress(0)` initializes the progress bar in
  Streamlit.
- **Passing the Progress Bar**: `task_with_tqdm` accepts
  `streamlit_progress_bar` as an argument and updates it within each iteration
  of `tqdm`.
- **Syncing with TQDM**: The Streamlit progress bar advances with each step,
  giving real-time progress alongside `tqdm`.

This approach allows the Streamlit app’s progress bar to synchronize with
`tqdm`, giving users real-time feedback directly in the Streamlit interface.
