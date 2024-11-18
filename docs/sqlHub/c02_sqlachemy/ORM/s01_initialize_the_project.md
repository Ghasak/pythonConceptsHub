# SQLachmed in Action

To get started with SQLAlchemy 2.0, let's begin by understanding
**connections**—the foundation for working with databases in SQLAlchemy.

### What is a Connection?

In SQLAlchemy, a **connection** represents a single, established link between
your Python application and a database. SQLAlchemy handles the connection
through an **Engine**, which is the core interface to the database and is
responsible for managing connections.

### Step 1: Creating the Engine

In SQLAlchemy 2.0, the first step in almost any database interaction is to
create an **Engine**. The Engine provides a central object for connecting to
the database and sending SQL queries.

Here’s how you can create an Engine:

```python
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://admin:admin@localhost:5432/mydatabase"

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)
```

- `DATABASE_URL`: The URL format includes the driver (e.g., `psycopg2`),
  username, password, host, port, and database name.

- `echo=True`: This enables SQL logging, showing the raw SQL being sent to the
  database, which is helpful for debugging.

### Step 2: Using `engine.connect()` to Create a Connection

Once you have an engine, you can use `engine.connect()` to establish a connection to the database.

```python
# Open a connection to the database
with engine.connect() as conn:
    result = conn.execute(text("SELECT 'Hello, world!' AS message"))
    hello = result.scalar_one()
    print(hello)  # Should print 'Hello, world!'
```

#### Explanation

- `with engine.connect() as conn`: The `with` statement here ensures that the
  connection (`conn`) is properly closed after the block is exited, even if an
  error occurs.
- `conn.execute(...)`: This runs a SQL command. Here, we use it to send a
  simple “Hello, world!” message.
- `result.scalar_one()`: This fetches the result of the query, returning a
  single scalar value.

### Step 3: Performing a Basic Query with a Connection

After establishing the connection, you can execute SQL queries. Here’s an
example of querying all rows from a table called `employee`:

```py
from sqlalchemy import text

with engine.connect() as conn:
    # Execute a query to fetch all records in the "employee" table
    result = conn.execute(text("SELECT * FROM employee"))
    rows = result.fetchall()

    for row in rows:
        print(row)
```

#### Explanation of Query Methods

- **`text("...")`**: Used to write raw SQL queries. SQLAlchemy also has ways to
  build SQL statements dynamically, but `text` is useful for direct SQL.
- **`result.fetchall()`**: Fetches all rows from the query result.

### Summary

- **Engine**: Central object to manage database connections.
- **Connection**: Created with `engine.connect()` and used to execute queries.
- **Query Execution**: `conn.execute()` runs a SQL query; `text()` enables raw SQL commands.

### What’s Next?

After understanding basic connections and executing queries, the next steps
would include:

1. Understanding **Session Management** (for transactions and ORM use).
2. Performing CRUD operations in a structured way (Create, Read, Update,
   Delete).

Let me know if you'd like to explore sessions next or go deeper into using
`conn` for more complex queries.

## URL for connection

```py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://admin:admin@localhost:5432/mydatabase"
# Create the synchronous engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a session factory
Session = sessionmaker(bind=engine)

print("Hello")


# Function to connect and query the database
def test_connection():
    with Session() as session:
        # Run a simple query to confirm the connection
        result = session.execute(text("SELECT 'Hello, world!' AS message"))
        hello = result.scalar_one()
        print(hello)  # Should print 'Hello, world!'

        # Query a given table, replace 'your_table' with your actual table name
        query_result = session.execute(text("SELECT * FROM employee"))
        rows = query_result.fetchall()

        for row in rows:
            print(row)


def test_connection2():
    session = Session()
    # Run a simple query to confirm the connection
    result = session.execute(text("SELECT 'Hello, world!' AS message"))
    hello = result.scalar_one()
    print(hello)  # Should print 'Hello, world!'

    # Query a given table, replace 'your_table' with your actual table name
    query_result = session.execute(text("SELECT * FROM employee"))
    rows = query_result.fetchall()

    for row in rows:
        print(row)

    session.close()


# Run the connection test
if __name__ == "__main__":
    #test_connection()
    test_connection2()

```
