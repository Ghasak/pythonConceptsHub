# PostgreSQL with python
<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [PostgreSQL with python](#postgresql-with-python)
    - [Concept](#concept)
        - [Step 1: Install SQLAlchemy and psycopg2](#step-1-install-sqlalchemy-and-psycopg2)
        - [Step 2: Set Up the Connection URL](#step-2-set-up-the-connection-url)
        - [Step 3: Connecting to PostgreSQL with SQLAlchemy](#step-3-connecting-to-postgresql-with-sqlalchemy)
            - [Using Python Interactive Shell (PyCon or Standard Python Shell)](#using-python-interactive-shell-pycon-or-standard-python-shell)
            - [Alternative: Using SQLAlchemy ORM to Interact with the Database](#alternative-using-sqlalchemy-orm-to-interact-with-the-database)
    - [Inisight](#inisight)
        - [Connection URL Formats for Other Databases](#connection-url-formats-for-other-databases)
        - [Summary Table](#summary-table)
        - [Explanation of Parts in URL](#explanation-of-parts-in-url)
    - [Real life scenario](#real-life-scenario)
        - [Step 1: Install Required Libraries](#step-1-install-required-libraries)
        - [Step 2: Define the Database Connection and ORM Model](#step-2-define-the-database-connection-and-orm-model)
        - [Step 3: Initial Load of Employee Data](#step-3-initial-load-of-employee-data)
        - [Step 4: Incremental (Delta) Load](#step-4-incremental-delta-load)
        - [Step 5: Verify the Data](#step-5-verify-the-data)
        - [Explanation of the Steps](#explanation-of-the-steps)

<!-- markdown-toc end -->

## Concept

Let's now use Python with SQLAlchemy to connect to this database within the
container. My Python environment is from a virtual environment on my local
machine.

Show me the possible connection methods, especially using PyCon or something
similar with PostgreSQL. I believe the URL includes "+" between the components.

To connect to your PostgreSQL container from Python using SQLAlchemy, you’ll
need to set up the correct connection URL and use the `psycopg2` or `asyncpg`
driver. Since SQLAlchemy requires a driver to connect to PostgreSQL, the
connection URL typically includes `+psycopg2` or `+asyncpg`.

Here’s how to set this up.

### Step 1: Install SQLAlchemy and psycopg2

If you haven’t already, activate your virtual environment and install SQLAlchemy
and the PostgreSQL driver `psycopg2`:

```bash
pip install sqlalchemy psycopg2
```

### Step 2: Set Up the Connection URL

In SQLAlchemy, the connection URL format for PostgreSQL is:

```plaintext
postgresql+psycopg2://username:password@host:port/database
```

Given your setup, here’s what the connection URL will look like:

```python
connection_url = "postgresql+psycopg2://myuser:mypassword@localhost:5432/mydatabase"
```

### Step 3: Connecting to PostgreSQL with SQLAlchemy

Once you have the connection URL, you can use SQLAlchemy’s `create_engine`
function to connect to the database. Here’s how you can do it interactively in a
Python session (like PyCon or Jupyter) or in a script:

#### Using Python Interactive Shell (PyCon or Standard Python Shell)

1. Open your Python shell:

   ```bash
   python
   ```

2. Run the following code to establish a connection and check it:

   ```python
   from sqlalchemy import create_engine

   # Define the connection URL
   connection_url = "postgresql+psycopg2://myuser:mypassword@localhost:5432/mydatabase"

   # Create the engine
   engine = create_engine(connection_url)

   # Test the connection
   try:
       with engine.connect() as connection:
           print("Connection successful!")
   except Exception as e:
       print(f"Connection failed: {e}")
   ```

This code will print “Connection successful!” if the database is accessible from
your local machine.

#### Alternative: Using SQLAlchemy ORM to Interact with the Database

If you’re working in a Python script or want to create tables and perform
operations, here’s an example of using SQLAlchemy’s ORM.

```python
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the connection URL
connection_url = "postgresql+psycopg2://myuser:mypassword@localhost:5432/mydatabase"

# Create the engine
engine = create_engine(connection_url)

# Define a base class for ORM models
Base = declarative_base()

# Define an example table model
class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    salary = Column(Float)

# Create tables in the database (if they don't exist already)
Base.metadata.create_all(engine)

# Set up a session
Session = sessionmaker(bind=engine)
session = Session()

# Example: Add a new employee
new_employee = Employee(first_name="John", last_name="Doe", age=30, gender="Male", salary=50000.00)
session.add(new_employee)
session.commit()

# Query the employees
employees = session.query(Employee).all()
for emp in employees:
    print(emp.first_name, emp.last_name, emp.age, emp.gender, emp.salary)

# Close the session
session.close()
```

This script:

- Creates an SQLAlchemy engine using your connection URL.
- Defines an `Employee` table model.
- Creates tables in the database.
- Adds a new employee and queries all employees in the `employee` table.

With these steps, you’ll be able to connect to PostgreSQL in your Docker
container from a local Python environment using SQLAlchemy.

## Inisight

Explain to me the url why this `+` and meaning of two things in this url which
are postgresql and psycopg2? then show all other types of url connection for
other databasees using python like with mysql, redist, mongodb, and also make a
table summary for these

In SQLAlchemy’s connection URL, `postgresql+psycopg2://` uses two parts:

1. **`postgresql`**: This part specifies the **database type** or **dialect**
   that SQLAlchemy should use. It tells SQLAlchemy to expect PostgreSQL as the
   database.

2. **`+psycopg2`**: This specifies the **database driver** or **DBAPI** that
   SQLAlchemy should use to connect to PostgreSQL. `psycopg2` is a popular
   driver for PostgreSQL in Python.

The `+` is necessary to separate the dialect (`postgresql`) from the driver
(`psycopg2`), as SQLAlchemy supports multiple drivers for some databases.

---

### Connection URL Formats for Other Databases

Each database in SQLAlchemy (or other libraries) follows a similar URL pattern. Here are some common ones:

| Database       | SQLAlchemy URL Format                                                                 | Description                                        |
| -------------- | ------------------------------------------------------------------------------------- | -------------------------------------------------- |
| **PostgreSQL** | `postgresql+psycopg2://username:password@host:port/database`                          | Uses `psycopg2` driver for PostgreSQL              |
| **MySQL**      | `mysql+pymysql://username:password@host:port/database`                                | Uses `pymysql` driver for MySQL                    |
| **SQLite**     | `sqlite:///path/to/database.db`                                                       | Direct access to a SQLite file; no hostname needed |
| **Oracle**     | `oracle+cx_oracle://username:password@host:port/?sid=database`                        | Uses `cx_oracle` driver for Oracle                 |
| **SQL Server** | `mssql+pyodbc://username:password@host/database?driver=ODBC+Driver+17+for+SQL+Server` | Uses `pyodbc` with ODBC driver for SQL Server      |
| **Redis**      | `redis://username:password@host:port`                                                 | Uses `redis-py` to connect to Redis                |
| **MongoDB**    | `mongodb://username:password@host:port/database`                                      | Connects to MongoDB using MongoDB’s connection URI |

### Summary Table

| Database   | Example Connection URL                                                           | Library / Driver                   |
| ---------- | -------------------------------------------------------------------------------- | ---------------------------------- |
| PostgreSQL | `postgresql+psycopg2://user:pass@localhost:5432/dbname`                          | `psycopg2`                         |
| MySQL      | `mysql+pymysql://user:pass@localhost:3306/dbname`                                | `pymysql`                          |
| SQLite     | `sqlite:///path/to/database.db`                                                  | Built-in SQLite                    |
| Oracle     | `oracle+cx_oracle://user:pass@localhost:1521/?sid=dbname`                        | `cx_oracle`                        |
| SQL Server | `mssql+pyodbc://user:pass@localhost/dbname?driver=ODBC+Driver+17+for+SQL+Server` | `pyodbc`                           |
| Redis      | `redis://user:pass@localhost:6379`                                               | `redis-py`                         |
| MongoDB    | `mongodb://user:pass@localhost:27017/dbname`                                     | MongoDB URI (e.g., with `pymongo`) |

### Explanation of Parts in URL

- **Database Type**: Specifies the type of database you’re connecting to (e.g.,
  `postgresql`, `mysql`, `sqlite`).
- **Driver**: Indicates which driver SQLAlchemy (or another library) should use
  to connect to the database.
- **Username, Password, Host, Port, Database**: Authentication details and
  location for the database server.

These connection URLs allow SQLAlchemy (or other Python libraries) to connect
seamlessly with different databases by just changing the database type and
driver.

## Real life scenario

Using python provide me a table connect to database then to a table,
and

- Show how you will increment a delta load which comes as a pd dataframe
- Use the example of employee
- Add uuid for each employee
- Use also ORm

To set up a delta load incrementally in a PostgreSQL database using Python and
SQLAlchemy ORM, I'll show you how to:

1. **Define a table model with UUIDs** for each employee.
2. **Connect to the database** and **load initial data**.
3. **Incrementally add new records** (delta load) from a `pandas` DataFrame.
4. **Generate UUIDs** for each employee entry.

Let’s go step by step.

### Step 1: Install Required Libraries

Make sure you have `sqlalchemy`, `psycopg2`, and `pandas` installed in your environment.

```bash
pip install sqlalchemy psycopg2 pandas
```

### Step 2: Define the Database Connection and ORM Model

1. **Connect to PostgreSQL using SQLAlchemy** with the ORM.
2. **Define the `Employee` model** with a UUID.

Here’s the code:

```python
import pandas as pd
import uuid
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define database connection URL
connection_url = "postgresql+psycopg2://myuser:mypassword@localhost:5432/mydatabase"
engine = create_engine(connection_url)

# Define ORM base and session
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define the Employee model with a UUID primary key
class Employee(Base):
    __tablename__ = 'employee'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(50))
    last_name = Column(String(50))
    age = Column(Integer)
    gender = Column(String(10))
    salary = Column(Float)

# Create the table if it does not exist
Base.metadata.create_all(engine)
```

### Step 3: Initial Load of Employee Data

Let’s assume you have initial data in a `pandas` DataFrame. Load it into the `employee` table.

```python
# Sample initial data in a DataFrame
initial_data = pd.DataFrame({
    "first_name": ["Alice", "Bob", "Carol"],
    "last_name": ["Smith", "Johnson", "Davis"],
    "age": [30, 40, 27],
    "gender": ["Female", "Male", "Female"],
    "salary": [75000.00, 80000.00, 62000.00]
})

# Insert initial data
for _, row in initial_data.iterrows():
    employee = Employee(
        first_name=row['first_name'],
        last_name=row['last_name'],
        age=row['age'],
        gender=row['gender'],
        salary=row['salary']
    )
    session.add(employee)
session.commit()
```

### Step 4: Incremental (Delta) Load

Assume the new incremental data comes in as a `pandas` DataFrame with new or
updated records. We’ll add only the new entries by checking if they already
exist (you could adjust this logic for updates as needed).

```python
# Sample delta data (new employees)
delta_data = pd.DataFrame({
    "first_name": ["David", "Eve"],
    "last_name": ["Wilson", "Brown"],
    "age": [35, 29],
    "gender": ["Male", "Female"],
    "salary": [85000.00, 70000.00]
})

# Insert delta data, assuming uniqueness based on name (for simplicity)
for _, row in delta_data.iterrows():
    # Check if the employee already exists (based on name and age for this example)
    existing_employee = session.query(Employee).filter_by(
        first_name=row['first_name'],
        last_name=row['last_name'],
        age=row['age']
    ).first()

    # Add new employee only if they do not exist
    if not existing_employee:
        new_employee = Employee(
            first_name=row['first_name'],
            last_name=row['last_name'],
            age=row['age'],
            gender=row['gender'],
            salary=row['salary']
        )
        session.add(new_employee)

session.commit()
```

### Step 5: Verify the Data

To check the contents of the `employee` table after loading:

```python
# Query and display all employees
employees = session.query(Employee).all()
for emp in employees:
    print(emp.id, emp.first_name, emp.last_name, emp.age, emp.gender, emp.salary)
```

### Explanation of the Steps

1. **Initial Load**: We insert records from the initial DataFrame.
2. **Delta Load**: For each new record in the delta DataFrame, we check if it
   already exists (based on a unique identifier such as name and age). If it
   doesn’t, we add it.
3. **UUID**: Each `Employee` entry has a UUID primary key, automatically
   generated for new entries.

This setup supports a delta load while preventing duplicates. You can refine the
“existence check” logic based on your actual requirements for identifying unique
records.
