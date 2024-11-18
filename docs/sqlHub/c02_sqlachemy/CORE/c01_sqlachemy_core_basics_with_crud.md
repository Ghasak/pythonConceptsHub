# SQLAlchemy Core

Let’s dive into **SQLAlchemy Core** from Part 1, covering its
foundational concepts. Unlike the ORM, SQLAlchemy Core is a lower-level API
focused on SQL expressions and manual query construction, offering fine-grained
control over SQL generation and execution.

---

## Suggested Title for Notes

**Title**: `"SQLAlchemy Core Basics - Building a Car Inventory Database (Part 1)"`

---

### Summary of Part 1: Core Basics and Setting Up Tables

**Summary**:
In this section, we’ll set up a car inventory system using SQLAlchemy Core. We’ll:

1. **Set Up the Engine**: Define the connection to the database.
2. **Define Tables with MetaData and Table Objects**: Learn to manually define tables and columns.
3. **Create Tables**: Use Core functions to create tables directly in the database.
4. **Insert Data**: Add initial car records to test our setup.

This will give you a strong foundation in SQLAlchemy Core, preparing you to work with tables and manage data at a low level.

---

### Step 1: Setting Up the Engine

In SQLAlchemy Core, the **Engine** is the core interface to the database, and
unlike in the ORM, we don’t need a base class or sessions for setup.

1. **Define the Engine**:

   ```python
   from sqlalchemy import create_engine

   DATABASE_URL = "postgresql+psycopg2://admin:admin@localhost:5432/mydatabase"
   engine = create_engine(DATABASE_URL, echo=True)
   ```

2. **Explanation**:
   - **Engine**: Connects directly to the database and executes queries. The `echo=True` flag logs each SQL statement.

---

### Step 2: Defining Tables with MetaData and Table Objects

In SQLAlchemy Core, we define tables using `MetaData` and `Table` objects, specifying columns, types, and constraints manually.

1. **Set Up MetaData and Define a Car Table**:

   ```python
   from sqlalchemy import MetaData, Table, Column, Integer, String, Float, Boolean

   # MetaData instance stores information about tables and schemas
   metadata = MetaData()

   # Define the Car table
   cars_table = Table(
       "cars", metadata,
       Column("id", Integer, primary_key=True),
       Column("make", String, nullable=False),
       Column("model", String, nullable=False),
       Column("year", Integer, nullable=False),
       Column("price", Float, nullable=False),
       Column("is_sold", Boolean, default=False)
   )
   ```

2. **Explanation**:
   - **MetaData**: Holds information about tables and their structure.
   - **Table**: Represents a table in the database.
   - **Columns**: Define attributes for each table (e.g., `id`, `make`, `model`).

---

### Step 3: Creating Tables in the Database

After defining tables, we use the `create_all()` method to create tables in the database.

1. **Create the Tables**:

   ```python
   # Use metadata.create_all() to create tables in the database
   metadata.create_all(engine)
   ```

2. **Explanation**:
   - `create_all(engine)` inspects `metadata` and creates any tables defined but not yet present in the database.

---

### Step 4: Inserting Data with Core

With tables created, we can now insert data using SQLAlchemy Core’s `insert()` function.

1. **Insert a Single Record**:

   ```python
   from sqlalchemy import insert

   # Insert a new car into the cars table
   insert_statement = insert(cars_table).values(
       make="Toyota",
       model="Corolla",
       year=2020,
       price=20000,
       is_sold=False
   )

   # Execute the statement
   with engine.connect() as conn:
       conn.execute(insert_statement)
       conn.commit()
   ```

2. **Insert Multiple Records**:

   ```python
   with engine.connect() as conn:
       conn.execute(insert(cars_table), [
           {"make": "Honda", "model": "Civic", "year": 2019, "price": 18000, "is_sold": False},
           {"make": "Ford", "model": "Focus", "year": 2021, "price": 22000, "is_sold": False}
       ])
       conn.commit()
   ```

3. **Explanation**:
   - **`insert()`**: Creates an `INSERT` statement for the table.
   - **`conn.execute()`**: Executes the statement directly on the database.
   - **`conn.commit()`**: Commits the transaction to save changes.

---

### Example Usage in `__main__`

Here’s how to test each setup step within the `if __name__ == "__main__"` block:

```python
if __name__ == "__main__":
    # Create tables
    metadata.create_all(engine)

    # Insert sample data
    with engine.connect() as conn:
        # Insert a single car
        conn.execute(insert(cars_table).values(
            make="Toyota", model="Corolla", year=2020, price=20000, is_sold=False
        ))

        # Insert multiple cars
        conn.execute(insert(cars_table), [
            {"make": "Honda", "model": "Civic", "year": 2019, "price": 18000, "is_sold": False},
            {"make": "Ford", "model": "Focus", "year": 2021, "price": 22000, "is_sold": False}
        ])
        conn.commit()
```

### Summary of Part 1

- **Engine**: Set up the database connection with `create_engine()`.
- **Table Definition**: Use `MetaData` and `Table` to define tables and columns.
- **Table Creation**: Use `metadata.create_all(engine)` to create tables in the database.
- **Data Insertion**: Use `insert()` to add data to tables directly.

This foundational setup provides the essentials for working with SQLAlchemy
Core, giving you a lower-level but powerful interface for database
interactions. In the next part, we can look at **querying data** with Core,
covering `select` statements and filters. Let me know if you’d like to proceed!

---

Let’s extend **Part 1** to include **CRUD operations** in SQLAlchemy Core. In
SQLAlchemy Core, you can use Pythonic methods to construct SQL expressions, but
you also have the option to execute raw SQL if needed—both are considered part
of SQLAlchemy Core.

---

### Suggested Title for Notes

**Title**: `"SQLAlchemy Core Basics with CRUD Operations (Part 1)"`

---

### Summary of Part 1: Core Basics with CRUD Operations

**Summary**:
This section covers foundational concepts in SQLAlchemy Core, including setting up tables and performing CRUD operations. You’ll learn:

1. How to **define and create tables**.
2. **Performing CRUD operations** (Create, Read, Update, Delete) using Core’s expression language.
3. **Executing raw SQL queries** for cases where direct SQL syntax is preferred.

This setup will give you control over data management at a low level, using both SQLAlchemy’s constructs and raw SQL as needed.

---

### Step 1: Setting Up the Engine and Defining Tables

As covered previously, let’s start by setting up the **Engine** and defining the **cars_table** with **MetaData** and **Table** objects.

```python
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean, insert

DATABASE_URL = "postgresql+psycopg2://admin:admin@localhost:5432/mydatabase"
engine = create_engine(DATABASE_URL, echo=True)
metadata = MetaData()

# Define the Car table
cars_table = Table(
    "cars", metadata,
    Column("id", Integer, primary_key=True),
    Column("make", String, nullable=False),
    Column("model", String, nullable=False),
    Column("year", Integer, nullable=False),
    Column("price", Float, nullable=False),
    Column("is_sold", Boolean, default=False)
)

# Create tables in the database
metadata.create_all(engine)
```

---

### Step 2: CRUD Operations with SQLAlchemy Core

With the table defined, let’s perform CRUD operations (Create, Read, Update, Delete) using SQLAlchemy Core.

#### Create (Insert Data)

1. **Inserting a Single Record**:

   ```python
   with engine.connect() as conn:
       conn.execute(insert(cars_table).values(
           make="Toyota", model="Corolla", year=2020, price=20000, is_sold=False
       ))
       conn.commit()
   ```

2. **Inserting Multiple Records**:

   ```python
   with engine.connect() as conn:
       conn.execute(insert(cars_table), [
           {"make": "Honda", "model": "Civic", "year": 2019, "price": 18000, "is_sold": False},
           {"make": "Ford", "model": "Focus", "year": 2021, "price": 22000, "is_sold": False}
       ])
       conn.commit()
   ```

#### Read (Select Data)

1. **Select All Records**:

   ```python
   from sqlalchemy import select

   with engine.connect() as conn:
       result = conn.execute(select(cars_table))
       for row in result:
           print(row)
   ```

2. **Select Records with Filtering**:

   ```python
   with engine.connect() as conn:
       stmt = select(cars_table).where(cars_table.c.cars_table.c.price < 21000)
       result = conn.execute(stmt)
       for row in result:
           print(row)
   ```

#### Update (Modify Data)

1. **Update a Single Record**:

   ```python
   from sqlalchemy import update

   with engine.connect() as conn:
       stmt = update(cars_table).where(cars_table.c.model == "Corolla").values(price=19000)
       conn.execute(stmt)
       conn.commit()
   ```

2. **Update Multiple Records**:

   ```python
   with engine.connect() as conn:
       stmt = update(cars_table).where(cars_table.c.is_sold == False).values(is_sold=True)
       conn.execute(stmt)
       conn.commit()
   ```

#### Delete (Remove Data)

1. **Delete a Single Record**:

   ```python
   from sqlalchemy import delete

   with engine.connect() as conn:
       stmt = delete(cars_table).where(cars_table.c.model == "Focus")
       conn.execute(stmt)
       conn.commit()
   ```

2. **Delete All Records**:

   ```python
   with engine.connect() as conn:
       conn.execute(delete(cars_table))
       conn.commit()
   ```

---

### Step 3: Executing Raw SQL Queries

SQLAlchemy Core also allows executing raw SQL queries. This can be helpful when working with complex SQL statements or performance-critical code.

1. **Example of Raw SQL for Inserting Data**:

   ```python
   with engine.connect() as conn:
       conn.execute("INSERT INTO cars (make, model, year, price, is_sold) VALUES ('Mazda', 'MX-5', 2021, 25000, false)")
       conn.commit()
   ```

2. **Example of Raw SQL for Reading Data**:

   ```python
   with engine.connect() as conn:
       result = conn.execute("SELECT * FROM cars WHERE price < 21000")
       for row in result:
           print(row)
   ```

3. **Explanation**:
   - **Raw SQL Queries**: Using direct SQL statements with `conn.execute()` provides full SQL flexibility while still leveraging SQLAlchemy for connection management.

---

### Example Usage in `__main__`

Here’s a sample block for testing each CRUD function and raw SQL query.

```python
if __name__ == "__main__":
    # Create tables
    metadata.create_all(engine)

    # Insert records
    with engine.connect() as conn:
        # Insert a single car
        conn.execute(insert(cars_table).values(
            make="Toyota", model="Corolla", year=2020, price=20000, is_sold=False
        ))

        # Insert multiple cars
        conn.execute(insert(cars_table), [
            {"make": "Honda", "model": "Civic", "year": 2019, "price": 18000, "is_sold": False},
            {"make": "Ford", "model": "Focus", "year": 2021, "price": 22000, "is_sold": False}
        ])
        conn.commit()

    # Read records
    with engine.connect() as conn:
        result = conn.execute(select(cars_table))
        for row in result:
            print(row)

    # Update records
    with engine.connect() as conn:
        conn.execute(update(cars_table).where(cars_table.c.model == "Civic").values(price=19000))
        conn.commit()

    # Delete records
    with engine.connect() as conn:
        conn.execute(delete(cars_table).where(cars_table.c.model == "Focus"))
        conn.commit()

    # Execute raw SQL
    with engine.connect() as conn:
        conn.execute("INSERT INTO cars (make, model, year, price, is_sold) VALUES ('Mazda', 'MX-5', 2021, 25000, false)")
        result = conn.execute("SELECT * FROM cars WHERE price < 21000")
        for row in result:
            print(row)
```

### Summary of Part 1

- **Engine**: Connect to the database with `create_engine()`.
- **Defining Tables**: Use `MetaData` and `Table` to define and structure tables.
- **CRUD Operations**: Perform CRUD operations with Core expressions (`insert`, `select`, `update`, `delete`).
- **Raw SQL Queries**: Use `conn.execute()` to run raw SQL queries when direct SQL syntax is preferred.

With these tools, SQLAlchemy Core provides you with flexible, low-level access to manage and manipulate data efficiently. In the next part, we can focus on **querying data** in more depth, covering filtering, ordering, and grouping in Core. Let me know if you’d like to proceed!
