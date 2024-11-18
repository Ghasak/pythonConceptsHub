# SQLAlchemy in Action

## Things to be consider always

- [x] Index
- [x] ORM relationships
- [x] docker container for a given database while store databases locally.

## TODO

With the fundamentals and advanced topics covered, here are a few directions you could take next:

1. **Testing and Mocking with SQLAlchemy**:

   - Learn techniques for testing database interactions, including using
     in-memory SQLite databases and mocking for isolated tests.

2. **Asynchronous SQLAlchemy**:

   - Explore SQLAlchemy’s asynchronous API for high-performance, concurrent
     applications, ideal for web applications handling multiple requests
     simultaneously.

3. **Working with Migrations (Alembic)**:

   - Dive into schema migrations with Alembic, SQLAlchemy’s official migration
     tool, which helps manage schema changes over time.

4. **Advanced Querying with CTEs and Window Functions**:

   - Explore Common Table Expressions (CTEs) and window functions for complex
     analytical queries.

5. **Caching Strategies**:
   - Implement caching mechanisms to store frequently accessed data, reducing
     database load for read-heavy applications.

Let me know if any of these topics interests you, or if there’s another area
you’d like to explore!

6. about async with sqlalchemy such as `asyncpg` driver for postgres
   [here](https://magicstack.github.io/asyncpg/current/usage.html).

---

## Differences between ORM and CORE

Here’s a table summarizing the differences between **SQLAlchemy Core** and **SQLAlchemy ORM**, focusing on syntax, API methods, and usage patterns. This table covers method comparisons and highlights the differences in query building and data retrieval techniques.

| Feature                        | SQLAlchemy Core                                  | SQLAlchemy ORM                                   |
| ------------------------------ | ------------------------------------------------ | ------------------------------------------------ |
| **Primary Abstraction**        | **Explicit SQL Constructs**                      | **Object-Relational Mapping**                    |
| **Connection Management**      | `engine.connect()`                               | `Session()` with `sessionmaker()`                |
| **Model Definition**           | `Table` object in `MetaData()`                   | Python classes inheriting from `Base`            |
| **Defining Columns**           | `Column` with types in `Table`                   | `Column` in class definition                     |
| **Example Table Definition**   | `cars_table = Table("cars", MetaData(), ...)`    | `class Car(Base): __tablename__ = "cars"`        |
| **Data Insertion (Single)**    | `insert(cars_table).values(...)`                 | `session.add(new_car)`                           |
| **Data Insertion (Multiple)**  | `conn.execute(insert(cars_table), [dicts...])`   | `session.add_all([objects...])`                  |
| **Data Retrieval - All Rows**  | `conn.execute(select(cars_table)).fetchall()`    | `session.query(Car).all()`                       |
| **Data Retrieval - One Row**   | `conn.execute(select(cars_table)).fetchone()`    | `session.query(Car).first()`                     |
| **Data Retrieval - Filtering** | `select(cars_table).where(...)`                  | `session.query(Car).filter(...)`                 |
| **Executing Queries**          | `conn.execute(query)`                            | Implicit with `session.query()`                  |
| **Committing Changes**         | `conn.commit()`                                  | `session.commit()`                               |
| **Rollback Transaction**       | `conn.rollback()`                                | `session.rollback()`                             |
| **Update Data**                | `conn.execute(update(cars_table).values(...))`   | `session.query(Car).filter(...).update(...)`     |
| **Delete Data**                | `conn.execute(delete(cars_table).where(...))`    | `session.query(Car).filter(...).delete()`        |
| **Row Fetching Methods**       | `.fetchall()` for all rows                       | `.all()` for all results                         |
|                                | `.fetchone()` for a single row                   | `.first()` for the first result                  |
|                                | `.fetchmany(size=n)` for multiple rows           | N/A                                              |
| **Lazy/Eager Loading**         | Not applicable                                   | `joinedload`, `subqueryload` in relationships    |
| **Method for Raw SQL**         | `conn.execute("SQL Statement")`                  | `session.execute("SQL Statement")`               |
| **Transaction Control**        | Explicit with `begin()` and `commit()`           | Implicitly managed by `Session()`                |
| **Batch Insertion**            | `conn.execute(insert(...), [values...])`         | `session.bulk_insert_mappings()`                 |
| **Aggregations**               | `select(func.count(...))`                        | `session.query(func.count(...))`                 |
| **Execution Style**            | Low-level SQL execution with explicit constructs | High-level, Pythonic ORM with object handling    |
| **Data Retrieval as Objects**  | Returns `Row` objects or tuples                  | Returns ORM model objects (`Car` instances)      |
| **Best for**                   | Complex SQL, Performance-sensitive apps          | Object-Oriented Data Manipulation, Relationships |

---

### Key Differences in Fetching and Execution Methods

1. **Core Fetching Methods**:

   - `.fetchall()`: Fetches all results as a list of `Row` objects.
   - `.fetchone()`: Fetches the next single result as a `Row`.
   - `.fetchmany(size=n)`: Fetches a list with up to `n` results.

2. **ORM Fetching Methods**:
   - `.all()`: Returns all results as a list of ORM model instances.
   - `.first()`: Returns the first result as a model instance or `None`.
   - **Relationships**: With lazy loading, related data isn’t fetched until
     accessed, while eager loading (`joinedload`, `subqueryload`) preloads
     related data.

### Additional Notes

- **SQL Syntax in Core vs. ORM**:
  - **Core** allows **direct SQL syntax** using `conn.execute("SQL Statement")`,
    which is also compatible in ORM with `session.execute("SQL Statement")`.
- **Transaction Control**:
  - **Core** requires explicit transaction management (`conn.begin()`), while
    **ORM** sessions handle transactions implicitly.

---
