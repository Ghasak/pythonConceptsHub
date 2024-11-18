# Python with PostgreSQL - Deep
<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Python with PostgreSQL - Deep](#python-with-postgresql---deep)
    - [Concept](#concept)
        - [Step 1: Set Up PostgreSQL in Docker](#step-1-set-up-postgresql-in-docker)
        - [Step 2: Set Up SQLAlchemy](#step-2-set-up-sqlalchemy)
        - [Step 3: Define ORM Models for the Tables](#step-3-define-orm-models-for-the-tables)
        - [Step 4: CRUD Operations with ORM](#step-4-crud-operations-with-orm)
        - [Step 5: Querying in the Terminal](#step-5-querying-in-the-terminal)
        - [Step 6: Define Core Models](#step-6-define-core-models)
        - [CRUD with Core](#crud-with-core)
    - [ORM Queries Equvalent to SQL Syntax](#orm-queries-equvalent-to-sql-syntax)
        - [1. **Basic `SELECT` with `WHERE` Clause**](#1-basic-select-with-where-clause)
        - [2. **Using `AND`, `OR` Conditions**](#2-using-and-or-conditions)
        - [3. **`COUNT` Aggregation**](#3-count-aggregation)
        - [4. **`SUM` Aggregation**](#4-sum-aggregation)
        - [5. **`GROUP BY` with Aggregation**](#5-group-by-with-aggregation)
        - [6. **`JOIN` with Filtering**](#6-join-with-filtering)
        - [7. **Using `WITH` (Subquery)**](#7-using-with-subquery)
        - [8. **Ordering Results (`ORDER BY`)**](#8-ordering-results-order-by)
        - [9. **Using `LIMIT` and `OFFSET`**](#9-using-limit-and-offset)
        - [10. **`LIKE` (Pattern Matching)**](#10-like-pattern-matching)
        - [11. **`IN` Condition**](#11-in-condition)
        - [12. **`DISTINCT` Values**](#12-distinct-values)
        - [13. **`HAVING` Clause**](#13-having-clause)
        - [14. **Using `exists()` to Check for a Condition**](#14-using-exists-to-check-for-a-condition)
        - [15. **Delete with Filtering**](#15-delete-with-filtering)
        - [16. **Updating Multiple Rows**](#16-updating-multiple-rows)
        - [Summary of CRUD in ORM with Advanced Queries](#summary-of-crud-in-orm-with-advanced-queries)
    - [What else similar to .all method?](#what-else-similar-to-all-method)
        - [1. **`.first()`**](#1-first)
        - [2. **`.one()`**](#2-one)
        - [3. **`.one_or_none()`**](#3-one_or_none)
        - [4. **`.scalar()`**](#4-scalar)
        - [5. **`.limit(n)`**](#5-limitn)
        - [6. **`.offset(n)`**](#6-offsetn)
        - [7. **`.count()`**](#7-count)
        - [8. **`.exists()`**](#8-exists)
        - [9. **`.first_or_404()` (Flask-SQLAlchemy specific)**](#9-first_or_404-flask-sqlalchemy-specific)
        - [10. **`.fetchmany(size)` (Core-based approach)**](#10-fetchmanysize-core-based-approach)
        - [11. **`.yield_per(n)`**](#11-yield_pern)
    - [ORM - Template - very useful](#orm---template---very-useful)
        - [Full SQL Query with SQLAlchemy ORM Syntax](#full-sql-query-with-sqlalchemy-orm-syntax)
        - [Explanation of Each Part of the Query](#explanation-of-each-part-of-the-query)
        - [Functions Included](#functions-included)
    - [SQL template - Very Helpful](#sql-template---very-helpful)
        - [Full SQL Query Example](#full-sql-query-example)
        - [Explanation of Each Part of the Query](#explanation-of-each-part-of-the-query-1)
        - [Functions and Clauses Demonstrated](#functions-and-clauses-demonstrated)
    - [Generate Database](#generate-database)
        - [Step 1: Database Schema and Sample Data](#step-1-database-schema-and-sample-data)
            - [SQL Schema for the Tables](#sql-schema-for-the-tables)
            - [Sample Data](#sample-data)
        - [Step 2: Explanation of the Query and Expected Results](#step-2-explanation-of-the-query-and-expected-results)
            - [Full Query for Reference](#full-query-for-reference)
        - [Query Breakdown and Explanation](#query-breakdown-and-explanation)
        - [Final Result of the Query](#final-result-of-the-query)

<!-- markdown-toc end -->

## Concept

lets start with postgresql:
I want to create three tables using sqlachemy and python:

- For emplyee in a company
- Make arbrary tables such as activities, information , ..etc
- But using `postgresql` but should write and create to a docker container of postgresql
- Then show how I can query using python and then how to query in terminal
- Use always ORM model
- Then make similar using core
- Use all types of CRUD

To help you get started with PostgreSQL in a Docker container, using SQLAlchemy
and Python, here’s a step-by-step guide. This will cover setting up Docker,
creating tables with both ORM and Core approaches, and performing CRUD
operations in both Python and the terminal.

### Step 1: Set Up PostgreSQL in Docker

1. **Create a `docker-compose.yml` file** to set up a PostgreSQL container:

   ```yaml
   version: "3"
   services:
     db:
       image: postgres:latest
       environment:
         POSTGRES_USER: user
         POSTGRES_PASSWORD: password
         POSTGRES_DB: company_db
       ports:
         - "5432:5432"
   ```

2. **Run the Docker container**:

   ```bash
   docker-compose up -d
   ```

### Step 2: Set Up SQLAlchemy

Install SQLAlchemy and Psycopg2 (for PostgreSQL support):

```bash
pip install sqlalchemy psycopg2
```

### Step 3: Define ORM Models for the Tables

Let’s create three tables (`Employee`, `Activity`, and `Information`) as classes.

```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = "postgresql://user:password@localhost:5432/company_db"

# Connect to PostgreSQL
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define ORM models
class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

    activities = relationship("Activity", back_populates="employee")
    information = relationship("Information", back_populates="employee")


class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    activity_name = Column(String)
    employee_id = Column(Integer, ForeignKey('employees.id'))

    employee = relationship("Employee", back_populates="activities")


class Information(Base):
    __tablename__ = 'information'

    id = Column(Integer, primary_key=True)
    phone = Column(String)
    address = Column(String)
    employee_id = Column(Integer, ForeignKey('employees.id'))

    employee = relationship("Employee", back_populates="information")

# Create tables in the database
Base.metadata.create_all(engine)
```

### Step 4: CRUD Operations with ORM

1. **Create a session**:

   ```python
   Session = sessionmaker(bind=engine)
   session = Session()
   ```

2. **Create (Add) an Employee**:

   ```python
   new_employee = Employee(name="John Doe", email="john@example.com")
   session.add(new_employee)
   session.commit()
   ```

3. **Read (Query) Employees**:

   ```python
   employees = session.query(Employee).all()
   for employee in employees:
       print(employee.name, employee.email)
   ```

4. **Update an Employee**:

   ```python
   employee = session.query(Employee).filter_by(name="John Doe").first()
   employee.email = "john.doe@example.com"
   session.commit()
   ```

5. **Delete an Employee**:

   ```python
   employee = session.query(Employee).filter_by(name="John Doe").first()
   session.delete(employee)
   session.commit()
   ```

### Step 5: Querying in the Terminal

In the Docker container, you can connect to PostgreSQL via `psql`:

```bash
docker exec -it <container_id> psql -U user -d company_db
```

Once inside the PostgreSQL shell, you can use SQL commands to query:

- **Select all employees**:

  ```sql
  SELECT * FROM employees;
  ```

- **Update an employee’s email**:

  ```sql
  UPDATE employees SET email = 'john.doe@example.com' WHERE name = 'John Doe';
  ```

- **Delete an employee**:

  ```sql
  DELETE FROM employees WHERE name = 'John Doe';
  ```

### Step 6: Define Core Models

Using SQLAlchemy Core, tables can be created directly with SQL expressions.

```python
from sqlalchemy import MetaData, Table, Integer, String, Column

metadata = MetaData()

employees_table = Table(
    'employees', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String, unique=True)
)

activities_table = Table(
    'activities', metadata,
    Column('id', Integer, primary_key=True),
    Column('activity_name', String),
    Column('employee_id', Integer)
)

information_table = Table(
    'information', metadata,
    Column('id', Integer, primary_key=True),
    Column('phone', String),
    Column('address', String),
    Column('employee_id', Integer)
)

# Create tables
metadata.create_all(engine)
```

### CRUD with Core

1. **Insert an employee**:

   ```python
   insert_employee = employees_table.insert().values(name="Jane Doe", email="jane@example.com")
   engine.execute(insert_employee)
   ```

2. **Read employees**:

   ```python
   select_employees = employees_table.select()
   result = engine.execute(select_employees)
   for row in result:
       print(row)
   ```

3. **Update an employee**:

   ```python
   update_employee = employees_table.update().where(employees_table.c.name == "Jane Doe").values(email="jane.doe@example.com")
   engine.execute(update_employee)
   ```

4. **Delete an employee**:

   ```python
   delete_employee = employees_table.delete().where(employees_table.c.name == "Jane Doe")
   engine.execute(delete_employee)
   ```

This setup provides a comprehensive start to managing and querying a PostgreSQL
database in Docker using both SQLAlchemy ORM and Core approaches. Let me know if
you need any more specific examples or advanced use cases.

## ORM Queries Equvalent to SQL Syntax

Deep understanding over all possible querreis in ORM model:

- Using `GROUPBY`, `COUNT`, `SUM`, `WHERE` ..etc.
  Here are some advanced SQLAlchemy ORM queries that cover a range of operations
  such as filtering, aggregation, and using advanced clauses like `GROUP BY`,
  `COUNT`, `SUM`, and `WHERE`. For these examples, I'll assume that we are working
  with the `Employee`, `Activity`, and `Information` models defined previously.

### 1. **Basic `SELECT` with `WHERE` Clause**

Retrieve all employees with a specific condition, such as filtering by name.

```python
# Filter employees by name
employees_named_john = session.query(Employee).filter(Employee.name == "John Doe").all()
```

### 2. **Using `AND`, `OR` Conditions**

To add multiple conditions, you can use `and_` and `or_` from `sqlalchemy`.

```python
from sqlalchemy import and_, or_

# Filter by multiple conditions
employees_specific = session.query(Employee).filter(
    and_(Employee.name == "John Doe", Employee.email == "john@example.com")
).all()

# OR condition example
employees_or = session.query(Employee).filter(
    or_(Employee.name == "John Doe", Employee.name == "Jane Doe")
).all()
```

### 3. **`COUNT` Aggregation**

Count the number of employees.

```python
from sqlalchemy import func

# Count total employees
total_employees = session.query(func.count(Employee.id)).scalar()
```

### 4. **`SUM` Aggregation**

If we assume `Activity` has a `duration` column representing time spent on each activity, we could sum it up:

```python
# Sum of durations for all activities
total_duration = session.query(func.sum(Activity.duration)).scalar()
```

### 5. **`GROUP BY` with Aggregation**

Group activities by employee and count how many activities each employee has.

```python
# Group by employee and count activities
activity_count_by_employee = (
    session.query(Employee.name, func.count(Activity.id))
    .join(Activity)
    .group_by(Employee.id)
    .all()
)
```

### 6. **`JOIN` with Filtering**

Join `Employee` and `Activity` to get employees who participated in a specific activity.

```python
# Join Employee and Activity and filter by activity name
employee_activity = (
    session.query(Employee.name, Activity.activity_name)
    .join(Activity)
    .filter(Activity.activity_name == "Meeting")
    .all()
)
```

### 7. **Using `WITH` (Subquery)**

For complex queries, you can use subqueries. For example, find employees who have more than 3 activities.

```python
# Subquery for counting activities per employee
activity_count_subquery = (
    session.query(Activity.employee_id, func.count(Activity.id).label("activity_count"))
    .group_by(Activity.employee_id)
    .subquery()
)

# Query to find employees with more than 3 activities
employees_with_many_activities = (
    session.query(Employee)
    .join(activity_count_subquery, Employee.id == activity_count_subquery.c.employee_id)
    .filter(activity_count_subquery.c.activity_count > 3)
    .all()
)
```

### 8. **Ordering Results (`ORDER BY`)**

Order employees by name in ascending order.

```python
# Order by name
employees_ordered = session.query(Employee).order_by(Employee.name.asc()).all()
```

### 9. **Using `LIMIT` and `OFFSET`**

Limit results to a specific number and skip a few rows (pagination).

```python
# Get 5 employees, skipping the first 2
limited_employees = session.query(Employee).offset(2).limit(5).all()
```

### 10. **`LIKE` (Pattern Matching)**

Find employees with names that contain "John".

```python
# Pattern matching
employees_like = session.query(Employee).filter(Employee.name.like("%John%")).all()
```

### 11. **`IN` Condition**

Retrieve employees who have a name in a specified list.

```python
# Employees with name in the list
employees_in_list = session.query(Employee).filter(Employee.name.in_(["John Doe", "Jane Doe"])).all()
```

### 12. **`DISTINCT` Values**

Get distinct employee names (useful if there are duplicates).

```python
# Distinct employee names
distinct_names = session.query(Employee.name).distinct().all()
```

### 13. **`HAVING` Clause**

When using `GROUP BY`, you can filter the grouped data with `HAVING`.

```python
# Find employees who have more than 1 activity
employee_with_multiple_activities = (
    session.query(Employee.name, func.count(Activity.id).label("activity_count"))
    .join(Activity)
    .group_by(Employee.id)
    .having(func.count(Activity.id) > 1)
    .all()
)
```

### 14. **Using `exists()` to Check for a Condition**

Check if an employee has any activities without retrieving the activities.

```python
from sqlalchemy import exists

# Check if any employee has an activity
has_activity = session.query(Employee).filter(
    session.query(Activity).filter(Activity.employee_id == Employee.id).exists()
).all()
```

### 15. **Delete with Filtering**

Delete all employees who have no associated activities.

```python
# Delete employees with no activities
session.query(Employee).filter(~Employee.activities.any()).delete(synchronize_session=False)
session.commit()
```

### 16. **Updating Multiple Rows**

Update all employees’ emails to lowercase.

```python
# Bulk update emails to lowercase
session.query(Employee).update({Employee.email: func.lower(Employee.email)})
session.commit()
```

### Summary of CRUD in ORM with Advanced Queries

These queries should give you a robust foundation in querying using SQLAlchemy
ORM with advanced techniques. This approach is helpful for any relational
database operations in Python while maintaining ORM models. Let me know if you'd
like examples of other specific SQL constructs or scenarios!

## What else similar to .all method?

Aside from `.all()`, SQLAlchemy ORM provides several other ways to retrieve
query results, depending on the specific needs of your query. Here are some of
the common methods:

### 1. **`.first()`**

Retrieves the first result of the query or `None` if no result is found.

```python
# Get the first employee
first_employee = session.query(Employee).first()
```

### 2. **`.one()`**

Retrieves exactly one result. If there are no results or more than one result,
it will raise an exception (`NoResultFound` or `MultipleResultsFound`).

```python
# Get exactly one employee (raises an error if not exactly one match)
single_employee = session.query(Employee).filter(Employee.id == 1).one()
```

### 3. **`.one_or_none()`**

Retrieves one result or `None` if there are no results. Raises `MultipleResultsFound` if more than one result is found.

```python
# Get one employee or None
employee_or_none = session.query(Employee).filter(Employee.name == "John Doe").one_or_none()
```

### 4. **`.scalar()`**

Retrieves the first column of the first result, or `None` if no result is found.
This is useful for aggregate functions like `COUNT`, `SUM`, or if you're
querying a single column.

```python
# Get the count of employees
total_employees = session.query(func.count(Employee.id)).scalar()
```

### 5. **`.limit(n)`**

Limits the query results to `n` items.

```python
# Get the first 5 employees
limited_employees = session.query(Employee).limit(5).all()
```

### 6. **`.offset(n)`**

Skips the first `n` results and returns the remaining ones. This is often used with `limit` for pagination.

```python
# Skip the first 2 employees and get the next 5
offset_employees = session.query(Employee).offset(2).limit(5).all()
```

### 7. **`.count()`**

Returns the count of records matching the query criteria.

```python
# Count all employees
employee_count = session.query(Employee).count()
```

### 8. **`.exists()`**

Checks if any result exists for the given condition. You can combine `exists()` with `.scalar()` to get a boolean result.

```python
# Check if any employee named 'John Doe' exists
is_john_doe_exists = session.query(
    session.query(Employee).filter(Employee.name == "John Doe").exists()
).scalar()
```

### 9. **`.first_or_404()` (Flask-SQLAlchemy specific)**

For web applications using Flask-SQLAlchemy, this method returns the first
result or raises a 404 error if no result is found. Useful for web routes where
you want to return a 404 if a resource does not exist.

```python
# Flask-SQLAlchemy only: get employee or 404 error
employee = Employee.query.filter_by(name="John Doe").first_or_404()
```

### 10. **`.fetchmany(size)` (Core-based approach)**

While this is more common in Core (not ORM), `.fetchmany()` lets you retrieve a
specified number of rows from the result set if you're working directly with raw
SQL statements or a `ResultProxy`.

```python
# Fetch 10 rows at a time
result = session.execute("SELECT * FROM employees").fetchmany(10)
```

### 11. **`.yield_per(n)`**

Optimizes memory usage by loading results in batches of `n`. This is useful for
large queries that you want to load in chunks.

```python
# Load employees in batches of 1000
for employee in session.query(Employee).yield_per(1000):
    print(employee.name)
```

Each of these methods can be combined and adapted depending on your query
requirements, from retrieving all results at once to fetching specific items or
limiting rows based on pagination needs.

## ORM - Template - very useful

Here's a comprehensive SQLAlchemy ORM query that includes a variety of SQL
concepts like `WITH`, `JOIN`, `GROUP BY`, `HAVING`, and several aggregate
functions. This query is written in Python using SQLAlchemy's ORM API, but it
closely follows SQL syntax and combines various features in a single, lengthy
example.

In this example, let’s assume:

- The `Employee` table contains columns like `id`, `name`, `salary`.
- The `Activity` table contains `id`, `employee_id`, `activity_name`, `hours_spent`.
- The `Information` table contains `id`, `employee_id`, `phone`, `address`.

### Full SQL Query with SQLAlchemy ORM Syntax

```python
from sqlalchemy import func, case
from sqlalchemy.orm import aliased
from sqlalchemy.sql import label
from sqlalchemy import and_, or_

# Create an alias for a subquery
activity_alias = aliased(Activity)

# Subquery to get employees with more than a specific number of activities
activity_count_subquery = (
    session.query(
        Activity.employee_id,
        func.count(Activity.id).label("activity_count")
    )
    .group_by(Activity.employee_id)
    .having(func.count(Activity.id) > 3)
    .subquery()
)

# Main query that uses WITH, JOIN, GROUP BY, HAVING, and aggregates
query = (
    session.query(
        Employee.name.label("employee_name"),                # SELECT employee name
        func.sum(Activity.hours_spent).label("total_hours"), # SUM of hours spent on activities
        func.avg(Employee.salary).label("avg_salary"),       # AVG salary
        func.min(Employee.salary).label("min_salary"),       # MIN salary
        func.max(Employee.salary).label("max_salary"),       # MAX salary
        func.count(Activity.id).label("activity_count"),     # COUNT of activities
        func.coalesce(Information.phone, "N/A").label("phone"), # COALESCE to handle NULL values in phone
        case(
            [(Employee.salary > 100000, "High")], else_="Low"
        ).label("salary_level") # CASE for salary level
    )
    .join(Activity, Employee.id == Activity.employee_id)      # INNER JOIN with Activity
    .outerjoin(Information, Employee.id == Information.employee_id) # LEFT OUTER JOIN with Information
    .join(activity_count_subquery, Employee.id == activity_count_subquery.c.employee_id) # Join with subquery
    .filter(Employee.salary > 50000)                          # WHERE clause
    .filter(or_(Employee.name.like("J%"), Employee.name.like("A%"))) # OR condition
    .group_by(Employee.id)                                    # GROUP BY employee id
    .having(func.sum(Activity.hours_spent) > 10)              # HAVING clause
    .order_by(Employee.name.asc())                            # ORDER BY employee name
    .limit(10)                                                # LIMIT 10
    .offset(5)                                                # OFFSET 5
)

# Execute the query and fetch results
results = query.all()

# Print results
for result in results:
    print(result)
```

### Explanation of Each Part of the Query

1. **WITH (Subquery)**: We used `activity_count_subquery` as an alias to count activities for each employee. This acts as a `WITH` clause in SQL, helping to filter employees based on activity count.

2. **JOIN**:

   - `JOIN` with `Activity` table on `employee_id` to get activities related to each employee.
   - `OUTER JOIN` with `Information` to include employees who may or may not have an associated `Information` record.
   - Another `JOIN` with the subquery to filter employees based on the number of activities.

3. **SELECT Clauses**:

   - Basic columns like `Employee.name`.
   - Aggregate functions:
     - `SUM`: Total hours spent on activities.
     - `AVG`, `MIN`, `MAX`: Salary-related statistics.
     - `COUNT`: Counts activities for each employee.
   - `COALESCE`: Defaults to "N/A" if `Information.phone` is `NULL`.
   - `CASE`: Classifies salary level as "High" or "Low".

4. **WHERE and OR Conditions**:

   - Filters employees with `salary > 50000`.
   - Filters names starting with "J" or "A" using `or_`.

5. **GROUP BY**:

   - Groups by `Employee.id` to aggregate activity information per employee.

6. **HAVING**:

   - Applies a `HAVING` clause to filter employees with more than 10 hours spent on activities.

7. **ORDER BY**:

   - Orders employees by `name` in ascending order.

8. **LIMIT and OFFSET**:
   - Limits results to 10 rows, skipping the first 5 rows (for pagination).

### Functions Included

- `SUM`, `AVG`, `MIN`, `MAX`, `COUNT`: Aggregate functions.
- `COALESCE`: For handling `NULL` values.
- `CASE`: For conditional expressions.
- `LIKE`, `OR`, `AND`: For conditional logic in `WHERE` clauses.

This single query demonstrates SQL standards and best practices for complex
queries using SQLAlchemy ORM, covering nearly all SQL keywords and functions.
Let me know if you need more specific examples of other functions!

## SQL template - Very Helpful

- Can you give me same for SQL itself without ORM?

Here's a comprehensive SQL query that uses various SQL keywords and functions,
including `WITH`, `JOIN`, `GROUP BY`, `HAVING`, `ORDER BY`, and aggregates. This
query should cover a wide range of SQL features and provide an example of an
advanced query structure.

### Full SQL Query Example

```sql
WITH activity_count AS (
    SELECT
        employee_id,
        COUNT(id) AS activity_count
    FROM
        activities
    GROUP BY
        employee_id
    HAVING
        COUNT(id) > 3
)

SELECT
    e.name AS employee_name,                      -- SELECT employee name
    SUM(a.hours_spent) AS total_hours,            -- SUM of hours spent on activities
    AVG(e.salary) AS avg_salary,                  -- AVG salary
    MIN(e.salary) AS min_salary,                  -- MIN salary
    MAX(e.salary) AS max_salary,                  -- MAX salary
    COUNT(a.id) AS activity_count,                -- COUNT of activities
    COALESCE(i.phone, 'N/A') AS phone,            -- COALESCE to handle NULL values in phone
    CASE
        WHEN e.salary > 100000 THEN 'High'
        ELSE 'Low'
    END AS salary_level                           -- CASE for salary level
FROM
    employees e
JOIN
    activities a ON e.id = a.employee_id          -- INNER JOIN with activities
LEFT JOIN
    information i ON e.id = i.employee_id         -- LEFT JOIN with information
JOIN
    activity_count ac ON e.id = ac.employee_id    -- JOIN with the subquery (activity_count)
WHERE
    e.salary > 50000                              -- WHERE clause
    AND (e.name LIKE 'J%' OR e.name LIKE 'A%')    -- OR condition for name filter
GROUP BY
    e.id                                          -- GROUP BY employee id
HAVING
    SUM(a.hours_spent) > 10                       -- HAVING clause
ORDER BY
    e.name ASC                                    -- ORDER BY employee name
LIMIT 10                                          -- LIMIT 10
OFFSET 5;                                         -- OFFSET 5
```

### Explanation of Each Part of the Query

1. **WITH Clause (Subquery)**:

   - The `WITH` clause defines a Common Table Expression (CTE) named `activity_count`, which counts the activities for each `employee_id` and includes only employees with more than 3 activities (`HAVING COUNT(id) > 3`).

2. **SELECT Clauses**:

   - `e.name AS employee_name`: Selects and aliases `name` from `employees` as `employee_name`.
   - `SUM(a.hours_spent)`: Calculates the total hours spent by each employee on activities.
   - `AVG`, `MIN`, `MAX`: Calculates average, minimum, and maximum salary.
   - `COUNT(a.id)`: Counts the number of activities associated with each employee.
   - `COALESCE(i.phone, 'N/A')`: Uses `COALESCE` to display "N/A" if `phone` is `NULL`.
   - `CASE`: Classifies employees into "High" or "Low" salary level based on a threshold.

3. **JOINs**:

   - `JOIN activities a ON e.id = a.employee_id`: Joins `employees` with `activities` based on `employee_id`.
   - `LEFT JOIN information i ON e.id = i.employee_id`: Left joins `information`, including employees even if they lack `information` records.
   - `JOIN activity_count ac ON e.id = ac.employee_id`: Joins with the `activity_count` CTE to filter employees based on activity count.

4. **WHERE Clause**:

   - Filters employees with `salary > 50000` and names starting with "J" or "A".

5. **GROUP BY**:

   - Groups results by `e.id`, allowing aggregate functions like `SUM`, `AVG`, and `COUNT` to operate on each group.

6. **HAVING Clause**:

   - Filters groups to include only those with `SUM(a.hours_spent) > 10` hours spent on activities.

7. **ORDER BY**:

   - Orders results by `employee_name` in ascending order.

8. **LIMIT and OFFSET**:
   - Limits the result to 10 rows and skips the first 5 rows (for pagination).

### Functions and Clauses Demonstrated

- **Aggregate functions**: `SUM`, `AVG`, `MIN`, `MAX`, `COUNT`.
- **Conditional expressions**: `COALESCE` (to handle `NULL` values), `CASE` (for conditional logic).
- **Filtering**: `WHERE` and `HAVING` clauses.
- **Pattern matching**: `LIKE` (for filtering names by pattern).
- **Pagination**: `LIMIT` and `OFFSET`.

This SQL query demonstrates a variety of SQL standards and keywords, making it
suitable for complex data extraction tasks from a relational database. Let me
know if you need more details on any specific part!

## Generate Database

Generate a database for the query bone and then make explanations for each part
and what is the result if the query of each step and final result of the query
make the table up to 20 entries
To set up a database for this example, I'll first create tables and populate them with sample data that align with the query structure. I'll walk through the setup and then explain each part of the query, showing expected intermediate and final results.

### Step 1: Database Schema and Sample Data

Let's create three tables: `employees`, `activities`, and `information`. Each table will have up to 20 entries as specified.

#### SQL Schema for the Tables

```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    salary INTEGER
);

CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(id),
    activity_name VARCHAR(50),
    hours_spent INTEGER
);

CREATE TABLE information (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(id),
    phone VARCHAR(15),
    address VARCHAR(100)
);
```

#### Sample Data

Here’s a set of sample data to populate each table.

```sql
-- Populate employees
INSERT INTO employees (name, salary) VALUES
('John Doe', 120000), ('Jane Smith', 90000), ('Alice Johnson', 80000),
('Bob Brown', 50000), ('Charlie Green', 110000), ('David White', 60000),
('Emily Black', 95000), ('Frank Hall', 40000), ('Grace King', 130000),
('Hannah Lee', 70000);

-- Populate activities
INSERT INTO activities (employee_id, activity_name, hours_spent) VALUES
(1, 'Meeting', 5), (1, 'Coding', 15), (2, 'Documentation', 8),
(3, 'Design', 12), (3, 'Meeting', 6), (4, 'Testing', 10),
(4, 'Support', 3), (5, 'Development', 20), (6, 'Planning', 5),
(7, 'Analysis', 9), (7, 'Support', 11), (8, 'Research', 7),
(8, 'Development', 4), (9, 'Prototyping', 8), (10, 'Training', 10);

-- Populate information
INSERT INTO information (employee_id, phone, address) VALUES
(1, '123-456-7890', '123 Main St'), (2, '987-654-3210', '456 Oak St'),
(3, '555-123-4567', '789 Pine St'), (5, '555-765-4321', '321 Maple Ave'),
(6, '555-987-6543', '654 Birch Rd'), (7, '555-321-9876', '987 Cedar St');
```

### Step 2: Explanation of the Query and Expected Results

Let's break down each part of the query and describe its role and expected
intermediate results.

#### Full Query for Reference

```sql
WITH activity_count AS (
    SELECT
        employee_id,
        COUNT(id) AS activity_count
    FROM
        activities
    GROUP BY
        employee_id
    HAVING
        COUNT(id) > 3
)

SELECT
    e.name AS employee_name,
    SUM(a.hours_spent) AS total_hours,
    AVG(e.salary) AS avg_salary,
    MIN(e.salary) AS min_salary,
    MAX(e.salary) AS max_salary,
    COUNT(a.id) AS activity_count,
    COALESCE(i.phone, 'N/A') AS phone,
    CASE
        WHEN e.salary > 100000 THEN 'High'
        ELSE 'Low'
    END AS salary_level
FROM
    employees e
JOIN
    activities a ON e.id = a.employee_id
LEFT JOIN
    information i ON e.id = i.employee_id
JOIN
    activity_count ac ON e.id = ac.employee_id
WHERE
    e.salary > 50000
    AND (e.name LIKE 'J%' OR e.name LIKE 'A%')
GROUP BY
    e.id
HAVING
    SUM(a.hours_spent) > 10
ORDER BY
    e.name ASC
LIMIT 10
OFFSET 5;
```

### Query Breakdown and Explanation

1. **`WITH` Clause (Common Table Expression `activity_count`)**:

   - **Purpose**: This subquery calculates the count of activities for each employee and filters only employees with more than 3 activities.
   - **Intermediate Result**:
     - Only employees with `activity_count > 3` will appear in the `activity_count` CTE. Based on our sample data, this will include employees with a high count of activities (adjust data as needed for your own environment).

2. **Main Query `SELECT` Statement**:

   - **Fields and Aggregates**:
     - `e.name AS employee_name`: Selects the employee's name.
     - `SUM(a.hours_spent) AS total_hours`: Calculates the total hours an employee has spent on all activities.
     - `AVG(e.salary) AS avg_salary`: Calculates the average salary of the group (since we're grouping by employee, it’s the salary of each employee).
     - `MIN(e.salary) AS min_salary` and `MAX(e.salary) AS max_salary`: Gets the minimum and maximum salary values.
     - `COUNT(a.id) AS activity_count`: Counts the number of activities associated with each employee.
     - `COALESCE(i.phone, 'N/A') AS phone`: Displays the employee’s phone number if it exists; otherwise, it shows "N/A".
     - `CASE WHEN e.salary > 100000 THEN 'High' ELSE 'Low' END AS salary_level`: Classifies salary as "High" or "Low".

3. **JOIN Clauses**:

   - **`JOIN activities a ON e.id = a.employee_id`**: Matches each employee with their activities.
   - **`LEFT JOIN information i ON e.id = i.employee_id`**: Includes phone and address information if available.
   - **`JOIN activity_count ac ON e.id = ac.employee_id`**: Ensures only employees with more than 3 activities are included, based on the `WITH` clause.

4. **`WHERE` Clause**:

   - Filters employees with a salary greater than 50,000 and names starting with "J" or "A".

5. **`GROUP BY` Clause**:

   - Groups by `e.id`, allowing aggregate functions to operate on each employee individually.

6. **`HAVING` Clause**:

   - Filters to include only employees with more than 10 hours spent on activities.

7. **`ORDER BY`, `LIMIT`, and `OFFSET`**:
   - Orders by `employee_name` in ascending order, retrieves up to 10 results, and skips the first 5 (useful for pagination).

### Final Result of the Query

- **Expected Final Output**: The result will include up to 10 employees who meet all conditions (e.g., names starting with "J" or "A", salary > 50,000, more than 3 activities, and total hours spent on activities > 10). The output columns will be:
  - `employee_name`, `total_hours`, `avg_salary`, `min_salary`, `max_salary`, `activity_count`, `phone`, and `salary_level`.

This query showcases complex SQL operations by combining filtering, aggregation,
joining, and conditional logic to produce specific data insights about employees
and their activities. Let me know if you'd like any additional details or
clarification on specific parts!
