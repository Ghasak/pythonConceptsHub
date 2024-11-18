# Connect Postgresql with Streamlit

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->

**Table of Contents**

- [Connect Postgresql with Streamlit](#connect-postgresql-with-streamlit)
  - [Solution for listed requirements](#solution-for-listed-requirements)
    - [Streamlit Code](#streamlit-code)
    - [Features of the Code:](#features-of-the-code)
    - [How to Run:](#how-to-run)

<!-- markdown-toc end -->

In streamlit code that connect to database postgresql:

1. Then there is a page that accept the user input as sql query.
2. Which will fetch a data from the database and present it to the page the
   results.
3. It also should show a spinning wheel to show that the query is in progress
   and show a success message of how long it takes

---

## Solution for listed requirements

Here’s a Streamlit code snippet that connects to a PostgreSQL database, accepts
SQL queries from the user, fetches data from the database, and displays the
results. It includes a spinner to indicate that the query is in progress and
shows a success message with the query execution time:

### Streamlit Code

```python
import streamlit as st
import psycopg2
import pandas as pd
import time

# Set up the Streamlit page
st.title("PostgreSQL Query Executor")
st.sidebar.header("Database Connection")

# Sidebar for database connection parameters
db_host = st.sidebar.text_input("Host", "localhost")
db_port = st.sidebar.text_input("Port", "5432")
db_name = st.sidebar.text_input("Database Name", "mydatabase")
db_user = st.sidebar.text_input("User", "myuser")
db_password = st.sidebar.text_input("Password", type="password")

# Create a function to connect to the database
def create_connection():
    try:
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# SQL query input box
st.subheader("Enter SQL Query")
query = st.text_area("Write your SQL query here:", height=200)

# Execute query button
if st.button("Execute Query"):
    if query.strip() == "":
        st.warning("Please enter a valid SQL query.")
    else:
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    # Show spinner while query is running
                    with st.spinner("Executing query..."):
                        start_time = time.time()
                        cursor.execute(query)
                        columns = [desc[0] for desc in cursor.description]
                        data = cursor.fetchall()
                        end_time = time.time()

                        # Convert the results into a pandas DataFrame
                        df = pd.DataFrame(data, columns=columns)

                        # Display results in a table
                        st.success(f"Query executed successfully in {end_time - start_time:.2f} seconds.")
                        st.write("Query Results:")
                        st.dataframe(df)

            except Exception as e:
                st.error(f"Error executing query: {e}")
            finally:
                connection.close()
```

### Features of the Code:

1. **Database Connection Parameters**: Users can input the host, port, database name, user, and password from the sidebar.
2. **SQL Query Input**: A text area allows users to input custom SQL queries.
3. **Loading Spinner**: Displays a spinner animation while the query is being executed.
4. **Execution Time**: Shows the time taken to execute the query.
5. **Result Display**: Displays the query result in a pandas DataFrame format on the page.
6. **Error Handling**: Handles errors for database connection and query execution.

### How to Run:

1. Save the script as `app.py`.
2. Install dependencies:
   ```bash
   pip install streamlit psycopg2 pandas
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```
4. Access the app in your browser at `http://localhost:8501`.

---
