Let's go through Part 1 from the beginning, including a note about the correct order of each code section to ensure that SQLAlchemy recognizes models before performing any CRUD operations.

# Part -1

## Summary of Part 1: Building Models with the ORM

**Summary**:
This section covers setting up the foundational components of SQLAlchemy's ORM for a car inventory application. We’ll define a base class, create a `Car` model, and ensure proper ordering for table creation and CRUD functions. Key steps include:

1. Setting up the **Base class** for ORM models.
2. Defining the **`Car` model** to represent a car in the inventory.
3. **Creating tables** based on defined models in the correct order.
4. Writing **CRUD functions** to add, retrieve, update, and delete records.

Following the correct order is crucial to ensure SQLAlchemy recognizes models and creates the necessary tables before CRUD operations.

---

### Note: Correct Order of Code Execution

**Correct Order**:

1. **Define the Base class**: This is the foundation for all ORM models.
2. **Define the Model class (`Car`)**: Ensure this class is defined before table creation.
3. **Create the Engine and Session**: Set up the connection to the database and session factory.
4. **Create Tables**: Use `Base.metadata.create_all(engine)` after defining the model classes to create tables.
5. **Write CRUD Functions**: Write functions to handle database operations.
6. **Execute CRUD Operations**: Only after the above setup should you execute CRUD functions.

Following this order prevents errors related to missing tables and ensures a smooth database setup.

---

### Step 1: Setting Up the Base Class

The base class serves as the foundation for all models, telling SQLAlchemy that these classes represent database tables.

```python
from sqlalchemy.orm import declarative_base

# Create a base class for our models
Base = declarative_base()
```

### Step 2: Defining the `Car` Model Class

Next, define the `Car` model to represent each car in the inventory. This class inherits from `Base`, and each attribute represents a column in the `cars` table.

```python
from sqlalchemy import Column, Integer, String, Float, Boolean

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False, unique=True)  # Set unique=True if each model should be unique
    year = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    is_sold = Column(Boolean, default=False)
```

- **`__tablename__`**: Defines the table name as `cars`.
- **Attributes**: Represent the columns for each car's details.

### Step 3: Creating the Engine and Session

The **Engine** is the main interface to the database, and the **Session** is used to manage transactions and queries.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://admin:admin@localhost:5432/mydatabase"

# Define your engine with the appropriate database URL
engine = create_engine(DATABASE_URL, echo=True)

# Create a session factory
Session = sessionmaker(bind=engine)
```

- **`DATABASE_URL`**: Specifies the database connection details.
- **Engine**: Manages the database connection and handles SQL operations.
- **Session**: Used to execute transactions and database interactions.

### Step 4: Creating Tables in the Database

Call `Base.metadata.create_all(engine)` to create tables in the database. Make sure this line is executed only after defining all models.

```python
# Create all tables based on models
Base.metadata.create_all(engine)
```

- **Explanation**: This statement inspects all models inheriting from `Base` and creates tables for each model in the database if they don’t already exist.

---

### Step 5: CRUD Functions

Now that the setup is complete, we can define CRUD functions to interact with the `Car` model. These functions allow us to add, retrieve, update, and delete cars in the inventory.

#### Create Function

```python
def create_car(make, model, year, price, is_sold=False):
    """Adds a new car to the inventory."""
    session = Session()
    new_car = Car(make=make, model=model, year=year, price=price, is_sold=is_sold)
    session.add(new_car)
    session.commit()
    session.close()
    print(f"Car {make} {model} added.")
```

#### Read Functions

Retrieve all cars or a specific car by model.

```python
def read_all_cars():
    """Retrieves and prints all cars in the inventory."""
    session = Session()
    cars = session.query(Car).all()
    for car in cars:
        print(
            f"ID: {car.id}, Make: {car.make}, Model: {car.model}, Year: {car.year}, Price: ${car.price}, Sold: {car.is_sold}"
        )
    session.close()

def read_car_by_model(model):
    """Retrieves a car by model name."""
    session = Session()
    car = session.query(Car).filter(Car.model == model).first()
    if car:
        print(
            f"Found Car - ID: {car.id}, Make: {car.make}, Model: {car.model}, Year: {car.year}, Price: ${car.price}, Sold: {car.is_sold}"
        )
    else:
        print(f"No car found with model {model}.")
    session.close()
```

#### Update Function

Update the price of a car based on its model name.

```python
def update_car_price_by_model(model, new_price):
    """Updates the price of a car by model."""
    session = Session()
    car = session.query(Car).filter(Car.model == model).first()
    if car:
        car.price = new_price
        session.commit()
        print(f"Updated price for {model} to ${new_price}.")
    else:
        print(f"No car found with model {model} to update.")
    session.close()
```

#### Delete Function

Delete a car by its model name.

```python
def delete_car_by_model(model):
    """Deletes a car by model."""
    session = Session()
    car = session.query(Car).filter(Car.model == model).first()
    if car:
        session.delete(car)
        session.commit()
        print(f"Deleted car with model {model}.")
    else:
        print(f"No car found with model {model} to delete.")
    session.close()
```

### Step 6: Testing CRUD Operations

Once all functions are defined, you can call them to test each CRUD operation.

```python
def create_cars():
    # Create cars
    create_car("Toyota", "Corolla", 2020, 20000)
    create_car("Honda", "Civic", 2019, 18000)
    create_car("Ford", "Focus", 2021, 22000)

if __name__ == "__main__":
    # Run initial create operations
    create_cars()

    # Run read operations
    print("\nAll cars in inventory:")
    read_all_cars()

    print("\nRead specific car by model:")
    read_car_by_model("Corolla")

    # Run update operation
    print("\nUpdating car price:")
    update_car_price_by_model("Corolla", 19500)

    # Run delete operation
    print("\nDeleting a car by model:")
    delete_car_by_model("Focus")

    print("\nAll cars after deletion:")
    read_all_cars()
```

---

### Summary of Part 1

1. **Define Base and Model**: Start with `Base` and define the `Car` model with necessary attributes.
2. **Set Up Engine and Session**: Use `create_engine()` and `sessionmaker()` to manage database connections.
3. **Create Tables**: Ensure tables are created by calling `Base.metadata.create_all(engine)` after defining all models.
4. **CRUD Functions**: Write and test `create`, `read`, `update`, and `delete` functions in the correct order.

Following this structure will ensure smooth interaction with the database using SQLAlchemy ORM. Let me know if you’d like to move to the next part on handling relationships or other advanced features!

## Full code

```py

from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from rich.console import Console

console = Console()

# Create a base class for our models
Base = declarative_base()

DATABASE_URL = "postgresql+psycopg2://admin:admin@localhost:5432/mydatabase"

# Define your engine with the appropriate database URL
engine = create_engine(DATABASE_URL, echo=True)

# Create a session factory
Session = sessionmaker(bind=engine)


# Define the Car model class
class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    is_sold = Column(Boolean, default=False)


# Create all tables based on models
Base.metadata.create_all(engine)

# CRUD Functions


def create_car(make, model, year, price, is_sold=False):
    """Adds a new car to the inventory."""
    session = Session()
    new_car = Car(make=make, model=model, year=year, price=price, is_sold=is_sold)
    session.add(new_car)
    session.commit()
    session.close()
    console.log(f"Car {make} {model} added.")


def read_all_cars():
    """Retrieves and console.logs all cars in the inventory."""
    session = Session()
    cars = session.query(Car).all()
    for car in cars:
        console.log(
            f"ID: {car.id}, Make: {car.make}, Model: {car.model}, Year: {car.year}, Price: ${car.price}, Sold: {car.is_sold}"
        )
    session.close()


def read_car_by_model(model):
    """Retrieves a car by model name."""
    session = Session()
    car = session.query(Car).filter(Car.model == model).first()
    if car:
        console.log(
            f"Found Car - ID: {car.id}, Make: {car.make}, Model: {car.model}, Year: {car.year}, Price: ${car.price}, Sold: {car.is_sold}"
        )
    else:
        console.log(f"No car found with model {model}.")
    session.close()


def update_car_price_by_model(model, new_price):
    """Updates the price of a car by model."""
    session = Session()
    car = session.query(Car).filter(Car.model == model).first()
    if car:
        car.price = new_price
        session.commit()
        console.log(f"Updated price for {model} to ${new_price}.")
    else:
        console.log(f"No car found with model {model} to update.")
    session.close()


def delete_car_by_model(model):
    """Deletes a car by model."""
    session = Session()
    car = session.query(Car).filter(Car.model == model).first()
    if car:
        session.delete(car)
        session.commit()
        console.log(f"Deleted car with model {model}.")
    else:
        console.log(f"No car found with model {model} to delete.")
    session.close()


def create_cars():
    # Create
    create_car("Toyota", "Corolla", 2020, 20000)
    create_car("Honda", "Civic", 2019, 18000)
    create_car("Ford", "Focus", 2021, 22000)


if __name__ == "__main__":
    #create_cars()
    read_all_cars()
    #read_car_by_model("Civic")

```
