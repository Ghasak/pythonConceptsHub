# **Title**: `"Transaction Management and Error Handling in SQLAlchemy Core (Part 3)"`

In **Part 3** of SQLAlchemy Core, we’ll cover **transaction management and error handling**. Managing transactions properly and handling errors is essential to ensure data consistency, especially when dealing with multiple operations that should succeed or fail as a unit.

---

## Summary of Part 3: Transactions and Error Handling

**Summary**:
This section covers transaction management and error handling in SQLAlchemy Core. Transactions allow you to group multiple operations together, ensuring that either all changes are saved or none are. Key topics include:

1. **Using Transactions Explicitly**: Committing or rolling back operations as needed.
2. **Context Managers**: Simplifying transaction management with context managers.
3. **Error Handling**: Catching and handling exceptions, using rollbacks to maintain data integrity.
4. **Nested Transactions with Savepoints**: Rolling back to intermediate states within a transaction.

Mastering these techniques helps ensure data consistency and error resilience in database interactions.

---

### Step 1: Basic Transaction Management

In SQLAlchemy Core, transactions can be managed manually or using context managers. Let’s start with basic transaction management using `begin()` and `commit()`.

1. **Starting a Transaction**:

   ```python
   # Begin a transaction, insert a record, then commit
   with engine.connect() as conn:
       trans = conn.begin()  # Start a transaction
       try:
           conn.execute(insert(cars_table).values(make="Mazda", model="MX-5", year=2021, price=25000, is_sold=False))
           trans.commit()  # Commit if successful
           print("Transaction committed.")
       except Exception as e:
           trans.rollback()  # Rollback if an error occurs
           print(f"Transaction failed: {e}")
   ```

2. **Explanation**:
   - `begin()`: Starts a transaction.
   - `commit()`: Finalizes the transaction if no errors occur.
   - `rollback()`: Undoes changes if an error occurs.

---

### Step 2: Using Context Managers for Transactions

SQLAlchemy provides a more Pythonic way to handle transactions using `begin()` with a context manager, which automatically commits or rolls back as necessary.

1. **Transaction with Context Manager**:

   ```python
   # Begin a transaction with a context manager
   with engine.begin() as conn:
       conn.execute(insert(cars_table).values(make="Toyota", model="Camry", year=2022, price=30000, is_sold=False))
       conn.execute(insert(cars_table).values(make="Honda", model="Accord", year=2021, price=28000, is_sold=True))
       print("Transaction committed.")
   ```

2. **Explanation**:
   - `engine.begin()` opens a connection with transaction control.
   - If all statements execute successfully, the transaction is committed automatically.
   - If an error occurs, the transaction is rolled back automatically.

---

### Step 3: Error Handling with Transactions

To maintain data integrity, transactions should be rolled back if an error occurs. SQLAlchemy allows you to manage errors within the transaction block, handling issues gracefully.

1. **Error Handling Example**:

   ```python
   with engine.begin() as conn:
       try:
           conn.execute(insert(cars_table).values(make="Ford", model="Mustang", year=2020, price=45000, is_sold=False))
           conn.execute(insert(cars_table).values(make="Ford", model="Mustang", year="invalid year", price=45000, is_sold=False))  # Causes an error
           print("Transaction committed.")
       except Exception as e:
           print(f"Transaction failed: {e}")
           # Transaction is automatically rolled back due to the exception
   ```

2. **Explanation**:
   - The invalid year data type triggers an exception.
   - The transaction is automatically rolled back, preventing partial updates.

---

### Step 4: Nested Transactions with Savepoints

SQLAlchemy Core supports **savepoints**, which are nested transactions within a main transaction. Savepoints allow you to roll back to a certain point within a transaction without affecting the entire transaction.

1. **Using Savepoints**:

   ```python
   with engine.connect() as conn:
       trans = conn.begin()  # Begin the outer transaction
       try:
           # Insert a car outside savepoint
           conn.execute(insert(cars_table).values(make="Chevrolet", model="Malibu", year=2021, price=23000, is_sold=False))

           # Start a savepoint for nested transaction
           savepoint = conn.begin_nested()
           try:
               # Insert another car within the savepoint
               conn.execute(insert(cars_table).values(make="Dodge", model="Charger", year="invalid year", price=32000, is_sold=True))
               savepoint.commit()  # Commit savepoint if successful
           except Exception as e:
               savepoint.rollback()  # Rollback only to savepoint if an error occurs
               print(f"Savepoint rollback: {e}")

           trans.commit()  # Commit outer transaction
           print("Outer transaction committed.")
       except Exception as e:
           trans.rollback()
           print(f"Outer transaction failed: {e}")
   ```

2. **Explanation**:
   - **Savepoint**: Created with `begin_nested()`, allowing a partial rollback within the main transaction.
   - In this example, an error in the savepoint does not affect the main transaction.

---

### Example Usage in `__main__`

Here’s a block to test each transaction management method:

```python
if __name__ == "__main__":
    # Basic transaction with manual commit/rollback
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            conn.execute(insert(cars_table).values(make="Mazda", model="MX-5", year=2021, price=25000, is_sold=False))
            trans.commit()
            print("Manual transaction committed.")
        except Exception as e:
            trans.rollback()
            print(f"Manual transaction failed: {e}")

    # Transaction with context manager
    with engine.begin() as conn:
        conn.execute(insert(cars_table).values(make="Toyota", model="Camry", year=2022, price=30000, is_sold=False))
        conn.execute(insert(cars_table).values(make="Honda", model="Accord", year=2021, price=28000, is_sold=True))
        print("Context-managed transaction committed.")

    # Error handling in transaction
    with engine.begin() as conn:
        try:
            conn.execute(insert(cars_table).values(make="Ford", model="Mustang", year=2020, price=45000, is_sold=False))
            conn.execute(insert(cars_table).values(make="Ford", model="Mustang", year="invalid year", price=45000, is_sold=False))
        except Exception as e:
            print(f"Error-handled transaction failed: {e}")

    # Nested transaction with savepoints
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            conn.execute(insert(cars_table).values(make="Chevrolet", model="Malibu", year=2021, price=23000, is_sold=False))
            savepoint = conn.begin_nested()
            try:
                conn.execute(insert(cars_table).values(make="Dodge", model="Charger", year="invalid year", price=32000, is_sold=True))
                savepoint.commit()
            except Exception as e:
                savepoint.rollback()
                print(f"Savepoint rollback: {e}")
            trans.commit()
        except Exception as e:
            trans.rollback()
            print(f"Outer transaction failed: {e}")
```

### Summary of Part 3

- **Basic Transaction Management**: Use `begin()`, `commit()`, and `rollback()` for explicit transaction control.
- **Context Managers**: Simplify transaction handling with `engine.begin()` for auto-commit and rollback.
- **Error Handling**: Use `try-except` to manage errors, ensuring rollbacks on failures.
- **Savepoints**: Use nested transactions to roll back partially within a larger transaction.

This provides robust transaction management techniques in SQLAlchemy Core, ensuring data consistency and control. Let me know if you’d like to move to **Part 4**, where we’ll focus on **batch operations and performance optimization** in SQLAlchemy Core!
