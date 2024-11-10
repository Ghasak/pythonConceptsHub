# Postgresql

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->

**Table of Contents**

- [Postgresql](#postgresql)
  - [Concept ](#concept)
    - [1. Using the URL in a Browser](#1-using-the-url-in-a-browser)
    - [2. Using `curl` to Check the Port](#2-using-curl-to-check-the-port)
    - [3. Using `pg_isready` (PostgreSQL Utility)](#3-using-pg_isready-postgresql-utility)
    - [4. Using a PostgreSQL Client (like `psql`)](#4-using-a-postgresql-client-like-psql)
    - [5. Testing with Python and `psycopg2`](#5-testing-with-python-and-psycopg2)
    - [Summary](#summary)

<!-- markdown-toc end -->

## Concept

Here are some methods to check if your PostgreSQL server is accessible using its
connection URL.

### 1. Using the URL in a Browser

PostgreSQL is not accessible directly through a web browser by default, as it
doesn’t provide an HTTP-based web interface. If you paste a PostgreSQL URL like
`postgresql://myuser:mypassword@localhost:5432/mydatabase` into a browser, it
won't connect or display content, since browsers are not designed to interpret
database URLs directly.

However, you can test the connection in a few other ways.

### 2. Using `curl` to Check the Port

While `curl` cannot directly connect to PostgreSQL in the way it does with HTTP,
you can check if the PostgreSQL port is open and accessible using `curl`. Here’s
how:

```bash
curl -v telnet://localhost:5432
```

If the server is listening on port 5432, you should see output confirming a
connection. If the port is closed or inaccessible, you’ll see a connection
error.

### 3. Using `pg_isready` (PostgreSQL Utility)

The `pg_isready` command is a built-in PostgreSQL tool for checking the
connection status of a PostgreSQL server. If you have `psql` installed locally,
you can use it as follows:

```bash
pg_isready -h localhost -p 5432 -U myuser
```

This command will return a success message if PostgreSQL is accepting
connections on the specified host and port, or an error message if it’s not.

### 4. Using a PostgreSQL Client (like `psql`)

To check the URL with a PostgreSQL client like `psql`, run:

```bash
psql postgresql://myuser:mypassword@localhost:5432/mydatabase
```

If the credentials and connection are correct, this command will connect you to
the database and open a PostgreSQL session.

### 5. Testing with Python and `psycopg2`

If you’re comfortable with Python, you can use the `psycopg2` library to test
the URL programmatically:

```python
import psycopg2
from psycopg2 import sql

try:
    conn = psycopg2.connect("postgresql://myuser:mypassword@localhost:5432/mydatabase")
    print("Connection successful")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
```

This will help you confirm that the URL is valid and can establish a connection to the database.

### Summary

For PostgreSQL URLs, methods like using `pg_isready`, connecting via `psql`, or
testing with a simple Python script provide reliable ways to confirm
connectivity. Direct connection via browsers is unsupported, but `curl` can
still check if the port is open and listening.
