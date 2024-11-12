# **Title**: `"Mixins, Inheritance, and Polymorphism in SQLAlchemy ORM (Part 6)"`

In **Part 6**, we’ll explore **SQLAlchemy ORM’s mixins, inheritance, and polymorphism**. These advanced ORM techniques allow you to create reusable model components, structure class hierarchies, and represent diverse entities within the same table or across related tables.

---

## Summary of Part 6: Mixins, Inheritance, and Polymorphism

**Summary**:
This section covers using mixins, inheritance, and polymorphism in SQLAlchemy to build flexible, reusable models. Specifically, we’ll:

1. Introduce **Mixins** for reusable model attributes and methods.
2. Implement **Single Table Inheritance** for polymorphic entities in one table.
3. Use **Joined Table Inheritance** for entities distributed across related tables.
4. Understand **polymorphic querying** to retrieve specific subclasses.

These techniques enable efficient code reuse, complex data modeling, and easier maintenance for applications with diverse but related data structures.

---

### Step 1: Using Mixins for Reusable Components

**Mixins** are classes that encapsulate common attributes or methods, allowing you to reuse them across models.

1. **Example of a Mixin**:

   - Let’s create a `TimestampMixin` that adds `created_at` and `updated_at` fields to any model.

   ```python
   from sqlalchemy import DateTime
   from datetime import datetime

   class TimestampMixin:
       created_at = Column(DateTime, default=datetime.utcnow)
       updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
   ```

2. **Using the Mixin in Models**:

   ```python
   class Car(TimestampMixin, Base):
       __tablename__ = "cars"

       id = Column(Integer, primary_key=True)
       make = Column(String, nullable=False)
       model = Column(String, nullable=False)
       year = Column(Integer, nullable=False)
       price = Column(Float, nullable=False)
       is_sold = Column(Boolean, default=False)
   ```

3. **Explanation**:
   - By including `TimestampMixin`, each `Car` instance will have `created_at` and `updated_at` fields, automatically set and updated with each modification.

---

### Step 2: Single Table Inheritance (STI)

**Single Table Inheritance (STI)** uses a single table to store multiple related entities, distinguished by a `type` column.

1. **Define a Base Class with a Type Column**:

   ```python
   class Vehicle(Base):
       __tablename__ = "vehicles"

       id = Column(Integer, primary_key=True)
       type = Column(String, nullable=False)  # Discriminator column
       make = Column(String, nullable=False)
       model = Column(String, nullable=False)
       year = Column(Integer, nullable=False)
       __mapper_args__ = {
           "polymorphic_on": type,
           "polymorphic_identity": "vehicle"
       }
   ```

2. **Define Subclasses with Polymorphic Identities**:

   ```python
   class Car(Vehicle):
       __mapper_args__ = {
           "polymorphic_identity": "car"
       }
       price = Column(Float, nullable=False)

   class Motorcycle(Vehicle):
       __mapper_args__ = {
           "polymorphic_identity": "motorcycle"
       }
       has_sidecar = Column(Boolean, default=False)
   ```

3. **Explanation**:

   - **`type`**: Discriminator column differentiates subclasses.
   - **`polymorphic_on`**: Specifies the column to differentiate subclasses.
   - **`polymorphic_identity`**: Identifies each subclass within `type`.

4. **Example Usage of Single Table Inheritance**:

   ```python
   def add_vehicle(vehicle_type, make, model, year, **kwargs):
       """Adds a vehicle (car or motorcycle) using Single Table Inheritance."""
       with Session() as session:
           if vehicle_type == "car":
               vehicle = Car(make=make, model=model, year=year, price=kwargs.get("price", 0))
           elif vehicle_type == "motorcycle":
               vehicle = Motorcycle(make=make, model=model, year=year, has_sidecar=kwargs.get("has_sidecar", False))
           else:
               console.log(f"Unknown vehicle type: {vehicle_type}")
               return
           session.add(vehicle)
           session.commit()
           console.log(f"Added {vehicle_type}: {make} {model}")
   ```

---

### Step 3: Joined Table Inheritance (JTI)

**Joined Table Inheritance (JTI)** uses separate tables for each subclass, with a primary key reference to the base table.

1. **Define a Base Class**:

   ```python
   class BaseVehicle(Base):
       __tablename__ = "base_vehicles"

       id = Column(Integer, primary_key=True)
       make = Column(String, nullable=False)
       model = Column(String, nullable=False)
       year = Column(Integer, nullable=False)
       __mapper_args__ = {
           "polymorphic_on": None,
           "polymorphic_identity": "base_vehicle"
       }
   ```

2. **Define Subclasses with Separate Tables**:

   ```python
   class Car(BaseVehicle):
       __tablename__ = "cars"

       id = Column(Integer, ForeignKey("base_vehicles.id"), primary_key=True)
       price = Column(Float, nullable=False)
       __mapper_args__ = {
           "polymorphic_identity": "car"
       }

   class Motorcycle(BaseVehicle):
       __tablename__ = "motorcycles"

       id = Column(Integer, ForeignKey("base_vehicles.id"), primary_key=True)
       has_sidecar = Column(Boolean, default=False)
       __mapper_args__ = {
           "polymorphic_identity": "motorcycle"
       }
   ```

3. **Explanation**:
   - Each subclass has its own table with a foreign key reference to `base_vehicles.id`.
   - Allows for specific columns per subclass without storing unused columns in a single table.

---

### Step 4: Polymorphic Querying

Polymorphic queries allow you to query the base class and retrieve instances of its subclasses.

1. **Example of Polymorphic Query**:

   ```python
   def list_all_vehicles():
       """Lists all vehicles, whether cars or motorcycles."""
       with Session() as session:
           vehicles = session.query(BaseVehicle).all()
           for vehicle in vehicles:
               if isinstance(vehicle, Car):
                   console.log(f"Car: {vehicle.make} {vehicle.model} - Price: ${vehicle.price}")
               elif isinstance(vehicle, Motorcycle):
                   sidecar_status = "with sidecar" if vehicle.has_sidecar else "no sidecar"
                   console.log(f"Motorcycle: {vehicle.make} {vehicle.model} - {sidecar_status}")
   ```

2. **Explanation**:
   - This query fetches all `BaseVehicle` records and distinguishes between `Car` and `Motorcycle` instances.

---

### Example Usage in `__main__`

You can test these functionalities by calling each function in the `if __name__ == "__main__"` block.

```python
if __name__ == "__main__":
    # Test mixin and STI
    add_vehicle("car", "Toyota", "Camry", 2022, price=25000)
    add_vehicle("motorcycle", "Harley", "Sportster", 2021, has_sidecar=True)

    # List all vehicles
    list_all_vehicles()
```

### Summary of Part 6

- **Mixins**: Create reusable components to standardize attributes and methods across models.
- **Single Table Inheritance (STI)**: Store related subclasses in a single table, differentiated by a `type` column.
- **Joined Table Inheritance (JTI)**: Store subclasses in separate tables, joined by a foreign key.
- **Polymorphic Querying**: Query base classes and retrieve subclasses for flexible data handling.

These advanced ORM techniques enhance flexibility and modularity in your data models, making SQLAlchemy ideal for applications with diverse but interrelated data structures. Let me know if you'd like more examples or are ready to move on!
