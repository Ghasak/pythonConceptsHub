# Amazong driver Delivery
<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Amazong driver Delivery](#amazong-driver-delivery)
    - [G01 -](#g01--)
        - [Sample Table: `drivers`](#sample-table-drivers)
        - [First Question: Calculating Driver Performance KPI](#first-question-calculating-driver-performance-kpi)
        - [Results](#results)
    - [G02 -](#g02--)
        - [Second Question: Calculating Average Distance Per Delivery](#second-question-calculating-average-distance-per-delivery)
        - [Third Question (Difficulty: Easy): Calculating Delivery Efficiency Score](#third-question-difficulty-easy-calculating-delivery-efficiency-score)
    - [Specify some questions of drivers who join after specific time for example](#specify-some-questions-of-drivers-who-join-after-specific-time-for-example)
        - [Updated Sample Table: `drivers`](#updated-sample-table-drivers)
        - [Fourth Question (Difficulty: Easy): Retrieving Drivers Who Joined After a Specific Date](#fourth-question-difficulty-easy-retrieving-drivers-who-joined-after-a-specific-date)
    - [Question involving conditions and aggregates.](#question-involving-conditions-and-aggregates)
        - [Fifth Question (Difficulty: Medium): Finding Drivers with High On-Time Performance Who Joined Recently](#fifth-question-difficulty-medium-finding-drivers-with-high-on-time-performance-who-joined-recently)
        - [Sixth Question (Difficulty: Medium): Finding the Top 3 Drivers Based on Total Deliveries](#sixth-question-difficulty-medium-finding-the-top-3-drivers-based-on-total-deliveries)
        - [Seventh Question (Difficulty: Medium): Calculating Average On-Time Rate for All Drivers](#seventh-question-difficulty-medium-calculating-average-on-time-rate-for-all-drivers)
        - [Eighth Question (Difficulty: Medium): Finding Drivers with Low On-Time Delivery Rate](#eighth-question-difficulty-medium-finding-drivers-with-low-on-time-delivery-rate)
        - [Ninth Question (Difficulty: Medium): Finding Deliveries Completed by Drivers in the Last 6 Months](#ninth-question-difficulty-medium-finding-deliveries-completed-by-drivers-in-the-last-6-months)
    - [ok next](#ok-next)
        - [New Sample Table: `deliveries`](#new-sample-table-deliveries)
        - [Tenth Question (Difficulty: Medium): Aggregating Deliveries for Each Driver](#tenth-question-difficulty-medium-aggregating-deliveries-for-each-driver)
        - [Eleventh Question (Difficulty: Hard): Calculating Performance Metrics for Each Driver Using Aggregated Data](#eleventh-question-difficulty-hard-calculating-performance-metrics-for-each-driver-using-aggregated-data)
        - [Twelfth Question (Difficulty: Hard): Calculating the Average Delivery Efficiency Across All Drivers](#twelfth-question-difficulty-hard-calculating-the-average-delivery-efficiency-across-all-drivers)
        - [Thirteenth Question (Difficulty: Hard): Calculating Monthly Delivery Totals for Each Driver](#thirteenth-question-difficulty-hard-calculating-monthly-delivery-totals-for-each-driver)
        - [Explanation:](#explanation)
        - [Fourteenth Question (Difficulty: Very Hard): Finding Drivers with a 100% On-Time Delivery Rate Over the Last Three Months](#fourteenth-question-difficulty-very-hard-finding-drivers-with-a-100-on-time-delivery-rate-over-the-last-three-months)
        - [Fifteenth Question (Difficulty: Very Hard): Calculating a 7-Day Rolling Average of On-Time Delivery Rate for Each Driver](#fifteenth-question-difficulty-very-hard-calculating-a-7-day-rolling-average-of-on-time-delivery-rate-for-each-driver)
        - [Sixteenth Question (Difficulty: Very Hard): Identifying Drivers with Exceptional Delivery Efficiency](#sixteenth-question-difficulty-very-hard-identifying-drivers-with-exceptional-delivery-efficiency)
        - [Seventeenth Question (Difficulty: Very Hard): Calculating Monthly Driver Retention Rate](#seventeenth-question-difficulty-very-hard-calculating-monthly-driver-retention-rate)
        - [Eighteenth Question (Difficulty: Very Hard): Identifying Drivers with Consistent High On-Time Delivery Rate Over the Last 6 Months](#eighteenth-question-difficulty-very-hard-identifying-drivers-with-consistent-high-on-time-delivery-rate-over-the-last-6-months)
        - [Explanation:](#explanation-1)
        - [Expected Result:](#expected-result)
        - [Nineteenth Question (Difficulty: Very Hard): Ranking Drivers Based on Total Deliveries Over the Last 3 Months](#nineteenth-question-difficulty-very-hard-ranking-drivers-based-on-total-deliveries-over-the-last-3-months)
        - [Explanation:](#explanation-2)
        - [Expected Result:](#expected-result-1)

<!-- markdown-toc end -->

## G01 -

```
Assume i have a database with table for drivers who are working for delivery  as third party
like in amazon
now formulate to me sql questions with answer for interview questions to test my knowledge in sql
should be most common questions from daily work like
create a kpi for the drivers performance ..etc
you can test my knowledge little by little
first show some entries of the table say 5 rows
for all questions should show the expected table view result
you will be my guide to teach me about most common questions in sql and step up little by little
```

Based on the questions we will cover here, we will develop a solid understanding of SQL, especially with intermediate to advanced topics. You will tackle questions involving:

- Aggregations and basic calculations (e.g., delivery efficiency, on-time rate)
- Complex filtering with conditional logic
- Window functions and ranking (e.g., rolling averages, monthly ranks)
- Multi-step queries using CTEs to build layered analyses

Your comfort with increasingly complex queries suggests you’re operating at an intermediate to advanced level. You’re capable of handling performance-related metrics, cohort analysis, and advanced ranking techniques—all essential for real-world data analysis.

Next steps could involve:

- Exploring performance optimization for large datasets (indexing, query plan analysis).
- Diving into database-specific advanced functions.
- Practicing with real-world datasets to simulate larger-scale analysis.

Your foundation is strong, and you’re well on your way to mastering SQL at a professional level! Let me know if you’d like to focus on any specific areas or continue practicing.

---

Let's start with a basic setup and a sample table of delivery drivers. This table will include essential columns that track each driver’s performance and other relevant metrics.

### Sample Table: `drivers`

| driver_id | name       | total_deliveries | on_time_deliveries | late_deliveries | distance_covered | working_hours |
| --------- | ---------- | ---------------- | ------------------ | --------------- | ---------------- | ------------- |
| 1         | John Smith | 120              | 110                | 10              | 250.5            | 50            |
| 2         | Jane Doe   | 200              | 190                | 10              | 320.0            | 60            |
| 3         | Mike Brown | 150              | 140                | 10              | 270.8            | 55            |
| 4         | Emma Green | 180              | 160                | 20              | 300.0            | 58            |
| 5         | Liam White | 130              | 120                | 10              | 220.3            | 53            |

---

### First Question: Calculating Driver Performance KPI

A common KPI for driver performance could be the "on-time delivery rate," which is the percentage of deliveries made on time. Let's calculate this KPI for each driver.

**Question**: Write an SQL query to calculate the on-time delivery rate for each driver. The on-time delivery rate is defined as:

$$
\text{On-time Delivery Rate} = \frac{\sum_{k=1}^n \text{on\_time\_deliveries}_k}{\sum_{k=1}^n \text{total\_deliveries}_k} \times 100
$$

**Expected Result:**

| driver_id | name       | on_time_rate |
| --------- | ---------- | ------------ |
| 1         | John Smith | 91.67        |
| 2         | Jane Doe   | 95.00        |
| 3         | Mike Brown | 93.33        |
| 4         | Emma Green | 88.89        |
| 5         | Liam White | 92.31        |

Would you like to try answering this first, or should I go over the SQL query and answer directly?

### Results

Here’s the SQL query to calculate the on-time delivery rate for each driver:

```sql
SELECT
    driver_id,
    name,
    ROUND((on_time_deliveries / total_deliveries) * 100, 2) AS on_time_rate
FROM
    drivers;
```

**Expected Result:**

| driver_id | name       | on_time_rate |
| --------- | ---------- | ------------ |
| 1         | John Smith | 91.67        |
| 2         | Jane Doe   | 95.00        |
| 3         | Mike Brown | 93.33        |
| 4         | Emma Green | 88.89        |
| 5         | Liam White | 92.31        |

This result shows the on-time delivery rate as a percentage for each driver, rounded to two decimal places. Let me know if you'd like to try another question or explore further with this example!

## G02 -

Let's move on to another common metric for driver performance: **average distance per delivery**. This can help assess how efficiently drivers cover distances, which may indicate fuel consumption and route optimization.

### Second Question: Calculating Average Distance Per Delivery

**Question**: Write an SQL query to calculate the average distance per delivery for each driver. This metric is defined as:

$$\text{Average Distance per Delivery} = \frac{\sum_{k=1}^n \text{distance\_covered}_k}{\sum_{k=1}^n \text{total\_deliveries}_k}$$

**Expected Result:**

| driver_id | name       | avg_distance_per_delivery |
| --------- | ---------- | ------------------------- |
| 1         | John Smith | 2.09                      |
| 2         | Jane Doe   | 1.60                      |
| 3         | Mike Brown | 1.81                      |
| 4         | Emma Green | 1.67                      |
| 5         | Liam White | 1.69                      |

Would you like to try writing this query yourself, or should I provide the solution directly?

---

Here’s the SQL query to calculate the average distance per delivery for each driver:

```sql
SELECT
    driver_id,
    name,
    ROUND((distance_covered / total_deliveries), 2) AS avg_distance_per_delivery
FROM
    drivers;
```

**Expected Result:**

| driver_id | name       | avg_distance_per_delivery |
| --------- | ---------- | ------------------------- |
| 1         | John Smith | 2.09                      |
| 2         | Jane Doe   | 1.60                      |
| 3         | Mike Brown | 1.81                      |
| 4         | Emma Green | 1.67                      |
| 5         | Liam White | 1.69                      |

This table shows the average distance each driver covers per delivery, rounded to two decimal places. Let me know if you're ready for the next question!

---

### Third Question (Difficulty: Easy): Calculating Delivery Efficiency Score

Another useful metric is the **delivery efficiency score**, which can help evaluate the number of deliveries a driver completes per hour worked. This metric shows productivity and helps in optimizing scheduling and workload distribution.

**Question**: Write an SQL query to calculate the delivery efficiency score for each driver, defined as:

$$
\text{Delivery Efficiency Score} = \frac{\sum_{k=1}^n \text{total\_deliveries}_k}{\sum_{k=1}^n \text{working\_hours}_k}
$$

**Expected Result:**

| driver_id | name       | delivery_efficiency |
| --------- | ---------- | ------------------- |
| 1         | John Smith | 2.40                |
| 2         | Jane Doe   | 3.33                |
| 3         | Mike Brown | 2.73                |
| 4         | Emma Green | 3.10                |
| 5         | Liam White | 2.45                |

Would you like to try this one yourself, or should I provide the answer?

Here’s the SQL query to calculate the delivery efficiency score for each driver:

```sql
SELECT
    driver_id,
    name,
    ROUND((total_deliveries / working_hours), 2) AS delivery_efficiency
FROM
    drivers;
```

**Expected Result:**

| driver_id | name       | delivery_efficiency |
| --------- | ---------- | ------------------- |
| 1         | John Smith | 2.40                |
| 2         | Jane Doe   | 3.33                |
| 3         | Mike Brown | 2.73                |
| 4         | Emma Green | 3.10                |
| 5         | Liam White | 2.45                |

This result shows each driver’s efficiency score in terms of deliveries per hour worked, rounded to two decimal places. Let me know if you're ready for the next question!

## Specify some questions of drivers who join after specific time for example

move to next question now
Let’s move on to filtering drivers based on their joining date. To proceed, let's assume an additional column, `join_date`, in the `drivers` table, which stores the date each driver joined the company.

### Updated Sample Table: `drivers`

| driver_id | name       | total_deliveries | on_time_deliveries | late_deliveries | distance_covered | working_hours | join_date  |
| --------- | ---------- | ---------------- | ------------------ | --------------- | ---------------- | ------------- | ---------- |
| 1         | John Smith | 120              | 110                | 10              | 250.5            | 50            | 2023-01-15 |
| 2         | Jane Doe   | 200              | 190                | 10              | 320.0            | 60            | 2023-05-20 |
| 3         | Mike Brown | 150              | 140                | 10              | 270.8            | 55            | 2023-08-01 |
| 4         | Emma Green | 180              | 160                | 20              | 300.0            | 58            | 2022-12-10 |
| 5         | Liam White | 130              | 120                | 10              | 220.3            | 53            | 2023-02-18 |

---

### Fourth Question (Difficulty: Easy): Retrieving Drivers Who Joined After a Specific Date

**Question**: Write an SQL query to retrieve the names and join dates of drivers who joined after `2023-01-01`.

**Expected Result:**

| driver_id | name       | join_date  |
| --------- | ---------- | ---------- |
| 1         | John Smith | 2023-01-15 |
| 2         | Jane Doe   | 2023-05-20 |
| 3         | Mike Brown | 2023-08-01 |
| 5         | Liam White | 2023-02-18 |

Would you like to try this one, or should I provide the query directly?

Here’s the SQL query to retrieve the names and join dates of drivers who joined after `2023-01-01`:

```sql
SELECT
    driver_id,
    name,
    join_date
FROM
    drivers
WHERE
    join_date > '2023-01-01';
```

**Expected Result:**

| driver_id | name       | join_date  |
| --------- | ---------- | ---------- |
| 1         | John Smith | 2023-01-15 |
| 2         | Jane Doe   | 2023-05-20 |
| 3         | Mike Brown | 2023-08-01 |
| 5         | Liam White | 2023-02-18 |

This result lists the drivers who joined after January 1, 2023. Let me know if you’re ready for the next question!

## Question involving conditions and aggregates.

---

### Fifth Question (Difficulty: Medium): Finding Drivers with High On-Time Performance Who Joined Recently

**Question**: Write an SQL query to find drivers who joined after `2023-01-01` and have an on-time delivery rate of at least 90%. Display their `driver_id`, `name`, `join_date`, and `on_time_rate`.

You can calculate the on-time delivery rate as:

$$
\text{On-time Delivery Rate} = \frac{\sum_{k=1}^n \text{on\_time\_deliveries}_k}{\sum_{k=1}^n \text{total\_deliveries}_k} \times 100
$$

**Expected Result:**

| driver_id | name       | join_date  | on_time_rate |
| --------- | ---------- | ---------- | ------------ |
| 1         | John Smith | 2023-01-15 | 91.67        |
| 2         | Jane Doe   | 2023-05-20 | 95.00        |
| 3         | Mike Brown | 2023-08-01 | 93.33        |
| 5         | Liam White | 2023-02-18 | 92.31        |

Would you like to give it a try, or should I go ahead with the solution?

Good attempt! There’s a small correction needed in the query. The `on_time_rate` is not a column in the table; we need to calculate it within the query. Additionally, remove the semicolon before `ORDER BY` to avoid a syntax error.

Here’s the correct query:

```sql
SELECT
    driver_id,
    name,
    join_date,
    ROUND((on_time_deliveries / total_deliveries) * 100, 2) AS on_time_rate
FROM
    drivers
WHERE
    join_date > '2023-01-01'
    AND (on_time_deliveries / total_deliveries) * 100 >= 90.0
ORDER BY
    on_time_rate DESC;
```

**Expected Result:**

| driver_id | name       | join_date  | on_time_rate |
| --------- | ---------- | ---------- | ------------ |
| 2         | Jane Doe   | 2023-05-20 | 95.00        |
| 3         | Mike Brown | 2023-08-01 | 93.33        |
| 5         | Liam White | 2023-02-18 | 92.31        |
| 1         | John Smith | 2023-01-15 | 91.67        |

This query calculates the on-time delivery rate on the fly and filters drivers who joined after January 1, 2023, with a rate of 90% or higher, ordered by `on_time_rate` in descending order. Let me know if you're ready for the next question!

Let's proceed with a question that combines filtering, aggregation, and ordering to analyze performance.

---

### Sixth Question (Difficulty: Medium): Finding the Top 3 Drivers Based on Total Deliveries

**Question**: Write an SQL query to identify the top 3 drivers based on the total number of deliveries. Display `driver_id`, `name`, and `total_deliveries`.

**Expected Result:**

| driver_id | name       | total_deliveries |
| --------- | ---------- | ---------------- |
| 2         | Jane Doe   | 200              |
| 4         | Emma Green | 180              |
| 3         | Mike Brown | 150              |

Would you like to try this one, or should I show the solution?
Nice try! Your query is sorting by `on_time_rate`, which is good for ranking based on on-time performance. However, to get the top 3 drivers based on **total deliveries** rather than on-time rate, you’ll need to:

1. Select `driver_id`, `name`, and `total_deliveries` only.
2. Order by `total_deliveries` in descending order.
3. Limit the results to the top 3.

Here’s the modified query:

```sql
SELECT
    driver_id,
    name,
    total_deliveries
FROM
    drivers
ORDER BY
    total_deliveries DESC
LIMIT 3;
```

**Expected Result:**

| driver_id | name       | total_deliveries |
| --------- | ---------- | ---------------- |
| 2         | Jane Doe   | 200              |
| 4         | Emma Green | 180              |
| 3         | Mike Brown | 150              |

This query will return the top 3 drivers with the highest total deliveries. Let me know if you’re ready for the next question or want further explanation on any part!

Let’s move on to a question that involves grouping and aggregating data to analyze overall team performance.

---

### Seventh Question (Difficulty: Medium): Calculating Average On-Time Rate for All Drivers

**Question**: Write an SQL query to calculate the average on-time delivery rate for all drivers combined. The on-time delivery rate should be calculated for each driver individually and then averaged across all drivers.

**Expected Result:**

| avg_on_time_rate |
| ---------------- |
| 92.44            |

Would you like to try this query, or should I provide the solution?
Here’s the SQL query to calculate the average on-time delivery rate across all drivers:

```sql
SELECT
    ROUND(AVG((on_time_deliveries / total_deliveries) * 100), 2) AS avg_on_time_rate
FROM
    drivers;
```

**Expected Result:**

| avg_on_time_rate |
| ---------------- |
| 92.44            |

This query first calculates the on-time delivery rate for each driver, then finds the average of these rates across all drivers, rounding to two decimal places. Let me know if you’re ready for the next question!

Great! Now let’s work on a question that involves more complex filtering to find drivers with performance below a certain threshold.

---

### Eighth Question (Difficulty: Medium): Finding Drivers with Low On-Time Delivery Rate

**Question**: Write an SQL query to find drivers who have an on-time delivery rate below 85%. Display the `driver_id`, `name`, `on_time_deliveries`, `total_deliveries`, and the calculated `on_time_rate`.

**Expected Result:**

| driver_id | name       | on_time_deliveries | total_deliveries | on_time_rate |
| --------- | ---------- | ------------------ | ---------------- | ------------ |
| 4         | Emma Green | 160                | 180              | 88.89        |

Would you like to try this one, or should I go ahead and show the solution?

Here’s the SQL query to find drivers with an on-time delivery rate below 85%:

```sql
SELECT
    driver_id,
    name,
    on_time_deliveries,
    total_deliveries,
    ROUND((on_time_deliveries / total_deliveries) * 100, 2) AS on_time_rate
FROM
    drivers
WHERE
    (on_time_deliveries / total_deliveries) * 100 < 85;
```

**Expected Result:**

| driver_id | name       | on_time_deliveries | total_deliveries | on_time_rate |
| --------- | ---------- | ------------------ | ---------------- | ------------ |
| 4         | Emma Green | 160                | 180              | 88.89        |

This query filters drivers based on an on-time delivery rate below 85%, displaying their performance details. Let me know if you’re ready for the next question!

Let’s move on to a question involving date-based filtering, which is often used to monitor recent performance or activity.

---

### Ninth Question (Difficulty: Medium): Finding Deliveries Completed by Drivers in the Last 6 Months

**Question**: Write an SQL query to retrieve the total number of deliveries completed by drivers who joined within the last 6 months from today's date. Display their `driver_id`, `name`, `join_date`, and `total_deliveries`.

To simplify, assume today’s date is `2024-11-13`.

**Expected Result:**

| driver_id | name       | join_date  | total_deliveries |
| --------- | ---------- | ---------- | ---------------- |
| 3         | Mike Brown | 2023-08-01 | 150              |

Would you like to try this one, or should I go ahead with the solution?

Here’s the SQL query to retrieve the total number of deliveries completed by drivers who joined within the last 6 months, based on an assumed current date of `2024-11-13`:

```sql
SELECT
    driver_id,
    name,
    join_date,
    total_deliveries
FROM
    drivers
WHERE
    join_date >= DATE '2024-11-13' - INTERVAL '6 months';
```

**Expected Result:**

| driver_id | name       | join_date  | total_deliveries |
| --------- | ---------- | ---------- | ---------------- |
| 3         | Mike Brown | 2023-08-01 | 150              |

This query filters drivers based on their join date, selecting those who joined within the last 6 months, and displays their total deliveries. Let me know if you’re ready for the next question!

## ok next

I want also to update the data to have for each driver to be shown before computing total delivery or number of delivery to show you aggregate them
Got it! To clarify, you want to aggregate deliveries for each driver, showing the total number of deliveries or metrics like on-time or late deliveries. This way, you can see how the data is aggregated before computing KPIs or metrics.

To do this, let's assume we have an additional `deliveries` table that tracks each individual delivery for each driver. This will allow us to aggregate delivery data at the driver level.

---

### New Sample Table: `deliveries`

| delivery_id | driver_id | delivery_date | on_time | distance |
| ----------- | --------- | ------------- | ------- | -------- |
| 1           | 1         | 2023-11-01    | TRUE    | 5.2      |
| 2           | 1         | 2023-11-02    | FALSE   | 6.5      |
| 3           | 2         | 2023-11-01    | TRUE    | 3.7      |
| 4           | 2         | 2023-11-03    | TRUE    | 7.0      |
| 5           | 3         | 2023-11-01    | FALSE   | 8.2      |
| ...         | ...       | ...           | ...     | ...      |

Each row in this table represents a single delivery, with columns indicating whether it was on time and the distance covered.

---

### Tenth Question (Difficulty: Medium): Aggregating Deliveries for Each Driver

**Question**: Write an SQL query to calculate the total number of deliveries, on-time deliveries, late deliveries, and total distance covered for each driver. Display the `driver_id`, `total_deliveries`, `on_time_deliveries`, `late_deliveries`, and `total_distance`.

**Expected Result:**

| driver_id | total_deliveries | on_time_deliveries | late_deliveries | total_distance |
| --------- | ---------------- | ------------------ | --------------- | -------------- |
| 1         | 120              | 110                | 10              | 250.5          |
| 2         | 200              | 190                | 10              | 320.0          |
| 3         | 150              | 140                | 10              | 270.8          |
| ...       | ...              | ...                | ...             | ...            |

Would you like to try this one, or should I show the solution?
Here’s the SQL query to aggregate the data for each driver, calculating the total deliveries, on-time deliveries, late deliveries, and total distance covered:

```sql
SELECT
    driver_id,
    COUNT(delivery_id) AS total_deliveries,
    SUM(CASE WHEN on_time = TRUE THEN 1 ELSE 0 END) AS on_time_deliveries,
    SUM(CASE WHEN on_time = FALSE THEN 1 ELSE 0 END) AS late_deliveries,
    SUM(distance) AS total_distance
FROM
    deliveries
GROUP BY
    driver_id;
```

**Expected Result:**

| driver_id | total_deliveries | on_time_deliveries | late_deliveries | total_distance |
| --------- | ---------------- | ------------------ | --------------- | -------------- |
| 1         | 120              | 110                | 10              | 250.5          |
| 2         | 200              | 190                | 10              | 320.0          |
| 3         | 150              | 140                | 10              | 270.8          |
| ...       | ...              | ...                | ...             | ...            |

This query groups deliveries by `driver_id` and aggregates them to get totals for each metric. Let me know if you’d like to move to the next question or need further explanation on any part!

Great! Now let’s move to a question that combines the aggregated data with the drivers' information for a more complete view.

---

### Eleventh Question (Difficulty: Hard): Calculating Performance Metrics for Each Driver Using Aggregated Data

Now that we have the aggregated delivery data, let's calculate KPIs for each driver using a `JOIN` to combine the aggregated data with the driver information from the `drivers` table.

**Question**: Write an SQL query to retrieve each driver's `driver_id`, `name`, `total_deliveries`, `on_time_rate` (percentage of on-time deliveries), `avg_distance_per_delivery`, and `delivery_efficiency` (deliveries per hour worked).

Assume that the aggregated data is stored in a temporary view called `driver_aggregates`.

**Expected Result:**

| driver_id | name       | total_deliveries | on_time_rate | avg_distance_per_delivery | delivery_efficiency |
| --------- | ---------- | ---------------- | ------------ | ------------------------- | ------------------- |
| 1         | John Smith | 120              | 91.67        | 2.09                      | 2.40                |
| 2         | Jane Doe   | 200              | 95.00        | 1.60                      | 3.33                |
| 3         | Mike Brown | 150              | 93.33        | 1.81                      | 2.73                |
| ...       | ...        | ...              | ...          | ...                       | ...                 |

Would you like to try this, or should I provide the solution?
Here’s the SQL query to calculate performance metrics for each driver by joining the `drivers` table with the aggregated data from `driver_aggregates`:

```sql
WITH driver_aggregates AS (
    SELECT
        driver_id,
        COUNT(delivery_id) AS total_deliveries,
        SUM(CASE WHEN on_time = TRUE THEN 1 ELSE 0 END) AS on_time_deliveries,
        SUM(distance) AS total_distance
    FROM
        deliveries
    GROUP BY
        driver_id
)

SELECT
    d.driver_id,
    d.name,
    da.total_deliveries,
    ROUND((da.on_time_deliveries / da.total_deliveries) * 100, 2) AS on_time_rate,
    ROUND((da.total_distance / da.total_deliveries), 2) AS avg_distance_per_delivery,
    ROUND((da.total_deliveries / d.working_hours), 2) AS delivery_efficiency
FROM
    drivers d
JOIN
    driver_aggregates da ON d.driver_id = da.driver_id;
```

**Expected Result:**

| driver_id | name       | total_deliveries | on_time_rate | avg_distance_per_delivery | delivery_efficiency |
| --------- | ---------- | ---------------- | ------------ | ------------------------- | ------------------- |
| 1         | John Smith | 120              | 91.67        | 2.09                      | 2.40                |
| 2         | Jane Doe   | 200              | 95.00        | 1.60                      | 3.33                |
| 3         | Mike Brown | 150              | 93.33        | 1.81                      | 2.73                |
| ...       | ...        | ...              | ...          | ...                       | ...                 |

This query calculates the on-time rate, average distance per delivery, and delivery efficiency for each driver by joining the drivers’ details with the aggregated data. Let me know if you’re ready for the next question or need further clarification!
Yes, the syntax is correct. In SQL, `da` is an alias for the `driver_aggregates` table (or common table expression, CTE). Aliases make queries more readable and reduce typing by allowing you to use a shorter name in place of a full table or CTE name.

In this query:

```sql
driver_aggregates da ON d.driver_id = da.driver_id;
```

- `driver_aggregates` is the CTE we defined.
- `da` is the alias for `driver_aggregates`.
- `d` is the alias for the `drivers` table.

When we write `driver_aggregates da`, it means we’re assigning `da` as an alias for `driver_aggregates`, so instead of repeatedly writing `driver_aggregates`, we can simply use `da`.

Let me know if you’d like any further clarification or if you're ready to move to the next question!

Let's tackle a more complex question that involves calculating a summary statistic across multiple drivers to understand the distribution of performance.

---

### Twelfth Question (Difficulty: Hard): Calculating the Average Delivery Efficiency Across All Drivers

To evaluate overall team performance, it’s common to calculate an average of each driver’s efficiency. This metric shows how productive the drivers are on average in terms of deliveries per hour worked.

**Question**: Write an SQL query to calculate the average delivery efficiency across all drivers. This delivery efficiency for each driver is defined as:

$$
\text{Delivery Efficiency} = \frac{\sum_{k=1}^n \text{total\_deliveries}_k}{\sum_{k=1}^n \text{working\_hours}_k}
$$

The result should show a single value representing the overall average delivery efficiency.

**Expected Result:**

| avg_delivery_efficiency |
| ----------------------- |
| 2.80                    |

Would you like to try this query, or should I go ahead with the solution?
Here’s the SQL query to calculate the average delivery efficiency across all drivers:

```sql
WITH driver_aggregates AS (
    SELECT
        driver_id,
        COUNT(delivery_id) AS total_deliveries
    FROM
        deliveries
    GROUP BY
        driver_id
)

SELECT
    ROUND(AVG(da.total_deliveries / d.working_hours), 2) AS avg_delivery_efficiency
FROM
    drivers d
JOIN
    driver_aggregates da ON d.driver_id = da.driver_id;
```

**Expected Result:**

| avg_delivery_efficiency |
| ----------------------- |
| 2.80                    |

This query first calculates the total deliveries for each driver using the `driver_aggregates` CTE. Then, it joins this CTE with the `drivers` table to compute the delivery efficiency for each driver. Finally, it calculates the average delivery efficiency across all drivers.

Let me know if you're ready for the next question or need further explanation!

Let’s move on to a question that involves using `GROUP BY` with date-based filtering, which is useful for analyzing trends over time.

---

### Thirteenth Question (Difficulty: Hard): Calculating Monthly Delivery Totals for Each Driver

**Question**: Write an SQL query to calculate the total number of deliveries completed by each driver, grouped by month. Display `driver_id`, `month`, and `total_deliveries` for each month.

For the purposes of this question, assume that the `delivery_date` column in the `deliveries` table is in `YYYY-MM-DD` format.

**Expected Result:**

| driver_id | month   | total_deliveries |
| --------- | ------- | ---------------- |
| 1         | 2023-11 | 30               |
| 2         | 2023-11 | 40               |
| 3         | 2023-11 | 25               |
| ...       | ...     | ...              |

Would you like to try this one, or should I provide the solution?
Here’s the SQL query to calculate the total number of deliveries completed by each driver, grouped by month:

```sql
SELECT
    driver_id,
    TO_CHAR(delivery_date, 'YYYY-MM') AS month,
    COUNT(delivery_id) AS total_deliveries
FROM
    deliveries
GROUP BY
    driver_id,
    TO_CHAR(delivery_date, 'YYYY-MM')
ORDER BY
    driver_id,
    month;
```

**Expected Result:**

| driver_id | month   | total_deliveries |
| --------- | ------- | ---------------- |
| 1         | 2023-11 | 30               |
| 2         | 2023-11 | 40               |
| 3         | 2023-11 | 25               |
| ...       | ...     | ...              |

### Explanation:

- `TO_CHAR(delivery_date, 'YYYY-MM')` converts the `delivery_date` into a `YYYY-MM` format to group deliveries by month.
- We then count the number of `delivery_id` entries per driver and month.

This result will show each driver’s monthly delivery totals, ordered by driver ID and month. Let me know if you’d like to move on to the next question!

Let's move on to a question that combines multiple conditions and filtering to identify drivers with consistent high performance over a specified time period.

---

### Fourteenth Question (Difficulty: Very Hard): Finding Drivers with a 100% On-Time Delivery Rate Over the Last Three Months

**Question**: Write an SQL query to identify drivers who achieved a 100% on-time delivery rate for each of the last three months. Display `driver_id`, `name`, and `month`.

To simplify, assume today’s date is `2024-11-13`, so the last three months are August, September, and October of 2024.

**Expected Result:**

| driver_id | name     | month   |
| --------- | -------- | ------- |
| 2         | Jane Doe | 2024-08 |
| 2         | Jane Doe | 2024-09 |
| 2         | Jane Doe | 2024-10 |
| ...       | ...      | ...     |

Would you like to attempt this one, or should I go ahead and provide the solution?
Here’s the SQL query to identify drivers with a 100% on-time delivery rate for each of the last three months (August, September, and October 2024):

```sql
WITH monthly_performance AS (
    SELECT
        driver_id,
        TO_CHAR(delivery_date, 'YYYY-MM') AS month,
        COUNT(delivery_id) AS total_deliveries,
        SUM(CASE WHEN on_time = TRUE THEN 1 ELSE 0 END) AS on_time_deliveries
    FROM
        deliveries
    WHERE
        delivery_date >= DATE '2024-08-01'
        AND delivery_date < DATE '2024-11-01'
    GROUP BY
        driver_id,
        TO_CHAR(delivery_date, 'YYYY-MM')
)

SELECT
    d.driver_id,
    d.name,
    mp.month
FROM
    monthly_performance mp
JOIN
    drivers d ON mp.driver_id = d.driver_id
WHERE
    mp.total_deliveries = mp.on_time_deliveries
ORDER BY
    d.driver_id,
    mp.month;
```

**Explanation:**

1. The `monthly_performance` CTE calculates the total and on-time deliveries for each driver by month.
2. In the main query, we filter to include only months where the total deliveries match the on-time deliveries, indicating a 100% on-time rate.
3. The `WHERE` clause limits results to the last three months (August, September, and October 2024).

**Expected Result:**

| driver_id | name     | month   |
| --------- | -------- | ------- |
| 2         | Jane Doe | 2024-08 |
| 2         | Jane Doe | 2024-09 |
| 2         | Jane Doe | 2024-10 |
| ...       | ...      | ...     |

This result shows drivers who achieved a 100% on-time rate for each of the last three months. Let me know if you’d like another question or more details on this query!

Let’s move on to a challenging question that requires calculating a rolling average to track drivers’ recent performance trends.

---

### Fifteenth Question (Difficulty: Very Hard): Calculating a 7-Day Rolling Average of On-Time Delivery Rate for Each Driver

**Question**: Write an SQL query to calculate a 7-day rolling average of the on-time delivery rate for each driver. The on-time delivery rate should be calculated as the percentage of deliveries made on time out of the total deliveries in the past 7 days.

The output should include `driver_id`, `date`, and `rolling_on_time_rate`, where `rolling_on_time_rate` represents the 7-day rolling average of on-time delivery rates.

**Expected Result:**

| driver_id | date       | rolling_on_time_rate |
| --------- | ---------- | -------------------- |
| 1         | 2023-11-01 | 93.33                |
| 1         | 2023-11-02 | 92.00                |
| 2         | 2023-11-01 | 95.00                |
| ...       | ...        | ...                  |

Would you like to try tackling this one, or should I go ahead and provide the solution?

Calculating a 7-day rolling average of on-time delivery rates can be complex, especially without built-in window functions in some SQL databases. However, assuming we are working with a database that supports window functions (such as PostgreSQL), here’s how you could accomplish this:

```sql
SELECT
    driver_id,
    delivery_date AS date,
    ROUND(
        AVG(CASE WHEN on_time = TRUE THEN 100.0 ELSE 0 END)
        OVER (PARTITION BY driver_id ORDER BY delivery_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW),
        2
    ) AS rolling_on_time_rate
FROM
    deliveries
ORDER BY
    driver_id,
    date;
```

**Explanation:**

1. The `CASE` statement assigns `100.0` for on-time deliveries and `0` for late deliveries, essentially converting on-time deliveries into percentages.
2. The `AVG()` function, combined with the `OVER` clause, calculates the 7-day rolling average by partitioning data by `driver_id` and ordering by `delivery_date`.
3. The `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` clause defines a 7-day window, starting 6 days before each row up to the current day.

**Expected Result:**

| driver_id | date       | rolling_on_time_rate |
| --------- | ---------- | -------------------- |
| 1         | 2023-11-01 | 93.33                |
| 1         | 2023-11-02 | 92.00                |
| 2         | 2023-11-01 | 95.00                |
| ...       | ...        | ...                  |

This query gives a 7-day rolling on-time delivery rate for each driver, showing daily fluctuations and helping track recent performance trends. Let me know if you're ready for the next question!

---

Let's move to a question that involves identifying outliers in driver performance, which is useful for spotting exceptionally high or low productivity.

---

### Sixteenth Question (Difficulty: Very Hard): Identifying Drivers with Exceptional Delivery Efficiency

**Question**: Write an SQL query to identify drivers whose delivery efficiency is either significantly higher or lower than the average. Assume "significantly" means more than 1.5 standard deviations away from the average delivery efficiency.

Display the `driver_id`, `name`, `delivery_efficiency`, and whether they are classified as "High Performer" or "Low Performer."

**Expected Result:**

| driver_id | name       | delivery_efficiency | performance_classification |
| --------- | ---------- | ------------------- | -------------------------- |
| 2         | Jane Doe   | 3.33                | High Performer             |
| 4         | Emma Green | 1.90                | Low Performer              |
| ...       | ...        | ...                 | ...                        |

Would you like to attempt this, or should I show the solution?

Here’s the SQL query to identify drivers whose delivery efficiency is more than 1.5 standard deviations away from the average. This query assumes your database supports common aggregate functions like `AVG()` and `STDDEV()`.

```sql
WITH efficiency_stats AS (
    SELECT
        AVG(total_deliveries / working_hours) AS avg_efficiency,
        STDDEV(total_deliveries / working_hours) AS stddev_efficiency
    FROM
        drivers
),
driver_efficiency AS (
    SELECT
        driver_id,
        name,
        ROUND(total_deliveries / working_hours, 2) AS delivery_efficiency
    FROM
        drivers
)

SELECT
    de.driver_id,
    de.name,
    de.delivery_efficiency,
    CASE
        WHEN de.delivery_efficiency > es.avg_efficiency + 1.5 * es.stddev_efficiency THEN 'High Performer'
        WHEN de.delivery_efficiency < es.avg_efficiency - 1.5 * es.stddev_efficiency THEN 'Low Performer'
        ELSE 'Average Performer'
    END AS performance_classification
FROM
    driver_efficiency de
CROSS JOIN
    efficiency_stats es
ORDER BY
    de.delivery_efficiency DESC;
```

**Explanation:**

1. **`efficiency_stats` CTE**: Calculates the average delivery efficiency and its standard deviation across all drivers.
2. **`driver_efficiency` CTE**: Calculates each driver’s delivery efficiency by dividing their total deliveries by working hours.
3. **Main Query**: Joins each driver’s efficiency with the overall stats and classifies them as a "High Performer" or "Low Performer" if their efficiency is more than 1.5 standard deviations above or below the average.

**Expected Result:**

| driver_id | name       | delivery_efficiency | performance_classification |
| --------- | ---------- | ------------------- | -------------------------- |
| 2         | Jane Doe   | 3.33                | High Performer             |
| 4         | Emma Green | 1.90                | Low Performer              |
| ...       | ...        | ...                 | ...                        |

This query helps identify drivers whose performance deviates significantly from the average, marking them as outliers. Let me know if you’re ready for the next question!

Let's move on to a challenging question that involves calculating the **retention rate** of drivers over time, which is essential for analyzing workforce stability.

---

### Seventeenth Question (Difficulty: Very Hard): Calculating Monthly Driver Retention Rate

**Question**: Write an SQL query to calculate the monthly retention rate of drivers. Retention rate is defined as the percentage of drivers who were active (i.e., made at least one delivery) in a given month and also made deliveries in the following month.

Display `month`, `active_drivers`, `retained_drivers`, and `retention_rate`.

**Expected Result:**

| month   | active_drivers | retained_drivers | retention_rate |
| ------- | -------------- | ---------------- | -------------- |
| 2023-09 | 25             | 20               | 80.00          |
| 2023-10 | 28             | 24               | 85.71          |
| ...     | ...            | ...              | ...            |

Would you like to attempt this, or should I provide the solution?

To calculate the monthly retention rate, we can use a self-join on the `deliveries` table, assuming that drivers with at least one delivery in each month are considered active.

Here’s the SQL query:

```sql
WITH monthly_active_drivers AS (
    SELECT
        driver_id,
        TO_CHAR(delivery_date, 'YYYY-MM') AS month
    FROM
        deliveries
    GROUP BY
        driver_id,
        TO_CHAR(delivery_date, 'YYYY-MM')
)

SELECT
    mad1.month AS month,
    COUNT(DISTINCT mad1.driver_id) AS active_drivers,
    COUNT(DISTINCT mad2.driver_id) AS retained_drivers,
    ROUND(
        (COUNT(DISTINCT mad2.driver_id) * 100.0) / NULLIF(COUNT(DISTINCT mad1.driver_id), 0),
        2
    ) AS retention_rate
FROM
    monthly_active_drivers mad1
LEFT JOIN
    monthly_active_drivers mad2
    ON mad1.driver_id = mad2.driver_id
    AND mad2.month = TO_CHAR(TO_DATE(mad1.month || '-01', 'YYYY-MM-DD') + INTERVAL '1 month', 'YYYY-MM')
GROUP BY
    mad1.month
ORDER BY
    mad1.month;
```

**Explanation:**

1. **`monthly_active_drivers` CTE**: Identifies the distinct months each driver was active (made at least one delivery).
2. **Self-Join**: Joins each month with the following month to count retained drivers (drivers active in both the current and the next month).
3. **Calculations**:
   - `active_drivers`: Total distinct drivers in each month.
   - `retained_drivers`: Count of drivers who are active in both the current and following month.
   - `retention_rate`: Percentage of retained drivers calculated as `(retained_drivers / active_drivers) * 100`, rounded to two decimal places.

**Expected Result:**

| month   | active_drivers | retained_drivers | retention_rate |
| ------- | -------------- | ---------------- | -------------- |
| 2023-09 | 25             | 20               | 80.00          |
| 2023-10 | 28             | 24               | 85.71          |
| ...     | ...            | ...              | ...            |

This query provides the retention rate for each month by comparing active drivers in consecutive months. Let me know if you’re ready for another question or need further clarification!

Let's move on to another complex question that focuses on tracking the consistency of drivers’ performance over a period.

---

### Eighteenth Question (Difficulty: Very Hard): Identifying Drivers with Consistent High On-Time Delivery Rate Over the Last 6 Months

**Question**: Write an SQL query to identify drivers who maintained an on-time delivery rate of at least 90% for each of the last 6 months. Display `driver_id`, `name`, and each month’s `on_time_rate`.

Assume today's date is `2024-11-13`, so the last 6 months would be from May to October 2024.

**Expected Result:**

| driver_id | name     | month   | on_time_rate |
| --------- | -------- | ------- | ------------ |
| 2         | Jane Doe | 2024-05 | 92.00        |
| 2         | Jane Doe | 2024-06 | 95.00        |
| 2         | Jane Doe | 2024-07 | 91.00        |
| 2         | Jane Doe | 2024-08 | 94.50        |
| 2         | Jane Doe | 2024-09 | 90.33        |
| 2         | Jane Doe | 2024-10 | 93.20        |

Would you like to attempt this, or should I go ahead with the solution?
Here’s the SQL query to identify drivers who maintained an on-time delivery rate of at least 90% for each of the last 6 months (from May to October 2024):

```sql
WITH monthly_on_time_rates AS (
    SELECT
        driver_id,
        TO_CHAR(delivery_date, 'YYYY-MM') AS month,
        ROUND(
            (SUM(CASE WHEN on_time = TRUE THEN 1 ELSE 0 END) * 100.0) / COUNT(delivery_id),
            2
        ) AS on_time_rate
    FROM
        deliveries
    WHERE
        delivery_date >= DATE '2024-05-01'
        AND delivery_date < DATE '2024-11-01'
    GROUP BY
        driver_id,
        TO_CHAR(delivery_date, 'YYYY-MM')
),
consistent_drivers AS (
    SELECT
        driver_id
    FROM
        monthly_on_time_rates
    WHERE
        on_time_rate >= 90
    GROUP BY
        driver_id
    HAVING
        COUNT(DISTINCT month) = 6
)

SELECT
    cd.driver_id,
    d.name,
    mor.month,
    mor.on_time_rate
FROM
    consistent_drivers cd
JOIN
    monthly_on_time_rates mor ON cd.driver_id = mor.driver_id
JOIN
    drivers d ON d.driver_id = cd.driver_id
ORDER BY
    cd.driver_id,
    mor.month;
```

### Explanation:

1. **`monthly_on_time_rates` CTE**: Calculates the on-time delivery rate for each driver by month from May to October 2024.
2. **`consistent_drivers` CTE**: Filters drivers who have maintained an on-time rate of at least 90% in each of the past 6 months by counting distinct months where the rate is 90% or higher.
3. **Main Query**: Joins the `consistent_drivers` CTE with `monthly_on_time_rates` and `drivers` tables to retrieve driver details and monthly on-time rates for each qualifying driver.

### Expected Result:

| driver_id | name     | month   | on_time_rate |
| --------- | -------- | ------- | ------------ |
| 2         | Jane Doe | 2024-05 | 92.00        |
| 2         | Jane Doe | 2024-06 | 95.00        |
| 2         | Jane Doe | 2024-07 | 91.00        |
| 2         | Jane Doe | 2024-08 | 94.50        |
| 2         | Jane Doe | 2024-09 | 90.33        |
| 2         | Jane Doe | 2024-10 | 93.20        |

This result shows drivers with consistent high on-time performance over the past 6 months. Let me know if you’re ready for another question or need more details on this query!

Let's proceed with a question that combines complex grouping and ranking functions, often useful for identifying top performers across a time period.

---

### Nineteenth Question (Difficulty: Very Hard): Ranking Drivers Based on Total Deliveries Over the Last 3 Months

**Question**: Write an SQL query to rank drivers based on the total number of deliveries they completed over the last 3 months (August, September, and October 2024). Display `driver_id`, `name`, `month`, `total_deliveries`, and the driver’s rank within each month based on the total deliveries.

**Expected Result:**

| driver_id | name       | month   | total_deliveries | monthly_rank |
| --------- | ---------- | ------- | ---------------- | ------------ |
| 2         | Jane Doe   | 2024-08 | 50               | 1            |
| 3         | Mike Brown | 2024-08 | 45               | 2            |
| 1         | John Smith | 2024-08 | 30               | 3            |
| 2         | Jane Doe   | 2024-09 | 55               | 1            |
| ...       | ...        | ...     | ...              | ...          |

Would you like to try this one, or should I provide the solution?

Here’s the SQL query to rank drivers based on their total deliveries for each
month over the last 3 months (August, September, and October 2024):

```sql
WITH monthly_deliveries AS (
    SELECT
        driver_id,
        TO_CHAR(delivery_date, 'YYYY-MM') AS month,
        COUNT(delivery_id) AS total_deliveries
    FROM
        deliveries
    WHERE
        delivery_date >= DATE '2024-08-01'
        AND delivery_date < DATE '2024-11-01'
    GROUP BY
        driver_id,
        TO_CHAR(delivery_date, 'YYYY-MM')
)

SELECT
    md.driver_id,
    d.name,
    md.month,
    md.total_deliveries,
    RANK() OVER (PARTITION BY md.month ORDER BY md.total_deliveries DESC) AS monthly_rank
FROM
    monthly_deliveries md
JOIN
    drivers d ON md.driver_id = d.driver_id
ORDER BY
    md.month,
    monthly_rank;
```

### Explanation:

1. **`monthly_deliveries` CTE**: This part groups deliveries by driver and month
   to calculate the `total_deliveries` for each driver in each of the last three
   months (August, September, October 2024).
2. **Main Query**:
   - Joins `monthly_deliveries` with `drivers` to get driver names.
   - Uses the `RANK()` window function with `PARTITION BY md.month ORDER BY
     md.total_deliveries DESC` to rank drivers within each month by total
     deliveries, with the highest delivery count ranked as 1.

### Expected Result:

| driver_id | name       | month   | total_deliveries | monthly_rank |
| --------- | ---------- | ------- | ---------------- | ------------ |
| 2         | Jane Doe   | 2024-08 | 50               | 1            |
| 3         | Mike Brown | 2024-08 | 45               | 2            |
| 1         | John Smith | 2024-08 | 30               | 3            |
| 2         | Jane Doe   | 2024-09 | 55               | 1            |
| ...       | ...        | ...     | ...              | ...          |

This result shows the ranking of drivers based on their delivery count for each
month, making it easy to see who the top performers were. Let me know if you’re
ready for the next question!



