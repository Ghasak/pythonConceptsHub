# SQL Real Data Example
<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [SQL Real Data Example](#sql-real-data-example)
    - [Key Data Points](#key-data-points)
        - [Static Variables (Fixed Information)](#static-variables-fixed-information)
            - [Dynamic Variables (Varying Information)](#dynamic-variables-varying-information)
        - [Proposed Database Table Structure](#proposed-database-table-structure)
        - [1. Track Last Scrape Date](#1-track-last-scrape-date)
        - [2. Hash Important Fields to Detect Changes](#2-hash-important-fields-to-detect-changes)
        - [3. Conditional Scraping Based on Hash Comparison](#3-conditional-scraping-based-on-hash-comparison)
        - [4. Optimizing the Frequency of Scraping](#4-optimizing-the-frequency-of-scraping)
        - [Database Table Update with Additional Fields](#database-table-update-with-additional-fields)
        - [Summary of the Process](#summary-of-the-process)
    - [Using Python](#using-python)
        - [Explanation of Each Table](#explanation-of-each-table)
    - [Q1 - In Deepth](#q1---in-deepth)
        - [Explanation:](#explanation)

<!-- markdown-toc end -->

Based on the screenshots provided, I'll outline the key data points visible on
this car listing page and categorize them into **static** and **dynamic**
fields. Then, I’ll structure these fields into a database table that can
accommodate numerous entries.

## Key Data Points

### Static Variables (Fixed Information)

1. **Make** (e.g., BMW)
2. **Model** (e.g., 3 Series 320i)
3. **Year** (e.g., 2016)
4. **Body Type** (e.g., sedan)
5. **Engine Size** (e.g., 2000cc)
6. **Transmission Type** (e.g., Automatic/Manual)
7. **Drive Type** (e.g., 2WD)
8. **Fuel Type** (e.g., Gasoline)
9. **Exterior Color** (e.g., Mediterranean Blue)
10. **Seating Capacity** (e.g., 5 seats)
11. **Number of Doors** (e.g., 4 doors)
12. **Catalog Information (Dimensions, Weight)** (e.g., 4645x1800x1440 mm, 1580 kg)
13. **Standard Equipment** (features like ABS, Bluetooth, power steering)
14. **Safety Features** (e.g., airbags, anti-lock brakes)

#### Dynamic Variables (Varying Information)

1. **Mileage** (e.g., 2.77 km)
2. **Condition** (e.g., Condition rating)
3. **Price** (e.g., 163.9 万円 or 1.639 million yen)
4. **Location** (e.g., Chiba, Japan)
5. **Listing Date** (indicated as a recent listing)
6. **Inspection Status/Expiry** (e.g., valid until October 2025)
7. **Dealer Information** (e.g., Universe in Chiba, contact details)
8. **Market Demand Indicators** (interest, views if available)

### Proposed Database Table Structure

| Field Name         | Data Type     | Description                                          |
| ------------------ | ------------- | ---------------------------------------------------- |
| VIN                | VARCHAR(17)   | Unique vehicle identifier (if available).            |
| Make               | VARCHAR(50)   | Car manufacturer (e.g., BMW).                        |
| Model              | VARCHAR(50)   | Specific model name (e.g., 3 Series 320i).           |
| Year               | INT           | Year of manufacture (e.g., 2016).                    |
| Body_Type          | VARCHAR(50)   | Type of body (e.g., sedan).                          |
| Engine_Size        | VARCHAR(10)   | Engine capacity (e.g., 2000cc).                      |
| Transmission       | VARCHAR(20)   | Type of transmission (e.g., Automatic).              |
| Drive_Type         | VARCHAR(20)   | Drivetrain configuration (e.g., 2WD).                |
| Fuel_Type          | VARCHAR(20)   | Type of fuel (e.g., Gasoline).                       |
| Exterior_Color     | VARCHAR(50)   | Color of the exterior (e.g., Mediterranean Blue).    |
| Seating_Capacity   | INT           | Number of seats (e.g., 5).                           |
| Number_of_Doors    | INT           | Number of doors (e.g., 4).                           |
| Dimensions         | VARCHAR(50)   | Dimensions of the vehicle (e.g., 4645x1800x1440 mm). |
| Weight             | INT           | Weight of the vehicle in kg (e.g., 1580).            |
| Standard_Equipment | TEXT          | List of standard equipment/features.                 |
| Safety_Features    | TEXT          | List of safety features.                             |
| Mileage            | INT           | Distance traveled in kilometers (e.g., 2770).        |
| Condition          | VARCHAR(50)   | Condition status or rating.                          |
| Price              | DECIMAL(10,2) | Asking price (e.g., 163.9 万円).                     |
| Location           | VARCHAR(100)  | Location of the dealer (e.g., Chiba, Japan).         |
| Listing_Date       | DATE          | Date of listing.                                     |
| Inspection_Expiry  | DATE          | Date when inspection expires (e.g., 2025/10).        |
| Dealer_Name        | VARCHAR(100)  | Name of the dealer (e.g., Universe).                 |
| Dealer_Contact     | VARCHAR(50)   | Contact number of the dealer.                        |
| Market_Demand      | INT           | Indicator of market demand or views.                 |

This structure allows a systematic collection of data, which can then be
analyzed to understand pricing trends, demand patterns, and other variables
critical to formulating a business plan for buying and reselling used cars.

if i scrap this car but revisit by scrap again to see if something change what
is the best logic way to not repeat the scrapping process and wasting more time

To avoid redundant data scraping and optimize for efficiency when revisiting
listings to check for changes, you can implement a strategy based on **data
comparison and timestamp tracking**. Here’s an efficient approach to handle
this:

### 1. Track Last Scrape Date

Add a `last_scraped_date` field to your database. This field will keep track of the last time you scraped data for each car.

- **Field**: `last_scraped_date`
- **Data Type**: `DATETIME`

### 2. Hash Important Fields to Detect Changes

Create a hash or checksum of key fields that are likely to change (such as `Price`, `Mileage`, `Condition`, and `Market_Demand`). This way, you can quickly identify if a listing has been updated since the last scrape.

- **Key fields for hashing**: `Price`, `Mileage`, `Condition`, `Market_Demand`
- **Hash field**: `data_hash`
- **Data Type**: `VARCHAR`

Each time you scrape a car, calculate the hash of these fields. If the new hash differs from the stored hash, you know that one or more of the key values has changed.

### 3. Conditional Scraping Based on Hash Comparison

When you revisit a car’s listing:

- First, scrape the page but **only extract the key fields** for hashing.
- Calculate the hash and compare it to the stored hash in your database.
  - If the hash is **different**, proceed to re-scrape the full data and update the database accordingly.
  - If the hash is **the same**, skip re-scraping and update the `last_scraped_date` to record that it was checked.

### 4. Optimizing the Frequency of Scraping

For listings that don’t change often, you can implement a tiered scraping frequency based on the `last_scraped_date` and the nature of the listing:

- **New listings**: Scrape more frequently, as new listings might have price reductions or updates.
- **Older listings**: Check less frequently (e.g., every few days) if they haven’t shown recent changes.

### Database Table Update with Additional Fields

| Field Name        | Data Type     | Description                              |
| ----------------- | ------------- | ---------------------------------------- |
| VIN               | VARCHAR(17)   | Unique vehicle identifier.               |
| Make              | VARCHAR(50)   | Car manufacturer (e.g., BMW).            |
| Model             | VARCHAR(50)   | Specific model name.                     |
| ...               | ...           | (other fields as defined previously)     |
| Price             | DECIMAL(10,2) | Asking price.                            |
| Mileage           | INT           | Distance traveled in kilometers.         |
| Condition         | VARCHAR(50)   | Condition status or rating.              |
| Market_Demand     | INT           | Indicator of market demand or views.     |
| last_scraped_date | DATETIME      | Timestamp of the last successful scrape. |
| data_hash         | VARCHAR(64)   | Hash of key fields to detect changes.    |

### Summary of the Process

1. **Initial Scrape**: Save all car details, hash key fields, and store the `last_scraped_date`.
2. **Subsequent Visits**:
   - Scrape only the key fields.
   - Compute and compare the hash with the stored `data_hash`.
   - If the hash is unchanged, update only the `last_scraped_date`.
   - If the hash differs, re-scrape and update the full data, including the new hash and `last_scraped_date`.

This approach minimizes redundant scraping and database updates, focusing only on listings that have meaningful changes.

---

## Using Python

Here's a basic SQL schema with three tables (`brand`, `model`, and `used_car`) to represent a relational database for managing used car data. Each table is linked, where `brand` connects to `model`, and `model` connects to `used_car`, representing hierarchical relationships.

```sql
-- Table for storing car brands
CREATE TABLE brand (
    brand_id INT PRIMARY KEY AUTO_INCREMENT,
    brand_name VARCHAR(50) NOT NULL UNIQUE
);

-- Table for storing car models, linked to the brand
CREATE TABLE model (
    model_id INT PRIMARY KEY AUTO_INCREMENT,
    brand_id INT NOT NULL,
    model_name VARCHAR(50) NOT NULL,
    year INT,
    FOREIGN KEY (brand_id) REFERENCES brand(brand_id)
);

-- Table for storing specific used car details, linked to the model
CREATE TABLE used_car (
    car_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT NOT NULL,
    vin VARCHAR(17) UNIQUE,
    price DECIMAL(10, 2),
    mileage INT,
    condition VARCHAR(50),
    location VARCHAR(100),
    exterior_color VARCHAR(50),
    interior_color VARCHAR(50),
    transmission VARCHAR(20),
    drive_type VARCHAR(20),
    fuel_type VARCHAR(20),
    seating_capacity INT,
    number_of_doors INT,
    market_demand INT,
    last_scraped_date DATETIME,
    data_hash VARCHAR(64),
    FOREIGN KEY (model_id) REFERENCES model(model_id)
);
```

### Explanation of Each Table

1. **`brand` Table**:

   - **`brand_id`**: Primary key, unique identifier for each brand.
   - **`brand_name`**: Name of the car brand (e.g., BMW, Toyota), must be unique.

2. **`model` Table**:

   - **`model_id`**: Primary key, unique identifier for each model.
   - **`brand_id`**: Foreign key linking to the `brand` table, establishing which brand the model belongs to.
   - **`model_name`**: Specific model name (e.g., 3 Series, Camry).
   - **`year`**: Year of manufacture.

3. **`used_car` Table**:
   - **`car_id`**: Primary key, unique identifier for each used car listing.
   - **`model_id`**: Foreign key linking to the `model` table, identifying which model the used car is.
   - **`vin`**: Vehicle Identification Number, unique for each car.
   - **Other Fields**: Specific details about the used car, such as `price`, `mileage`, `condition`, `location`, `exterior_color`, `interior_color`, etc.
   - **`last_scraped_date`**: Timestamp of the last time this car’s data was scraped.
   - **`data_hash`**: Hash of key fields to detect any changes during subsequent scrapes.

This schema will allow you to store information hierarchically, with each brand having multiple models and each model having multiple specific used car listings. It also enables easy querying to gather insights at different levels (e.g., by brand, model, or individual car).

---

## Q1 - In Deepth

I want to create using python with sqlite and sqlachemy 2.0

- Also i want to check if the table existed and how to append to it a new car or
  new model or new brand for each level and
- Show the car is already scrapped and based on our previous talk to check if
  change then create anew entry and don’t modify the last but keep them stored
  with timestamp
- For example price should be variable with time only when the price is changed
  and keep tracking
- Maybe should i add a new table for tracking activities of a given used car

Here’s the complete Python code using SQLAlchemy 2.0 and SQLite to implement the
database with `Brand`, `Model`, `UsedCar`, and `CarActivity` tables. This setup
checks if entries exist, adds new ones if necessary, and logs changes in key
fields over time.

```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, DECIMAL, Text
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import hashlib

# Initialize the database
engine = create_engine('sqlite:///used_cars.db', echo=True)
Base = declarative_base()

# Define tables
class Brand(Base):
    __tablename__ = 'brand'
    brand_id = Column(Integer, primary_key=True, autoincrement=True)
    brand_name = Column(String(50), unique=True, nullable=False)

class Model(Base):
    __tablename__ = 'model'
    model_id = Column(Integer, primary_key=True, autoincrement=True)
    brand_id = Column(Integer, ForeignKey('brand.brand_id'), nullable=False)
    model_name = Column(String(50), nullable=False)
    year = Column(Integer, nullable=True)

    brand = relationship("Brand", back_populates="models")

class UsedCar(Base):
    __tablename__ = 'used_car'
    car_id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey('model.model_id'), nullable=False)
    vin = Column(String(17), unique=True)
    price = Column(DECIMAL(10, 2))
    mileage = Column(Integer)
    condition = Column(String(50))
    location = Column(String(100))
    exterior_color = Column(String(50))
    interior_color = Column(String(50))
    transmission = Column(String(20))
    drive_type = Column(String(20))
    fuel_type = Column(String(20))
    seating_capacity = Column(Integer)
    number_of_doors = Column(Integer)
    market_demand = Column(Integer)
    last_scraped_date = Column(DateTime, default=datetime.now)
    data_hash = Column(String(64))

    model = relationship("Model", back_populates="cars")

class CarActivity(Base):
    __tablename__ = 'car_activity'
    activity_id = Column(Integer, primary_key=True, autoincrement=True)
    car_id = Column(Integer, ForeignKey('used_car.car_id'), nullable=False)
    price = Column(DECIMAL(10, 2))
    mileage = Column(Integer)
    condition = Column(String(50))
    market_demand = Column(Integer)
    timestamp = Column(DateTime, default=datetime.now)

    car = relationship("UsedCar", back_populates="activities")

# Set up relationships
Brand.models = relationship("Model", order_by=Model.model_id, back_populates="brand")
Model.cars = relationship("UsedCar", order_by=UsedCar.car_id, back_populates="model")
UsedCar.activities = relationship("CarActivity", order_by=CarActivity.activity_id, back_populates="car")

# Create all tables
Base.metadata.create_all(engine)

# Set up session
Session = sessionmaker(bind=engine)
session = Session()

# Function to create or get a brand
def get_or_create_brand(brand_name):
    brand = session.query(Brand).filter_by(brand_name=brand_name).first()
    if not brand:
        brand = Brand(brand_name=brand_name)
        session.add(brand)
        session.commit()
    return brand

# Function to create or get a model
def get_or_create_model(brand_name, model_name, year=None):
    brand = get_or_create_brand(brand_name)
    model = session.query(Model).filter_by(model_name=model_name, brand_id=brand.brand_id).first()
    if not model:
        model = Model(brand_id=brand.brand_id, model_name=model_name, year=year)
        session.add(model)
        session.commit()
    return model

# Function to create or update a used car entry with activity tracking
def add_or_update_used_car(model_name, vin, new_data):
    model = session.query(Model).filter_by(model_name=model_name).first()
    if not model:
        print(f"Model {model_name} not found.")
        return

    car = session.query(UsedCar).filter_by(vin=vin).first()

    # Calculate the hash of key fields to detect changes
    key_string = f"{new_data['price']}_{new_data['mileage']}_{new_data['condition']}_{new_data['market_demand']}"
    new_data_hash = hashlib.sha256(key_string.encode()).hexdigest()

    if car:
        # Check if data has changed by comparing hashes
        if car.data_hash != new_data_hash:
            # Log the old data in CarActivity
            activity = CarActivity(
                car_id=car.car_id,
                price=car.price,
                mileage=car.mileage,
                condition=car.condition,
                market_demand=car.market_demand
            )
            session.add(activity)

            # Update the car's data
            car.price = new_data['price']
            car.mileage = new_data['mileage']
            car.condition = new_data['condition']
            car.market_demand = new_data['market_demand']
            car.last_scraped_date = datetime.now()
            car.data_hash = new_data_hash
            session.commit()
            print(f"Car data updated for VIN {vin}.")
        else:
            print(f"No changes detected for VIN {vin}.")
    else:
        # Add new car
        car = UsedCar(
            model_id=model.model_id,
            vin=vin,
            price=new_data['price'],
            mileage=new_data['mileage'],
            condition=new_data['condition'],
            market_demand=new_data['market_demand'],
            last_scraped_date=datetime.now(),
            data_hash=new_data_hash
        )
        session.add(car)
        session.commit()
        print(f"New car added for VIN {vin}.")

# Example usage
get_or_create_brand("BMW")
get_or_create_model("BMW", "3 Series", 2016)

new_car_data = {
    'price': 163.9,
    'mileage': 2775,
    'condition': 'Good',
    'market_demand': 50
}

# First entry
add_or_update_used_car("3 Series", "123ABC456", new_car_data)

# Update with changed data
updated_car_data = {
    'price': 160.0,  # Price dropped
    'mileage': 2800,  # Mileage increased
    'condition': 'Good',  # Same condition
    'market_demand': 52  # Demand increased slightly
}
add_or_update_used_car("3 Series", "123ABC456", updated_car_data)

# Check results
session.query(UsedCar).all(), session.query(CarActivity).all()
```

### Explanation:

- **Tables**: `Brand`, `Model`, `UsedCar`, and `CarActivity` tables are defined, with relationships to track brands, models, cars, and their activities.
- **Hashing**: A hash of key fields (`price`, `mileage`, `condition`, `market_demand`) is used to detect changes in car data.
- **Activity Tracking**: If data has changed, a new entry is added to `CarActivity`, recording the previous values.
- **Data Insertion and Update**: The `add_or_update_used_car` function either inserts a new car or updates an existing one based on the hash comparison, logging changes.

Run this code in your local environment with SQLAlchemy installed, and it will create the necessary tables, track car information, and log updates as entries change.`
