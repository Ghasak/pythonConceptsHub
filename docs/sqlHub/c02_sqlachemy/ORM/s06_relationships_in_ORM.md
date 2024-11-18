# **Title**: `"Working with Relationships in SQLAlchemy ORM (Part 2)"`

In **Part 2**, we’ll focus on **relationships** in SQLAlchemy’s ORM. Relationships allow us to link different tables and retrieve related data, essential for representing real-world associations in databases.

## Summary of Part 2: Relationships in ORM

**Summary**:
This section covers defining relationships between tables in SQLAlchemy’s ORM, building on our `Car` model from Part 1. We’ll introduce concepts like **one-to-many** and **many-to-many** relationships using examples, enabling you to:

1. Add a **Dealership** model representing a dealership that owns cars.
2. Set up a **one-to-many relationship** between `Dealership` and `Car`.
3. Add a **Customer** model and demonstrate **many-to-many relationships** between `Customer` and `Car` (e.g., tracking car purchases).
4. Understand how to query and interact with related data using the ORM.

This knowledge will enable you to manage complex data relationships in your database effectively.

---

### Step 1: Setting Up the `Dealership` Model (One-to-Many Relationship)

Let’s start by adding a `Dealership` model, where each dealership can own multiple cars. This relationship is a **one-to-many** relationship because a single dealership may have multiple cars, but each car belongs to only one dealership.

1. **Define the `Dealership` Model**:

   - Each dealership has an `id` and a `name`.
   - We’ll add a `cars` relationship to the `Dealership` model, which will connect to multiple `Car` instances.

2. **Update the `Car` Model**:

   - Add a `dealership_id` column to `Car` as a **foreign key** reference to the `Dealership` model.
   - Use the `relationship()` function to define the linkage.

3. **Code Example**:

   ```python
   from sqlalchemy import ForeignKey
   from sqlalchemy.orm import relationship

   class Dealership(Base):
       __tablename__ = "dealerships"

       id = Column(Integer, primary_key=True)
       name = Column(String, nullable=False)
       cars = relationship("Car", back_populates="dealership")  # Establish relationship

   # Update the Car model to include a dealership_id foreign key
   class Car(Base):
       __tablename__ = "cars"

       id = Column(Integer, primary_key=True)
       make = Column(String, nullable=False)
       model = Column(String, nullable=False, unique=True)
       year = Column(Integer, nullable=False)
       price = Column(Float, nullable=False)
       is_sold = Column(Boolean, default=False)
       dealership_id = Column(Integer, ForeignKey("dealerships.id"))  # Foreign key column

       # Establish the other side of the relationship
       dealership = relationship("Dealership", back_populates="cars")
   ```

4. **Explanation**:
   - `dealership_id`: Links each car to a specific dealership by referencing the `id` of the `Dealership` model.
   - `cars = relationship("Car", back_populates="dealership")`: Defines a relationship in `Dealership` to access all cars it owns.
   - `dealership = relationship("Dealership", back_populates="cars")`: Defines the reverse side of the relationship in `Car`.

---

### Step 2: Creating Tables and Testing the One-to-Many Relationship

After defining the `Dealership` model and updating `Car`, make sure to create tables in the correct order, then test the relationship.

1. **Create Tables**:

   ```python
   # Create all tables for models
   Base.metadata.create_all(engine)
   ```

2. **Example CRUD Functions for Dealership and Cars**:

   ```python
   def create_dealership(name):
       """Adds a new dealership."""
       session = Session()
       dealership = Dealership(name=name)
       session.add(dealership)
       session.commit()
       session.close()
       print(f"Dealership {name} added.")

   def add_car_to_dealership(dealership_name, make, model, year, price):
       """Adds a car to a specific dealership."""
       session = Session()
       dealership = session.query(Dealership).filter_by(name=dealership_name).first()
       if dealership:
           car = Car(make=make, model=model, year=year, price=price, dealership=dealership)
           session.add(car)
           session.commit()
           print(f"Car {make} {model} added to dealership {dealership_name}.")
       else:
           print(f"Dealership {dealership_name} not found.")
       session.close()

   def get_cars_by_dealership(dealership_name):
       """Retrieves all cars for a specific dealership."""
       session = Session()
       dealership = session.query(Dealership).filter_by(name=dealership_name).first()
       if dealership:
           for car in dealership.cars:
               print(f"{car.make} {car.model} - ${car.price}")
       else:
           print(f"No dealership found with name {dealership_name}.")
       session.close()
   ```

3. **Explanation**:

   - **`create_dealership(name)`**: Adds a new dealership.
   - **`add_car_to_dealership(dealership_name, make, model, year, price)`**: Adds a car associated with a dealership.
   - **`get_cars_by_dealership(dealership_name)`**: Retrieves all cars in a specified dealership.

4. **Testing the One-to-Many Relationship**:

   ```python
   if __name__ == "__main__":
       create_dealership("Central Dealership")
       create_dealership("East Side Dealership")

       add_car_to_dealership("Central Dealership", "Toyota", "Corolla", 2020, 20000)
       add_car_to_dealership("Central Dealership", "Honda", "Civic", 2019, 18000)
       add_car_to_dealership("East Side Dealership", "Ford", "Focus", 2021, 22000)

       print("\nCars at Central Dealership:")
       get_cars_by_dealership("Central Dealership")

       print("\nCars at East Side Dealership:")
       get_cars_by_dealership("East Side Dealership")
   ```

This will add dealerships and cars, assigning each car to a specific dealership. When you retrieve the cars by dealership, you’ll see the associated cars displayed.

---

### Step 3: Many-to-Many Relationship with `Customer` and `Car`

Now, let’s introduce a **many-to-many relationship** between `Customer` and `Car` to track which cars are purchased by which customers. For this, we need an **association table**.

1. **Define the `Customer` Model**:

   - Add a `Customer` model with attributes like `id` and `name`.

2. **Create an Association Table**:

   - Define an intermediary table, `purchases`, to establish a many-to-many relationship between `Customer` and `Car`.

3. **Code Example**:

   ```python
   from sqlalchemy import Table

   # Association table for the many-to-many relationship
   purchases = Table(
       "purchases",
       Base.metadata,
       Column("customer_id", Integer, ForeignKey("customers.id"), primary_key=True),
       Column("car_id", Integer, ForeignKey("cars.id"), primary_key=True),
   )

   class Customer(Base):
       __tablename__ = "customers"

       id = Column(Integer, primary_key=True)
       name = Column(String, nullable=False)
       cars = relationship("Car", secondary=purchases, back_populates="customers")

   # Update Car model to include customers relationship
   class Car(Base):
       __tablename__ = "cars"

       id = Column(Integer, primary_key=True)
       make = Column(String, nullable=False)
       model = Column(String, nullable=False, unique=True)
       year = Column(Integer, nullable=False)
       price = Column(Float, nullable=False)
       is_sold = Column(Boolean, default=False)
       dealership_id = Column(Integer, ForeignKey("dealerships.id"))
       dealership = relationship("Dealership", back_populates="cars")
       customers = relationship("Customer", secondary=purchases, back_populates="cars")
   ```

4. **Explanation**:
   - `purchases`: Acts as an association table, linking `customer_id` with `car_id`.
   - `cars = relationship("Car", secondary=purchases, back_populates="customers")`: Defines the many-to-many relationship in `Customer`.
   - `customers = relationship("Customer", secondary=purchases, back_populates="cars")`: Defines the relationship in `Car`.

---

### Summary of Part 2

- **One-to-Many Relationships**: Set up a `Dealership` that owns multiple `Car` entries.
- **Many-to-Many Relationships**: Link `Customer` and `Car` through an association table, allowing customers to purchase multiple cars.
- **CRUD Functions**: Define functions for managing relationships, such as adding cars to dealerships and retrieving cars by dealership.

This provides the basis for managing more complex relationships in your database. Let me know if you’d like to explore more advanced querying with relationships, or if you’d like to proceed with a specific aspect in more detail!
