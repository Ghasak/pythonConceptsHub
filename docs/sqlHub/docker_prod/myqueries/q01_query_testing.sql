CREATE TABLE employee (
  id SERIAL8 PRIMARY KEY,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  age INT8,
  gender VARCHAR(10),
  salary DECIMAL(10, 2)
);

SELECT
  *
FROM
  employee
LIMIT
  20;
