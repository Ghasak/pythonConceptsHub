# What is Session in SQL

Great! Now that we understand **connections** (`conn`), let’s move on to **sessions**—a key component in SQLAlchemy, especially when using the ORM (Object-Relational Mapping) approach.

### What is a Session?

In SQLAlchemy, a **Session** is an interface that manages interactions between your Python code and the database. It acts as a staging area for all database operations, including **transactions** (a sequence of operations that are executed as a unit). The Session can be seen as a “workspace” where objects are created, updated, and deleted before changes are saved to the database.

### Key Differences: When to Use a Session vs. Connection

1. **Connections (`conn`)**:

   - Connections are created directly with `engine.connect()`.
   - They’re used for executing **raw SQL queries** and are part of the **Core** approach.
   - Typically used when you want to run **isolated, stateless SQL commands** that don’t need to be managed in transactions or object states.

2. **Sessions**:
   - Sessions are created using `sessionmaker` and are meant to manage **transactions** and **ORM objects**.
   - They’re useful when working with **database objects as Python objects** (ORM).
   - Sessions automatically handle commits and rollbacks for **transactions** (groups of operations that succeed or fail together).
   - They support **batch operations** on multiple objects and keep track of changes until you commit.

### Step 1: Setting Up the Session

To use sessions in SQLAlchemy, start by creating a `sessionmaker` linked to your engine.

```python
from sqlalchemy.orm import sessionmaker

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a session instance
session = Session()
```

### Step 2: Using Sessions to Perform Transactions

Let’s look at examples of creating, querying, updating, and deleting data with a session.

#### Example 1: Creating (Inserting) Data

With the ORM, we work with classes that represent tables. Here’s an example of adding a new row to an `Employee` table:

```python
# Define the Employee class (ORM model)
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Add a new employee
new_employee = Employee(name="Alice")
session.add(new_employee)
session.commit()  # Save to the database
```

#### Example 2: Querying Data

```python
# Query all employees
employees = session.query(Employee).all()
for employee in employees:
    print(employee.name)
```

#### Example 3: Updating Data

```python
# Update an employee's name
employee_to_update = session.query(Employee).filter_by(name="Alice").first()
employee_to_update.name = "Alicia"
session.commit()  # Commit the change
```

#### Example 4: Deleting Data

```python
# Delete an employee
employee_to_delete = session.query(Employee).filter_by(name="Alicia").first()
session.delete(employee_to_delete)
session.commit()  # Commit the deletion
```

### Key Methods and Their Uses

- **`add()`**: Adds an object to the session, preparing it for insertion into the database.
- **`commit()`**: Saves all pending changes to the database.
- **`rollback()`**: Undoes any uncommitted changes.
- **`query()`**: Allows you to query ORM-mapped classes.

### Table Summary: Session vs. Connection

Here’s a table that outlines the differences, when to use each, and how they work.

| Aspect                  | **Connection (`conn`)**                                                                                                                                         | **Session**                                                                                                                   |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Purpose**             | Execute isolated, low-level SQL statements.                                                                                                                     | Manage ORM objects, transactions, and batch operations.                                                                       |
| **Usage**               | Use with `engine.connect()`.                                                                                                                                    | Use with `sessionmaker` and `Session` instance.                                                                               |
| **Best for**            | Simple, stateless SQL queries.                                                                                                                                  | Complex, stateful transactions and ORM object manipulation.                                                                   |
| **Transaction Control** | Each connection command is independent; no automatic transactions.                                                                                              | Manages transactions automatically; use `commit()` and `rollback()`.                                                          |
| **ORM Support**         | No.                                                                                                                                                             | Yes, specifically designed for ORM operations.                                                                                |
| **Typical Methods**     | `execute()`, `fetchall()`, `scalar_one()`.                                                                                                                      | `add()`, `query()`, `commit()`, `rollback()`, `delete()`.                                                                     |
| **Performance**         | Slightly faster for single, direct SQL statements.                                                                                                              | More overhead due to transaction management, but necessary for ORM.                                                           |
| **Example**             | `python<br>with engine.connect() as conn:<br> &nbsp; &nbsp;result = conn.execute(text("SELECT * FROM employee"))<br> &nbsp; &nbsp;rows = result.fetchall()<br>` | `python<br>session = Session()<br>new_employee = Employee(name="Alice")<br>session.add(new_employee)<br>session.commit()<br>` |

### Summary

- Use **Connections** for straightforward, single SQL statements or when working with SQLAlchemy Core.
- Use **Sessions** for transactions, ORM, and managing multiple changes as a single unit.

Next, we can dive into building models with the ORM or explore Core functions for more advanced SQL if you'd like!

