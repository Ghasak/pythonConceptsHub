# PYGWALKER with Streamlit

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->

**Table of Contents**

- [PYGWALKER with Streamlit](#pygwalker-with-streamlit)
  - [Concept](#concept)
    - [Steps:](#steps)
    - [Code Example](#code-example)
- [Function to create a PostgreSQL connection](#function-to-create-a-postgresql-connection)
  - [-](#-)
  - [Requirements:](#requirements)
  - [Running the App:](#running-the-app)
  - [Notes:](#notes)

<!-- markdown-toc end -->

## Concept

- Can we use pygwalker with streamlit based on passing a query to postgresql and
  fetch the results and present them with pygwlaker instead pandas

---

Yes, you can use **Pygwalker** with Streamlit to visualize the results of a
query executed on a PostgreSQL database. Pygwalker provides an interactive data
exploration interface similar to Tableau, and it works seamlessly with pandas
DataFrames.

Here’s how you can implement it:

### Steps:

1. Use **psycopg2** (or SQLAlchemy) to connect to PostgreSQL and fetch the query results.
2. Convert the fetched results into a pandas DataFrame.
3. Use **Pygwalker** to visualize the DataFrame.
4. Embed the Pygwalker visualization in the Streamlit app.

---

### Code Example

```python
import streamlit as st
import psycopg2
import pandas as pd
import pygwalker as pyg

# Function to create a PostgreSQL connection
def create_connection():
    try:
        connection = psycopg2.connect(
            dbname="mydatabase",
            user="myuser",
            password="mypassword",
            host="localhost",
            port="5432"
        )
        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Streamlit app
st.title("PostgreSQL Query and Visualization with Pygwalker")

# SQL Query Input
query = st.text_area("Enter your SQL query:")

if st.button("Execute Query"):
    if not query.strip():
        st.warning("Please enter a valid SQL query.")
    else:
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    st.info("Executing query...")
                    cursor.execute(query)

                    # Fetch query results and convert to pandas DataFrame
                    columns = [desc[0] for desc in cursor.description]
                    data = cursor.fetchall()
                    df = pd.DataFrame(data, columns=columns)

                    # Display success message
                    st.success("Query executed successfully! Visualizing data with Pygwalker...")

                    # Render Pygwalker visualization
                    pyg.walk(df)

            except Exception as e:
                st.error(f"Error executing query: {e}")
            finally:
                connection.close()
```

---

### Features of the Code:

1. **Query Execution**: Fetch data from PostgreSQL using psycopg2.
2. **DataFrame Conversion**: Converts the query results to a pandas DataFrame.
3. **Visualization**: Uses Pygwalker for interactive visualizations.
4. **Integration with Streamlit**: Embeds the Pygwalker UI directly in the Streamlit page.

---

### Requirements:

Install the required packages:

```bash
pip install streamlit psycopg2 pandas pygwalker
```

---

### Running the App:

1. Save the script as `app.py`.
2. Run the app:
   ```bash
   streamlit run app.py
   ```
3. Access the app in your browser at `http://localhost:8501`.

---

### Notes:

- Pygwalker will render a fully interactive visualization interface for the
  DataFrame, allowing you to explore data (create charts, filter, etc.).
- This approach seamlessly integrates your PostgreSQL query results with
  Pygwalker for enhanced data exploration.

Let me know if you need further customization!
