# PostgreSQL
<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [PostgreSQL](#postgresql)
    - [Useful commmands](#useful-commmands)
    - [More Insights](#more-insights)
        - [1. Databases](#1-databases)
        - [2. Tables](#2-tables)
        - [3. Rows (Data Manipulation in Tables)](#3-rows-data-manipulation-in-tables)
        - [4. Indexes (Optional but Common for Optimization)](#4-indexes-optional-but-common-for-optimization)
        - [Summary Table: Overall Workflow](#summary-table-overall-workflow)

<!-- markdown-toc end -->

## Useful commmands

Here’s a PostgreSQL command cheatsheet with descriptions, syntax, notes, and
contexts for each command, including common commands used for database, table,
and schema management. This will help you work efficiently with PostgreSQL in
both the terminal and inside specific databases or tables.

- **NOTE**: inside the terminal session and after selecting a database you can run external sql script using `\i`, such as

```sql
\i /Users/{user_name}/Desktop/my_file.sql
```

| Command     | Description                                                                                     | Syntax                       | Context                                | Notes                                                                                                |
| ----------- | ----------------------------------------------------------------------------------------------- | ---------------------------- | -------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `\c`        | Connects to a database.                                                                         | `\c dbname`                  | Terminal                               | Used to switch between databases within the same session.                                            |
| `\l`        | Lists all databases.                                                                            | `\l`                         | Terminal                               | Shows details about each database, including owner, encoding, collation, etc.                        |
| `\dt`       | Lists all tables in the connected database.                                                     | `\dt`                        | Inside a selected database             | Only shows tables; use `\d` for other relations (views, sequences).                                  |
| `\d`        | Displays information about a specific table, view, sequence, or index.                          | `\d table_name`              | Inside a selected database             | Provides details on table structure, columns, types, and indexes.                                    |
| `\dn`       | Lists all schemas in the connected database.                                                    | `\dn`                        | Inside a selected database             | Shows all schemas; useful to organize and isolate database objects.                                  |
| `\di`       | Lists all indexes in the connected database.                                                    | `\di`                        | Inside a selected database             | Only lists indexes; can use `\d table_name` for indexes specific to a table.                         |
| `\df`       | Lists all functions in the connected database.                                                  | `\df`                        | Inside a selected database             | Use `\df function_name` for specific function details.                                               |
| `\du`       | Lists all roles in the database cluster.                                                        | `\du`                        | Terminal                               | Shows roles, which are used to manage permissions and access.                                        |
| `\i`        | Executes a SQL script file from the provided path.                                              | `\i /path/to/script.sql`     | Terminal or inside a selected database | Useful for running large SQL scripts or setups directly in the PostgreSQL session.                   |
| `\pset`     | Sets output format options like border, expanded view, and null display.                        | `\pset option value`         | Any                                    | Can be used for customizing output formatting for better readability.                                |
| `\timing`   | Toggles timing of SQL commands.                                                                 | `\timing`                    | Any                                    | Shows execution time for each command; helpful for performance analysis.                             |
| `\x`        | Toggles expanded table display mode, which formats table output vertically.                     | `\x`                         | Any                                    | Useful for large tables with many columns; each row's fields are displayed in a vertical list.       |
| `\q`        | Exits the PostgreSQL interactive terminal.                                                      | `\q`                         | Any                                    | Useful for quickly leaving the PostgreSQL session.                                                   |
| `\copy`     | Copies data between a file and a table. Can also copy data to the terminal in CSV format.       | `\copy table FROM/TO 'file'` | Inside a selected database             | Use this for quick data imports/exports; requires file path and permissions if using local files.    |
| `\g`        | Sends the current query buffer to the server for execution.                                     | `\g`                         | Any                                    | Executes a command after typing it without a semicolon (helpful for multiline commands).             |
| `\echo`     | Outputs text to the terminal.                                                                   | `\echo text`                 | Any                                    | Useful for debugging or displaying messages during scripts.                                          |
| `\set`      | Sets a variable in the session.                                                                 | `\set var value`             | Any                                    | Variables can be set for temporary use in the session, e.g., `\set VERBOSITY verbose`.               |
| `\password` | Sets or changes the password of a PostgreSQL user.                                              | `\password [username]`       | Terminal                               | If no username is provided, it changes the password for the current user.                            |
| `\watch`    | Re-runs the previous command every specified number of seconds.                                 | `\watch interval`            | Inside a selected database             | Useful for monitoring changes or running a query repeatedly (e.g., checking table updates).          |
| `\h`        | Displays help on SQL commands.                                                                  | `\h` or `\h command`         | Any                                    | Helpful for quick reference on SQL commands.                                                         |
| `\encoding` | Shows or sets client-side encoding for the database session.                                    | `\encoding [encoding]`       | Any                                    | Can be used to set encoding, e.g., `\encoding UTF8`.                                                 |
| `\conninfo` | Displays information about the current database connection.                                     | `\conninfo`                  | Any                                    | Useful for checking current connection details, such as host, port, and user.                        |
| `\d+`       | Provides more detailed information about tables, including size and table description.          | `\d+ table_name`             | Inside a selected database             | Extra details on table structure and metadata, including size info.                                  |
| `\a`        | Toggles between unaligned (plain text) and aligned (table) output modes.                        | `\a`                         | Any                                    | Helpful for formatting output as plain text for easier copying.                                      |
| `\o`        | Writes query output to a specified file or directs it to the terminal.                          | `\o filename` or `\o`        | Any                                    | Use `\o filename` to save output to a file; `\o` alone returns output to terminal.                   |
| `\s`        | Saves or displays command history.                                                              | `\s [filename]`              | Any                                    | `\s filename` saves history to a file, while `\s` alone shows it on the terminal.                    |
| `\db`       | Lists all tablespaces.                                                                          | `\db`                        | Terminal                               | Tablespaces specify storage locations for data.                                                      |
| `\dd`       | Describes database objects (comments associated with tables, columns, functions, etc.).         | `\dd object_name`            | Inside a selected database             | Shows comments/documentation on database objects (if any).                                           |
| `\dconfig`  | Displays current configuration parameters for the database or a specific parameter if provided. | `\dconfig [parameter_name]`  | Inside a selected database             | Useful for checking configurations directly in PostgreSQL, such as work_mem or maintenance_work_mem. |

## More Insights

Here's a structured workflow and list of essential commands for managing
databases, tables, and queries in PostgreSQL via a terminal session. This guide
will walk you through commands to list, create, modify, and delete at each
level, with a final summary table at the end.

---

### 1. Databases

| Action                | Command                                     | Description                         |
| --------------------- | ------------------------------------------- | ----------------------------------- |
| List databases        | `\l` or `\list`                             | List all databases                  |
| Create database       | `CREATE DATABASE dbname;`                   | Create a new database               |
| Delete database       | `DROP DATABASE dbname;`                     | Delete a database                   |
| Connect to a database | `\c dbname`                                 | Connect to a specific database      |
| Rename database       | `ALTER DATABASE oldname RENAME TO newname;` | Rename a database                   |
| Set owner             | `ALTER DATABASE dbname OWNER TO newowner;`  | Change database owner               |
| View current database | `SELECT current_database();`                | Show the current connected database |

---

### 2. Tables

| Action                   | Command                                                              | Description                                 |
| ------------------------ | -------------------------------------------------------------------- | ------------------------------------------- |
| List tables              | `\dt`                                                                | List all tables in the current database     |
| Create table             | `CREATE TABLE table_name (...);`                                     | Create a new table with defined columns     |
| Delete table             | `DROP TABLE table_name;`                                             | Delete a table                              |
| Rename table             | `ALTER TABLE oldname RENAME TO newname;`                             | Rename a table                              |
| Describe table structure | `\d table_name`                                                      | Show column details, types, and constraints |
| Add a column             | `ALTER TABLE table_name ADD COLUMN column_name TYPE;`                | Add a new column to an existing table       |
| Delete a column          | `ALTER TABLE table_name DROP COLUMN column_name;`                    | Remove a column from an existing table      |
| Modify column type       | `ALTER TABLE table_name ALTER COLUMN column_name TYPE new_type;`     | Change a column's data type                 |
| Set default value        | `ALTER TABLE table_name ALTER COLUMN column_name SET DEFAULT value;` | Set default value for a column              |

---

### 3. Rows (Data Manipulation in Tables)

| Action      | Command                                                    | Description                                 |
| ----------- | ---------------------------------------------------------- | ------------------------------------------- |
| Insert row  | `INSERT INTO table_name (col1, col2) VALUES (val1, val2);` | Insert a new row in a table                 |
| Update rows | `UPDATE table_name SET column = value WHERE condition;`    | Update rows that match a condition          |
| Delete rows | `DELETE FROM table_name WHERE condition;`                  | Delete rows that match a condition          |
| Select data | `SELECT * FROM table_name;`                                | Retrieve all data from a table              |
| Filter data | `SELECT * FROM table_name WHERE condition;`                | Retrieve specific data matching a condition |
| Count rows  | `SELECT COUNT(*) FROM table_name;`                         | Count the number of rows in a table         |

---

### 4. Indexes (Optional but Common for Optimization)

| Action              | Command                                                  | Description                              |
| ------------------- | -------------------------------------------------------- | ---------------------------------------- |
| Create index        | `CREATE INDEX index_name ON table_name (column);`        | Create an index on a column              |
| List indexes        | `\di`                                                    | List all indexes in the current database |
| Delete index        | `DROP INDEX index_name;`                                 | Remove an index                          |
| Create unique index | `CREATE UNIQUE INDEX index_name ON table_name (column);` | Ensure unique values in a column         |

---

### Summary Table: Overall Workflow

| Step          | Action              | Command                                                              |
| ------------- | ------------------- | -------------------------------------------------------------------- |
| **Databases** | List databases      | `\l` or `\list`                                                      |
|               | Create database     | `CREATE DATABASE dbname;`                                            |
|               | Delete database     | `DROP DATABASE dbname;`                                              |
|               | Connect to database | `\c dbname`                                                          |
|               | Rename database     | `ALTER DATABASE oldname RENAME TO newname;`                          |
|               | Set database owner  | `ALTER DATABASE dbname OWNER TO newowner;`                           |
| **Tables**    | List tables         | `\dt`                                                                |
|               | Create table        | `CREATE TABLE table_name (...);`                                     |
|               | Delete table        | `DROP TABLE table_name;`                                             |
|               | Rename table        | `ALTER TABLE oldname RENAME TO newname;`                             |
|               | Describe table      | `\d table_name`                                                      |
|               | Add column          | `ALTER TABLE table_name ADD COLUMN column_name TYPE;`                |
|               | Delete column       | `ALTER TABLE table_name DROP COLUMN column_name;`                    |
|               | Modify column type  | `ALTER TABLE table_name ALTER COLUMN column_name TYPE new_type;`     |
|               | Set column default  | `ALTER TABLE table_name ALTER COLUMN column_name SET DEFAULT value;` |
| **Rows**      | Insert row          | `INSERT INTO table_name (col1, col2) VALUES (val1, val2);`           |
|               | Update rows         | `UPDATE table_name SET column = value WHERE condition;`              |
|               | Delete rows         | `DELETE FROM table_name WHERE condition;`                            |
|               | Select data         | `SELECT * FROM table_name;`                                          |
|               | Filter data         | `SELECT * FROM table_name WHERE condition;`                          |
|               | Count rows          | `SELECT COUNT(*) FROM table_name;`                                   |
| **Indexes**   | Create index        | `CREATE INDEX index_name ON table_name (column);`                    |
|               | List indexes        | `\di`                                                                |
|               | Delete index        | `DROP INDEX index_name;`                                             |
|               | Create unique index | `CREATE UNIQUE INDEX index_name ON table_name (column);`             |

These commands cover a range of database management tasks, from creating and
listing databases and tables to manipulating rows and adding indexes for
optimization. This reference provides a comprehensive toolkit for managing
PostgreSQL databases in a terminal session.
