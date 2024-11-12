# **Title**: `"Transaction Management and Error Handling in SQLAlchemy ORM (Part 3)"`

For **Part 3**, let’s delve into **transactions** and **error handling** in SQLAlchemy ORM. Managing transactions effectively and handling errors properly is crucial for maintaining data integrity and ensuring smooth database operations.

---

## Summary of Part 3: Transactions and Error Handling

**Summary**:
This section covers transaction management and error handling in SQLAlchemy’s ORM. Transactions ensure that a series of database operations are treated as a single unit, so either all changes are saved, or none are. We’ll:

1. Introduce **transaction basics** in SQLAlchemy.
2. Use **context managers** to simplify transaction management.
3. Explore **error handling** to manage exceptions and roll back changes when needed.
4. Demonstrate **batch operations** within transactions.

Learning these techniques will help you maintain reliable database operations and prevent data inconsistencies.

---

### Step 1: Understanding Transactions

A **transaction** groups multiple database operations together as a single unit. If any operation within a transaction fails, the entire transaction is rolled back to maintain data integrity.

1. **Implicit Transactions**:

   - SQLAlchemy automatically begins a transaction when you perform any database operation.
   - Transactions are committed only when `session.commit()` is called, and rolled back if an error occurs before committing.

2. **Explicit Transactions**:
   - You can manage transactions manually for fine-grained control, especially for more complex operations.

---

### Step 2: Using Context Managers for Transactions

Using a **context manager** (`with` statement) for transactions is a best practice as it ensures that the session is correctly closed and changes are committed or rolled back.

1. **Basic Transaction Example**:

   ```python
   def add_car_with_transaction(make, model, year, price, dealership_id):
       """Adds a car within a transaction using a context manager."""
       with Session() as session:
           try:
               new_car = Car(make=make, model=model, year=year, price=price, dealership_id=dealership_id)
               session.add(new_car)
               session.commit()  # Commit transaction
               print(f"Car {make} {model} added.")
           except Exception as e:
               session.rollback()  # Roll back transaction if an error occurs
               print(f"Error occurred: {e}")
   ```

2. **Explanation**:
   - **`with Session() as session`**: Ensures the session is automatically closed at the end of the block.
   - **`session.commit()`**: Commits the transaction if no exceptions occur.
   - **`session.rollback()`**: Rolls back changes if an error occurs, ensuring data integrity.

---

### Step 3: Handling Errors

Error handling is essential for gracefully managing unexpected situations, such as database connectivity issues or constraint violations.

1. **Try-Except Blocks**:

   - Wrapping database operations in `try-except` blocks allows you to catch exceptions and handle them appropriately.

2. **Example of Error Handling**:

   ```python
   def update_car_price_safely(model, new_price):
       """Updates a car's price with error handling."""
       with Session() as session:
           try:
               car = session.query(Car).filter_by(model=model).first()
               if car:
                   car.price = new_price
                   session.commit()
                   print(f"Updated {model} price to ${new_price}.")
               else:
                   print(f"Car model {model} not found.")
           except Exception as e:
               session.rollback()
               print(f"Failed to update car price: {e}")
   ```

3. **Explanation**:
   - **Exception Handling**: Catches any error and rolls back changes to prevent partial updates.

---

### Step 4: Batch Operations in Transactions

Batch operations allow you to modify multiple rows within a single transaction, which is efficient and helps maintain consistency.

1. **Updating Multiple Records in a Transaction**:

   ```python
   def batch_update_prices(make, percentage_increase):
       """Increases the price of all cars of a specific make by a percentage."""
       with Session() as session:
           try:
               cars = session.query(Car).filter_by(make=make).all()
               for car in cars:
                   car.price += car.price * (percentage_increase / 100)
               session.commit()
               print(f"Prices for all {make} cars increased by {percentage_increase}%.")
           except Exception as e:
               session.rollback()
               print(f"Batch update failed: {e}")
   ```

2. **Explanation**:
   - All price updates are staged in the session.
   - **`session.commit()`**: Saves all updates at once.
   - **Batch Rollback**: If any update fails, all updates are rolled back.

---

### Step 5: Handling Nested Transactions with Savepoints

For complex applications, **savepoints** within transactions allow you to roll back to an intermediate state without rolling back the entire transaction.

1. **Example of Nested Transactions with Savepoints**:

   ```python
   def add_dealership_and_car(dealership_name, car_make, car_model, car_year, car_price):
       """Adds a dealership and a car within a nested transaction."""
       with Session() as session:
           try:
               # Add a dealership
               new_dealership = Dealership(name=dealership_name)
               session.add(new_dealership)
               session.flush()  # Flush to access new_dealership.id

               # Start a savepoint for adding a car
               savepoint = session.begin_nested()  # Savepoint created
               try:
                   new_car = Car(make=car_make, model=car_model, year=car_year, price=car_price, dealership_id=new_dealership.id)
                   session.add(new_car)
                   session.commit()  # Commit car addition
                   print(f"Added dealership '{dealership_name}' and car '{car_make} {car_model}'")
               except Exception as car_error:
                   savepoint.rollback()  # Roll back only the car addition if it fails
                   print(f"Failed to add car: {car_error}")

               session.commit()  # Commit dealership addition
           except Exception as e:
               session.rollback()  # Roll back entire transaction if dealership fails
               print(f"Transaction failed: {e}")
   ```

2. **Explanation**:
   - **Savepoints** (`session.begin_nested()`): Allow partial rollbacks within transactions.
   - **Use Cases**: Useful for handling related operations, where one operation may fail without impacting the other.

---

### Summary of Part 3

- **Implicit and Explicit Transactions**: SQLAlchemy provides automatic transaction management but allows manual control when needed.
- **Error Handling**: Wrapping operations in try-except blocks ensures graceful handling of errors.
- **Batch Operations**: Efficiently update or delete multiple records within a single transaction.
- **Savepoints**: Allow partial rollbacks, useful for nested or complex operations.

This part provides the foundation for managing reliable and consistent database interactions. Let me know if you'd like to go deeper into advanced querying techniques or continue with another area!

---

## Related code

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

# CRUD Functions with Context Managers and Error Handling

def create_car(make, model, year, price, is_sold=False):
    """Adds a new car to the inventory."""
    with Session() as session:
        try:
            new_car = Car(make=make, model=model, year=year, price=price, is_sold=is_sold)
            session.add(new_car)
            session.commit()
            console.log(f"Car {make} {model} added.")
        except Exception as e:
            session.rollback()
            console.log(f"Failed to add car {make} {model}: {e}")

def read_all_cars():
    """Retrieves and logs all cars in the inventory."""
    with Session() as session:
        try:
            cars = session.query(Car).all()
            for car in cars:
                console.log(
                    f"ID: {car.id}, Make: {car.make}, Model: {car.model}, Year: {car.year}, Price: ${car.price}, Sold: {car.is_sold}"
                )
        except Exception as e:
            console.log(f"Failed to read cars: {e}")

def read_car_by_model(model):
    """Retrieves a car by model name."""
    with Session() as session:
        try:
            car = session.query(Car).filter(Car.model == model).first()
            if car:
                console.log(
                    f"Found Car - ID: {car.id}, Make: {car.make}, Model: {car.model}, Year: {car.year}, Price: ${car.price}, Sold: {car.is_sold}"
                )
            else:
                console.log(f"No car found with model {model}.")
        except Exception as e:
            console.log(f"Failed to read car with model {model}: {e}")

def update_car_price_by_model(model, new_price):
    """Updates the price of a car by model."""
    with Session() as session:
        try:
            car = session.query(Car).filter(Car.model == model).first()
            if car:
                car.price = new_price
                session.commit()
                console.log(f"Updated price for {model} to ${new_price}.")
            else:
                console.log(f"No car found with model {model} to update.")
        except Exception as e:
            session.rollback()
            console.log(f"Failed to update price for car model {model}: {e}")

def delete_car_by_model(model):
    """Deletes a car by model."""
    with Session() as session:
        try:
            car = session.query(Car).filter(Car.model == model).first()
            if car:
                session.delete(car)
                session.commit()
                console.log(f"Deleted car with model {model}.")
            else:
                console.log(f"No car found with model {model} to delete.")
        except Exception as e:
            session.rollback()
            console.log(f"Failed to delete car with model {model}: {e}")

def create_cars():
    # Create
    create_car("Toyota", "Corolla", 2020, 20000)
    create_car("Honda", "Civic", 2019, 18000)
    create_car("Ford", "Focus", 2021, 22000)


if __name__ == "__main__":
    # Uncomment to create initial cars
    # create_cars()

    # Read all cars
    read_all_cars()

    # Read specific car by model
    # read_car_by_model("Civic")

    # Update a car price
    # update_car_price_by_model("Civic", 18500)

    # Delete a car by model
    # delete_car_by_model("Focus")

```
