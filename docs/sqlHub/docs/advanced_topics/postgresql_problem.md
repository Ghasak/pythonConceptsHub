# PostgreSQL Problem

## Fundamental PostgreSQL core design

In PostgreSQL, one of the biggest challenges is managing the "bloat" that can
occur over time due to its multi-version concurrency control (MVCC) model.
Let's break down the concepts of vacuuming, bloat, and how PostgreSQL compares
to Oracle and Microsoft SQL Server.

### 1. Understanding VACUUM in PostgreSQL PostgreSQL's MVCC model allows

multiple versions of rows to exist in the database to support concurrent
transactions. When a row is updated or deleted, PostgreSQL doesn't immediately
reclaim the space occupied by the old version of the row. Instead, it marks the
old row as dead while keeping it in storage until it can safely be removed.
This approach improves concurrency but leads to "bloat" over time, as dead
tuples (unused rows) accumulate.

To reclaim this space, PostgreSQL requires periodic maintenance through a
process called **VACUUM**. The vacuum process cleans up dead tuples, compacting
the storage used by tables and indexes. There are two types of vacuum
operations:

- **Autovacuum**: Runs in the background, but it may not be sufficient for very
  large databases or tables with heavy write activity.
- **Manual VACUUM**: Can be run manually to clean up tables, but for the most
  thorough cleanup, you might need to use **VACUUM FULL**.

### 2. Challenges with VACUUM FULL and Downtime While a standard vacuum can run

without taking the database offline, **VACUUM FULL** requires a lock on the
table, making it inaccessible to other processes. This can lead to downtime,
which is challenging for applications needing high availability. **VACUUM
FULL** essentially rewrites the table to remove all dead tuples, which can be a
time-consuming operation on large tables.

Due to this need for periodic maintenance that may impact availability,
managing bloat in PostgreSQL requires careful planning to avoid performance
issues or downtime.

### 3. Bloat in PostgreSQL Bloat refers to the accumulation of dead tuples that

aren't immediately reclaimed, which can increase storage usage and degrade
performance over time. As bloat grows, queries may slow down due to the
increased disk I/O required to scan through unused data.

When bloat is excessive, you may need to use **VACUUM FULL** to reclaim the
space fully, but this requires downtime, as mentioned. PostgreSQL lacks some of
the automatic storage compaction features found in other systems, making it
more dependent on the vacuum process to manage space.

### 4. Comparison with Oracle and Microsoft SQL Server Other databases like

Oracle and Microsoft SQL Server handle storage and concurrency differently,
which can reduce the impact of bloat:

- **Oracle**: Uses undo segments to manage row versions. When a transaction is
  committed, Oracle reclaims space more aggressively, so you don't need a process
  like VACUUM to reclaim space. Oracle's Automatic Segment Space Management
  (ASSM) can also manage storage more effectively, reducing the occurrence of
  bloat.

- **Microsoft SQL Server**: Uses a system called "versioning" for concurrency
  (if snapshot isolation is enabled), which also handles row versioning
  differently. SQL Server also offers better control over reclaiming space, and
  its row-level locking reduces the need for something like VACUUM. Space is
  reclaimed as rows are deleted or updated.

### Summary The biggest challenge for PostgreSQL with regard to vacuuming is

managing bloat without incurring downtime. In contrast, Oracle and Microsoft
SQL Server have mechanisms that reduce the need for manual space reclamation
and tend to handle storage compaction and concurrency control in a way that
leads to less bloat.

--- ## Why we need Versioning? Let’s break down why versioning (Multi-Version
Concurrency Control, or MVCC) is needed and how it supports concurrent access
using a simple example of transferring money between two people.

Imagine we have two people, **Person A** and **Person B**, each with accounts
in a bank database. Let’s say Person A wants to send $100 to Person B, and at
the same time, there are other transactions happening (such as withdrawals or
deposits) that also need to read and update the account balances.

### Why Versioning? In a database without versioning, each transaction that

tries to read or write data would need to lock the data entirely to prevent
conflicts. This could lead to **contention** (where transactions are stuck
waiting for each other to finish), which would slow things down significantly.
Versioning solves this problem by allowing each transaction to work with its
own "version" of the data while other transactions operate on their own
versions, enabling them to run concurrently without conflicts.

Let’s go through the example of Person A transferring money to Person B to see
how this works.

### Example: Transfer Between Person A and Person B

1. **Initial Balances:**

   - Person A has $500.
   - Person B has $300.

2. **The Transaction Begins:**

   - Person A wants to transfer $100 to Person B.
   - The database opens a transaction and **creates a new version** of Person
     A's and Person B's account rows for this transaction.

3. **Concurrent Transactions with Versioning:**

   - Let’s say that at the same time, someone is withdrawing money from Person
     B’s account or checking the balances of both accounts. With MVCC, each
     transaction works with its own "snapshot" of the data to prevent conflicts.
   - **Transaction 1 (Transfer):** Person A’s account is updated to $400
     (subtracting $100), and Person B’s account is updated to $400 (adding $100).
   - **Transaction 2 (Withdrawal):** Another transaction is trying to withdraw
     $50 from Person B's account while Transaction 1 is still processing. Thanks
     to versioning, Transaction 2 can read the original $300 balance of Person
     B’s account without being blocked or waiting for Transaction 1 to finish.

4. **How MVCC Resolves Conflicts:**

   - MVCC allows Transaction 2 to continue reading or even modifying data based
     on its version, which isolates it from changes in Transaction 1.
   - Once Transaction 1 is completed and committed, the new versions of Person
     A’s and Person B’s balances become the latest version in the database.
   - At this point, Transaction 2 will either commit with the older snapshot it
     worked with or adjust if it depends on the updated balance after Transaction
     1's changes.

5. **Dead Tuples and Cleanup (VACUUM):**
   - Over time, as many transactions create versions (old versions of account
     rows, like Person A’s $500 and Person B’s $300 in this case), they add up as
     "dead tuples" that aren’t immediately removed. The database must run
     **VACUUM** to clean up these old versions, or "dead tuples," freeing up
     space.

### Why Versioning Helps with Concurrency With versioning, each transaction has

a “snapshot” of the data at the start of the transaction. This means:

- Transactions don’t have to wait for each other to finish, avoiding
  bottlenecks.
- Read operations don’t block writes, and writes don’t block reads.
- This allows the system to handle many operations at once, which is crucial
  for databases that need to support many users simultaneously (like bank
  transactions).

### Without Versioning If the database didn’t use versioning, the transfer

transaction would need to lock both Person A's and Person B's accounts entirely
until it’s done. Other transactions trying to read or write these accounts
would have to wait, which would slow down the whole system.

### Summary In a money transfer situation, versioning ensures that:

- Person A’s and Person B’s balances can be updated without blocking other
  users from reading or modifying the balances.
- Multiple transactions can work concurrently without stepping on each other’s
  toes.
- The database remains efficient even when many transactions happen at once,
  thanks to snapshots provided by MVCC.

This is why MVCC and versioning are crucial for supporting concurrency in
PostgreSQL and similar databases.
