# SQL Fundamentals

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [SQL Fundamentals](#sql-fundamentals)
    - [Concept](#concept)
        - [1. **SELECT Queries**](#1-select-queries)
        - [2. **INSERT Query**](#2-insert-query)
        - [3. **UPDATE Query**](#3-update-query)
        - [4. **DELETE Query**](#4-delete-query)
        - [5. **JOINs**](#5-joins)
        - [6. **Subqueries**](#6-subqueries)
        - [7. **UNION and UNION ALL**](#7-union-and-union-all)
        - [8. **GROUP BY and Aggregations**](#8-group-by-and-aggregations)
        - [9. **ALTER Table**](#9-alter-table)
        - [10. **CREATE and DROP Statements**](#10-create-and-drop-statements)
        - [11. **Transactions**](#11-transactions)
        - [12. **Views**](#12-views)
        - [13. **CASE Statement**](#13-case-statement)
        - [14. **Window Functions**](#14-window-functions)
        - [15. **EXISTS and NOT EXISTS**](#15-exists-and-not-exists)
        - [**SQL Query to Get Drivers Who Joined After 2021**](#sql-query-to-get-drivers-who-joined-after-2021)
        - [**Explanation:**](#explanation)
        - [**SQL Query to Group Drivers' Deliveries and Calculate Success Rate**](#sql-query-to-group-drivers-deliveries-and-calculate-success-rate)
        - [**Explanation:**](#explanation-1)
    - [Insight - 1](#insight---1)
        - [1. **Using `CASE` Statements (Conditional Columns)**](#1-using-case-statements-conditional-columns)
        - [2. **Using `COALESCE()` (Handling Null Values)**](#2-using-coalesce-handling-null-values)
        - [3. **Using `IF` Statements (MySQL Specific)**](#3-using-if-statements-mysql-specific)
        - [4. **Using Mathematical Operations on Columns**](#4-using-mathematical-operations-on-columns)
        - [5. **Using String Manipulation (e.g., `CONCAT()`)**](#5-using-string-manipulation-eg-concat)
        - [6. **Using `AS` (Column Aliases)**](#6-using-as-column-aliases)
        - [7. **Using Window Functions for Calculated Columns**](#7-using-window-functions-for-calculated-columns)
        - [8. **Using Subqueries to Generate New Columns**](#8-using-subqueries-to-generate-new-columns)
    - [**1. Identify Duplicate Records**](#1-identify-duplicate-records)
    - [**2. Delete Duplicate Records (Keeping One Record)**](#2-delete-duplicate-records-keeping-one-record)
        - [**Query to Remove Duplicates:**](#query-to-remove-duplicates)
    - [**3. Remove Duplicates Using `DISTINCT` in a Query**](#3-remove-duplicates-using-distinct-in-a-query)
    - [**4. Aggregate Data for Duplicates**](#4-aggregate-data-for-duplicates)
    - [**5. Use `UNIQUE` Constraint to Prevent Future Duplicates**](#5-use-unique-constraint-to-prevent-future-duplicates)
    - [**6. Insert Unique Records Only (`INSERT IGNORE` or `ON CONFLICT`)**](#6-insert-unique-records-only-insert-ignore-or-on-conflict)

<!-- markdown-toc end -->

## Concept

Here’s a comprehensive overview of SQL syntax to cover the most common query
types. This guide includes the structure and key elements used in SQL queries,
ranging from basic SELECT queries to more advanced concepts like joins,
subqueries, and transactions.

---

### 1. **SELECT Queries**

**Retrieve data from a table.**

```sql
SELECT column1, column2, ...
FROM table_name
WHERE condition
GROUP BY column1, column2
HAVING condition
ORDER BY column1 [ASC|DESC]
LIMIT n OFFSET m;
```

**Example:**

```sql
SELECT first_name, last_name
FROM employees
WHERE department = 'Sales'
ORDER BY last_name ASC
LIMIT 10 OFFSET 5;
```

---

### 2. **INSERT Query**

**Insert new rows into a table.**

```sql
INSERT INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...);
```

**Example:**

```sql
INSERT INTO employees (first_name, last_name, salary)
VALUES ('John', 'Doe', 50000);
```

---

### 3. **UPDATE Query**

**Modify existing rows in a table.**

```sql
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;
```

**Example:**

```sql
UPDATE employees
SET salary = 55000
WHERE employee_id = 1;
```

---

### 4. **DELETE Query**

**Remove rows from a table.**

```sql
DELETE FROM table_name
WHERE condition;
```

**Example:**

```sql
DELETE FROM employees
WHERE employee_id = 1;
```

---

### 5. **JOINs**

**Combine rows from two or more tables based on a related column.**

- **INNER JOIN:** Only matching rows from both tables.

```sql
SELECT a.column1, b.column2
FROM table1 a
INNER JOIN table2 b ON a.common_column = b.common_column;
```

- **LEFT JOIN:** All rows from the left table, with matching rows from the right.

```sql
SELECT a.column1, b.column2
FROM table1 a
LEFT JOIN table2 b ON a.common_column = b.common_column;
```

- **RIGHT JOIN:** All rows from the right table, with matching rows from the left.

```sql
SELECT a.column1, b.column2
FROM table1 a
RIGHT JOIN table2 b ON a.common_column = b.common_column;
```

- **FULL OUTER JOIN:** All rows from both tables, with matches where possible.

```sql
SELECT a.column1, b.column2
FROM table1 a
FULL OUTER JOIN table2 b ON a.common_column = b.common_column;
```

---

### 6. **Subqueries**

**Queries within another query.**

```sql
SELECT column1
FROM table1
WHERE column2 = (SELECT column2 FROM table2 WHERE condition);
```

**Example:**

```sql
SELECT first_name
FROM employees
WHERE department_id = (SELECT department_id FROM departments WHERE name = 'Sales');
```

---

### 7. **UNION and UNION ALL**

**Combine the results of two queries.**

- **UNION:** Removes duplicates.

```sql
SELECT column1 FROM table1
UNION
SELECT column1 FROM table2;
```

- **UNION ALL:** Keeps all duplicates.

```sql
SELECT column1 FROM table1
UNION ALL
SELECT column1 FROM table2;
```

---

### 8. **GROUP BY and Aggregations**

**Aggregate data with functions like SUM, COUNT, AVG, MAX, MIN.**

```sql
SELECT column1, COUNT(*)
FROM table_name
GROUP BY column1
HAVING COUNT(*) > 1;
```

**Example:**

```sql
SELECT department_id, AVG(salary)
FROM employees
GROUP BY department_id;
```

---

### 9. **ALTER Table**

**Modify table structure.**

- **Add a column:**

```sql
ALTER TABLE table_name
ADD column_name datatype;
```

- **Drop a column:**

```sql
ALTER TABLE table_name
DROP COLUMN column_name;
```

- **Modify a column:**

```sql
ALTER TABLE table_name
MODIFY column_name datatype;
```

---

### 10. **CREATE and DROP Statements**

- **Create a new table:**

```sql
CREATE TABLE table_name (
    column1 datatype PRIMARY KEY,
    column2 datatype,
    ...
);
```

- **Drop a table:**

```sql
DROP TABLE table_name;
```

- **Create a new index:**

```sql
CREATE INDEX index_name
ON table_name (column_name);
```

- **Drop an index:**

```sql
DROP INDEX index_name;
```

---

### 11. **Transactions**

**Ensure data integrity using transactions.**

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
COMMIT;
```

- **ROLLBACK:** Revert changes.

```sql
ROLLBACK;
```

---

### 12. **Views**

**Create a virtual table.**

- **Create a view:**

```sql
CREATE VIEW view_name AS
SELECT column1, column2
FROM table_name
WHERE condition;
```

- **Drop a view:**

```sql
DROP VIEW view_name;
```

---

### 13. **CASE Statement**

**Conditional logic within a query.**

```sql
SELECT
    employee_id,
    salary,
    CASE
        WHEN salary > 50000 THEN 'High'
        ELSE 'Low'
    END AS salary_level
FROM employees;
```

---

### 14. **Window Functions**

**Perform calculations across a subset of data.**

```sql
SELECT
    employee_id,
    department_id,
    salary,
    RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rank
FROM employees;
```

---

### 15. **EXISTS and NOT EXISTS**

**Check for the existence of rows.**

- **EXISTS:**

```sql
SELECT column1
FROM table_name
WHERE EXISTS (SELECT 1 FROM another_table WHERE condition);
```

- **NOT EXISTS:**

```sql
SELECT column1
FROM table_name
WHERE NOT EXISTS (SELECT 1 FROM another_table WHERE condition);
```

---

These are the essential SQL query syntaxes to cover various scenarios. Let me
know if you'd like a more detailed explanation or examples for any specific
section!

I’ve created a sample table for you to visualize. Now, here is how you can write the SQL query logically:

### **SQL Query to Get Drivers Who Joined After 2021**

```sql
SELECT driver_id, driver_delivery, joining_date
FROM drivers
WHERE joining_date > '2021-12-31';
```

### **Explanation:**

1. **`SELECT` Clause:** We select the relevant columns – `driver_id`, `driver_delivery`, and `joining_date`.
2. **`FROM` Clause:** This specifies the table, in this case, called `drivers`.
3. **`WHERE` Clause:** We filter the rows to include only those drivers who joined after **December 31, 2021**.

This query ensures that only drivers with a `joining_date` in **2022 or later** are retrieved.

I’ve created a mock table showing the total deliveries, successful deliveries, and success rate per driver.

### **SQL Query to Group Drivers' Deliveries and Calculate Success Rate**

```sql
SELECT driver_id,
       COUNT(*) AS total_deliveries,
       SUM(CASE WHEN driver_delivery = 'success' THEN 1 ELSE 0 END) AS successful_deliveries,
       SUM(CASE WHEN driver_delivery = 'success' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS success_rate
FROM deliveries
GROUP BY driver_id;
```

### **Explanation:**

1. **`COUNT(*)`**: Counts the total number of deliveries for each driver.
2. **`SUM(CASE WHEN driver_delivery = 'success' THEN 1 ELSE 0 END)`**: Counts only the successful deliveries.
3. **`success_rate`**: Calculates the ratio of successful deliveries to total deliveries, ensuring a floating-point division by multiplying by `1.0`.

This query answers the interview question by grouping deliveries by driver,
showing total deliveries, the number of successful deliveries, and calculating
the success rate for each driver.

## Insight - 1

- What are the possible ways to create a column using SQL? I noticed that you use CASE for example

In SQL, there are several ways to create or manipulate columns dynamically within queries. Here are the key techniques:

---

### 1. **Using `CASE` Statements (Conditional Columns)**

The `CASE` statement allows you to create conditional logic inside a query.

**Syntax:**

```sql
SELECT
    driver_id,
    CASE
        WHEN driver_delivery = 'success' THEN 1
        ELSE 0
    END AS is_successful
FROM deliveries;
```

**Example:**  
This query creates a new column `is_successful` that assigns 1 for successful deliveries and 0 otherwise.

---

### 2. **Using `COALESCE()` (Handling Null Values)**

`COALESCE()` returns the first non-NULL value from a list of columns or expressions.

**Syntax:**

```sql
SELECT
    driver_id,
    COALESCE(completed_deliveries, 0) AS adjusted_deliveries
FROM drivers;
```

**Example:**  
This ensures that if the `completed_deliveries` column is `NULL`, it will display 0.

---

### 3. **Using `IF` Statements (MySQL Specific)**

`IF` statements work similarly to `CASE` but are specific to MySQL.

**Syntax:**

```sql
SELECT
    driver_id,
    IF(driver_delivery = 'success', 'Yes', 'No') AS delivery_status
FROM deliveries;
```

---

### 4. **Using Mathematical Operations on Columns**

You can create a new column by performing mathematical operations on existing ones.

**Syntax:**

```sql
SELECT
    driver_id,
    total_deliveries - successful_deliveries AS failed_deliveries
FROM drivers;
```

**Example:**  
This creates a new column showing the number of failed deliveries.

---

### 5. **Using String Manipulation (e.g., `CONCAT()`)**

You can create new columns by concatenating or formatting strings.

**Syntax:**

```sql
SELECT
    driver_id,
    CONCAT(first_name, ' ', last_name) AS full_name
FROM drivers;
```

---

### 6. **Using `AS` (Column Aliases)**

The simplest way to rename or format a column is with `AS`.

**Syntax:**

```sql
SELECT
    driver_id AS id,
    joining_date AS date_joined
FROM drivers;
```

---

### 7. **Using Window Functions for Calculated Columns**

Window functions allow row-by-row operations across partitions of data.

**Syntax:**

```sql
SELECT
    driver_id,
    RANK() OVER (PARTITION BY region ORDER BY total_deliveries DESC) AS delivery_rank
FROM drivers;
```

**Example:**  
This query assigns a delivery rank to drivers within each region.

---

### 8. **Using Subqueries to Generate New Columns**

A subquery in the `SELECT` clause can generate a column dynamically.

**Syntax:**

```sql
SELECT
    driver_id,
    (SELECT COUNT(*) FROM deliveries d WHERE d.driver_id = drivers.driver_id) AS delivery_count
FROM drivers;
```

---

These are various ways to create, manipulate, and customize columns in SQL
queries. Using these techniques, you can answer complex interview questions or
analyze data effectively. Let me know if you need further clarifications on any
of these methods!

To handle **duplicates in SQL**, there are several strategies depending on how
you want to deal with them. Below are different approaches with explanations and
SQL queries to remove or manage duplicates based on a `driver_id` column.

---

## **1. Identify Duplicate Records**

First, you might want to check if there are duplicate `driver_id` entries in your table.

**Query to Find Duplicates:**

```sql
SELECT driver_id, COUNT(*) AS occurrences
FROM drivers
GROUP BY driver_id
HAVING COUNT(*) > 1;
```

This query groups by `driver_id` and shows which drivers have more than one record.

---

## **2. Delete Duplicate Records (Keeping One Record)**

If you want to **delete duplicate rows**, keeping only one record per `driver_id`, you can use the `ROW_NUMBER()` function.

### **Query to Remove Duplicates:**

```sql
WITH CTE AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY driver_id ORDER BY joining_date DESC) AS row_num
    FROM drivers
)
DELETE FROM drivers
WHERE driver_id IN (
    SELECT driver_id
    FROM CTE
    WHERE row_num > 1
);
```

**Explanation:**

- **`ROW_NUMBER()`** assigns a unique number to each row within the same `driver_id` partition.
- We keep only the first occurrence (e.g., latest `joining_date`).
- Records with `row_num > 1` are deleted.

---

## **3. Remove Duplicates Using `DISTINCT` in a Query**

If you want to retrieve **unique records** without modifying the original data, you can use the `DISTINCT` keyword.

**Query with `DISTINCT`:**

```sql
SELECT DISTINCT driver_id, driver_delivery, joining_date
FROM drivers;
```

This query returns only one row per unique combination of columns.

---

## **4. Aggregate Data for Duplicates**

If you need to aggregate data (like getting total deliveries per driver), you can use `GROUP BY`.

**Query to Aggregate Data:**

```sql
SELECT
    driver_id,
    COUNT(*) AS total_deliveries,
    SUM(CASE WHEN driver_delivery = 'success' THEN 1 ELSE 0 END) AS successful_deliveries
FROM drivers
GROUP BY driver_id;
```

This query gives a summary for each driver, even if there are multiple rows per `driver_id`.

---

## **5. Use `UNIQUE` Constraint to Prevent Future Duplicates**

To prevent duplicate `driver_id` entries, you can **modify the table** to add a `UNIQUE` constraint.

**Query to Add `UNIQUE` Constraint:**

```sql
ALTER TABLE drivers
ADD CONSTRAINT unique_driver UNIQUE (driver_id);
```

This ensures that no new rows with duplicate `driver_id` values are inserted.

---

## **6. Insert Unique Records Only (`INSERT IGNORE` or `ON CONFLICT`)**

- **MySQL:** Use `INSERT IGNORE` to skip duplicate entries.

```sql
INSERT IGNORE INTO drivers (driver_id, driver_delivery, joining_date)
VALUES (101, 'success', '2022-01-01');
```

- **PostgreSQL:** Use `ON CONFLICT` to update or skip duplicates.

```sql
INSERT INTO drivers (driver_id, driver_delivery, joining_date)
VALUES (101, 'success', '2022-01-01')
ON CONFLICT (driver_id) DO NOTHING;
```

---

These strategies give you multiple options for handling and preventing
duplicates. Let me know if you need further clarifications or examples for any
of these!
