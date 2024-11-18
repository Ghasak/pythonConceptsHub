# OOP calling class by name in Terminal

Manim is a Python-based mathematics engine. I noticed its design relies on
passing class names through the terminal to draw shapes, like circles. I will
elaborate on this design and provide an easy way to achieve something similar?

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [OOP calling class by name in Terminal](#oop-calling-class-by-name-in-terminal)
    - [Concept of class-based execution system](#concept-of-class-based-execution-system)
        - [**Key Design Principles**](#key-design-principles)
        - [**How to Create a Similar System**](#how-to-create-a-similar-system)
            - [**1. Define a Base Class**](#1-define-a-base-class)
            - [**2. Create Subclasses for Specific Shapes**](#2-create-subclasses-for-specific-shapes)
            - [**3. Add an Entry Script**](#3-add-an-entry-script)
            - [**4. Run Your Script**](#4-run-your-script)
        - [**Extensions and Improvements**](#extensions-and-improvements)
    - [benefit of this system design](#benefit-of-this-system-design)
        - [**Benefits of This Design**](#benefits-of-this-design)
            - [**1. Modular Design**](#1-modular-design)
            - [**2. Dynamism**](#2-dynamism)
            - [**3. Separation of Concerns**](#3-separation-of-concerns)
            - [**4. Scalability**](#4-scalability)
            - [**5. User-Friendliness**](#5-user-friendliness)
            - [**6. Testing and Debugging**](#6-testing-and-debugging)
            - [**7. Extensibility**](#7-extensibility)
            - [**8. Reusability**](#8-reusability)
        - [**Drawbacks to Consider**](#drawbacks-to-consider)
        - [**Summary Table**](#summary-table)
    - [Class-method exectuion system design ](#class-method-exectuion-system-design)
        - [**How to Let Users Specify a Method**](#how-to-let-users-specify-a-method)
            - [**1. Add Method Selection to the Entry Script**](#1-add-method-selection-to-the-entry-script)
            - [**2. Run the Script**](#2-run-the-script)
        - [**Benefits of Adding Method Selection**](#benefits-of-adding-method-selection)
        - [**Is This Pattern Common?**](#is-this-pattern-common)
            - [**Where This Pattern Is Used**](#where-this-pattern-is-used)
        - [**When to Use This Pattern**](#when-to-use-this-pattern)

<!-- markdown-toc end -->



---

## Concept of class-based execution system

The design pattern you observed in Manim, where you pass a class name in the
terminal to render animations or drawings, is based on a **class-based execution
system** combined with Python's ability to dynamically discover and run classes
or functions.

Here’s a breakdown of how this design works in Manim and how you can achieve
something similar in your own project:

---

### **Key Design Principles**

1. **Entry Point Script**:
   Manim has an entry script (like `manim`) that takes arguments from the
   command line, including the name of the class you want to execute.

2. **Dynamic Class Discovery**:
   The entry script dynamically imports and executes the class specified by the user.

3. **Inheritance and Overrides**:
   Each class typically inherits from a base class (like `Scene` in Manim),
   which provides essential methods for rendering.

4. **Command-Line Arguments**:
   Additional command-line arguments specify settings (e.g., resolution, output file).

---

### **How to Create a Similar System**

Here's how you can design a simple Python program that mimics this behavior:

#### **1. Define a Base Class**

Define a base class that provides the common functionality (e.g., drawing shapes).

```python
class BaseDrawing:
    def render(self):
        raise NotImplementedError("Subclasses must implement the render method!")
```

---

#### **2. Create Subclasses for Specific Shapes**

Create subclasses that inherit from the base class and implement the specific functionality.

```python
class DrawCircle(BaseDrawing):
    def render(self):
        print("Drawing a Circle!")

class DrawSquare(BaseDrawing):
    def render(self):
        print("Drawing a Square!")
```

---

#### **3. Add an Entry Script**

Create a script that dynamically loads and executes the class passed via the terminal.

```python
import sys

# Map class names to their implementations
CLASS_MAP = {
    "DrawCircle": DrawCircle,
    "DrawSquare": DrawSquare,
}

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <ClassName>")
        sys.exit(1)

    class_name = sys.argv[1]

    # Check if the class exists in the map
    if class_name not in CLASS_MAP:
        print(f"Error: Class '{class_name}' not found!")
        sys.exit(1)

    # Instantiate and run the class
    cls = CLASS_MAP[class_name]()
    cls.render()

if __name__ == "__main__":
    main()
```

---

#### **4. Run Your Script**

Save the code in a file (e.g., `drawing_script.py`) and run it from the terminal:

```bash
python drawing_script.py DrawCircle
# Output: Drawing a Circle!

python drawing_script.py DrawSquare
# Output: Drawing a Square!
```

---

### **Extensions and Improvements**

1. **Automatic Class Discovery**: Instead of manually maintaining `CLASS_MAP`,
   you can use Python’s `globals()` or dynamic imports.

2. **Command-Line Arguments Parsing**: Use libraries like `argparse` for better
   command-line argument handling.

3. **File Output**: Extend the `render` method to generate outputs (e.g., images
   or animations).

4. **Dynamic Imports**: You can dynamically import classes from separate files
   for scalability.

---

This is a simplified version of what Manim does. If you'd like a more advanced
design (e.g., dynamic imports, decorators), let me know, and I can expand
further!

---

## benefit of this system design

What are the benefits of using this design, and why should we choose it? Please
provide a summary table at the end.

This design offers several benefits, particularly for modularity, scalability,
and usability. Here's a detailed breakdown of why this design is useful,
followed by a summary table.

---

### **Benefits of This Design**

#### **1. Modular Design**

- Each class represents a specific task or functionality.
- Easy to add new features by simply creating a new class without modifying the main code.

#### **2. Dynamism**

- The program dynamically selects and executes the desired class at runtime.
- Reduces the need for hardcoded logic in the main script.

#### **3. Separation of Concerns**

- The entry script handles input and dispatching, while classes handle specific
  functionality.
- Keeps the codebase clean and organized.

#### **4. Scalability**

- As more features are added, new classes can be written independently.
- There's no need to rewrite or heavily modify existing logic.

#### **5. User-Friendliness**

- Users can specify the class to execute through simple terminal commands.
- Additional options can be provided via command-line arguments (e.g., file
  paths, settings).

#### **6. Testing and Debugging**

- Individual classes can be tested in isolation.
- Easier to debug a single component without affecting the rest of the system.

#### **7. Extensibility**

- New developers can quickly add new functionalities by adhering to a simple base-class structure.
- Libraries and plugins can integrate seamlessly with the system.

#### **8. Reusability**

- Common functionality can be placed in the base class, avoiding duplication
  across subclasses.
- Subclasses focus only on implementing their unique behavior.

---

### **Drawbacks to Consider**

While this design is highly beneficial, it may not be ideal for all use cases:

- **Overhead**: For simple projects, the overhead of dynamic class loading may
  not be justified.
- **Learning Curve**: New developers may need time to understand how the system
  dynamically maps and executes classes.

---

### **Summary Table**

| **Benefit**                | **Description**                                                                |
| -------------------------- | ------------------------------------------------------------------------------ |
| **Modular Design**         | Classes represent individual tasks, allowing isolated development and updates. |
| **Dynamism**               | Classes are dynamically loaded and executed based on user input.               |
| **Separation of Concerns** | Entry script handles dispatching, while classes handle specific functionality. |
| **Scalability**            | Easy to expand functionality by adding new classes without modifying the core. |
| **User-Friendliness**      | Users can specify tasks via terminal commands, enhancing usability.            |
| **Testing & Debugging**    | Classes can be tested and debugged independently, improving reliability.       |
| **Extensibility**          | New features or plugins can be added by creating subclasses.                   |
| **Reusability**            | Shared logic in the base class reduces code duplication.                       |

---

If you're working on a project where new features or components are frequently
added, or if you want to allow users to choose what the program should do
dynamically, this design is an excellent choice!

---

## Class-method exectuion system design 

Can the user also specify which method to run? Is this pattern also common?

Yes, the user can also specify which method to run within the chosen class by
extending the design slightly. This pattern is less common than selecting a
class because it requires exposing more control to the user, but it is highly
flexible and is often used in scripting engines, testing frameworks, and
CLI-based automation tools.

---

### **How to Let Users Specify a Method**

Here’s how you can modify the design:

#### **1. Add Method Selection to the Entry Script**

Instead of hardcoding which method to execute (e.g., `render`), let the user
specify the method name as an additional argument.

```python
import sys

# Map class names to their implementations
class BaseDrawing:
    def render(self):
        raise NotImplementedError("Subclasses must implement the render method!")

    def info(self):
        print("This is the base drawing class.")

class DrawCircle(BaseDrawing):
    def render(self):
        print("Drawing a Circle!")

    def area(self):
        print("Calculating area of the Circle!")

class DrawSquare(BaseDrawing):
    def render(self):
        print("Drawing a Square!")

    def perimeter(self):
        print("Calculating perimeter of the Square!")


CLASS_MAP = {
    "DrawCircle": DrawCircle,
    "DrawSquare": DrawSquare,
}

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <ClassName> <MethodName>")
        sys.exit(1)

    class_name = sys.argv[1]
    method_name = sys.argv[2]

    # Check if the class exists in the map
    if class_name not in CLASS_MAP:
        print(f"Error: Class '{class_name}' not found!")
        sys.exit(1)

    # Instantiate the class
    cls = CLASS_MAP[class_name]()

    # Check if the method exists in the class
    if not hasattr(cls, method_name):
        print(f"Error: Method '{method_name}' not found in class '{class_name}'!")
        sys.exit(1)

    # Execute the method
    method = getattr(cls, method_name)
    method()

if __name__ == "__main__":
    main()
```

---

#### **2. Run the Script**

You can now specify both the class and the method in the terminal:

```bash
python script.py DrawCircle render
# Output: Drawing a Circle!

python script.py DrawCircle area
# Output: Calculating area of the Circle!

python script.py DrawSquare render
# Output: Drawing a Square!

python script.py DrawSquare perimeter
# Output: Calculating perimeter of the Square!
```

---

### **Benefits of Adding Method Selection**

| **Benefit**               | **Description**                                                                 |
|----------------------------|---------------------------------------------------------------------------------|
| **Increased Flexibility**  | Users can invoke different methods without modifying the code.                  |
| **Simplifies Automation**  | Users can write scripts to call specific methods dynamically.                   |
| **Dynamic Workflows**      | Allows combining multiple methods into a sequence for complex workflows.        |

---

### **Is This Pattern Common?**

This pattern is **not as common** as selecting classes because:

1. **Security Risks**: Exposing method execution dynamically can lead to abuse
   if methods are not carefully managed.
2. **Complexity**: Requires users to know both the class and method names.
3. **Error Handling**: Increased chance of runtime errors if the method doesn't
   exist or has unexpected arguments.

#### **Where This Pattern Is Used**

- **Testing Frameworks** (e.g., `pytest`):
  - Run specific tests dynamically (`pytest test_file.py::test_method`).
- **Scripting Engines** (e.g., `Blender`, `Maya`):
  - Users can run specific scripts or functions from a CLI.
- **Command-Line Tools** (e.g., `Fabric` or `Invoke`):
  - Users can run specific tasks or methods dynamically.

---

### **When to Use This Pattern**

- When users need fine-grained control over what the program does.
- For task runners, testing tools, or interactive scripting systems.
- If your application requires exposing dynamic workflows or pipelines.

---

Let me know if you'd like to see a further extension of this design or examples
of integrating arguments into methods!
