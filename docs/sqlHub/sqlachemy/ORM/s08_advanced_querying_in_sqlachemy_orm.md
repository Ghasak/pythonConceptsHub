# **Title**: `"Advanced Querying in SQLAlchemy ORM (Part 4)"`

For **Part 4**, we’ll dive into **advanced querying techniques** in SQLAlchemy’s ORM. Advanced queries enable you to perform more complex data retrieval and manipulation, leveraging SQLAlchemy’s expressive API to filter, aggregate, and join data across related tables.

---

-

## Summary of Part 4: Advanced Querying Techniques

**Summary**:
In this section, we explore SQLAlchemy’s advanced querying capabilities, focusing on:

1. **Filtering with Conditions**: Using filters with multiple conditions.
2. **Aggregations and Functions**: Leveraging aggregate functions like `SUM`, `COUNT`, `AVG`.
3. **Joins**: Performing inner and outer joins to query data across related tables.
4. **Ordering and Limiting Results**: Sorting and controlling the number of returned records.

These techniques provide a powerful set of tools to retrieve and process complex data efficiently.

---

### Step 1: Filtering with Conditions

SQLAlchemy’s `filter` and `filter_by` methods allow you to apply conditions to your queries. Let’s start by refining our queries with multiple conditions.

1. **Basic Filtering with `filter()`**:

   ```python
   from sqlalchemy import and_, or_

   def get_cars_by_price_and_year(min_price, max_price, min_year):
       """Retrieves cars within a specific price range and minimum year."""
       with Session() as session:
           cars = session.query(Car).filter(
               and_(
                   Car.price >= min_price,
                   Car.price <= max_price,
                   Car.year >= min_year
               )
           ).all()
           for car in cars:
               console.log(f"{car.make} {car.model} - Year: {car.year}, Price: ${car.price}")
   ```

2. **Using OR Conditions**:

   ```python
   def get_cars_by_make_or_year(make, year):
       """Retrieves cars with a specific make or minimum year."""
       with Session() as session:
           cars = session.query(Car).filter(
               or_(Car.make == make, Car.year >= year)
           ).all()
           for car in cars:
               console.log(f"{car.make} {car.model} - Year: {car.year}, Price: ${car.price}")
   ```

3. **Explanation**:
   - `and_()` and `or_()` allow you to chain multiple conditions.
   - **Example**: `get_cars_by_price_and_year(15000, 25000, 2018)` retrieves cars priced between $15,000 and $25,000 and manufactured after 2018.

---

### Step 2: Aggregations and Functions

Aggregation functions like `SUM`, `COUNT`, and `AVG` help summarize data.

1. **Count the Number of Cars**:

   ```python
   from sqlalchemy import func

   def count_total_cars():
       """Counts the total number of cars."""
       with Session() as session:
           total_cars = session.query(func.count(Car.id)).scalar()
           console.log(f"Total number of cars: {total_cars}")
   ```

2. **Calculate Average Price of Cars**:

   ```python
   def average_car_price():
       """Calculates the average price of all cars."""
       with Session() as session:
           avg_price = session.query(func.avg(Car.price)).scalar()
           console.log(f"Average car price: ${avg_price:.2f}")
   ```

3. **Explanation**:
   - **`func.count()`** and **`func.avg()`** represent SQL functions for counting rows and calculating averages.
   - **`scalar()`** retrieves a single value from the query.

---

### Step 3: Joins for Related Data

Joining tables allows you to combine data from related tables. Let’s join `Car` with `Dealership` to retrieve information about each car and its associated dealership.

1. **Inner Join Example**:

   ```python
   def get_cars_with_dealerships():
       """Retrieves cars along with their dealerships."""
       with Session() as session:
           cars = session.query(Car, Dealership).join(Dealership).all()
           for car, dealership in cars:
               console.log(f"{car.make} {car.model} - Dealership: {dealership.name}")
   ```

2. **Left Outer Join Example**:

   ```python
   def get_all_cars_with_or_without_dealerships():
       """Retrieves all cars, including those without dealerships."""
       with Session() as session:
           cars = session.query(Car, Dealership).outerjoin(Dealership).all()
           for car, dealership in cars:
               dealership_name = dealership.name if dealership else "No Dealership"
               console.log(f"{car.make} {car.model} - Dealership: {dealership_name}")
   ```

3. **Explanation**:
   - **`join()`** performs an inner join, retrieving only cars with associated dealerships.
   - **`outerjoin()`** performs a left outer join, retrieving all cars, including those without associated dealerships.

---

### Step 4: Ordering and Limiting Results

You can control the order and number of returned results using `order_by()` and `limit()`.

1. **Ordering Results**:

   ```python
   def get_cars_sorted_by_price(descending=False):
       """Retrieves cars sorted by price."""
       with Session() as session:
           if descending:
               cars = session.query(Car).order_by(Car.price.desc()).all()
           else:
               cars = session.query(Car).order_by(Car.price.asc()).all()
           for car in cars:
               console.log(f"{car.make} {car.model} - Price: ${car.price}")
   ```

2. **Limiting Results**:

   ```python
   def get_top_n_expensive_cars(n):
       """Retrieves the top N most expensive cars."""
       with Session() as session:
           cars = session.query(Car).order_by(Car.price.desc()).limit(n).all()
           for car in cars:
               console.log(f"{car.make} {car.model} - Price: ${car.price}")
   ```

3. **Explanation**:
   - **`order_by()`** sorts the results based on specified columns.
   - **`limit(n)`** restricts the number of records returned by the query.

---

### Example Usage in `__main__`

You can test these functions by calling them in the `if __name__ == "__main__"` block.

```python
if __name__ == "__main__":
    # Filter examples
    get_cars_by_price_and_year(15000, 25000, 2018)
    get_cars_by_make_or_year("Toyota", 2019)

    # Aggregation examples
    count_total_cars()
    average_car_price()

    # Join examples
    get_cars_with_dealerships()
    get_all_cars_with_or_without_dealerships()

    # Ordering and limiting examples
    get_cars_sorted_by_price(descending=True)
    get_top_n_expensive_cars(2)
```

### Summary of Part 4

- **Filtering**: Use conditions with `and_()` and `or_()` for complex filtering.
- **Aggregations**: Use SQL functions like `COUNT`, `SUM`, `AVG` with `func` for data summaries.
- **Joins**: Combine data from related tables using `join()` and `outerjoin()`.
- **Ordering and Limiting**: Control the order and number of records returned with `order_by()` and `limit()`.

These techniques empower you to query and manipulate data with precision and efficiency. Let me know if you’d like further customization in any of these areas or are ready to move to the next part!

---

## Related code

Here’s the complete code for Part 4, incorporating all advanced querying techniques, including filtering, aggregations, joins, and ordering/limiting results.

```python
from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine, func, and_, or_
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import ForeignKey
from rich.console import Console

console = Console()

# Create a base class for our models
Base = declarative_base()

DATABASE_URL = "postgresql+psycopg2://admin:admin@localhost:5432/mydatabase"

# Define the engine and session factory
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)

# Define the Dealership model
class Dealership(Base):
    __tablename__ = "dealerships"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cars = relationship("Car", back_populates="dealership")

# Define the Car model
class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    is_sold = Column(Boolean, default=False)
    dealership_id = Column(Integer, ForeignKey("dealerships.id"))
    dealership = relationship("Dealership", back_populates="cars")

# Create all tables
Base.metadata.create_all(engine)

# Advanced Query Functions

# Filtering with Conditions
def get_cars_by_price_and_year(min_price, max_price, min_year):
    """Retrieves cars within a specific price range and minimum year."""
    with Session() as session:
        cars = session.query(Car).filter(
            and_(
                Car.price >= min_price,
                Car.price <= max_price,
                Car.year >= min_year
            )
        ).all()
        for car in cars:
            console.log(f"{car.make} {car.model} - Year: {car.year}, Price: ${car.price}")

def get_cars_by_make_or_year(make, year):
    """Retrieves cars with a specific make or minimum year."""
    with Session() as session:
        cars = session.query(Car).filter(
            or_(Car.make == make, Car.year >= year)
        ).all()
        for car in cars:
            console.log(f"{car.make} {car.model} - Year: {car.year}, Price: ${car.price}")

# Aggregations
def count_total_cars():
    """Counts the total number of cars."""
    with Session() as session:
        total_cars = session.query(func.count(Car.id)).scalar()
        console.log(f"Total number of cars: {total_cars}")

def average_car_price():
    """Calculates the average price of all cars."""
    with Session() as session:
        avg_price = session.query(func.avg(Car.price)).scalar()
        console.log(f"Average car price: ${avg_price:.2f}")

# Joins
def get_cars_with_dealerships():
    """Retrieves cars along with their dealerships."""
    with Session() as session:
        cars = session.query(Car, Dealership).join(Dealership).all()
        for car, dealership in cars:
            console.log(f"{car.make} {car.model} - Dealership: {dealership.name}")

def get_all_cars_with_or_without_dealerships():
    """Retrieves all cars, including those without dealerships."""
    with Session() as session:
        cars = session.query(Car, Dealership).outerjoin(Dealership).all()
        for car, dealership in cars:
            dealership_name = dealership.name if dealership else "No Dealership"
            console.log(f"{car.make} {car.model} - Dealership: {dealership_name}")

# Ordering and Limiting Results
def get_cars_sorted_by_price(descending=False):
    """Retrieves cars sorted by price."""
    with Session() as session:
        if descending:
            cars = session.query(Car).order_by(Car.price.desc()).all()
        else:
            cars = session.query(Car).order_by(Car.price.asc()).all()
        for car in cars:
            console.log(f"{car.make} {car.model} - Price: ${car.price}")

def get_top_n_expensive_cars(n):
    """Retrieves the top N most expensive cars."""
    with Session() as session:
        cars = session.query(Car).order_by(Car.price.desc()).limit(n).all()
        for car in cars:
            console.log(f"{car.make} {car.model} - Price: ${car.price}")

# Example usage
if __name__ == "__main__":
    # Filter examples
    get_cars_by_price_and_year(15000, 25000, 2018)
    get_cars_by_make_or_year("Toyota", 2019)

    # Aggregation examples
    count_total_cars()
    average_car_price()

    # Join examples
    get_cars_with_dealerships()
    get_all_cars_with_or_without_dealerships()

    # Ordering and limiting examples
    get_cars_sorted_by_price(descending=True)
    get_top_n_expensive_cars(2)

```

### Explanation of Each Section

1. **Filtering with Conditions**:

   - `get_cars_by_price_and_year`: Filters cars by price range and minimum year.
   - `get_cars_by_make_or_year`: Filters cars by a specific make or year.

2. **Aggregations**:

   - `count_total_cars`: Counts the total number of cars.
   - `average_car_price`: Calculates the average price of cars.

3. **Joins**:

   - `get_cars_with_dealerships`: Retrieves cars with associated dealerships using an inner join.
   - `get_all_cars_with_or_without_dealerships`: Uses an outer join to get all cars, including those without dealerships.

4. **Ordering and Limiting**:
   - `get_cars_sorted_by_price`: Sorts cars by price in ascending or descending order.
   - `get_top_n_expensive_cars`: Retrieves the top `n` most expensive cars.

Each function in this code provides a specific advanced query capability, giving you a robust set of tools for complex data retrieval and manipulation in SQLAlchemy ORM. Let me know if you need further customization or explanation of any section!
