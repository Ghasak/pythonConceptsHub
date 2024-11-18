# Create a session

Here’s how to create an `employee` table, insert data, and query it using Dadbod in Neovim.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Create a session](#create-a-session)
    - [Step 1: Create the Employee Table](#step-1-create-the-employee-table)
        - [Step 2: Insert Employee Records](#step-2-insert-employee-records)
        - [Step 3: Query and View the Data](#step-3-query-and-view-the-data)
        - [Step 1: Create the Employee Table](#step-1-create-the-employee-table-1)
        - [Step 2: Insert Employee Records](#step-2-insert-employee-records-1)
        - [Step 3: Query the Data](#step-3-query-the-data)
        - [Exiting the PostgreSQL Session](#exiting-the-postgresql-session)
        - [Additional Commands for Database Objects](#additional-commands-for-database-objects)

<!-- markdown-toc end -->

## Step 1: Create the Employee Table

First, connect to the database in Neovim using Dadbod. Once connected, you can
use the following SQL to create the `employee` table:

```sql
CREATE TABLE employee (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    age INT,
    gender VARCHAR(10),
    salary DECIMAL(10, 2)
);
```

To execute this in Dadbod:

1. Open a new buffer in Neovim and paste the SQL command.
2. Use the command `:DB` to ensure you’re connected to your PostgreSQL instance.
3. Highlight the SQL code for creating the table.
4. Run `:DB` again to execute the highlighted code.

### Step 2: Insert Employee Records

Now, insert data for five employees. Use the following SQL commands:

```sql
INSERT INTO employee (first_name, last_name, age, gender, salary) VALUES
('Alice', 'Smith', 30, 'Female', 75000.00),
('Bob', 'Johnson', 40, 'Male', 80000.00),
('Carol', 'Davis', 27, 'Female', 62000.00),
('David', 'Wilson', 35, 'Male', 85000.00),
('Eve', 'Brown', 29, 'Female', 70000.00);
```

To execute these commands:

1. Paste these insert statements in your Neovim buffer.
2. Highlight all the statements.
3. Use `:DB` to execute the highlighted SQL code and insert the rows.

### Step 3: Query and View the Data

To check the inserted data, use the following SQL query:

```sql
SELECT * FROM employee;
```

1. Write this `SELECT` statement in a Neovim buffer.
2. Highlight the statement and run `:DB` to execute it.
3. Dadbod will display the query results directly within Neovim, allowing you
   to view the `employee` table data.

This workflow allows you to create tables, insert data, and query information
directly in Neovim using Dadbod.

---

Since you’re already inside the PostgreSQL session within the Docker container,
you can directly execute the SQL commands in your terminal to create the table,
insert data, and query it.

Here’s how:

### Step 1: Create the Employee Table

Run the following command directly in your PostgreSQL session:

```sql
CREATE TABLE employee (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    age INT,
    gender VARCHAR(10),
    salary DECIMAL(10, 2)
);
```

This will create the `employee` table with the specified columns.

### Step 2: Insert Employee Records

Now, insert data for five employees by running this command:

```sql
INSERT INTO employee (first_name, last_name, age, gender, salary) VALUES
('Alice', 'Smith', 30, 'Female', 75000.00),
('Bob', 'Johnson', 40, 'Male', 80000.00),
('Carol', 'Davis', 27, 'Female', 62000.00),
('David', 'Wilson', 35, 'Male', 85000.00),
('Eve', 'Brown', 29, 'Female', 70000.00);
```

This will add five entries to the `employee` table.

### Step 3: Query the Data

To view all records in the `employee` table, execute the following command:

```sql
SELECT * FROM employee;
```

This will display the data you just inserted, showing the entire table with the
fields `first_name`, `last_name`, `age`, `gender`, and `salary`.

### Exiting the PostgreSQL Session

When you’re done, you can exit the PostgreSQL session by typing:

```bash
\q
```

This will bring you back to the regular Docker shell or your local terminal.
You should now see your table and data in both your terminal session and your
Dadbod setup in Neovim.

To view all tables in your current PostgreSQL database session, you can use the
following command while in the `psql` session:

```sql
\dt
```

This command lists all tables in the current database schema. You’ll see the
table names along with their schema, type, and owner.

### Additional Commands for Database Objects

- **To list all databases**: `\l`
- **To list all tables in a specific schema**: `\dt schema_name.*`
- **To describe a specific table's structure**: `\d table_name`
- **To list all commands**: `\?`

Using these commands will help you navigate and inspect your database structure
easily within the PostgreSQL session.

It looks like there may be a misunderstanding. In PostgreSQL, `mydatabase` is
the name of your **database**, not a **table**. To list tables in the currently
connected database (`mydatabase`), you can simply use the `\dt` command without
specifying a table name.

Here's how to proceed:

1. **Ensure You're Connected to the Correct Database**
   You've already connected to `mydatabase`, so you're good to go here.

2. **List All Tables in `mydatabase`**
   Run this command to list all tables:

   ```sql
   \dt
   ```

   This will display all tables within the `mydatabase` database. If you've
   created the `employee` table as described, it should appear in the list.

3. **Check Table Structure (Optional)**
   If you want to see the structure of the `employee` table, you can use:

   ```sql
   \d employee
   ```

This command will show the columns and data types in the `employee` table.
