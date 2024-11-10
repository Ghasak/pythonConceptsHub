# SQLAlchemy with Python
<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [SQLAlchemy with Python](#sqlalchemy-with-python)
    - [Concept](#concept)
    - [Starting point](#starting-point)
        - [Step 1: Setting Up the Tables](#step-1-setting-up-the-tables)
        - [Step 2: Inserting Data](#step-2-inserting-data)
        - [Step 3: Querying the Tables](#step-3-querying-the-tables)
        - [Notes on Execution](#notes-on-execution)
    - [Concept -2](#concept--2)
        - [Understanding `relationship`](#understanding-relationship)
        - [Correct Way to Think of `relationship`](#correct-way-to-think-of-relationship)
        - [ASCII Diagram of the Car Database Relationships](#ascii-diagram-of-the-car-database-relationships)
        - [Explanation of the Diagram](#explanation-of-the-diagram)
        - [How Relationships Work in Practice](#how-relationships-work-in-practice)

<!-- markdown-toc end -->

## Concept

show me now three tables

- One for car brand
- One for car model
- One for car info
  and one for tracking changing for the car
  each should be having unique id using uuid
  also for last table should be tracking for example the price changing with timestamp
  then show how you query from these tables and show also the full mart table

## Starting point

Let's define three main tables and a tracking table, each with a unique
identifier using UUIDs. Here's how you can set them up in SQLAlchemy 2.0 ORM and
perform queries that join these tables.

### Step 1: Setting Up the Tables

1. **CarBrand**: Holds car brands.
2. **CarModel**: Holds car models and links to a brand.
3. **CarInfo**: Contains specific car details (e.g., year, price) and links to a model.
4. **CarTracking**: Tracks changes, such as price updates, with timestamps for a given car.

```python
import uuid
from sqlalchemy import create_engine, Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

# Database setup
engine = create_engine('sqlite:///cars.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Table definitions

class CarBrand(Base):
    __tablename__ = 'car_brands'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)

    models = relationship("CarModel", back_populates="brand")


class CarModel(Base):
    __tablename__ = 'car_models'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    brand_id = Column(UUID(as_uuid=True), ForeignKey('car_brands.id'), nullable=False)

    brand = relationship("CarBrand", back_populates="models")
    cars = relationship("CarInfo", back_populates="model")


class CarInfo(Base):
    __tablename__ = 'car_info'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    year = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    model_id = Column(UUID(as_uuid=True), ForeignKey('car_models.id'), nullable=False)

    model = relationship("CarModel", back_populates="cars")
    tracking = relationship("CarTracking", back_populates="car")


class CarTracking(Base):
    __tablename__ = 'car_tracking'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    car_id = Column(UUID(as_uuid=True), ForeignKey('car_info.id'), nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=func.now())

    car = relationship("CarInfo", back_populates="tracking")

# Create all tables
Base.metadata.create_all(engine)
```

### Step 2: Inserting Data

Now, let's add some sample data for each table.

```python
# Adding a brand
brand = CarBrand(name="Toyota")
session.add(brand)

# Adding a model linked to the brand
model = CarModel(name="Corolla", brand=brand)
session.add(model)

# Adding a car linked to the model with initial price
car = CarInfo(year="2022", price=20000, model=model)
session.add(car)
session.commit()

# Adding a price change for tracking
tracking1 = CarTracking(car=car, price=20000)  # initial price
tracking2 = CarTracking(car=car, price=19000)  # updated price
session.add_all([tracking1, tracking2])
session.commit()
```

### Step 3: Querying the Tables

1. **Retrieve all information about a car, including brand and model**:

   ```python
   car_details = session.query(CarInfo).join(CarModel).join(CarBrand).filter(CarInfo.id == car.id).first()
   print(f"Car: {car_details.year}, Price: {car_details.price}, Model: {car_details.model.name}, Brand: {car_details.model.brand.name}")
   ```

2. **Get all price changes for a specific car**:

   ```python
   price_changes = session.query(CarTracking).filter(CarTracking.car_id == car.id).order_by(CarTracking.timestamp).all()
   for change in price_changes:
       print(f"Price: {change.price}, Timestamp: {change.timestamp}")
   ```

3. **Display a “Mart” table with all details for cars, including the latest tracked price**:

   ```python
   from sqlalchemy import select

   # A complex query to get all car info with the latest price tracking
   result = session.query(
       CarInfo.id.label("car_id"),
       CarBrand.name.label("brand_name"),
       CarModel.name.label("model_name"),
       CarInfo.year.label("car_year"),
       CarTracking.price.label("latest_price"),
       CarTracking.timestamp.label("price_timestamp")
   ).join(CarModel, CarInfo.model_id == CarModel.id
   ).join(CarBrand, CarModel.brand_id == CarBrand.id
   ).join(CarTracking, CarInfo.id == CarTracking.car_id
   ).order_by(CarTracking.timestamp.desc()
   ).all()

   for row in result:
       print(f"Car ID: {row.car_id}, Brand: {row.brand_name}, Model: {row.model_name}, Year: {row.car_year}, Latest Price: {row.latest_price}, Timestamp: {row.price_timestamp}")
   ```

### Notes on Execution

- **Table Creation** (`Base.metadata.create_all(engine)`) only once, unless
  schema changes.
- **Insertions** (`session.add()` + `session.commit()`) can be repeated but
  `commit()` should be batched.
- **Query Execution**: Queries can be executed as often as needed without
  altering data.
- **Updates/Tracking**: For tracking changes, insert new `CarTracking` records
  rather than updating existing ones to keep historical data intact.

This setup and these queries cover the basics of how to use SQLAlchemy 2.0 to
build and query a more complex database with relationships and a tracking system
for historical price changes. Let me know if you'd like more examples!

## Concept -2

Can you explain how u use and what is the correct way to think of the
relationships using the relationship method then include an ASCII diagram about
tables relationship of the car database above The `relationship` method in
SQLAlchemy ORM is used to define the relationship between tables in an
object-oriented way. By setting up relationships, you can use Python attributes
to navigate between linked records rather than writing raw SQL joins. Here’s a
breakdown of how and why we use `relationship`.

### Understanding `relationship`

1. **One-to-Many Relationship (e.g., CarBrand and CarModel)**:

   - A `CarBrand` can have multiple `CarModel` records associated with it.
   - We define `relationship` on both sides of this relationship:
     - `CarBrand` has `models` as a list of `CarModel` objects.
     - `CarModel` has `brand` as a reference to the `CarBrand` it belongs to.
   - This allows you to query `CarBrand` and access its models directly, or
     query `CarModel` and access its brand.

2. **One-to-Many Relationship (e.g., CarModel and CarInfo)**:

   - Each `CarModel` can have multiple `CarInfo` entries (specific cars with
     year, price, etc.).
   - Similarly, `CarModel` has `cars` (list of related `CarInfo`), and `CarInfo`
     has `model` (the specific model it’s associated with).

3. **One-to-Many Relationship (e.g., CarInfo and CarTracking)**:
   - A `CarInfo` record can have multiple `CarTracking` entries that keep track
     of historical data, such as price changes.
   - `CarInfo` has `tracking` as a list of all associated `CarTracking` entries,
     and `CarTracking` has `car` as a reference back to `CarInfo`.

### Correct Way to Think of `relationship`

1. **Determine the Cardinality**:

   - Is the relationship one-to-many, many-to-one, or many-to-many?
   - In our example, each relationship is one-to-many: one brand can have many
     models, one model can have many cars, and one car can have many tracking
     records.

2. **Define `relationship` on Both Sides**:

   - SQLAlchemy uses `relationship` to establish a connection on both sides of
     the relationship.
   - Use `back_populates` to link relationships on both sides, which keeps them
     in sync. For instance, when you assign `brand.models`, it automatically
     links back to `CarModel.brand`.

3. **Choose a Collection or Single Object**:
   - In a one-to-many relationship, use a list for the "many" side (e.g.,
     `models`, `cars`, `tracking`) and a single object for the "one" side (e.g.,
     `brand`, `model`, `car`).

### ASCII Diagram of the Car Database Relationships

Here’s an ASCII diagram to visualize the relationships between the tables in our
car database:

```plaintext
+------------+       +------------+       +------------+       +------------+
| CarBrand   | 1   * | CarModel   | 1   * | CarInfo    | 1   * | CarTracking|
|------------|-------|------------|-------|------------|-------|------------|
| id (UUID)  |       | id (UUID)  |       | id (UUID)  |       | id (UUID)  |
| name       |       | name       |       | year       |       | price      |
|            |       | brand_id   |------>| price      |------>| car_id     |
|            |       |            |       | model_id   |       | timestamp  |
+------------+       +------------+       +------------+       +------------+
    |                     |                    |                       |
    |  models             |   cars             |   tracking           |
    |                     |                    |                       |
    +---------------------+--------------------+-----------------------+
```

### Explanation of the Diagram

- **CarBrand and CarModel**:

  - `CarBrand` has a one-to-many relationship with `CarModel`.
  - The `brand_id` in `CarModel` references `CarBrand.id`.

- **CarModel and CarInfo**:

  - `CarModel` has a one-to-many relationship with `CarInfo`.
  - The `model_id` in `CarInfo` references `CarModel.id`.

- **CarInfo and CarTracking**:
  - `CarInfo` has a one-to-many relationship with `CarTracking`.
  - The `car_id` in `CarTracking` references `CarInfo.id`.

### How Relationships Work in Practice

- **Navigating Relationships**:

  - After querying a `CarBrand`, you can easily access its `models`:
    ```python
    brand = session.query(CarBrand).first()
    for model in brand.models:
        print(model.name)
    ```
  - Similarly, after querying a `CarInfo`, you can see its price history:
    ```python
    car = session.query(CarInfo).first()
    for tracking in car.tracking:
        print(tracking.price, tracking.timestamp)
    ```

- **Back-Populates**:
  - Using `back_populates` ensures bidirectional access between related objects:
    - Setting `brand.models` will update `model.brand`, and vice versa.
    - This ensures consistency, as changes to one side of the relationship are automatically reflected on the other side.

The diagram and explanation here should provide a clear mental model for setting
up and thinking through relationships in SQLAlchemy, especially when working
with complex relational databases. Let me know if you need further details on
querying or setting up additional relationships!
