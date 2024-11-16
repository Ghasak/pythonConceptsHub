# Handling Full Load and Delta Load

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->

**Table of Contents**

- [Handling Full Load and Delta Load](#handling-full-load-and-delta-load)
  - [Concept](#concept)
    - [Steps:](#steps)
    - [Explanation:](#explanation)
    - [Output:](#output)
  - [More in depth](#more-in-depth)
    - [Full Load:](#full-load)
    - [Incremental Load:](#incremental-load)
    - [Explanation:](#explanation-1)
      - [Full Load:](#full-load-1)
      - [Incremental Load:](#incremental-load-1)
    - [Output:](#output-1)
      - [After Full Load:](#after-full-load)
      - [After Incremental Load:](#after-incremental-load)
  - [Limitation of previous approach](#limitation-of-previous-approach)
    - [**Why This Approach is Limited for Big Data**](#why-this-approach-is-limited-for-big-data)
    - [**Practical Dataset Size**](#practical-dataset-size)
    - [**Optimizing for Larger Datasets**](#optimizing-for-larger-datasets)
      - [Chunked Processing Example:](#chunked-processing-example)
    - [**For Big Data: Scalable Solutions**](#for-big-data-scalable-solutions)
    - [Recommendations:](#recommendations)
  - [New Request](#new-request)
    - [**1. Full Load:**](#1-full-load)
    - [SQLAlchemy ORM Model Definitions:](#sqlalchemy-orm-model-definitions)
    - [**Full Load Data Insertion:**](#full-load-data-insertion)
    - [**2. Delta Load:**](#2-delta-load)
      - [Delta Load Logic:](#delta-load-logic)
    - [**3. Explanation:**](#3-explanation)
    - [**4. Output Verification**:](#4-output-verification)
    - [**5. Optimizing for Larger Data:**](#5-optimizing-for-larger-data)
  - [Update the requirements](#update-the-requirements)
    - [**1. Schema Design for `CarData` Table**](#1-schema-design-for-cardata-table)
    - [**2. Create Table**](#2-create-table)
    - [**3. Full Load**](#3-full-load)
- [Full Load Data](#full-load-data)
  - [-](#-)
  - [**5. Fetch History for a Given Car**](#5-fetch-history-for-a-given-car)
  - [**6. Expected Results**](#6-expected-results)
  - [**Next Steps:**](#next-steps)

<!-- markdown-toc end -->

## Concept

Can you demonstrate how to send a pandas DataFrame directly to a database,
creating a new table within the database using SQLAlchemy 2.0?

- We can directly send a pandas DataFrame to a database and create a table using
  SQLAlchemy 2.0. Here's how you can do it:

### Steps:

1. **Install Necessary Libraries**: Ensure you have `pandas` and `SQLAlchemy`
   installed.
2. **Create an SQLAlchemy Engine**: Use it to connect to your database.
3. **Use `pandas.DataFrame.to_sql`**: This method allows sending a DataFrame
   directly to the database. It will create the table if it does not already
   exist.

Here is an example:

```python
from sqlalchemy import create_engine
import pandas as pd

# Sample DataFrame
data = {
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
}
df = pd.DataFrame(data)

# SQLAlchemy 2.0 connection string
DATABASE_URL = "sqlite:///example.db"  # Replace with your database URL
engine = create_engine(DATABASE_URL, future=True)

# Send DataFrame to the database and create a table named 'people'
df.to_sql('people', con=engine, if_exists='replace', index=False)

# Verify: Query the database
with engine.connect() as connection:
    result = connection.execute("SELECT * FROM people")
    for row in result:
        print(row)
```

### Explanation:

1. **`create_engine`**: Creates a database connection.
2. **`to_sql`**: Transfers the DataFrame to the database. Key arguments:
   - `name`: The name of the table in the database.
   - `con`: SQLAlchemy engine or connection.
   - `if_exists`: Determines behavior if the table already exists:
     - `'replace'`: Drops the table and creates a new one.
     - `'append'`: Appends the data to the existing table.
     - `'fail'`: Raises an error if the table exists.
   - `index`: Specifies whether to write the DataFrame index as a column.

### Output:

- A table `people` will be created in your database with the DataFrame data.
- You can query the database to confirm the data insertion.

Let me know if you need further customization or explanations!

---

## More in depth

What if I want to incrementally update later? Please first demonstrate the
process of a full data load, and then explain how to handle incremental data
loads.

To handle both a **full load** and subsequent **incremental loads** using
SQLAlchemy 2.0 with a pandas DataFrame, you can follow these steps:

### Full Load:

The first step involves creating the database table and loading the initial data.

```python
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import pandas as pd

# Sample DataFrame for Full Load
data_full = {
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
}
df_full = pd.DataFrame(data_full)

# SQLAlchemy 2.0 connection string
DATABASE_URL = "sqlite:///example.db"  # Replace with your database URL
engine = create_engine(DATABASE_URL, future=True)

# Full Load: Create table and insert data
df_full.to_sql('people', con=engine, if_exists='replace', index=False)

# Verify: Query the database
with engine.connect() as connection:
    result = connection.execute("SELECT * FROM people")
    print("Full Load Results:")
    for row in result:
        print(row)
```

### Incremental Load:

For incremental loads, you need to check if the data already exists in the
database to avoid duplicates. This can be done by querying the database for
existing records and appending only new ones.

```python
# Sample DataFrame for Incremental Load
data_incremental = {
    'id': [3, 4, 5],  # `id` 3 already exists; `id` 4 and 5 are new
    'name': ['Charlie', 'Diana', 'Eve'],
    'age': [35, 40, 28]
}
df_incremental = pd.DataFrame(data_incremental)

# Incremental Load Logic
with engine.connect() as connection:
    # Query existing IDs from the database
    existing_ids = pd.read_sql("SELECT id FROM people", con=connection)['id'].tolist()

# Filter out rows where `id` already exists
new_data = df_incremental[~df_incremental['id'].isin(existing_ids)]

# Append new data to the database
if not new_data.empty:
    new_data.to_sql('people', con=engine, if_exists='append', index=False)

# Verify: Query the database after incremental load
with engine.connect() as connection:
    result = connection.execute("SELECT * FROM people")
    print("After Incremental Load Results:")
    for row in result:
        print(row)
```

### Explanation:

#### Full Load:

1. **`to_sql` with `if_exists='replace'`**: Drops the table if it exists and
   creates a new one, loading all data from the DataFrame.

#### Incremental Load:

1. **Query Existing Records**: Fetch existing `id`s (or a unique identifier)
   from the database.
2. **Filter DataFrame**: Use pandas filtering to exclude rows already present in
   the database.
3. **Append New Records**: Use `to_sql` with `if_exists='append'` to add only
   new rows to the database.

### Output:

#### After Full Load:

```plaintext
Full Load Results:
(1, 'Alice', 25)
(2, 'Bob', 30)
(3, 'Charlie', 35)
```

#### After Incremental Load:

```plaintext
After Incremental Load Results:
(1, 'Alice', 25)
(2, 'Bob', 30)
(3, 'Charlie', 35)
(4, 'Diana', 40)
(5, 'Eve', 28)
```

This approach ensures no duplicate records during incremental loads. You can
adapt the filtering logic based on your table schema and requirements. Let me
know if you'd like further clarification!

## Limitation of previous approach

Is this practical? I think this might not be suitable for large datasets. What
is the maximum amount of data it can handle?

- You're absolutely right—this approach using `pandas` is practical for small to
  medium-sized datasets but may not scale efficiently for **big data** due to
  memory constraints and the overhead of data transfers between pandas and the
  database.

Here are the limitations and practical boundaries:

---

### **Why This Approach is Limited for Big Data**

1. **Memory Constraints**:

   - Pandas loads the entire DataFrame into memory, which may not be feasible for very large datasets.
   - Filtering or processing millions of rows in pandas requires significant RAM.

2. **Query Overhead**:

   - The step to query existing records (e.g., fetching `id`s) can become slow for large datasets.
   - The transfer of data between pandas and the database via `to_sql` has overhead.

3. **Database Write Limitations**:
   - While databases are optimized for bulk writes, the pandas-to-SQLAlchemy
     pipeline is not as efficient for large, continuous data streams.

---

### **Practical Dataset Size**

- **Small Datasets (< 1M rows)**: Works fine with moderate memory and
  computational resources.
- **Medium Datasets (1M–10M rows)**: Possible, but you may need chunked
  processing (explained below).
- **Large Datasets (>10M rows or >1GB)**: Not recommended; switch to more
  scalable tools like **ETL pipelines**, **Apache Spark**, or **Dask**.

---

### **Optimizing for Larger Datasets**

If your data is moderately large (e.g., 1M–10M rows), you can improve
scalability by processing data in **chunks** and avoiding memory overload.

#### Chunked Processing Example:

```python
chunk_size = 10000  # Number of rows per chunk

# Incremental Load in Chunks
for chunk in pd.read_csv('large_dataset.csv', chunksize=chunk_size):
    # Query existing IDs (consider batching this for larger datasets)
    with engine.connect() as connection:
        existing_ids = pd.read_sql("SELECT id FROM people", con=connection)['id'].tolist()

    # Filter out rows where `id` already exists
    new_data = chunk[~chunk['id'].isin(existing_ids)]

    # Append new data to the database
    if not new_data.empty:
        new_data.to_sql('people', con=engine, if_exists='append', index=False)
```

---

### **For Big Data: Scalable Solutions**

When working with massive datasets, consider the following tools:

1. **Direct Bulk Inserts**:

   - Use SQLAlchemy's `executemany` or database-specific bulk insert methods for better performance:
     ```python
     with engine.connect() as connection:
         connection.execute(
             people_table.insert(),
             [{'id': 4, 'name': 'Diana', 'age': 40}, {'id': 5, 'name': 'Eve', 'age': 28}]
         )
     ```

2. **ETL Tools**:

   - **Apache Airflow**, **dbt**, or custom Python ETL pipelines with parallelism.
   - Use **SQL bulk utilities** for database-optimized ingestion.

3. **Big Data Frameworks**:

   - **Apache Spark**: Handles distributed computation and writes to databases efficiently.
   - **Dask**: Pandas-compatible for parallel processing of large datasets.

4. **Database-Side Deduplication**:
   - Write data to a staging table in the database and use SQL for deduplication:
     ```sql
     INSERT INTO people (id, name, age)
     SELECT id, name, age
     FROM staging_people
     WHERE id NOT IN (SELECT id FROM people);
     ```

---

### Recommendations:

- For datasets **<1M rows**, chunked `pandas.to_sql` is sufficient.
- For datasets **1M–10M rows**, chunking with database-side filtering/deduplication is more efficient.
- For **big data (>10M rows)**:
  - Use tools like **Apache Spark** or **Dask** for scalable processing.
  - Leverage database-specific bulk insert and deduplication techniques.

Let me know your dataset's characteristics, and I can suggest a more tailored solution!

---

## New Request

Now, assume I have three tables: one for car brands, one for car models, and one
for car information. The relationship between brand and model is one-to-many.
Handle the remaining relationships and implement both full load and delta load
processes as you did before.

Here’s a structured approach to handling **full load** and **delta load** for
three related tables (`CarBrand`, `CarModel`, and `CarInfo`) using SQLAlchemy
2.0. The relationships are:

- **One-to-Many**: `CarBrand` → `CarModel`
- **One-to-Many**: `CarModel` → `CarInfo`

---

### **1. Full Load:**

Create the tables and insert initial data into the database, ensuring relationships are maintained.

### SQLAlchemy ORM Model Definitions:

```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, Session
import pandas as pd

Base = declarative_base()

# Define ORM models
class CarBrand(Base):
    __tablename__ = "car_brand"
    brand_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    models = relationship("CarModel", back_populates="brand", cascade="all, delete-orphan")


class CarModel(Base):
    __tablename__ = "car_model"
    model_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    brand_id = Column(Integer, ForeignKey("car_brand.brand_id"))
    cars = relationship("CarInfo", back_populates="model")
    brand = relationship("CarBrand", back_populates="models")


class CarInfo(Base):
    __tablename__ = "car_info"
    car_id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey("car_model.model_id"))
    price = Column(Integer)
    is_sold = Column(Integer)  # 0 for False, 1 for True
    model = relationship("CarModel", back_populates="cars")

# Create database engine
DATABASE_URL = "sqlite:///cars.db"  # Replace with your database URL
engine = create_engine(DATABASE_URL, future=True)

# Create tables
Base.metadata.create_all(engine)
```

---

### **Full Load Data Insertion:**

```python
# Sample data
brand_data = pd.DataFrame({
    'brand_id': [1, 2],
    'name': ['Toyota', 'Honda']
})

model_data = pd.DataFrame({
    'model_id': [1, 2, 3],
    'name': ['Camry', 'Civic', 'Accord'],
    'brand_id': [1, 2, 2]
})

car_info_data = pd.DataFrame({
    'car_id': [1, 2, 3],
    'model_id': [1, 2, 3],
    'price': [30000, 25000, 28000],
    'is_sold': [0, 1, 0]
})

# Insert Full Load Data
with Session(engine) as session:
    # Insert CarBrand
    for _, row in brand_data.iterrows():
        session.add(CarBrand(brand_id=row['brand_id'], name=row['name']))

    # Insert CarModel
    for _, row in model_data.iterrows():
        session.add(CarModel(model_id=row['model_id'], name=row['name'], brand_id=row['brand_id']))

    # Insert CarInfo
    for _, row in car_info_data.iterrows():
        session.add(CarInfo(car_id=row['car_id'], model_id=row['model_id'], price=row['price'], is_sold=row['is_sold']))

    session.commit()

print("Full load completed!")
```

---

### **2. Delta Load:**

Delta load involves inserting or updating data by checking for differences
between the database and new data.

#### Delta Load Logic:

```python
# Delta data for CarInfo
delta_car_info_data = pd.DataFrame({
    'car_id': [3, 4],
    'model_id': [3, 2],
    'price': [29000, 27000],
    'is_sold': [1, 0]
})

with Session(engine) as session:
    # Query existing car IDs
    existing_car_ids = {car.car_id for car in session.query(CarInfo).all()}

    # Filter new rows
    new_data = delta_car_info_data[~delta_car_info_data['car_id'].isin(existing_car_ids)]

    # Update existing rows
    for _, row in delta_car_info_data.iterrows():
        if row['car_id'] in existing_car_ids:
            car = session.query(CarInfo).filter(CarInfo.car_id == row['car_id']).one()
            car.price = row['price']
            car.is_sold = row['is_sold']

    # Add new rows
    for _, row in new_data.iterrows():
        session.add(CarInfo(car_id=row['car_id'], model_id=row['model_id'], price=row['price'], is_sold=row['is_sold']))

    session.commit()

print("Delta load completed!")
```

---

### **3. Explanation:**

- **Full Load**:
  - Inserts all data into the database using the ORM models.
  - Relationships (`brand_id` and `model_id`) are maintained automatically.
- **Delta Load**:
  - **Insert**: Adds new rows if the `car_id` does not exist in the database.
  - **Update**: Modifies existing rows by matching on `car_id` and updating
    fields (`price`, `is_sold`).

---

### **4. Output Verification**:

To verify the data after full load and delta load, you can query the tables:

```python
# Query all data
with Session(engine) as session:
    brands = session.query(CarBrand).all()
    models = session.query(CarModel).all()
    cars = session.query(CarInfo).all()

    print("Brands:")
    for brand in brands:
        print(brand.brand_id, brand.name)

    print("\nModels:")
    for model in models:
        print(model.model_id, model.name, model.brand_id)

    print("\nCars:")
    for car in cars:
        print(car.car_id, car.model_id, car.price, car.is_sold)
```

---

### **5. Optimizing for Larger Data:**

For larger datasets, apply **chunked processing** and/or database-side
operations for deduplication and updates. You can also use bulk insert and
database transactions for efficiency.

Let me know if you need further optimizations or explanations!

---

## Update the requirements

I need a single table with a complete data load, including all information.

- Following this initial full load, subsequent data loads will be incremental
  deltas, each timestamped to indicate the loading session.
- When retrieving data for a specific car, it should display its complete history.
- Each car can have multiple rows representing changes in prices or other dynamic variables.
- Each activity originates from a unique delta load session, identifiable by a unique ID.
- The expected result is a time series for price with timestamps, indicating the
  number of days since the full load.
- Additionally, delta loads should include NaN
  values for static variables that remain unchanged.

---

To achieve this, we’ll design a single table with the following properties:

1. **One table (`CarData`)**: This table will store all the data, including
   dynamic and static variables.
2. **Full Load**: Inserts all cars and their initial details, marking them as
   the baseline (`load_type='full'`).
3. **Delta Load**: Tracks changes in dynamic variables (e.g., `price`) while
   static variables remain `NULL` unless updated. Each delta load session has a
   unique session ID and timestamp.
4. **Querying**: Fetch a car's history, showing a **time series** of changes in
   variables like `price`, `days_since_full_load`, and other relevant fields.

---

### **1. Schema Design for `CarData` Table**

The schema includes:

- `car_id`: Unique identifier for the car.
- `model_id`: Foreign key linking to the car model.
- `price`: Dynamic variable.
- `is_sold`: Dynamic variable.
- `brand_name`, `model_name`: Static variables.
- `load_type`: `full` for full loads and `delta` for delta loads.
- `load_session_id`: Unique session ID for each load.
- `load_timestamp`: Timestamp of the load.
- Other metadata (e.g., `days_since_full_load`).

---

### **2. Create Table**

```python
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, ForeignKey, DateTime
)
from sqlalchemy.orm import declarative_base
from datetime import datetime
import pandas as pd

Base = declarative_base()

class CarData(Base):
    __tablename__ = 'car_data'

    car_id = Column(Integer, primary_key=True)
    model_id = Column(Integer, nullable=False)
    brand_name = Column(String, nullable=True)  # Static variable
    model_name = Column(String, nullable=True)  # Static variable
    price = Column(Float, nullable=True)  # Dynamic variable
    is_sold = Column(Integer, nullable=True)  # Dynamic variable (0/1)
    load_type = Column(String, nullable=False)  # 'full' or 'delta'
    load_session_id = Column(String, nullable=False)  # Unique ID for the load
    load_timestamp = Column(DateTime, default=datetime.utcnow)
    days_since_full_load = Column(Integer, nullable=True)  # Computed on fetch

DATABASE_URL = "sqlite:///car_data.db"
engine = create_engine(DATABASE_URL, future=True)

# Create table
Base.metadata.create_all(engine)
```

---

### **3. Full Load**

Insert initial car data with all details.

```python
# Full Load Data
full_load_data = pd.DataFrame({
    'car_id': [1, 2, 3],
    'model_id': [101, 102, 103],
    'brand_name': ['Toyota', 'Honda', 'Ford'],
    'model_name': ['Camry', 'Civic', 'Focus'],
    'price': [30000, 25000, 20000],
    'is_sold': [0, 1, 0],
    'load_type': 'full',
    'load_session_id': 'full_load_1',
    'load_timestamp': [datetime(2024, 11, 16)] * 3  # Use current date
})

# Insert Full Load into the database
with engine.connect() as connection:
    full_load_data.to_sql('car_data', con=connection, if_exists='append', index=False)

print("Full load completed!")
```

---

### **4. Delta Load**

Handle changes in dynamic variables (`price`, `is_sold`) and insert `NULL` for static variables.

```python
# Delta Load Data
delta_load_data = pd.DataFrame({
    'car_id': [1, 3],  # Car IDs being updated
    'model_id': [101, 103],  # Model IDs remain the same
    'brand_name': [None, None],  # Static variables unchanged
    'model_name': [None, None],  # Static variables unchanged
    'price': [31000, 21000],  # Updated prices
    'is_sold': [0, 1],  # Updated sold status
    'load_type': 'delta',
    'load_session_id': 'delta_load_1',
    'load_timestamp': [datetime(2024, 11, 17)] * 2  # Use current date
})

# Insert Delta Load into the database
with engine.connect() as connection:
    delta_load_data.to_sql('car_data', con=connection, if_exists='append', index=False)

print("Delta load completed!")
```

---

### **5. Fetch History for a Given Car**

Query the history of a specific car, compute derived fields like `days_since_full_load`, and generate a time series.

```python
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Session = sessionmaker(bind=engine)
session = Session()

# Fetch history for a specific car
car_id_to_fetch = 1
history_query = session.execute(
    f"""
    SELECT car_id, model_id, brand_name, model_name, price, is_sold,
           load_type, load_session_id, load_timestamp
    FROM car_data
    WHERE car_id = {car_id_to_fetch}
    ORDER BY load_timestamp
    """
)

# Process the result to calculate `days_since_full_load`
history = []
full_load_date = None
for row in history_query:
    if row.load_type == 'full':
        full_load_date = row.load_timestamp
    days_since_full_load = (row.load_timestamp - full_load_date).days if full_load_date else None
    history.append({
        'car_id': row.car_id,
        'price': row.price,
        'is_sold': row.is_sold,
        'load_session_id': row.load_session_id,
        'load_type': row.load_type,
        'load_timestamp': row.load_timestamp,
        'days_since_full_load': days_since_full_load
    })

# Display time series
print(pd.DataFrame(history))
```

---

### **6. Expected Results**

For a car with `car_id = 1`, the table might look like this:

| car_id | price | is_sold | load_session_id | load_type | load_timestamp      | days_since_full_load |
| ------ | ----- | ------- | --------------- | --------- | ------------------- | -------------------- |
| 1      | 30000 | 0       | full_load_1     | full      | 2024-11-16 00:00:00 | 0                    |
| 1      | 31000 | 0       | delta_load_1    | delta     | 2024-11-17 00:00:00 | 1                    |

This structure shows:

1. **Time series of changes** for dynamic variables (`price`, `is_sold`).
2. Computed `days_since_full_load`.

---

### **Next Steps:**

- Extend the logic for **bulk delta loads** using session IDs.
- Add indexes to optimize queries on `car_id` and `load_timestamp`.

Let me know if you need further enhancements!
