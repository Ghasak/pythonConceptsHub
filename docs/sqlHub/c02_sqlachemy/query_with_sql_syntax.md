# SQL query directly

In SQLAlchemy, the `text()` construct is used for **executing raw SQL
statements** directly. It allows you to write SQL commands as text, providing
flexibility when you need to use specific SQL syntax that may not be easily
expressed in SQLAlchemy’s expression language. The `text()` construct can be
used in both **SQLAlchemy Core** and **SQLAlchemy ORM**.

### Overview of `text()` in SQLAlchemy

- **Purpose**: Enables direct SQL execution using raw SQL syntax.
- **Usage**: Commonly used for complex queries, database-specific SQL, or when
  you want to bypass SQLAlchemy’s query generation.
- **Compatibility**: Works with both SQLAlchemy Core and ORM.

### Syntax and Examples for `text()` in SQLAlchemy Core

In Core, `text()` can be used with the `engine.connect()` method to execute raw SQL statements.

1. **Basic Query with `text()`**:

   ```python
   from sqlalchemy import text

   with engine.connect() as conn:
       result = conn.execute(text("SELECT * FROM cars WHERE price < :price"), {"price": 21000})
       for row in result:
           print(row)
   ```

   - **Explanation**:
     - `text("SELECT * FROM cars WHERE price < :price")`: The SQL statement with a named placeholder (`:price`).
     - **Parameter Binding**: Passes `{"price": 21000}` to bind the `:price` parameter in the SQL.

2. **Inserting Data with `text()`**:

   ```python
   with engine.connect() as conn:
       conn.execute(text("INSERT INTO cars (make, model, year, price, is_sold) VALUES (:make, :model, :year, :price, :is_sold)"),
                    {"make": "Nissan", "model": "Altima", "year": 2022, "price": 25000, "is_sold": False})
       conn.commit()
   ```

   - Here, `text()` is used to insert a row, with named placeholders binding values for insertion.

### Syntax and Examples for `text()` in SQLAlchemy ORM

In ORM, `text()` is used with `session.execute()` to run raw SQL commands within a session.

1. **Basic Query with `text()`**:

   ```python
   from sqlalchemy.orm import Session
   from sqlalchemy import text

   with Session(engine) as session:
       result = session.execute(text("SELECT * FROM cars WHERE make = :make"), {"make": "Toyota"})
       for row in result:
           print(row)
   ```

2. **Updating Data with `text()` in ORM**:

   ```python
   with Session(engine) as session:
       session.execute(
           text("UPDATE cars SET price = :price WHERE model = :model"),
           {"price": 22000, "model": "Civic"}
       )
       session.commit()
   ```

3. **Explanation**:
   - **session.execute(text(...))**: Executes the raw SQL statement within the session.
   - **Committing**: Like other ORM operations, `session.commit()` is used to finalize changes.

### Comparison of `text()` in Core vs. ORM

| Feature               | SQLAlchemy Core                     | SQLAlchemy ORM                             |
| --------------------- | ----------------------------------- | ------------------------------------------ |
| Basic Query Execution | `conn.execute(text(...))`           | `session.execute(text(...))`               |
| Connection Handling   | Managed through `engine.connect()`  | Managed through `Session()`                |
| Parameter Binding     | Pass dictionary to `conn.execute()` | Pass dictionary to `session.execute()`     |
| Transaction Control   | Manual with `conn.commit()`         | Auto-managed within `session.commit()`     |
| Best Use Case         | Direct, low-level query execution   | When using raw SQL in ORM-managed sessions |

### Summary

- **Core and ORM Compatibility**: `text()` can be used in both SQLAlchemy Core
  and ORM.
- **Parameter Binding**: Supports named placeholders (e.g., `:parameter`) with
  dictionaries for parameter binding.
- **Transactional Control**: In Core, use `conn.commit()`; in ORM, manage with
  `session.commit()`.
- **Best Use Case**: Ideal for direct SQL statements that require control over
  the exact SQL syntax, often for performance optimization or custom queries.


