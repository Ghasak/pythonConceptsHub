# Method of Query Data From DataBase in Python

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Method of Query Data From DataBase in Python](#method-of-query-data-from-database-in-python)
    - [Show All methods for query from a database in python](#show-all-methods-for-query-from-a-database-in-python)
        - [**1. psycopg2**](#1-psycopg2)
            - [Code Example:](#code-example)
        - [**2. psycopg2 with Connection Pooling**](#2-psycopg2-with-connection-pooling)
            - [Code Example:](#code-example-1)
        - [**3. SQLite (Native)**](#3-sqlite-native)
            - [Code Example:](#code-example-2)
        - [**4. SQLAlchemy 2.0 Core**](#4-sqlalchemy-20-core)
            - [Code Example:](#code-example-3)
        - [**5. SQLAlchemy 2.0 ORM**](#5-sqlalchemy-20-orm)
            - [Code Example:](#code-example-4)
        - [**6. MySQL Connector**](#6-mysql-connector)
            - [Code Example:](#code-example-5)
        - [**7. PyODBC**](#7-pyodbc)
            - [Code Example:](#code-example-6)
        - [**8. Pandas with SQLAlchemy**](#8-pandas-with-sqlalchemy)
            - [Code Example:](#code-example-7)
        - [**Summary Table**](#summary-table)

<!-- markdown-toc end -->

## Show All methods for query from a database in python

All the ways to esablish a connection and query from a database
in python consider also the `sqlachemy 2.0` and then make me a table summary of
all these ways

---

Here is an overview of the common ways to establish a connection and query a
database in Python, including native libraries, ORM frameworks, and database
adapters like `psycopg2` and `SQLAlchemy 2.0`.

---

### **1. psycopg2**

- **Description**: A popular library for working with PostgreSQL databases in Python.
- **Usage**: Directly connects to PostgreSQL and allows manual query execution.

#### Code Example:

```python
import psycopg2

connection = psycopg2.connect(
    dbname="mydatabase",
    user="myuser",
    password="mypassword",
    host="localhost",
    port="5432"
)
cursor = connection.cursor()
cursor.execute("SELECT * FROM my_table;")
results = cursor.fetchall()
connection.close()
```

---

### **2. psycopg2 with Connection Pooling**

- **Description**: Efficiently manages database connections using pooling for
  better performance in multi-threaded environments.

#### Code Example:

```python
from psycopg2 import pool

connection_pool = pool.SimpleConnectionPool(
    1, 10,
    dbname="mydatabase",
    user="myuser",
    password="mypassword",
    host="localhost",
    port="5432"
)

connection = connection_pool.getconn()
cursor = connection.cursor()
cursor.execute("SELECT * FROM my_table;")
results = cursor.fetchall()
connection_pool.putconn(connection)
```

---

### **3. SQLite (Native)**

- **Description**: Python's built-in `sqlite3` module for lightweight databases.
- **Usage**: Works with SQLite databases only.

#### Code Example:

```python
import sqlite3

connection = sqlite3.connect("mydatabase.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM my_table;")
results = cursor.fetchall()
connection.close()
```

---

### **4. SQLAlchemy 2.0 Core**

- **Description**: Uses SQLAlchemy Core for querying databases programmatically while remaining close to raw SQL.
- **Usage**: Focuses on schema definitions and raw SQL execution.

#### Code Example:

```python
from sqlalchemy import create_engine, text

engine = create_engine("postgresql+psycopg2://myuser:mypassword@localhost/mydatabase")
with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM my_table"))
    for row in result:
        print(row)
```

---

### **5. SQLAlchemy 2.0 ORM**

- **Description**: Provides an ORM layer for working with objects instead of raw SQL.
- **Usage**: Simplifies complex relationships and schema management.

#### Code Example:

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class MyTable(Base):
    __tablename__ = "my_table"
    id = Column(Integer, primary_key=True)
    name = Column(String)

engine = create_engine("postgresql+psycopg2://myuser:mypassword@localhost/mydatabase")
Session = sessionmaker(bind=engine)
session = Session()

results = session.query(MyTable).all()
for row in results:
    print(row.name)
```

---

### **6. MySQL Connector**

- **Description**: Official MySQL connector for Python.
- **Usage**: Works with MySQL databases.

#### Code Example:

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="myuser",
    password="mypassword",
    database="mydatabase"
)
cursor = connection.cursor()
cursor.execute("SELECT * FROM my_table;")
results = cursor.fetchall()
connection.close()
```

---

### **7. PyODBC**

- **Description**: Connects to databases using ODBC drivers.
- **Usage**: General-purpose; works with multiple databases (SQL Server, PostgreSQL, etc.).

#### Code Example:

```python
import pyodbc

connection = pyodbc.connect(
    "DRIVER={PostgreSQL Unicode};SERVER=localhost;PORT=5432;DATABASE=mydatabase;UID=myuser;PWD=mypassword"
)
cursor = connection.cursor()
cursor.execute("SELECT * FROM my_table;")
results = cursor.fetchall()
connection.close()
```

---

### **8. Pandas with SQLAlchemy**

- **Description**: Reads data directly into Pandas DataFrames using SQLAlchemy.

#### Code Example:

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://myuser:mypassword@localhost/mydatabase")
df = pd.read_sql("SELECT * FROM my_table", engine)
print(df.head())
```

---

### **Summary Table**

| **Method**                 | **Description**                      | **Library**            | **Best For**                  |
| -------------------------- | ------------------------------------ | ---------------------- | ----------------------------- |
| **psycopg2**               | Native PostgreSQL connection         | `psycopg2`             | Direct query execution        |
| **psycopg2 Pooling**       | Connection pooling for performance   | `psycopg2.pool`        | Multi-threaded applications   |
| **SQLite**                 | Built-in SQLite module               | `sqlite3`              | Lightweight databases         |
| **SQLAlchemy Core**        | Schema and raw SQL execution         | `SQLAlchemy`           | Programmatic raw SQL          |
| **SQLAlchemy ORM**         | ORM for object-relational mapping    | `SQLAlchemy`           | Complex schemas and relations |
| **MySQL Connector**        | Official MySQL database connector    | `mysql.connector`      | MySQL databases               |
| **PyODBC**                 | ODBC-based connection                | `pyodbc`               | Multi-database compatibility  |
| **Pandas with SQLAlchemy** | Direct query results into DataFrames | `pandas`, `SQLAlchemy` | Data analysis and reporting   |

Let me know if you want more detailed code for any of these methods!
