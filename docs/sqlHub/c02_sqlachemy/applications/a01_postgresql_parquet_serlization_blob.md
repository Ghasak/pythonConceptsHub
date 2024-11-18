# System Build - Storing Blobs

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->

**Table of Contents**

- [System Build - Storing Blobs](#system-build---storing-blobs)
  - [Requirements advised](#requirements-advised)
  - [Solution](#solution)
    - [Explanation of Code](#explanation-of-code)
    - [Requirements](#requirements)
  - [Next Requirements](#next-requirements)
    - [Explanation of Code Updates](#explanation-of-code-updates)
  - [Next Requirements](#next-requirements-1)
    - [Step 1: Define the Table Structure with Relationships](#step-1-define-the-table-structure-with-relationships)
    - [Step 2: Create Tables if They Don’t Exist](#step-2-create-tables-if-they-dont-exist)
    - [Step 3: Insert Initial Data](#step-3-insert-initial-data)
    - [Step 4: Handle Delta Load](#step-4-handle-delta-load)
    - [Code Implementation](#code-implementation)
- [Define the base](#define-the-base)
- [UUID generator function](#uuid-generator-function)
- [Define CarBrand table (1-to-many with CarModel)](#define-carbrand-table-1-to-many-with-carmodel)
- [Define CarModel table (1-to-many with CarInfo, many-to-1 with CarBrand)](#define-carmodel-table-1-to-many-with-carinfo-many-to-1-with-carbrand)
  - [-](#-)
  - [Next Requirements](#next-requirements-2)
    - [1. **CarBrand Table**](#1-carbrand-table)
    - [2. **CarModel Table**](#2-carmodel-table)
    - [3. **CarInfo Table (Initial Load)**](#3-carinfo-table-initial-load)
    - [4. **CarInfo Table (After Delta Load)**](#4-carinfo-table-after-delta-load)
  - [Next Requirements](#next-requirements-3)
    - [SQLAlchemy Query to Find a Specific Car by `car_id`](#sqlalchemy-query-to-find-a-specific-car-by-car_id)
    - [Expected Result for the Query](#expected-result-for-the-query)
  - [Dyanmic delta load](#dyanmic-delta-load)
    - [Step 1: Create `CarInfoHistory` Table](#step-1-create-carinfohistory-table)
    - [Step 2: Modify the Update Function to Log Changes](#step-2-modify-the-update-function-to-log-changes)
    - [Step 3: Query Historical Data](#step-3-query-historical-data)
    - [Code Implementation](#code-implementation-1)
    - [Example Usage](#example-usage)
    - [Expected Results for `CarInfoHistory` Table](#expected-results-for-carinfohistory-table)
    - [Explanation of Output Fields:](#explanation-of-output-fields)
  - [What will be affected in Dynamic delta-load?](#what-will-be-affected-in-dynamic-delta-load)
  - [More about delta-load](#more-about-delta-load)
    - [1. **Data Ingestion and Initial Load Preparation**](#1-data-ingestion-and-initial-load-preparation)
    - [2. **Determine Change Detection Logic**](#2-determine-change-detection-logic)
    - [3. **Implement Table-Specific Logic**](#3-implement-table-specific-logic)
    - [4. **Optimize with Incremental Updates**](#4-optimize-with-incremental-updates)
    - [5. **Transaction Management**](#5-transaction-management)
    - [6. **Efficient Logging and Archiving**](#6-efficient-logging-and-archiving)
    - [Summary of the Workflow](#summary-of-the-workflow)
  - [Optimial way to store data in PostgreSQL](#optimial-way-to-store-data-in-postgresql)
    - [1. Storing a Pickled DataFrame in PostgreSQL](#1-storing-a-pickled-dataframe-in-postgresql)
      - [Steps](#steps)
      - [Example Code](#example-code)
      - [Expected Results](#expected-results)
    - [2. Storing a DataFrame as JSON in PostgreSQL](#2-storing-a-dataframe-as-json-in-postgresql)
      - [Steps](#steps-1)
      - [Example Code](#example-code-1)
      - [Expected Results](#expected-results-1)
    - [Summary](#summary)
  - [How about the size of the database?](#how-about-the-size-of-the-database)
  - [Strategies and Ways to Mitigate Database Size Growth](#strategies-and-ways-to-mitigate-database-size-growth)
  - [Serialize with Parquet](#serialize-with-parquet)
    - [Advantages of Using Parquet for Serialization](#advantages-of-using-parquet-for-serialization)
    - [How to Use Parquet for Serialization in PostgreSQL](#how-to-use-parquet-for-serialization-in-postgresql)
    - [Example Code](#example-code-2)
    - [Expected Results](#expected-results-2)
    - [Summary](#summary-1)

<!-- markdown-toc end -->

## Requirements advised

Using SQL Alchemy 2.0, I need you to:

1. **Establish a connection:** Connect with the psycopg2 driver to a PostgreSQL
   database.
2. **Create three tables:**
   - `car_brand`: Stores car brand information.
   - `car_model`: Stores car model information associated with each brand.
   - `car_info`: Stores detailed information about individual cars.
     This table should have columns representing various car attributes
     like engine size, VIN, color, price, status, etc.
3. **Handle existing tables:** Before creating any tables, check if they already
   exist. If they do, skip the creation process. Otherwise, create all three
   tables.
4. **Load initial data:** Assuming you have a Pandas DataFrame containing
   initial car information, load it into the respective tables after table
   creation.
5. **Implement delta loading:** Allow for subsequent runs to append new car data
   (provided as a Pandas DataFrame) to existing records in the `car_info` table.
6. **Utilize UUIDs:** Generate a unique hash number (UUID) for each record and
   use it as the primary key for all three tables.
7. **Optimize search speed:** Create an index on the `car_id` column in the
   `car_info` table to enhance search performance.

## Solution

To set up your environment with SQLAlchemy 2.0, using the `psycopg2` driver with
PostgreSQL, we'll define three tables: `CarBrand`, `CarModel`, and `CarInfo`.
We'll include an index on the `car_id` column in the `CarInfo` table for
optimized search performance and use a hash-based UUID for unique identification
of records.

Here’s a structured implementation for your requirements:

1. **Database Setup and Connection**: Use SQLAlchemy to connect with the `psycopg2` driver.
2. **Table Definitions**: Define tables `CarBrand`, `CarModel`, and `CarInfo` with UUIDs and indexed `car_id`.
3. **Table Creation**: Check if tables exist before creating them.
4. **Load Data**: Insert data from a pandas DataFrame, and handle delta loads.

```python
import uuid
import pandas as pd
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, Index, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Define the base
Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class CarBrand(Base):
    __tablename__ = 'car_brand'
    brand_id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True)

class CarModel(Base):
    __tablename__ = 'car_model'
    model_id = Column(String, primary_key=True, default=generate_uuid)
    brand_id = Column(String)  # ForeignKey if you'd like
    name = Column(String)

class CarInfo(Base):
    __tablename__ = 'car_info'
    car_id = Column(String, primary_key=True, default=generate_uuid)
    model_id = Column(String)  # ForeignKey if you'd like
    engine_size = Column(Float)
    vin = Column(String, unique=True)
    color = Column(String)
    price = Column(Float)
    status = Column(Boolean)
    # Add index for car_id
    __table_args__ = (Index('ix_car_id', "car_id"),)

DATABASE_URL = "postgresql+psycopg2://username:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Create tables if they don't exist
def create_tables():
    try:
        Base.metadata.create_all(engine)
        print("Tables created successfully.")
    except OperationalError as e:
        print(f"Error in creating tables: {e}")

# Insert data from DataFrame
def insert_data(df, table_class):
    with Session() as session:
        for _, row in df.iterrows():
            record = table_class(**row.to_dict())
            session.add(record)
        session.commit()
        print("Data inserted successfully.")

# Delta Load function
def load_delta_data(df, table_class):
    with Session() as session:
        for _, row in df.iterrows():
            # Here, add row only if not already present based on unique fields (e.g., vin)
            exists = session.query(table_class).filter_by(vin=row['vin']).first()
            if not exists:
                record = table_class(**row.to_dict())
                session.add(record)
        session.commit()
        print("Delta data loaded successfully.")

# Example usage
create_tables()

# Example pandas DataFrame (initial load)
df_car_brand = pd.DataFrame([{'name': 'Toyota'}, {'name': 'Honda'}])
df_car_model = pd.DataFrame([{'name': 'Corolla', 'brand_id': '1'}, {'name': 'Civic', 'brand_id': '2'}])
df_car_info = pd.DataFrame([
    {'model_id': '1', 'engine_size': 2.0, 'vin': 'ABC123', 'color': 'Red', 'price': 15000, 'status': True},
    {'model_id': '2', 'engine_size': 1.5, 'vin': 'DEF456', 'color': 'Blue', 'price': 13000, 'status': False},
])

# Insert initial data
insert_data(df_car_brand, CarBrand)
insert_data(df_car_model, CarModel)
insert_data(df_car_info, CarInfo)

# Example delta load
delta_df_car_info = pd.DataFrame([
    {'model_id': '1', 'engine_size': 2.2, 'vin': 'GHI789', 'color': 'Black', 'price': 16000, 'status': True}
])
load_delta_data(delta_df_car_info, CarInfo)
```

### Explanation of Code

- **UUIDs**: Each table record gets a UUID as its primary key using the
  `generate_uuid` function.
- **Index on `car_id`**: For faster search in `CarInfo`.
- **Create Tables if Not Exists**: `create_tables()` checks if the tables are
  present, and if not, creates them.
- **Data Insertion**: `insert_data()` adds initial data from pandas DataFrames.
- **Delta Load**: `load_delta_data()` checks if a record (e.g., by `vin`) exists
  before inserting new data, which is useful for handling delta loads.

### Requirements

- Adjust the `DATABASE_URL` to match your PostgreSQL setup.
- Ensure pandas DataFrames (`df_car_brand`, `df_car_model`, `df_car_info`)
  contain matching column names with SQLAlchemy table attributes.

This setup will provide a structured, scalable way to manage data in PostgreSQL
with SQLAlchemy, allowing for efficient initial loads and future delta loads.

---

## Next Requirements

The tables are connected using one-to-many relationships. Logic should be
revised to reflect that for a given brand, there are many models, and for each
model, there are many cars.

Thank you for clarifying. We can revise the implementation to include proper
one-to-many relationships between the tables `CarBrand`, `CarModel`, and
`CarInfo` as follows:

- **One `CarBrand` has many `CarModel`s**.
- **One `CarModel` has many `CarInfo` records**.

I’ll adjust the schema definitions accordingly, adding `ForeignKey` constraints
to establish these relationships. Here’s the updated code:

```python
import uuid
import pandas as pd
from sqlalchemy import (
    create_engine, Column, String, Integer, Float, Boolean, ForeignKey, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import OperationalError

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class CarBrand(Base):
    __tablename__ = 'car_brand'
    brand_id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True)

    # One-to-many relationship with CarModel
    models = relationship("CarModel", back_populates="brand", cascade="all, delete-orphan")

class CarModel(Base):
    __tablename__ = 'car_model'
    model_id = Column(String, primary_key=True, default=generate_uuid)
    brand_id = Column(String, ForeignKey('car_brand.brand_id'))
    name = Column(String)

    # Relationships
    brand = relationship("CarBrand", back_populates="models")
    cars = relationship("CarInfo", back_populates="model", cascade="all, delete-orphan")

class CarInfo(Base):
    __tablename__ = 'car_info'
    car_id = Column(String, primary_key=True, default=generate_uuid)
    model_id = Column(String, ForeignKey('car_model.model_id'))
    engine_size = Column(Float)
    vin = Column(String, unique=True)
    color = Column(String)
    price = Column(Float)
    status = Column(Boolean)

    # Relationship with CarModel
    model = relationship("CarModel", back_populates="cars")

    # Index for faster search
    __table_args__ = (Index('ix_car_id', "car_id"),)

DATABASE_URL = "postgresql+psycopg2://username:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_tables():
    try:
        Base.metadata.create_all(engine)
        print("Tables created successfully.")
    except OperationalError as e:
        print(f"Error in creating tables: {e}")

def insert_data(df, table_class):
    with Session() as session:
        for _, row in df.iterrows():
            record = table_class(**row.to_dict())
            session.add(record)
        session.commit()
        print("Data inserted successfully.")

def load_delta_data(df, table_class):
    with Session() as session:
        for _, row in df.iterrows():
            # Add row only if it doesn't exist based on unique fields (e.g., vin)
            exists = session.query(table_class).filter_by(vin=row['vin']).first()
            if not exists:
                record = table_class(**row.to_dict())
                session.add(record)
        session.commit()
        print("Delta data loaded successfully.")

create_tables()

df_car_brand = pd.DataFrame([{'name': 'Toyota'}, {'name': 'Honda'}])
df_car_model = pd.DataFrame([
    {'name': 'Corolla', 'brand_id': '1'}, {'name': 'Civic', 'brand_id': '2'}
])
df_car_info = pd.DataFrame([
    {'model_id': '1', 'engine_size': 2.0, 'vin': 'ABC123', 'color': 'Red', 'price': 15000, 'status': True},
    {'model_id': '2', 'engine_size': 1.5, 'vin': 'DEF456', 'color': 'Blue', 'price': 13000, 'status': False}
])
insert_data(df_car_brand, CarBrand)
insert_data(df_car_model, CarModel)
insert_data(df_car_info, CarInfo)

delta_df_car_info = pd.DataFrame([
    {'model_id': '1', 'engine_size': 2.2, 'vin': 'GHI789', 'color': 'Black', 'price': 16000, 'status': True}
])
load_delta_data(delta_df_car_info, CarInfo)
```

### Explanation of Code Updates

- **Relationships**:
  - `CarBrand` has a one-to-many relationship with `CarModel` using `models` as a relationship attribute.
  - `CarModel` has a one-to-many relationship with `CarInfo` using `cars` as a relationship attribute.
  - `CarInfo` references `CarModel` through the `model_id` foreign key.
- **Cascading Deletes**: Adding `cascade="all, delete-orphan"` to ensure dependent records are removed if a parent record is deleted.
- **Data Insertion with Relationships**: Data can be inserted with references using the IDs (e.g., `brand_id` in `CarModel` and `model_id` in `CarInfo`).

This ensures a properly relational structure, where:

- Each `CarBrand` can have multiple `CarModel`s.
- Each `CarModel` can be associated with multiple `CarInfo` records.

---

## Next Requirements

Let’s walk through the process of creating the tables and loading data
step-by-step for the initial load, followed by how to handle a delta load.

### Step 1: Define the Table Structure with Relationships

We’ll start by defining three tables with the necessary relationships:

1. **CarBrand**: Represents a car brand (e.g., Toyota, Honda).
2. **CarModel**: Represents a car model under a specific brand (e.g., Corolla, Civic).
3. **CarInfo**: Represents individual car information with specific details (e.g., engine size, color, price, etc.).

Each table will have a UUID-based primary key and one-to-many relationships, as follows:

- A brand can have multiple models.
- A model can have multiple cars.

### Step 2: Create Tables if They Don’t Exist

In the initial load, we need to check if the tables already exist. If not, we’ll
create them. This is handled by SQLAlchemy's `Base.metadata.create_all(engine)`,
which ensures tables are created based on the defined classes.

### Step 3: Insert Initial Data

For the initial load, we’ll prepare pandas DataFrames for each table with
example data and insert them into the tables.

### Step 4: Handle Delta Load

For subsequent loads (delta loads), we’ll check if each record already exists
(e.g., by checking the `vin` in `CarInfo`). If it does, we’ll skip it;
otherwise, we’ll add it.

Here’s how each step will look in code:

---

### Code Implementation

```python
import uuid
import pandas as pd
from sqlalchemy import (
    create_engine, Column, String, Float, Boolean, ForeignKey, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import OperationalError

# Define the base
Base = declarative_base()

# UUID generator function
def generate_uuid():
    return str(uuid.uuid4())

# Define CarBrand table (1-to-many with CarModel)
class CarBrand(Base):
    __tablename__ = 'car_brand'
    brand_id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True)
    models = relationship("CarModel", back_populates="brand", cascade="all, delete-orphan")

# Define CarModel table (1-to-many with CarInfo, many-to-1 with CarBrand)
class CarModel(Base):
    __tablename__ = 'car_model'
    model_id = Column(String, primary_key=True, default=generate_uuid)
    brand_id = Column(String, ForeignKey('car_brand.brand_id'))
    name = Column(String)
    brand = relationship("CarBrand", back_populates="models")
    cars = relationship("CarInfo", back_populates="model", cascade="all, delete-orphan")

# Define CarInfo table (many-to-1 with CarModel)
class CarInfo(Base):
    __tablename__ = 'car_info'
    car_id = Column(String, primary_key=True, default=generate_uuid)
    model_id = Column(String, ForeignKey('car_model.model_id'))
    engine_size = Column(Float)
    vin = Column(String, unique=True)
    color = Column(String)
    price = Column(Float)
    status = Column(Boolean)
    model = relationship("CarModel", back_populates="cars")
    __table_args__ = (Index('ix_car_id', "car_id"),)

# Set up the database connection
DATABASE_URL = "postgresql+psycopg2://username:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Step 1: Create tables if they don't exist
def create_tables():
    try:
        Base.metadata.create_all(engine)
        print("Tables created successfully.")
    except OperationalError as e:
        print(f"Error in creating tables: {e}")

# Step 2: Insert Initial Data
def insert_data(df, table_class):
    with Session() as session:
        for _, row in df.iterrows():
            record = table_class(**row.to_dict())
            session.add(record)
        session.commit()
        print("Data inserted successfully.")

# Step 3: Delta Load - Check if each record exists, insert if not
def load_delta_data(df, table_class):
    with Session() as session:
        for _, row in df.iterrows():
            # Only insert if the unique field (vin) does not already exist
            exists = session.query(table_class).filter_by(vin=row['vin']).first()
            if not exists:
                record = table_class(**row.to_dict())
                session.add(record)
        session.commit()
        print("Delta data loaded successfully.")

# Step 4: Run the initial setup and insert data

# Create tables
create_tables()

# Prepare example data for initial load
df_car_brand = pd.DataFrame([{'name': 'Toyota'}, {'name': 'Honda'}])
df_car_model = pd.DataFrame([
    {'name': 'Corolla', 'brand_id': '1'},  # Assuming '1' is Toyota's brand_id after insertion
    {'name': 'Civic', 'brand_id': '2'}     # Assuming '2' is Honda's brand_id after insertion
])
df_car_info = pd.DataFrame([
    {'model_id': '1', 'engine_size': 2.0, 'vin': 'ABC123', 'color': 'Red', 'price': 15000, 'status': True},
    {'model_id': '2', 'engine_size': 1.5, 'vin': 'DEF456', 'color': 'Blue', 'price': 13000, 'status': False}
])

# Insert initial data
insert_data(df_car_brand, CarBrand)
insert_data(df_car_model, CarModel)
insert_data(df_car_info, CarInfo)

# Step 5: Perform a delta load
delta_df_car_info = pd.DataFrame([
    {'model_id': '1', 'engine_size': 2.2, 'vin': 'GHI789', 'color': 'Black', 'price': 16000, 'status': True}
])

# Load delta data
load_delta_data(delta_df_car_info, CarInfo)
```

---

### Explanation of Each Step

1. **Table Creation**: `create_tables()` checks if tables already exist. If not,
   they are created based on the schema with relationships.

2. **Initial Load**:

   - Example data for `CarBrand`, `CarModel`, and `CarInfo` is created in pandas
     DataFrames.
   - `insert_data()` inserts records into each table. This function converts
     each row from the DataFrame into a SQLAlchemy object and commits it to the
     database.

3. **Delta Load**:
   - Additional data (delta load) for `CarInfo` is provided in a DataFrame
     (`delta_df_car_info`).
   - `load_delta_data()` checks each record's `vin` to see if it already exists
     in the database. If not, it adds the new record to prevent duplicates.

This setup establishes the initial data, and when new data is received in the
form of a pandas DataFrame, it only inserts records that do not already exist in
the `CarInfo` table. This approach maintains referential integrity across the
tables through foreign keys, and the relationships allow for easily querying
data by brand and model.

---

## Next Requirements

- Show tables of all the steps and expected results at each step
  Here are the expected results for each table with initial load and delta load entries.

---

### 1. **CarBrand Table**

| brand_id | name   |
| -------- | ------ |
| 1        | Toyota |
| 2        | Honda  |

- `brand_id` is a UUID generated for each brand.
- Each brand has a unique name.

---

### 2. **CarModel Table**

| model_id | brand_id | name    |
| -------- | -------- | ------- |
| 1        | 1        | Corolla |
| 2        | 2        | Civic   |

- `model_id` is a UUID generated for each model.
- `brand_id` links each model to its corresponding brand in the `CarBrand` table.
- Each model has a unique name under its brand.

---

### 3. **CarInfo Table (Initial Load)**

| car_id | model_id | engine_size | vin    | color | price | status |
| ------ | -------- | ----------- | ------ | ----- | ----- | ------ |
| abc123 | 1        | 2.0         | ABC123 | Red   | 15000 | True   |
| def456 | 2        | 1.5         | DEF456 | Blue  | 13000 | False  |

- `car_id` is a UUID generated for each car.
- `model_id` links each car to its corresponding model in the `CarModel` table.
- `vin` is unique for each car, which allows for delta checking.
- `status` indicates whether the car is available (True) or not (False).

---

### 4. **CarInfo Table (After Delta Load)**

After running the delta load, the table would include the new entry if it didn’t already exist:

| car_id | model_id | engine_size | vin    | color | price | status |
| ------ | -------- | ----------- | ------ | ----- | ----- | ------ |
| abc123 | 1        | 2.0         | ABC123 | Red   | 15000 | True   |
| def456 | 2        | 1.5         | DEF456 | Blue  | 13000 | False  |
| ghi789 | 1        | 2.2         | GHI789 | Black | 16000 | True   |

- The new entry with `vin = GHI789` has been added because it was not present in the initial load.

---

This layout illustrates how the relationships and primary keys work together,
maintaining the integrity of the data across tables. Each car is uniquely
identified by `car_id`, and each model and brand are associated via `model_id`
and `brand_id`, respectively. The `vin` acts as a unique field for checking
duplicates in the delta load.

---

## Next Requirements

If I want to query a specific car by its ID, please demonstrate how to do so
along with the expected results.

To query a specific car by its `car_id` in SQLAlchemy, you can create a function
that performs a query on the `CarInfo` table, filtering by the `car_id`. Here’s
how you would implement the query and the expected results.

### SQLAlchemy Query to Find a Specific Car by `car_id`

Assuming you want to query for a specific car with a known `car_id`, here’s the code to do it:

```python
from sqlalchemy.orm import Session

# Function to query a car by car_id
def get_car_by_id(car_id):
    with Session(engine) as session:
        car = session.query(CarInfo).filter_by(car_id=car_id).first()
        if car:
            print(f"Car found: {car}")
            return car
        else:
            print("Car not found.")
            return None

# Example usage
car_id_to_query = 'ghi789'  # Replace with the actual UUID of the car you're querying
car = get_car_by_id(car_id_to_query)
if car:
    print(f"Car ID: {car.car_id}, Model ID: {car.model_id}, Engine Size: {car.engine_size}, VIN: {car.vin}, Color: {car.color}, Price: {car.price}, Status: {car.status}")
```

This function opens a session, queries the `CarInfo` table by `car_id`, and returns the car details if found.

### Expected Result for the Query

If `car_id = 'ghi789'` is used, the expected result would be:

| car_id | model_id | engine_size | vin    | color | price | status |
| ------ | -------- | ----------- | ------ | ----- | ----- | ------ |
| ghi789 | 1        | 2.2         | GHI789 | Black | 16000 | True   |

**Explanation of Output Fields:**

- **`car_id`**: The unique ID of the queried car.
- **`model_id`**: The ID of the car model, linking to the `CarModel` table.
- **`engine_size`**: The engine size of the car.
- **`vin`**: The unique vehicle identification number (VIN).
- **`color`**: The color of the car.
- **`price`**: The price of the car.
- **`status`**: The availability status of the car (True for available, False for not available).

This function will print the car's details if found, matching the expected table result.

---

## Dyanmic delta load

Can I retrieve all the information about a given car, including all related
data, to observe changes over time? For example, I'd like to see when and how
the price was updated, along with timestamps.

To track changes such as price updates with timestamps, we can enhance the
`CarInfo` table by adding a separate history table, `CarInfoHistory`, which will
log each change in the car’s details, including the timestamp of when the change
occurred. Each time an update is made to the `CarInfo` table, a corresponding
entry is added to `CarInfoHistory` to log the previous details along with the
timestamp.

Here’s a way to set this up and query historical data.

### Step 1: Create `CarInfoHistory` Table

This table will store the history of changes for each car, including fields like
`price`, `status`, and `timestamp`.

### Step 2: Modify the Update Function to Log Changes

Each time a car’s information is updated (e.g., price), the function will first
insert the current details into `CarInfoHistory` with a timestamp, then update
the `CarInfo` table.

### Step 3: Query Historical Data

You can then query `CarInfoHistory` to view the change history for a specific
car.

---

### Code Implementation

```python
from sqlalchemy import DateTime, func
from datetime import datetime

# Define CarInfoHistory table for tracking changes
class CarInfoHistory(Base):
    __tablename__ = 'car_info_history'
    history_id = Column(String, primary_key=True, default=generate_uuid)
    car_id = Column(String, ForeignKey('car_info.car_id'))
    model_id = Column(String)
    engine_size = Column(Float)
    vin = Column(String)
    color = Column(String)
    price = Column(Float)
    status = Column(Boolean)
    timestamp = Column(DateTime, default=func.now())  # Timestamp for each change

# Update function that logs changes
def update_car_info(car_id, new_data):
    with Session(engine) as session:
        # Fetch the existing car record
        car = session.query(CarInfo).filter_by(car_id=car_id).first()

        if car:
            # Log current state to history table
            history_entry = CarInfoHistory(
                car_id=car.car_id,
                model_id=car.model_id,
                engine_size=car.engine_size,
                vin=car.vin,
                color=car.color,
                price=car.price,
                status=car.status,
                timestamp=datetime.now()
            )
            session.add(history_entry)

            # Update the car's information
            for key, value in new_data.items():
                setattr(car, key, value)

            session.commit()
            print("Car info updated and change logged in history.")
        else:
            print("Car not found.")

# Query function to get all historical data for a specific car
def get_car_history(car_id):
    with Session(engine) as session:
        history = session.query(CarInfoHistory).filter_by(car_id=car_id).order_by(CarInfoHistory.timestamp).all()
        for record in history:
            print(f"Timestamp: {record.timestamp}, Price: {record.price}, Status: {record.status}")
            # Add more fields as needed
        return history
```

---

### Example Usage

1. **Updating Car Information**: Assume the price of a car needs to be updated.

   ```python
   car_id_to_update = 'ghi789'  # Replace with actual car_id
   new_data = {'price': 16500, 'status': False}  # New price and status

   update_car_info(car_id_to_update, new_data)
   ```

   This function will:

   - Log the current data in `CarInfoHistory`.
   - Update the `CarInfo` table with new values.

2. **Querying Car History**: To view the change history for a specific car.

   ```python
   car_history = get_car_history('ghi789')
   ```

   This query will return a list of historical records for the given `car_id`,
   showing each change in the `price`, `status`, or any other tracked attributes
   along with the `timestamp`.

---

### Expected Results for `CarInfoHistory` Table

Assuming `car_id = 'ghi789'`, and a few changes were made over time, the `CarInfoHistory` table might look like this:

| history_id | car_id | model_id | engine_size | vin    | color | price | status | timestamp           |
| ---------- | ------ | -------- | ----------- | ------ | ----- | ----- | ------ | ------------------- |
| hist_1     | ghi789 | 1        | 2.2         | GHI789 | Black | 16000 | True   | 2024-11-10 10:00:00 |
| hist_2     | ghi789 | 1        | 2.2         | GHI789 | Black | 16500 | False  | 2024-11-12 15:30:00 |
| hist_3     | ghi789 | 1        | 2.2         | GHI789 | Black | 17000 | True   | 2024-11-14 09:00:00 |

### Explanation of Output Fields:

- **`history_id`**: A unique ID for each historical record.
- **`car_id`**: The ID of the car for which this record logs a change.
- **`model_id`, `engine_size`, `vin`, `color`**: Car details that remained the same during updates.
- **`price`**: The price at the time of each change.
- **`status`**: The status (availability) at each point in time.
- **`timestamp`**: The date and time when the change was logged.

This setup provides a full change history for each car, allowing you to track
past values and see how attributes like `price` and `status` changed over time.

---

## What will be affected in Dynamic delta-load?

Usually, a compensating delta load only affects car information and car history,
leaving other aspects unchanged.

Yes, exactly. Since `CarBrand` and `CarModel` represent more static data, they
are typically unaffected by delta loads. Delta loads will mostly update dynamic
information in the `CarInfo` table, such as `price` or `status`, and log those
changes in the `CarInfoHistory` table. This setup allows for efficient tracking
of changes where they are most likely to occur, without repeatedly altering the
relatively stable `CarBrand` and `CarModel` tables.

---

## More about delta-load

If these tables are separated as shown, but also dynamically change values, how
will the delta load be applied and separated between them? What are some common
coding practices for handling such scenarios? I'm looking for a discussion
rather than code examples.

In a scenario where delta loads affect dynamic values across different tables,
but most changes are concentrated in certain tables (like `CarInfo` and
`CarInfoHistory`), a common approach is to use a well-defined update and
tracking process that can efficiently detect and apply changes only where
needed. Here’s a breakdown of how this can be done:

### 1. **Data Ingestion and Initial Load Preparation**

- **Identify Unique Keys**: Ensure each record in your incoming delta load
  (e.g., a pandas DataFrame) has a unique identifier, such as `car_id` or
  `vin` for `CarInfo`. This makes it easy to compare incoming data with
  existing records.
- **Separate Data by Table**: The delta load might contain fields that belong
  to different tables. Use logic to separate these fields before processing
  (e.g., if only `price` or `status` fields are present, the data is relevant
  only for `CarInfo`).

### 2. **Determine Change Detection Logic**

- **Hashing**: One efficient way to detect changes is by hashing the rows or
  specific columns of each record and storing those hashes. When a delta load
  arrives, calculate the hash for each incoming record and compare it to the
  stored hash. If they differ, there’s a change.
- **Timestamps or Versioning**: If each record in `CarInfo` includes a
  `last_updated` timestamp, you can compare the timestamp in the delta load
  to detect if the incoming data is newer.

### 3. **Implement Table-Specific Logic**

- **For `CarInfo`**:

  - If the delta load contains changes to car attributes (e.g., `price`,
    `status`), update the existing records in `CarInfo` as needed.
  - After updating, log the original values along with a timestamp in
    `CarInfoHistory` for tracking purposes.

- **For `CarInfoHistory`**:

  - Each change to `CarInfo` should trigger an insertion into
    `CarInfoHistory`.
  - Maintain relationships through `car_id` so that each history entry
    corresponds to a unique car in `CarInfo`.
  - If only certain fields are updated (e.g., `price`), store only those
    specific changes, if that fits your tracking strategy.

- **For Static Tables (`CarBrand` and `CarModel`)**:
  - Since these tables don’t change frequently, apply delta updates only when
    absolutely necessary, such as adding new brands or models.
  - Periodically sync these tables only if the delta load indicates new
    entries (e.g., new model for an existing brand).

### 4. **Optimize with Incremental Updates**

- **Batch Updates**: Instead of updating each record individually, perform
  batch updates where possible. For example, use a bulk update operation for
  all modified records in `CarInfo`.
- **Partial Updates**: Update only the fields that have changed. For example,
  if only `price` and `status` have changed, avoid updating the entire row.

### 5. **Transaction Management**

- Use transactions to ensure data consistency. For instance, updating
  `CarInfo` and inserting into `CarInfoHistory` should be within the same
  transaction to avoid mismatched states.
- If an error occurs during an update, a rollback will prevent partial
  updates that could corrupt your data.

### 6. **Efficient Logging and Archiving**

- For tables like `CarInfoHistory` that can grow large, implement strategies
  to archive or purge outdated entries periodically.
- Indexing important fields in `CarInfoHistory`, such as `timestamp` and
  `car_id`, will help keep queries responsive as the history table grows.

### Summary of the Workflow

1. **Ingest delta load** and **separate data by table** based on fields.
2. **Check for changes** by hashing, timestamps, or direct comparisons.
3. **Apply updates to `CarInfo`** and **log changes in `CarInfoHistory`** if values have changed.
4. **Batch process updates** and handle in transactions for consistency.
5. **Maintain `CarBrand` and `CarModel`** tables only as needed with minimal updates.

By following these steps, you ensure efficient delta handling, tracking, and
historical logging across multiple tables without redundant updates to stable
tables.

---

## Optimial way to store data in PostgreSQL

Can a PostgreSQL database be used to store a Pandas DataFrame as a row? Or could
a pickle file achieve this? If so, please provide a simple example with the
expected results for both methods.

Yes, PostgreSQL can store a pandas DataFrame as a single row, typically by
serializing it before storage. Common approaches include:

1. **Storing as a Pickle File**: Serialize the DataFrame with `pickle`, then
   store it as a `BYTEA` (binary) in PostgreSQL.
2. **Storing as JSON**: Convert the DataFrame to JSON format, then store it as a
   JSON or JSONB type.

Let’s go over each approach with examples and expected results.

---

### 1. Storing a Pickled DataFrame in PostgreSQL

This approach serializes the DataFrame using `pickle` and saves it as binary data in a `BYTEA` column.

#### Steps

1. Serialize the DataFrame with `pickle.dumps`.
2. Insert it into a `BYTEA` column in PostgreSQL.
3. To retrieve, fetch the binary data and deserialize with `pickle.loads`.

#### Example Code

```python
import pandas as pd
import pickle
from sqlalchemy import create_engine, Column, Integer, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define base and create table structure
Base = declarative_base()

class DataFrameStore(Base):
    __tablename__ = 'dataframe_store'
    id = Column(Integer, primary_key=True)
    data = Column(LargeBinary)  # Column for pickled data

# Connect to PostgreSQL
DATABASE_URL = "postgresql+psycopg2://username:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

# Sample DataFrame
df = pd.DataFrame({'A': [1, 2, 3], 'B': ['X', 'Y', 'Z']})

# Serialize with pickle
pickled_data = pickle.dumps(df)

# Store the serialized DataFrame in PostgreSQL
with Session() as session:
    store = DataFrameStore(data=pickled_data)
    session.add(store)
    session.commit()
    print("DataFrame stored as binary.")

# Retrieve and deserialize
with Session() as session:
    stored_data = session.query(DataFrameStore).filter_by(id=1).first()
    retrieved_df = pickle.loads(stored_data.data)
    print(retrieved_df)
```

#### Expected Results

**In PostgreSQL:**

| id  | data                      |
| --- | ------------------------- |
| 1   | \x… (binary pickled data) |

**Retrieved DataFrame:**

```plaintext
   A  B
0  1  X
1  2  Y
2  3  Z
```

This approach allows you to store the entire DataFrame in a single column and retrieve it later with the exact structure intact.

---

### 2. Storing a DataFrame as JSON in PostgreSQL

This method converts the DataFrame to JSON format and stores it in a `JSONB` column in PostgreSQL. It’s useful for readability and partial querying.

#### Steps

1. Convert the DataFrame to JSON with `DataFrame.to_json`.
2. Store the JSON data in a `JSONB` column in PostgreSQL.
3. Retrieve it and convert back to a DataFrame with `pd.read_json`.

#### Example Code

```python
from sqlalchemy import JSON

class DataFrameStoreJSON(Base):
    __tablename__ = 'dataframe_store_json'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)  # Column for JSON data

# Create the table
Base.metadata.create_all(engine)

# Convert DataFrame to JSON format
json_data = df.to_json(orient="split")

# Store JSON data in PostgreSQL
with Session() as session:
    store_json = DataFrameStoreJSON(data=json_data)
    session.add(store_json)
    session.commit()
    print("DataFrame stored as JSON.")

# Retrieve and convert back to DataFrame
with Session() as session:
    stored_json_data = session.query(DataFrameStoreJSON).filter_by(id=1).first()
    retrieved_df_json = pd.read_json(stored_json_data.data, orient="split")
    print(retrieved_df_json)
```

#### Expected Results

**In PostgreSQL:**

| id  | data                                        |
| --- | ------------------------------------------- |
| 1   | {"columns":["A","B"],"index":[0,1,2], ... } |

**Retrieved DataFrame:**

```plaintext
   A  B
0  1  X
1  2  Y
2  3  Z
```

This JSON approach is more readable within the database and allows querying
specific parts of the JSON if needed.

---

### Summary

Both methods can store a pandas DataFrame in PostgreSQL, with differences in
readability and querying capabilities:

- **Pickle (BYTEA)**: Best for exact structural storage and retrieval but opaque
  in the database.
- **JSON (JSONB)**: Allows partial querying and is human-readable but may lose
  some precision in data types compared to the original DataFrame.

---

## How about the size of the database?

Storing serialized DataFrames (whether as pickled binary or JSON) in PostgreSQL
can increase the database size significantly, especially if:

1. **Frequent Updates**: You store frequent, large updates to the DataFrame in
   the database. Each stored instance adds data rather than updating specific
   fields, leading to rapid storage growth.
2. **Large DataFrames**: DataFrames with many rows or complex data (like nested
   structures in JSON) require substantial storage. JSON and pickle formats are
   not compressed, so they consume more space than plain tabular data.

3. **Historical Logs**: If you're storing multiple historical versions or
   snapshots of a DataFrame (e.g., for change tracking), each serialized
   DataFrame can add to storage requirements over time.

4. **Indexes**: Adding indexes to serialized data columns (especially JSONB) can
   further increase database size, as the database needs to store index data
   alongside the original JSON content.

## Strategies and Ways to Mitigate Database Size Growth

1. **Store Only Essential Data**: Instead of storing the entire DataFrame,
   consider breaking it down and storing only essential columns in normalized
   tables. For example, store key metrics or changes instead of full snapshots.

2. **Compression**: You could compress pickled data before storing it (e.g.,
   using gzip) to reduce size. However, this will add some complexity to the
   storage and retrieval processes.

3. **Archival Strategy**: Regularly archive older versions of the DataFrame to
   an external storage system (e.g., a data lake or file storage) and remove
   them from PostgreSQL to save space.

4. **Database Partitioning**: If historical data must stay in PostgreSQL,
   consider partitioning by time or categories to limit table size and improve
   query performance.

5. **Use External Storage**: For very large DataFrames, it’s often more
   efficient to store them in a dedicated data storage system (e.g., S3 or HDFS)
   and only keep metadata or references in PostgreSQL.

While PostgreSQL supports storing complex data structures, using it for full
DataFrame storage is best kept for small or infrequently updated snapshots. For
large, frequently changing datasets, external storage and optimized database
design will help manage database size and performance better.

---

## Serialize with Parquet

Using **Parquet** format to serialize pandas DataFrames is an excellent option
for reducing storage size, especially compared to JSON or pickled binary
formats. Parquet is a columnar storage format that is **highly efficient for
both storage and retrieval**, making it particularly suitable for large datasets
with complex structures.

### Advantages of Using Parquet for Serialization

1. **Compression**: Parquet is a compressed format, which means it takes up
   significantly less space than JSON or pickled formats. It’s designed to
   efficiently store complex data structures without inflating storage size.

2. **Columnar Storage**: Parquet’s columnar format makes it faster for
   analytical queries and partial reads, as you can access only the columns you
   need without reading the entire file.

3. **Better Compatibility**: Parquet is a popular format in data processing
   ecosystems (e.g., Spark, Hive, Hadoop), which makes it easy to move and
   analyze data in different platforms if needed.

4. **Performance**: Parquet files are faster to read and write compared to JSON
   or pickled formats, especially for large datasets, due to column-based
   compression and encoding.

### How to Use Parquet for Serialization in PostgreSQL

While PostgreSQL doesn’t directly support the Parquet format, you can still
store a serialized Parquet file as a binary blob in a `BYTEA` column, similar to
how you’d store pickled data. Here’s how it could work:

1. **Serialize the DataFrame to Parquet**: Use pandas and pyarrow to write the
   DataFrame to a Parquet binary stream.
2. **Store the Parquet Binary**: Insert the binary data into a `BYTEA` column in
   PostgreSQL.
3. **Retrieve and Deserialize**: When fetching, load the binary data from
   PostgreSQL and deserialize it back into a DataFrame.

### Example Code

```python
import pandas as pd
import io
import pyarrow as pa
import pyarrow.parquet as pq
from sqlalchemy import create_engine, Column, Integer, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define base and create table structure
Base = declarative_base()

class DataFrameStoreParquet(Base):
    __tablename__ = 'dataframe_store_parquet'
    id = Column(Integer, primary_key=True)
    data = Column(LargeBinary)  # Column for Parquet binary data

# Connect to PostgreSQL
DATABASE_URL = "postgresql+psycopg2://username:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

# Sample DataFrame
df = pd.DataFrame({'A': [1, 2, 3], 'B': ['X', 'Y', 'Z']})

# Serialize to Parquet
buffer = io.BytesIO()
table = pa.Table.from_pandas(df)
pq.write_table(table, buffer)
parquet_data = buffer.getvalue()

# Store the Parquet data in PostgreSQL
with Session() as session:
    store = DataFrameStoreParquet(data=parquet_data)
    session.add(store)
    session.commit()
    print("DataFrame stored as Parquet binary.")

# Retrieve and deserialize from Parquet
with Session() as session:
    stored_data = session.query(DataFrameStoreParquet).filter_by(id=1).first()
    if stored_data:
        buffer = io.BytesIO(stored_data.data)
        table = pq.read_table(buffer)
        retrieved_df = table.to_pandas()
        print(retrieved_df)
```

### Expected Results

**In PostgreSQL:**

| id  | data                      |
| --- | ------------------------- |
| 1   | \x… (binary Parquet data) |

**Retrieved DataFrame:**

```plaintext
   A  B
0  1  X
1  2  Y
2  3  Z
```

### Summary

Using Parquet can significantly reduce database size due to its efficient
compression. This is particularly useful if you plan to store multiple
DataFrames or large datasets. The approach is similar to storing pickled data
but offers better compression and performance for large or complex datasets.
