# **Title**: `"Advanced Querying with SQLAlchemy Core (Part 2)"`

For **Part 2** of SQLAlchemy Core, let’s explore **querying data with advanced filtering, ordering, and grouping**. In SQLAlchemy Core, querying is done using SQL expression language constructs, giving you granular control over data retrieval.

---

## Summary of Part 2: Advanced Querying with SQLAlchemy Core

**Summary**:
This section covers advanced querying techniques in SQLAlchemy Core, including:

1. **Filtering Data**: Using `where()` clauses to apply conditions.
2. **Ordering Results**: Sorting results using `order_by()`.
3. **Grouping and Aggregations**: Using `group_by()` and aggregate functions like `COUNT` and `AVG`.
4. **Joins**: Retrieving related data from multiple tables with `join()`.

This will enable you to construct efficient, complex queries directly in SQLAlchemy Core.

---

### Step 1: Filtering Data

In SQLAlchemy Core, the `where()` clause allows you to add conditions to your queries.

1. **Basic Filtering**:

   ```python
   from sqlalchemy import select

   # Filter cars based on price
   with engine.connect() as conn:
       stmt = select(cars_table).where(cars_table.c.price < 21000)
       result = conn.execute(stmt)
       for row in result:
           print(row)
   ```

2. **Multiple Conditions with AND / OR**:

   ```python
   from sqlalchemy import and_, or_

   # Filter cars by price range and year
   with engine.connect() as conn:
       stmt = select(cars_table).where(
           and_(
               cars_table.c.price >= 15000,
               cars_table.c.price <= 25000,
               cars_table.c.year >= 2018
           )
       )
       result = conn.execute(stmt)
       for row in result:
           print(row)
   ```

3. **Explanation**:
   - `and_()` and `or_()` help chain multiple conditions.
   - **Example**: Retrieves cars priced between $15,000 and $25,000, and made after 2018.

---

### Step 2: Ordering Results

You can control the order of your query results using `order_by()`.

1. **Ordering by a Single Column**:

   ```python
   # Order cars by price in ascending order
   with engine.connect() as conn:
       stmt = select(cars_table).order_by(cars_table.c.price)
       result = conn.execute(stmt)
       for row in result:
           print(row)
   ```

2. **Ordering by Multiple Columns**:

   ```python
   # Order cars by year descending, then by price ascending
   with engine.connect() as conn:
       stmt = select(cars_table).order_by(cars_table.c.year.desc(), cars_table.c.price)
       result = conn.execute(stmt)
       for row in result:
           print(row)
   ```

3. **Explanation**:
   - **`order_by()`**: Specifies the sort order of query results.
   - `.desc()` and `.asc()` can be chained for descending or ascending order.

---

### Step 3: Grouping and Aggregations

Grouping results allows you to perform aggregations on subsets of data, like counting the number of cars by make.

1. **Using Aggregate Functions**:

   ```python
   from sqlalchemy import func

   # Count the total number of cars
   with engine.connect() as conn:
       stmt = select(func.count(cars_table.c.id))
       total_cars = conn.execute(stmt).scalar()
       print(f"Total cars: {total_cars}")
   ```

2. **Grouping by Make and Aggregating**:

   ```python
   # Count the number of cars per make
   with engine.connect() as conn:
       stmt = select(cars_table.c.make, func.count(cars_table.c.id)).group_by(cars_table.c.make)
       result = conn.execute(stmt)
       for row in result:
           print(f"Make: {row.make}, Count: {row.count_1}")
   ```

3. **Explanation**:
   - **`func.count()`**: Represents SQL’s `COUNT` function.
   - **`group_by()`**: Groups results by a specified column, allowing aggregation on each group.

---

### Step 4: Joining Tables

To retrieve data across multiple tables, use `join()` to define relationships between tables. Let’s define a **dealerships_table** and demonstrate joins.

1. **Define the Dealership Table**:

   ```python
   dealerships_table = Table(
       "dealerships", metadata,
       Column("id", Integer, primary_key=True),
       Column("name", String, nullable=False)
   )

   # Create the table in the database
   metadata.create_all(engine)
   ```

2. **Adding Dealership Foreign Key in Cars Table**:

   ```python
   from sqlalchemy import ForeignKey

   # Update the Car table to include a dealership_id column
   cars_table.append_column(Column("dealership_id", Integer, ForeignKey("dealerships.id")))
   metadata.create_all(engine)  # Update the table structure
   ```

3. **Performing a Join Query**:

   ```python
   # Retrieve cars along with their dealership names
   with engine.connect() as conn:
       stmt = select(cars_table.c.make, cars_table.c.model, dealerships_table.c.name).join(
           dealerships_table, cars_table.c.dealership_id == dealerships_table.c.id
       )
       result = conn.execute(stmt)
       for row in result:
           print(f"Car: {row.make} {row.model} - Dealership: {row.name}")
   ```

4. **Explanation**:
   - **`join()`**: Joins `cars_table` and `dealerships_table` on `dealership_id`.
   - This query retrieves each car along with its associated dealership.

---

### Example Usage in `__main__`

Here’s a block to test each advanced querying function:

```python
if __name__ == "__main__":
    # Filtering examples
    with engine.connect() as conn:
        result = conn.execute(select(cars_table).where(cars_table.c.price < 21000))
        for row in result:
            print(f"Car: {row.make} {row.model} - Price: ${row.price}")

    # Ordering example
    with engine.connect() as conn:
        result = conn.execute(select(cars_table).order_by(cars_table.c.price.desc()))
        for row in result:
            print(f"Car: {row.make} {row.model} - Price: ${row.price}")

    # Aggregation example
    with engine.connect() as conn:
        total_cars = conn.execute(select(func.count(cars_table.c.id))).scalar()
        print(f"Total number of cars: {total_cars}")

    # Join example
    with engine.connect() as conn:
        stmt = select(cars_table.c.make, cars_table.c.model, dealerships_table.c.name).join(
            dealerships_table, cars_table.c.dealership_id == dealerships_table.c.id
        )
        result = conn.execute(stmt)
        for row in result:
            print(f"Car: {row.make} {row.model} - Dealership: {row.name}")
```

### Summary of Part 2

- **Filtering**: Use `where()`, `and_()`, and `or_()` for complex filtering conditions.
- **Ordering**: Control result order with `order_by()`, chaining `.asc()` and `.desc()`.
- **Grouping and Aggregations**: Aggregate data with `group_by()` and functions like `count()` and `avg()`.
- **Joins**: Use `join()` to retrieve data from related tables.

This approach to querying offers SQLAlchemy Core’s full control over data retrieval, ideal for performance and flexibility. Let me know if you’re ready for **Part 3**, where we’ll explore **transactions and error handling** in Core!
