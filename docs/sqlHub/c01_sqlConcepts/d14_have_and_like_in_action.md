# HAVE LIKE AND WITH in SQL

## CONCEPT

In SQL, `WHERE` and `HAVING` are both used to filter records, but they serve
different purposes and are applied at different stages in the query process:

- **`WHERE`**: This clause filters records at the row level before any grouping
  or aggregation takes place. It is generally used to filter rows based on column
  values.

- **`HAVING`**: This clause filters records after aggregation has been
  performed. It’s typically used with aggregate functions (e.g., `COUNT`, `SUM`,
  `AVG`) to filter groups of rows rather than individual rows.

Here's a breakdown of the syntax and usage for each:

### Syntax

- **WHERE Clause Syntax**

  ```sql
  SELECT column1, column2, ...
  FROM table_name
  WHERE condition;
  ```

- **HAVING Clause Syntax** (used with `GROUP BY`)
  ```sql
  SELECT column1, aggregate_function(column2), ...
  FROM table_name
  GROUP BY column1
  HAVING condition;
  ```

### Use Case Example

Suppose we have a table called `sales` with the following columns:

- `id` - Unique identifier for each sale
- `product` - Name of the product
- `quantity` - Quantity sold
- `price` - Price per unit
- `sales_date` - Date of the sale

#### Example 1: Using `WHERE`

You want to find all sales for the product "Laptop" where the price is more than 1000.

```sql
SELECT *
FROM sales
WHERE product = 'Laptop' AND price > 1000;
```

This query filters rows based on specific column values before any aggregation.

#### Example 2: Using `HAVING`

You want to find products with a total quantity sold greater than 50, regardless of individual sales.

```sql
SELECT product, SUM(quantity) AS total_quantity
FROM sales
GROUP BY product
HAVING SUM(quantity) > 50;
```

This query first groups the rows by `product`, then calculates the total
quantity for each product, and finally filters those groups with a total
quantity greater than 50.

### Expected Table View for Comparison

| Clause | Example Use Case                        | Syntax Example                                                                                           | Filter Level                   | Usage Scenario                                              |
| ------ | --------------------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------ | ----------------------------------------------------------- |
| WHERE  | Filter rows where `product` is "Laptop" | `SELECT * FROM sales WHERE product = 'Laptop' AND price > 1000;`                                         | Row-level (pre-aggregation)    | To filter records based on column values before aggregation |
| HAVING | Filter groups with total quantity > 50  | `SELECT product, SUM(quantity) AS total_quantity FROM sales GROUP BY product HAVING SUM(quantity) > 50;` | Group-level (post-aggregation) | To filter aggregated groups based on aggregate conditions   |

Using `WHERE` and `HAVING` correctly in SQL depends on whether you need to filter data before or after aggregation.

## WITH Clause

The `WITH` clause in SQL, also known as a **Common Table Expression (CTE)**,
allows you to define a temporary result set that can be referenced within a
`SELECT`, `INSERT`, `UPDATE`, or `DELETE` statement. This clause is useful for
breaking down complex queries, improving readability, and avoiding subquery
repetition.

### Syntax and Explanation

- **WITH Clause Syntax**
  ```sql
  WITH cte_name AS (
      SELECT column1, column2, ...
      FROM table_name
      WHERE condition
  )
  SELECT column1, column2, ...
  FROM cte_name;
  ```

### Use Case Example

Suppose you have a `sales` table with columns:

- `id` - Unique identifier for each sale
- `product` - Name of the product
- `quantity` - Quantity sold
- `price` - Price per unit
- `sales_date` - Date of the sale

#### Example 1: Simplifying a Query with `WITH`

Imagine you want to find products where the total quantity sold exceeds 50 and
the total revenue (quantity \* price) is above 5000. Instead of using a complex
subquery, you can define the intermediate results using `WITH`.

```sql
WITH product_totals AS (
    SELECT product, SUM(quantity) AS total_quantity, SUM(quantity * price) AS total_revenue
    FROM sales
    GROUP BY product
)
SELECT product
FROM product_totals
WHERE total_quantity > 50 AND total_revenue > 5000;
```

Here, the `WITH` clause (or CTE) `product_totals` calculates the total quantity
and total revenue per product. Then, in the main query, we simply filter
products based on those aggregated values.

#### Example 2: Using Multiple CTEs

You can define multiple CTEs in a single query. Suppose you want to identify
products that both meet a sales threshold and were sold on a specific date.

```sql
WITH product_totals AS (
    SELECT product, SUM(quantity) AS total_quantity
    FROM sales
    GROUP BY product
),
high_sales_products AS (
    SELECT product
    FROM product_totals
    WHERE total_quantity > 50
)
SELECT *
FROM sales
WHERE product IN (SELECT product FROM high_sales_products) AND sales_date = '2024-11-01';
```

In this example, we first create `product_totals` to calculate the total
quantity for each product, then filter those results to define
`high_sales_products` as products that meet the sales threshold. Finally, we
query the `sales` table to find records for these products on a specific date.

### Expected Table View for Comparison

| Clause | Example Use Case                                  | Syntax Example                                                                                                                       | Purpose                     | Usage Scenario                                         |
| ------ | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | --------------------------- | ------------------------------------------------------ |
| WITH   | Calculate totals for each product and filter data | `WITH product_totals AS (SELECT product, SUM(quantity) AS total_quantity FROM sales GROUP BY product) SELECT * FROM product_totals;` | Define intermediate results | To simplify complex queries or reuse temporary results |

The `WITH` clause is beneficial when you need to break down complex queries into manageable parts or when you need to reference the same calculated result multiple times within a single query.

## Note

In SQL, you can use the `WITH` clause with a **subquery directly** in the form:

```sql
WITH (SELECT ... ) AS mytable
```

However, this syntax is generally incorrect in SQL and will likely produce an
error. Instead, the correct syntax in SQL when using the `WITH` clause is:

```sql
WITH mytable AS (
    SELECT ...
)
```

The `WITH` clause in SQL requires that you give the CTE (Common Table
Expression) a **name directly after `WITH`** (e.g., `mytable`), followed by
`AS`, and then place the **subquery within parentheses**.

### Example of Correct Usage

Suppose you have a table called `sales` with columns:

- `id`
- `product`
- `quantity`
- `price`
- `sales_date`

And you want to create a CTE named `mytable` that calculates the total revenue per product:

```sql
WITH mytable AS (
    SELECT product, SUM(quantity * price) AS total_revenue
    FROM sales
    GROUP BY product
)
SELECT *
FROM mytable
WHERE total_revenue > 5000;
```

In this example:

1. `mytable` is the name of the CTE.
2. The CTE contains a subquery that calculates the `total_revenue` for each `product`.

### Why the Direct Subquery Syntax Doesn't Work

In SQL, the syntax `WITH (SELECT ...) AS mytable` isn’t supported because
`WITH` requires an **immediate CTE name** (like `mytable`) followed by `AS` and
a subquery in parentheses. SQL does not interpret `WITH (SELECT...)` as a named
expression without an identifier immediately after `WITH`.

To summarize, the correct pattern for using a subquery with `WITH` is:

```sql
WITH mytable AS (
    SELECT ...
)
SELECT ...
FROM mytable;
```

This syntax helps SQL interpret `mytable` as a temporary table defined by the
CTE, allowing it to be referenced in the main query.

## LIKE Clause

The `LIKE` clause in SQL is used for pattern matching within string columns.
It's commonly used with the `WHERE` clause to filter rows based on specific
patterns in text values. You can use wildcards to define these patterns, such
as `%` to represent any sequence of characters and `_` to represent a single
character.

### Syntax and Explanation

- **LIKE Clause Syntax**
  ```sql
  SELECT column1, column2, ...
  FROM table_name
  WHERE column_name LIKE pattern;
  ```

### Wildcards in `LIKE`

- `%` - Matches any sequence of characters (including zero characters).
- `_` - Matches any single character.

### Use Case Examples

Suppose you have a table called `customers` with the following columns:

- `id` - Unique identifier for each customer
- `name` - Customer name
- `email` - Customer email address
- `city` - City of the customer

#### Example 1: Using `LIKE` with `%` (Any Sequence of Characters)

You want to find customers whose names start with "Jo".

```sql
SELECT *
FROM customers
WHERE name LIKE 'Jo%';
```

This query will match any name that starts with "Jo" and is followed by any sequence of characters, such as "John" or "Joanna".

#### Example 2: Using `LIKE` with `_` (Single Character)

You want to find customers whose names have "a" as the second character and are four characters long.

```sql
SELECT *
FROM customers
WHERE name LIKE '_a__';
```

This query matches any name where:

- The first character can be any character (`_`)
- The second character is "a"
- The third and fourth characters can be any characters

For example, it will match names like "Jack" and "Kate".

#### Example 3: Using `LIKE` with Both `%` and `_`

You want to find customers whose emails contain "example.com" but start with exactly three characters.

```sql
SELECT *
FROM customers
WHERE email LIKE '___%example.com';
```

This query matches any email address where:

- The first three characters can be any characters (`___`)
- It’s followed by any sequence (`%`) and then "example.com"

For instance, it will match "abc@example.com" or "xyz@example.com".

### Expected Table View for Comparison

| Clause | Example Use Case                               | Syntax Example                                                | Wildcard          | Usage Scenario                                           |
| ------ | ---------------------------------------------- | ------------------------------------------------------------- | ----------------- | -------------------------------------------------------- |
| LIKE   | Find customers whose name starts with "Jo"     | `SELECT * FROM customers WHERE name LIKE 'Jo%';`              | `%` (any chars)   | Matching any sequence of characters after a given prefix |
| LIKE   | Find four-letter names with "a" as second char | `SELECT * FROM customers WHERE name LIKE '_a__';`             | `_` (single char) | Matching names with specific character placements        |
| LIKE   | Find emails with "example.com" after 3 chars   | `SELECT * FROM customers WHERE email LIKE '___%example.com';` | `_` and `%`       | Combining single and multiple-character patterns         |

### Summary of `LIKE` Clause Use

The `LIKE` clause is versatile for finding specific patterns in text columns.
It’s especially useful for flexible matching criteria, such as identifying
names with specific letters, emails that end in certain domains, or any
text-based pattern that can be defined with `%` and `_`.

---

## Pattern with Like

Here's a table of all common SQL pattern symbols used with the `LIKE` clause, along with their meanings:

| Pattern Symbol | Meaning                                                                                                   |
| -------------- | --------------------------------------------------------------------------------------------------------- |
| `%`            | Matches any sequence of characters (including zero characters).                                           |
| `_`            | Matches exactly one single character.                                                                     |
| `[abc]`        | Matches any single character within the brackets (`a`, `b`, or `c`).                                      |
| `[a-z]`        | Matches any single character within the specified range (`a` to `z`).                                     |
| `[A-Z]`        | Matches any single uppercase letter within the specified range (`A` to `Z`).                              |
| `[0-9]`        | Matches any single digit (`0` to `9`).                                                                    |
| `[!abc]`       | Matches any single character not within the brackets (not `a`, `b`, or `c`).                              |
| `[!a-z]`       | Matches any single character not within the specified range (`a` to `z`).                                 |
| `[^abc]`       | (Alternative syntax) Matches any single character not within the brackets.                                |
| `[^0-9]`       | (Alternative syntax) Matches any single character that is not a digit (`0` to `9`).                       |
| `\`            | Escape character to treat `%`, `_`, `[ ]`, or `\` as literals (e.g., `\%` to match a literal `%` symbol). |

This table covers the essential pattern symbols used in SQL for the `LIKE`
clause and pattern matching, providing flexibility for matching specific or
broad patterns in text fields.

---

## Examples of Patters

Here's an exhaustive table of common SQL `LIKE` patterns, including explanations of their functionality. This should cover most typical uses of pattern matching with `LIKE` and wildcards.

| Pattern       | Explanation                                                                                        | Example Matches                   | Example Non-Matches           |
| ------------- | -------------------------------------------------------------------------------------------------- | --------------------------------- | ----------------------------- |
| `%`           | Matches any sequence of characters (including zero characters).                                    | "", "abc", "123abc", "abcdefg"    | None                          |
| `_`           | Matches exactly one single character.                                                              | "a", "1", any single character    | "", "abc"                     |
| `A%`          | Matches any string starting with "A".                                                              | "Apple", "A123", "Avocado"        | "apple", "Banana", "123A"     |
| `%A`          | Matches any string ending with "A".                                                                | "Avocado", "Banana", "123A"       | "Apple", "a123"               |
| `%A%`         | Matches any string containing "A" anywhere.                                                        | "Banana", "123A456", "Avocado"    | "banana", "apple"             |
| `A_B`         | Matches any three-character string starting with "A" and ending with "B".                          | "ACB", "A1B", "A2B"               | "AB", "Apple", "ABCD"         |
| `A%B`         | Matches any string that starts with "A" and ends with "B".                                         | "AB", "AppleB", "A123B"           | "BA", "ABC123", "A123BC"      |
| `A%_%B`       | Matches any string that starts with "A", has at least one character in between, and ends with "B". | "A1B", "A123B", "ABCB"            | "AB", "ABC", "BA"             |
| `%123%`       | Matches any string containing "123" anywhere within it.                                            | "123", "abc123", "123xyz"         | "12", "ab1234", "456"         |
| `%[A-D]%`     | Matches any string containing any character between "A" and "D".                                   | "Apple", "Dog", "Bear"            | "Zebra", "apple"              |
| `_[a-z]_%`    | Matches any string where the second character is a lowercase letter.                               | "1a*", "Ba*", "Ma123"             | "1A*", "Ab*", "apple"         |
| `%[!A]%`      | Matches any string that does not contain the character "A".                                        | "Banana", "123", "xyz"            | "Apple", "Avocado", "A123"    |
| `[0-9]%`      | Matches any string starting with a digit (0-9).                                                    | "123abc", "4cars", "9lives"       | "abc123", "cars123", "lives9" |
| `___%`        | Matches any string with at least three characters.                                                 | "abc", "abcd", "123456"           | "ab", ""                      |
| `%_`          | Matches any string with at least one character.                                                    | "a", "1", "abc", "123"            | ""                            |
| `%__%`        | Matches any string with at least two characters.                                                   | "ab", "123", "abc", "xyz"         | "a", ""                       |
| `[A-Z]%`      | Matches any string starting with an uppercase letter (A-Z).                                        | "Apple", "Banana", "Cat"          | "apple", "123", "apple123"    |
| `[A-Z]%[0-9]` | Matches any string starting with an uppercase letter and ending with a digit.                      | "A1", "B123", "C9"                | "apple", "123", "Cat"         |
| `%[^0-9]%`    | Matches any string that does not contain a digit.                                                  | "Apple", "Banana", "Cat"          | "123", "Cat2", "Banana456"    |
| `____`        | Matches any string with exactly four characters.                                                   | "abcd", "1234", "xyzw"            | "abc", "12345", "a", ""       |
| `%@%.com`     | Matches any email ending with ".com".                                                              | "user@example.com", "a@b.com"     | "user@example.net", "a@b.org" |
| `%.%`         | Matches any string containing a period (useful for matching emails or domain names).               | "example.com", "test@example.org" | "example", "testexamplecom"   |
| `%[A-Za-z]%`  | Matches any string that contains at least one letter (uppercase or lowercase).                     | "123a456", "Test", "123ABC"       | "123", "456789"               |
| `%[^A-Za-z]%` | Matches any string that contains no letters.                                                       | "123", "456789", "!@#$"           | "Test", "123a456", "ABC"      |
| `%\_%`        | Matches any string that contains an underscore (escaped underscore).                               | "user_name", "example_123"        | "username", "example123"      |
| `%\%%`        | Matches any string that contains a percent sign (escaped percent).                                 | "50%", "discount%", "100%"        | "50", "discount", "100"       |

This table includes commonly used patterns for the `LIKE` clause with `%` and
`_` wildcards, including options for specific lengths, starting or ending
characters, and patterns involving uppercase, lowercase, digits, or special
characters. These patterns can be combined as needed to match specific string
patterns in SQL.

## Logic with Pattern

In SQL, logic symbols like `AND`, `OR`, and `NOT` are not used directly within
`LIKE` patterns themselves. However, you can combine multiple `LIKE` conditions
using these logical operators in the `WHERE` clause to build more complex
patterns. Here’s how they work in combination with `LIKE`:

### Using Logical Operators with `LIKE`

- **AND**: Combines multiple `LIKE` conditions where all must be true.
- **OR**: Combines multiple `LIKE` conditions where at least one must be true.
- **NOT**: Negates a `LIKE` condition to find records that do not match the specified pattern.

### Examples of Logical Operators with `LIKE`

Suppose we have a table called `customers` with a column `name` and you want to
match specific name patterns:

#### Example 1: Using `AND` with `LIKE`

Find names that start with "A" and also contain "n".

```sql
SELECT *
FROM customers
WHERE name LIKE 'A%' AND name LIKE '%n%';
```

In this case:

- The `name` must start with "A" (`LIKE 'A%'`) **and** contain "n" anywhere in the string (`LIKE '%n%'`).

#### Example 2: Using `OR` with `LIKE`

Find names that start with "A" or end with "z".

```sql
SELECT *
FROM customers
WHERE name LIKE 'A%' OR name LIKE '%z';
```

Here:

- The `name` can either start with "A" **or** end with "z".

#### Example 3: Using `NOT` with `LIKE`

Find names that do not contain "x".

```sql
SELECT *
FROM customers
WHERE name NOT LIKE '%x%';
```

This query selects rows where:

- The `name` does **not** contain the letter "x" anywhere in the string.

#### Combining `AND`, `OR`, and `NOT` with `LIKE`

You can combine these logical operators to create even more complex patterns.
For example, find names that start with "A" and do not contain "x", or end with
"z".

```sql
SELECT *
FROM customers
WHERE (name LIKE 'A%' AND name NOT LIKE '%x%') OR name LIKE '%z';
```

In this example:

- The `name` must either start with "A" and not contain "x", **or** end with "z".

### Summary Table of Logic Operators with `LIKE`

| Operator | Example Syntax                                | Explanation                                                |
| -------- | --------------------------------------------- | ---------------------------------------------------------- |
| AND      | `LIKE 'A%' AND LIKE '%n%'`                    | Matches rows where both `LIKE` conditions are true.        |
| OR       | `LIKE 'A%' OR LIKE '%z'`                      | Matches rows where at least one `LIKE` condition is true.  |
| NOT      | `NOT LIKE '%x%'`                              | Matches rows where the `LIKE` condition is not true.       |
| Combined | `(LIKE 'A%' AND NOT LIKE '%x%') OR LIKE '%z'` | Matches rows where complex conditions with `LIKE` are met. |

By combining `LIKE` with logical operators, you gain flexibility to filter results based on multiple patterns, exclusions, and conditions in a single query.
