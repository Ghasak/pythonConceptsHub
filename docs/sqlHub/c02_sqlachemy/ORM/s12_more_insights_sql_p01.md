# SQLALCHEMY with some

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->

**Table of Contents**

- [SQLALCHEMY with some](#sqlalchemy-with-some)
  - [Instructions and requirements event](#instructions-and-requirements-event)
    - [Step 1: Define ORM Models](#step-1-define-orm-models)
    - [Step 2: CRUD Operations](#step-2-crud-operations)
      - [Create Sample Data](#create-sample-data)
      - [Read Data](#read-data)
      - [Update Data](#update-data)
      - [Delete Data](#delete-data)
    - [Step 3: Data Mart Query](#step-3-data-mart-query)
  - [Explaination Relationships in ORM](#explaination-relationships-in-orm)
    - [Generic Syntax for Relationships](#generic-syntax-for-relationships)
      - [Explanation of Each Part](#explanation-of-each-part)
      - [Relationship Types](#relationship-types)
    - [Applying Relationships to the Tables](#applying-relationships-to-the-tables)
      - [Explanation of Relationships in Each Class](#explanation-of-relationships-in-each-class)
      - [Summary of Relationship Types](#summary-of-relationship-types)
  - [Confusion over the naming convention](#confusion-over-the-naming-convention)
    - [Generic Relationship Formula in SQLAlchemy](#generic-relationship-formula-in-sqlalchemy)
      - [Explanation of Naming Conventions](#explanation-of-naming-conventions)
    - [Applying Naming to `CarBrand`, `CarModel`, and `CarInfo`](#applying-naming-to-carbrand-carmodel-and-carinfo)
    - [Breaking Down the Relationships](#breaking-down-the-relationships)
    - [Summary of Naming Conventions](#summary-of-naming-conventions)
  - [All types of Relationships with ORM](#all-types-of-relationships-with-orm)
    - [1. **One-to-Many Relationship**](#1-one-to-many-relationship)
      - [Example](#example)
      - [Explanation](#explanation)
    - [2. **Many-to-One Relationship**](#2-many-to-one-relationship)
      - [Example (Using CarBrand and CarModel)](#example-using-carbrand-and-carmodel)
      - [Explanation](#explanation-1)
    - [3. **One-to-One Relationship**](#3-one-to-one-relationship)
      - [Example](#example-1)
      - [Explanation](#explanation-2)
    - [4. **Many-to-Many Relationship**](#4-many-to-many-relationship)
      - [Example](#example-2)
      - [Explanation](#explanation-3)
    - [Summary of Relationships](#summary-of-relationships)
  - [Where is the relationship and how to identify it?](#where-is-the-relationship-and-how-to-identify-it)
    - [1. One-to-Many Relationship](#1-one-to-many-relationship)
    - [2. Many-to-One Relationship](#2-many-to-one-relationship)
    - [3. One-to-One Relationship](#3-one-to-one-relationship)
    - [4. Many-to-Many Relationship](#4-many-to-many-relationship)
  - [Question -1](#question--1)
    - [Pure ORM Many-to-Many Relationship with an Association Class](#pure-orm-many-to-many-relationship-with-an-association-class)
    - [Explanation](#explanation-4)
    - [Benefits of Using an Association Class](#benefits-of-using-an-association-class)
    - [Usage Example](#usage-example)
  - [Question 2](#question-2)
    - [Why an Association Table or Class is Needed](#why-an-association-table-or-class-is-needed)
    - [Example Breakdown](#example-breakdown)
  - [Question 3](#question-3)
    - [Summary of Relationship Types](#summary-of-relationship-types-1)

<!-- markdown-toc end -->

## Instructions and requirements event

In sqlachemy 2.0 i want to create three tables in `orm`
and perform all types of `CRUD`:

- For `carBrand`, `carModel`, `carInfo` for many cars under each model each brand
- I want to add `index` for car id in the car info table
- Using `postgresql`
- This index supposed to make things faster when query.
- Then at the end create a query that will create a data mart out of all these
  three tables
- Show some rows like `5` for each table and when you do `CRUD` or final query
  also show expected table to make it clear to me and understand.

---

Let's break down the task into several steps. We’ll create three
tables—`CarBrand`, `CarModel`, and `CarInfo`—and establish relationships among
them using SQLAlchemy 2.0 ORM. Then, we’ll add an index on the `car_id` column
in the `CarInfo` table to optimize queries. After performing CRUD operations,
we’ll create a data mart query that aggregates information from all three
tables.

### Step 1: Define ORM Models

```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy.ext.asyncio import create_async_engine

# Database setup
Base = declarative_base()

class CarBrand(Base):
    __tablename__ = 'car_brand'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship with CarModel
    models = relationship("CarModel", back_populates="brand")

class CarModel(Base):
    __tablename__ = 'car_model'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    brand_id = Column(Integer, ForeignKey('car_brand.id'), nullable=False)

    # Relationships
    brand = relationship("CarBrand", back_populates="models")
    cars = relationship("CarInfo", back_populates="model")

class CarInfo(Base):
    __tablename__ = 'car_info'
    id = Column(Integer, primary_key=True)
    car_id = Column(String, unique=True, nullable=False)
    model_id = Column(Integer, ForeignKey('car_model.id'), nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(Integer)

    # Relationships
    model = relationship("CarModel", back_populates="cars")

    # Index for car_id to optimize query performance
    __table_args__ = (
        Index('idx_car_id', 'car_id'),
    )

# Create engine and tables
engine = create_engine("postgresql+psycopg2://user:password@localhost/dbname")
Base.metadata.create_all(engine)
```

### Step 2: CRUD Operations

#### Create Sample Data

```python
with Session(engine) as session:
    # Adding car brands
    brand1 = CarBrand(name="Toyota")
    brand2 = CarBrand(name="Honda")
    session.add_all([brand1, brand2])

    # Adding car models
    model1 = CarModel(name="Corolla", brand=brand1)
    model2 = CarModel(name="Civic", brand=brand2)
    session.add_all([model1, model2])

    # Adding car info
    car1 = CarInfo(car_id="C1", model=model1, year=2020, price=20000)
    car2 = CarInfo(car_id="C2", model=model1, year=2021, price=21000)
    car3 = CarInfo(car_id="C3", model=model2, year=2020, price=22000)
    car4 = CarInfo(car_id="C4", model=model2, year=2022, price=23000)
    session.add_all([car1, car2, car3, car4])

    session.commit()
```

#### Read Data

```python
with Session(engine) as session:
    car_info_data = session.query(CarInfo).join(CarModel).join(CarBrand).all()
    for car in car_info_data:
        print(f"{car.car_id}: {car.model.brand.name} {car.model.name}, {car.year} - ${car.price}")
```

Expected output:

```sh

C1: Toyota Corolla, 2020 - $20000
C2: Toyota Corolla, 2021 - $21000
C3: Honda Civic   , 2020 - $22000
C4: Honda Civic   , 2022 - $23000

```

#### Update Data

```python
with Session(engine) as session:
    car_to_update = session.query(CarInfo).filter_by(car_id="C2").first()
    car_to_update.price = 21500
    session.commit()
```

Expected output:

```sh
C2: Toyota Corolla, 2021 - $21500
```

#### Delete Data

```python
with Session(engine) as session:
    car_to_delete = session.query(CarInfo).filter_by(car_id="C4").first()
    session.delete(car_to_delete)
    session.commit()
```

Expected output:

```sh
Car C4 is removed from the database
```

### Step 3: Data Mart Query

The data mart aggregates `CarBrand`, `CarModel`, and `CarInfo` to provide
brand, model, year, and average price.

```python
from sqlalchemy import func

with Session(engine) as session:
    data_mart_query = session.query(
        CarBrand.name.label("Brand"),
        CarModel.name.label("Model"),
        CarInfo.year.label("Year"),
        func.avg(CarInfo.price).label("Average_Price")
    ).join(CarModel).join(CarInfo).group_by(CarBrand.name, CarModel.name, CarInfo.year).all()

    for row in data_mart_query:
        print(row)
```

Expected output (Data Mart):

| Brand  | Model   | Year | Average_Price |
| ------ | ------- | ---- | ------------- |
| Toyota | Corolla | 2020 | 20000         |
| Toyota | Corolla | 2021 | 21500         |
| Honda  | Civic   | 2020 | 22000         |

This setup provides a full overview of CRUD operations and showcases how to
create a basic data mart in SQLAlchemy ORM with efficient indexing.

---

## Explaination Relationships in ORM

In SQLAlchemy ORM, relationships are defined using the `relationship()` function in one or both classes to establish connections between tables. Let’s go through the generic syntax and apply it to the `CarBrand`, `CarModel`, and `CarInfo` tables to understand their relationships.

### Generic Syntax for Relationships

```python
class Parent(Base):
    __tablename__ = 'parent_table'
    id = Column(Integer, primary_key=True)
    # Relationship with Child
    children = relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = 'child_table'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent_table.id'))
    # Relationship with Parent
    parent = relationship("Parent", back_populates="children")
```

#### Explanation of Each Part

1. **Foreign Key in Child Class**:

   - `parent_id = Column(Integer, ForeignKey('parent_table.id'))`
   - This line in the child class (`Child`) establishes a foreign key constraint, linking `parent_id` in the child table to `id` in the parent table (`parent_table`). The `ForeignKey` argument specifies the column it references.
   - **Purpose**: It ensures referential integrity, meaning a record in the child table must have a valid reference to the parent table.

2. **relationship() in Parent Class**:

   - `children = relationship("Child", back_populates="parent")`
   - This line establishes a relationship from the parent to the child, allowing access to related child records directly from the parent object.
   - `relationship("Child")` tells SQLAlchemy that `Parent` has a relationship with the `Child` class.
   - `back_populates="parent"` defines a bidirectional relationship, linking this attribute to a corresponding attribute in `Child` (called `parent`).
   - **Purpose**: Allows ORM queries to seamlessly load related child objects, enabling `Parent` objects to have access to all associated `Child` objects.

3. **relationship() in Child Class**:
   - `parent = relationship("Parent", back_populates="children")`
   - This line establishes a relationship from the child to the parent, allowing access to the parent record directly from the child object.
   - `relationship("Parent")` tells SQLAlchemy that `Child` has a relationship with the `Parent` class.
   - `back_populates="children"` links this attribute to the corresponding attribute in `Parent` (called `children`).
   - **Purpose**: Enables bidirectional navigation between `Parent` and `Child`.

#### Relationship Types

1. **One-to-Many**: A single record in the parent table relates to multiple records in the child table. This is implemented by placing the `relationship()` in the parent table and using `ForeignKey` in the child table.

2. **One-to-One**: A single record in one table corresponds to a single record in another table. It can be established by setting `uselist=False` in the `relationship()`.

3. **Many-to-Many**: Each record in one table can relate to multiple records in another table, and vice versa. This requires an association table with foreign keys from both tables.

### Applying Relationships to the Tables

Now, let’s apply this to the `CarBrand`, `CarModel`, and `CarInfo` tables to demonstrate **One-to-Many** relationships.

```python
class CarBrand(Base):
    __tablename__ = 'car_brand'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # One-to-Many Relationship with CarModel
    models = relationship("CarModel", back_populates="brand")

class CarModel(Base):
    __tablename__ = 'car_model'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    brand_id = Column(Integer, ForeignKey('car_brand.id'), nullable=False)

    # Many-to-One Relationship with CarBrand
    brand = relationship("CarBrand", back_populates="models")

    # One-to-Many Relationship with CarInfo
    cars = relationship("CarInfo", back_populates="model")

class CarInfo(Base):
    __tablename__ = 'car_info'
    id = Column(Integer, primary_key=True)
    car_id = Column(String, unique=True, nullable=False)
    model_id = Column(Integer, ForeignKey('car_model.id'), nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(Integer)

    # Many-to-One Relationship with CarModel
    model = relationship("CarModel", back_populates="cars")
```

#### Explanation of Relationships in Each Class

1. **CarBrand to CarModel** (One-to-Many):

   - `CarBrand.models = relationship("CarModel", back_populates="brand")`
   - Each car brand can have multiple models. `CarBrand` is the parent, and `CarModel` is the child.
   - `models` in `CarBrand` represents all models related to a specific brand.
   - In `CarModel`, `brand_id` is a foreign key pointing to `CarBrand`, and `brand = relationship("CarBrand", back_populates="models")` defines the reverse relationship, allowing each model to access its associated brand.

2. **CarModel to CarInfo** (One-to-Many):
   - `CarModel.cars = relationship("CarInfo", back_populates="model")`
   - Each car model can have multiple specific car entries.
   - `cars` in `CarModel` represents all cars under a particular model.
   - In `CarInfo`, `model_id` is a foreign key pointing to `CarModel`, and `model = relationship("CarModel", back_populates="cars")` establishes the reverse relationship, letting each car entry access its associated model.

#### Summary of Relationship Types

- **CarBrand to CarModel**: **One-to-Many** – A single car brand can have multiple models.
- **CarModel to CarInfo**: **One-to-Many** – A single car model can have multiple specific car entries.

These relationships allow us to perform cascading queries and ensure data integrity through foreign keys.

---

## Confusion over the naming convention

In SQLAlchemy, naming conventions in relationships can sometimes be confusing because SQLAlchemy uses the class name (capitalized) to refer to other tables, while the instance variables (lowercase) represent attributes on an individual object. Here's a generic formula and explanation to help clarify:

### Generic Relationship Formula in SQLAlchemy

Let's start with a generic formula for setting up a **One-to-Many** relationship in two classes, `Parent` and `Child`.

```python
class Parent(Base):
    __tablename__ = 'parent_table'
    id = Column(Integer, primary_key=True)

    # Relationship with Child
    children = relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = 'child_table'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent_table.id'))

    # Relationship with Parent
    parent = relationship("Parent", back_populates="children")
```

#### Explanation of Naming Conventions

1. **Class Name** (Capitalized):

   - In `relationship()`, the first argument is always the **class name** of the related table, written with an initial capital letter and enclosed in quotes, like `"Child"` in `Parent` and `"Parent"` in `Child`.
   - Example: `relationship("Child")` in `Parent` or `relationship("Parent")` in `Child`.
   - **Purpose**: This tells SQLAlchemy which table (class) to relate to.

2. **Instance Variable** (Lowercase):

   - In `relationship()` or `ForeignKey`, the actual attribute name in lowercase is what you use to access the related records in a particular instance.
   - In the parent class (`Parent`), the instance variable is usually plural, representing a collection of related child objects (`children`).
   - In the child class (`Child`), the instance variable is singular (`parent`), representing a single related parent object.
   - **Purpose**: These lowercase names allow access to related instances at an object level, e.g., `parent.children` to access all `Child` objects related to a `Parent` object or `child.parent` to access the `Parent` object for a specific `Child`.

3. **Foreign Key Column**:
   - In the child class, the foreign key column uses lowercase syntax and points to the primary key of the parent table.
   - Syntax: `parent_id = Column(Integer, ForeignKey('parent_table.id'))`
   - **Purpose**: It links the child table to the parent table by referencing the parent table's primary key.

### Applying Naming to `CarBrand`, `CarModel`, and `CarInfo`

Using our `CarBrand`, `CarModel`, and `CarInfo` classes, let's apply the naming conventions.

```python
class CarBrand(Base):
    __tablename__ = 'car_brand'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship with CarModel (One-to-Many)
    models = relationship("CarModel", back_populates="brand")

class CarModel(Base):
    __tablename__ = 'car_model'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    brand_id = Column(Integer, ForeignKey('car_brand.id'), nullable=False)

    # Relationship with CarBrand (Many-to-One)
    brand = relationship("CarBrand", back_populates="models")

    # Relationship with CarInfo (One-to-Many)
    cars = relationship("CarInfo", back_populates="model")

class CarInfo(Base):
    __tablename__ = 'car_info'
    id = Column(Integer, primary_key=True)
    car_id = Column(String, unique=True, nullable=False)
    model_id = Column(Integer, ForeignKey('car_model.id'), nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(Integer)

    # Relationship with CarModel (Many-to-One)
    model = relationship("CarModel", back_populates="cars")
```

### Breaking Down the Relationships

1. **CarBrand to CarModel Relationship**:

   - In `CarBrand`: `models = relationship("CarModel", back_populates="brand")`
     - **"CarModel"**: Refers to the related class name `CarModel`.
     - **models**: The lowercase plural instance variable, representing a list of `CarModel` objects linked to each `CarBrand` instance.
     - **back_populates="brand"**: Links this attribute to the `brand` attribute in `CarModel`.
   - In `CarModel`: `brand = relationship("CarBrand", back_populates="models")`
     - **"CarBrand"**: Refers to the related class name `CarBrand`.
     - **brand**: The lowercase singular instance variable representing a single `CarBrand` object associated with each `CarModel` instance.
     - **back_populates="models"**: Links this attribute to the `models` attribute in `CarBrand`.

2. **CarModel to CarInfo Relationship**:

   - In `CarModel`: `cars = relationship("CarInfo", back_populates="model")`
     - **"CarInfo"**: Refers to the related class name `CarInfo`.
     - **cars**: The lowercase plural instance variable, representing a list of `CarInfo` objects linked to each `CarModel` instance.
     - **back_populates="model"**: Links this attribute to the `model` attribute in `CarInfo`.
   - In `CarInfo`: `model = relationship("CarModel", back_populates="cars")`
     - **"CarModel"**: Refers to the related class name `CarModel`.
     - **model**: The lowercase singular instance variable representing a single `CarModel` object associated with each `CarInfo` instance.
     - **back_populates="cars"**: Links this attribute to the `cars` attribute in `CarModel`.

### Summary of Naming Conventions

| Element          | Syntax                                     | Example                            |
| ---------------- | ------------------------------------------ | ---------------------------------- |
| **Class Name**   | Capitalized in quotes                      | `"CarModel"` in `CarBrand`         |
| **Instance Var** | Lowercase, plural (many) or singular (one) | `models`, `cars`, `brand`, `model` |
| **Foreign Key**  | Lowercase, child class                     | `brand_id`, `model_id`             |

These naming conventions keep relationships intuitive and consistent.

---

## All types of Relationships with ORM

Let's go over **all types of relationships** in SQLAlchemy: **One-to-Many**, **Many-to-One**, **One-to-One**, and **Many-to-Many**. For each, I'll provide a generic example and a breakdown of the key parts.

### 1. **One-to-Many Relationship**

This relationship is when one record in a parent table relates to multiple records in a child table. It’s commonly used for hierarchical data.

#### Example

```python
class Parent(Base):
    __tablename__ = 'parent_table'
    id = Column(Integer, primary_key=True)
    children = relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = 'child_table'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent_table.id'))
    parent = relationship("Parent", back_populates="children")
```

#### Explanation

- **Foreign Key in `Child`**: `parent_id = Column(Integer, ForeignKey('parent_table.id'))` links `Child` to `Parent`.
- **`relationship()` in `Parent`**: `children = relationship("Child", back_populates="parent")` lets each `Parent` instance access related `Child` records.
- **`relationship()` in `Child`**: `parent = relationship("Parent", back_populates="children")` lets each `Child` instance access the associated `Parent` record.

**Use Case**: This is commonly used for a structure where a single entity can own multiple items, like a `CarBrand` having multiple `CarModels`.

### 2. **Many-to-One Relationship**

This is simply the reverse of a One-to-Many relationship. A single record in a child table can be associated with one record in a parent table.

#### Example (Using CarBrand and CarModel)

```python
class CarBrand(Base):
    __tablename__ = 'car_brand'
    id = Column(Integer, primary_key=True)
    models = relationship("CarModel", back_populates="brand")

class CarModel(Base):
    __tablename__ = 'car_model'
    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey('car_brand.id'))
    brand = relationship("CarBrand", back_populates="models")
```

#### Explanation

- **Foreign Key in `CarModel`**: `brand_id = Column(Integer, ForeignKey('car_brand.id'))` links `CarModel` to `CarBrand`.
- **`relationship()` in `CarBrand`**: `models = relationship("CarModel", back_populates="brand")` lets each `CarBrand` instance access related `CarModel` records.
- **`relationship()` in `CarModel`**: `brand = relationship("CarBrand", back_populates="models")` lets each `CarModel` instance access the associated `CarBrand` record.

**Use Case**: When each child can only belong to one parent. For instance, each `CarModel` belongs to only one `CarBrand`.

### 3. **One-to-One Relationship**

In a One-to-One relationship, each record in one table has a single, unique related record in another table. This is achieved by setting `uselist=False` in `relationship()`.

#### Example

```python
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    profile = relationship("Profile", back_populates="user", uselist=False)

class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="profile")
```

#### Explanation

- **Foreign Key in `Profile`**: `user_id = Column(Integer, ForeignKey('user.id'))` links `Profile` to `User`.
- **`uselist=False` in `User`**: `profile = relationship("Profile", back_populates="user", uselist=False)` ensures that `User` has only one associated `Profile`.
- **`relationship()` in `Profile`**: `user = relationship("User", back_populates="profile")` links each `Profile` to a single `User`.

**Use Case**: This is useful when two entities are tightly coupled, such as a `User` and their `Profile`.

### 4. **Many-to-Many Relationship**

In a Many-to-Many relationship, each record in one table can relate to multiple records in another table, and vice versa. To implement this, we need an **association table**.

#### Example

Let's say we have a `Student` table and a `Course` table, where each student can enroll in multiple courses, and each course can have multiple students.

1. **Define an Association Table**: This table holds the foreign keys of both related tables.

   ```python
   from sqlalchemy import Table

   student_course = Table(
       'student_course', Base.metadata,
       Column('student_id', Integer, ForeignKey('student.id'), primary_key=True),
       Column('course_id', Integer, ForeignKey('course.id'), primary_key=True)
   )
   ```

2. **Define Many-to-Many Relationship in Both Classes**:

   ```python
   class Student(Base):
       __tablename__ = 'student'
       id = Column(Integer, primary_key=True)
       name = Column(String, nullable=False)
       courses = relationship("Course", secondary=student_course, back_populates="students")

   class Course(Base):
       __tablename__ = 'course'
       id = Column(Integer, primary_key=True)
       title = Column(String, nullable=False)
       students = relationship("Student", secondary=student_course, back_populates="courses")
   ```

#### Explanation

- **Association Table**: `student_course` holds foreign keys `student_id` and `course_id`. These act as a bridge between `Student` and `Course`.
- **`relationship()` in `Student`**: `courses = relationship("Course", secondary=student_course, back_populates="students")`
  - `"Course"`: Refers to the `Course` class.
  - `secondary=student_course`: Specifies the association table.
  - `back_populates="students"`: Links to the `students` attribute in `Course`.
- **`relationship()` in `Course`**: `students = relationship("Student", secondary=student_course, back_populates="courses")`
  - `"Student"`: Refers to the `Student` class.
  - `secondary=student_course`: Specifies the association table.
  - `back_populates="courses"`: Links to the `courses` attribute in `Student`.

**Use Case**: This is ideal for scenarios where both tables can relate to multiple records in each other, like students and courses.

### Summary of Relationships

| Relationship Type | Example Tables      | Foreign Key Location | `relationship()` Attribute in Parent | `relationship()` Attribute in Child | Association Table (if needed) |
| ----------------- | ------------------- | -------------------- | ------------------------------------ | ----------------------------------- | ----------------------------- |
| One-to-Many       | `Parent`, `Child`   | `Child`              | Plural (e.g., `children`)            | Singular (e.g., `parent`)           | No                            |
| Many-to-One       | `Child`, `Parent`   | `Child`              | Singular (e.g., `parent`)            | Plural (e.g., `children`)           | No                            |
| One-to-One        | `User`, `Profile`   | `Profile`            | Singular with `uselist=False`        | Singular                            | No                            |
| Many-to-Many      | `Student`, `Course` | Association Table    | Plural (e.g., `courses`)             | Plural (e.g., `students`)           | Yes                           |

This table and the examples should clarify how to set up each type of relationship with appropriate naming conventions.

## Where is the relationship and how to identify it?

Sure, let’s go through each type of relationship line-by-line with docstrings to explain exactly where and how the relationship type is defined in the code.

### 1. One-to-Many Relationship

```python
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Parent(Base):
    """
    Represents the parent table in a One-to-Many relationship.
    Each Parent can have multiple Children.
    """
    __tablename__ = 'parent_table'
    id = Column(Integer, primary_key=True)

    # One-to-Many relationship to Child
    # "Child" specifies the related class name
    # `children` is the attribute representing a collection of related Child instances
    # `back_populates="parent"` establishes a bidirectional link with the `parent` attribute in Child
    children = relationship("Child", back_populates="parent")

class Child(Base):
    """
    Represents the child table in a One-to-Many relationship.
    Each Child is associated with one Parent.
    """
    __tablename__ = 'child_table'
    id = Column(Integer, primary_key=True)

    # ForeignKey in Child indicates that each Child has a link to a Parent
    # Links `parent_id` to the `id` in Parent
    parent_id = Column(Integer, ForeignKey('parent_table.id'))

    # Many-to-One relationship back to Parent
    # "Parent" specifies the related class name
    # `parent` is the attribute representing the associated Parent instance
    # `back_populates="children"` establishes a bidirectional link with the `children` attribute in Parent
    parent = relationship("Parent", back_populates="children")
```

- **Relationship Type**: **One-to-Many**
- **Indicators**:
  - In `Parent`, `children = relationship("Child", back_populates="parent")` defines the **One-to-Many** direction.
  - In `Child`, `parent_id = Column(Integer, ForeignKey('parent_table.id'))` ensures each `Child` is linked to one `Parent`.
  - The `back_populates` attribute links `Parent` and `Child` bidirectionally.

### 2. Many-to-One Relationship

This is the reverse of a One-to-Many relationship, but the syntax remains the same.

```python
class CarBrand(Base):
    """
    Represents the CarBrand table in a Many-to-One relationship.
    Each CarBrand can have multiple CarModels.
    """
    __tablename__ = 'car_brand'
    id = Column(Integer, primary_key=True)

    # One-to-Many relationship to CarModel
    models = relationship("CarModel", back_populates="brand")

class CarModel(Base):
    """
    Represents the CarModel table in a Many-to-One relationship.
    Each CarModel is associated with one CarBrand.
    """
    __tablename__ = 'car_model'
    id = Column(Integer, primary_key=True)

    # ForeignKey in CarModel links each CarModel to one CarBrand
    brand_id = Column(Integer, ForeignKey('car_brand.id'))

    # Many-to-One relationship back to CarBrand
    brand = relationship("CarBrand", back_populates="models")
```

- **Relationship Type**: **Many-to-One**
- **Indicators**:
  - In `CarBrand`, `models = relationship("CarModel", back_populates="brand")` establishes a **One-to-Many** (or Many-to-One in reverse).
  - In `CarModel`, `brand_id = Column(Integer, ForeignKey('car_brand.id'))` indicates that each `CarModel` belongs to a single `CarBrand`.

### 3. One-to-One Relationship

```python
class User(Base):
    """
    Represents the User table in a One-to-One relationship.
    Each User has a single Profile.
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)

    # One-to-One relationship with Profile
    # Setting `uselist=False` ensures that each User has a single Profile
    profile = relationship("Profile", back_populates="user", uselist=False)

class Profile(Base):
    """
    Represents the Profile table in a One-to-One relationship.
    Each Profile is associated with one User.
    """
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)

    # ForeignKey in Profile links each Profile to one User
    user_id = Column(Integer, ForeignKey('user.id'))

    # One-to-One relationship back to User
    user = relationship("User", back_populates="profile")
```

- **Relationship Type**: **One-to-One**
- **Indicators**:
  - In `User`, `profile = relationship("Profile", back_populates="user", uselist=False)` uses `uselist=False` to indicate **One-to-One**.
  - In `Profile`, `user_id = Column(Integer, ForeignKey('user.id'))` ensures each `Profile` links to one `User`.

### 4. Many-to-Many Relationship

```python
from sqlalchemy import Table

# Association Table for Many-to-Many relationship
student_course = Table(
    'student_course', Base.metadata,
    Column('student_id', Integer, ForeignKey('student.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('course.id'), primary_key=True)
)

class Student(Base):
    """
    Represents the Student table in a Many-to-Many relationship.
    Each Student can enroll in multiple Courses.
    """
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Many-to-Many relationship to Course
    # `secondary=student_course` specifies the association table
    # `back_populates="students"` links back to the students attribute in Course
    courses = relationship("Course", secondary=student_course, back_populates="students")

class Course(Base):
    """
    Represents the Course table in a Many-to-Many relationship.
    Each Course can have multiple Students.
    """
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    # Many-to-Many relationship back to Student
    # `secondary=student_course` specifies the association table
    students = relationship("Student", secondary=student_course, back_populates="courses")
```

- **Relationship Type**: **Many-to-Many**
- **Indicators**:
  - **Association Table**: `student_course` is an association table linking `Student` and `Course`.
  - In `Student`, `courses = relationship("Course", secondary=student_course, back_populates="students")` establishes the Many-to-Many relationship.
  - In `Course`, `students = relationship("Student", secondary=student_course, back_populates="courses")` links back to `Student`, completing the **Many-to-Many** relationship.

These docstrings and explanations directly highlight how each relationship type is concluded in the code for clarity.

---

## Question -1

```sh
I don’t like for many to many to use table from core
I want everything to be orm
Unless there was a purpose for that
```

Using the `Table` from SQLAlchemy Core to define an association table for a Many-to-Many relationship is standard practice, but it’s possible to use a pure ORM approach by defining an association class instead of a `Table`. This approach provides more flexibility, especially if you need to add additional columns to the association table.

Here’s how you can define a Many-to-Many relationship purely using SQLAlchemy ORM, with an association class that functions like an ORM model.

### Pure ORM Many-to-Many Relationship with an Association Class

In this example, we’ll define a `StudentCourse` class as an association class to represent the relationship between `Student` and `Course`. This approach also allows you to add extra columns to the association table if needed.

```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Student(Base):
    """
    Represents the Student table in a Many-to-Many relationship.
    Each Student can enroll in multiple Courses.
    """
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Many-to-Many relationship to Course
    # Links to Course through the StudentCourse association class
    courses = relationship("StudentCourse", back_populates="student")

class Course(Base):
    """
    Represents the Course table in a Many-to-Many relationship.
    Each Course can have multiple Students.
    """
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    # Many-to-Many relationship back to Student
    # Links to Student through the StudentCourse association class
    students = relationship("StudentCourse", back_populates="course")

class StudentCourse(Base):
    """
    Association class to represent the many-to-many relationship between
    Student and Course.
    """
    __tablename__ = 'student_course'

    # Primary keys for the association table
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), primary_key=True)

    # Relationships back to Student and Course
    student = relationship("Student", back_populates="courses")
    course = relationship("Course", back_populates="students")
```

### Explanation

1. **Student and Course Models**:

   - Each `Student` can enroll in multiple `Course` records, and each `Course` can have multiple `Student` records. This creates a Many-to-Many relationship.
   - Instead of using a `Table` for the association, we define an ORM class, `StudentCourse`.

2. **StudentCourse Association Class**:

   - This class represents the association table between `Student` and `Course`.
   - It has two primary keys: `student_id` and `course_id`, which are foreign keys referencing `Student` and `Course`, respectively.
   - **Relationship Attributes**:
     - `student = relationship("Student", back_populates="courses")`: This links `StudentCourse` back to `Student`.
     - `course = relationship("Course", back_populates="students")`: This links `StudentCourse` back to `Course`.
   - Using `back_populates`, `Student` and `Course` can each access the `StudentCourse` association directly.

3. **Relationships in Student and Course**:
   - In `Student`, `courses = relationship("StudentCourse", back_populates="student")` establishes the connection from `Student` to `StudentCourse`, enabling access to all `Course` enrollments through the `StudentCourse` association class.
   - In `Course`, `students = relationship("StudentCourse", back_populates="course")` establishes the connection from `Course` to `StudentCourse`.

### Benefits of Using an Association Class

- **Additional Columns**: With an association class, you can add extra columns, such as enrollment date or grades, to represent additional attributes of the relationship.
- **ORM Consistency**: The association class is treated as a full ORM model, giving you more control over the relationship.

### Usage Example

To enroll a student in a course:

```python
with Session(engine) as session:
    # Create a new student and course
    student = Student(name="Alice")
    course = Course(title="Math 101")

    # Enroll student in the course using the association class
    enrollment = StudentCourse(student=student, course=course)

    # Add to the session
    session.add(enrollment)
    session.commit()
```

With this setup, you now have a pure ORM Many-to-Many relationship, where you
can access all `Course` objects related to a `Student` (and vice versa) through
the `StudentCourse` association class.

---

## Question 2

```
can i say
if i think of two tables
one to many from one direction
and then one to many in another direction then it is many to many relationship?
```

Yes, that's a good way to think about it!

In a **Many-to-Many relationship**, each record in one table can relate to multiple records in the other table, and vice versa. You can indeed think of it as **two One-to-Many relationships**, one in each direction. Here’s how:

- From the perspective of **Table A** (e.g., `Student`), each record can have
  multiple associated records in **Table B** (e.g., `Course`). So, **Table A has
  a One-to-Many relationship with Table B**.
- Conversely, from the perspective of **Table B**, each record can relate to
  multiple records in **Table A**. So, **Table B has a One-to-Many relationship
  with Table A**.

When you have a One-to-Many relationship going from **Table A to Table B** and another One-to-Many going from **Table B to Table A**, they together form a **Many-to-Many relationship**.

### Why an Association Table or Class is Needed

Because SQL databases don't directly support Many-to-Many relationships, you need an **association table** (or association class in ORM) to manage this. The association table holds the foreign keys for both tables, creating the link between them.

### Example Breakdown

For example, consider `Student` and `Course`:

- Each `Student` can enroll in multiple `Course` records (One-to-Many from `Student` to `Course`).
- Each `Course` can have multiple `Student` records enrolled (One-to-Many from `Course` to `Student`).

Combining these two One-to-Many relationships gives us a Many-to-Many relationship between `Student` and `Course`. The association table (or class) then connects them, representing each enrollment.

---

## Question 3

```sh
give me a table of examples for real life examples with their relationship and should cover all types of
make more than one example
put everything in a table
```

Here’s a table of real-life examples, covering all types of relationships (One-to-Many, Many-to-One, One-to-One, and Many-to-Many). Each example includes entities involved, the relationship type, and an explanation.

| Entities                    | Relationship Type | Description                                                                                                                                               |
| --------------------------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Company** & **Employee**  | One-to-Many       | Each **Company** has multiple **Employees**, but each **Employee** belongs to only one **Company**.                                                       |
| **CarBrand** & **CarModel** | One-to-Many       | A **CarBrand** (e.g., Toyota) can have multiple **CarModels** (e.g., Corolla, Camry), but each **CarModel** belongs to one brand.                         |
| **Library** & **Book**      | One-to-Many       | A **Library** can have multiple **Books**, but each **Book** belongs to only one **Library**.                                                             |
| **Student** & **Classroom** | Many-to-One       | Each **Classroom** has multiple **Students** (One-to-Many from the perspective of **Classroom**). Each **Student** is assigned to only one **Classroom**. |
| **Country** & **Capital**   | One-to-One        | Each **Country** has one **Capital** city, and each **Capital** city belongs to only one **Country**.                                                     |
| **Person** & **Passport**   | One-to-One        | Each **Person** has one **Passport**, and each **Passport** is assigned to only one **Person**.                                                           |
| **Doctor** & **Office**     | One-to-One        | Each **Doctor** has one **Office**, and each **Office** is assigned to only one **Doctor**.                                                               |
| **Student** & **Course**    | Many-to-Many      | Each **Student** can enroll in multiple **Courses**, and each **Course** can have multiple **Students** enrolled.                                         |
| **Author** & **Book**       | Many-to-Many      | Each **Author** can write multiple **Books**, and each **Book** can have multiple **Authors** (e.g., co-authors).                                         |
| **Patient** & **Doctor**    | Many-to-Many      | Each **Patient** can visit multiple **Doctors**, and each **Doctor** can have multiple **Patients**.                                                      |

### Summary of Relationship Types

1. **One-to-Many**: Examples include Company-Employee, CarBrand-CarModel,
   Library-Book.
2. **Many-to-One**: Examples are similar but viewed from the opposite
   perspective, e.g., Student-Classroom.
3. **One-to-One**: Examples include Country-Capital, Person-Passport,
   Doctor-Office.
4. **Many-to-Many**: Examples include Student-Course, Author-Book,
   Patient-Doctor.

These real-life examples should give you a clear understanding of each
relationship type and its practical application.
