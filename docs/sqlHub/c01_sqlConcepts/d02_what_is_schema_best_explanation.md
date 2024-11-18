# What is a schema in PostgreSQL?

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->

**Table of Contents**

- [What is a chema in PostgreSQL?](#what-is-a-chema-in-postgresql)
  - [Concept in Depth ](#concept-in-depth)
  - [The purpose of a schema](#the-purpose-of-a-schema)
    - [Schemas group tables](#schemas-group-tables)
  - [Schemas and PostgreSQL](#schemas-and-postgresql)
    - [Using the “public” schema](#using-the-public-schema)
  - [Basically, there are two ways to query the table.](#basically-there-are-two-ways-to-query-the-table)
  - [Another method to query the table](#another-method-to-query-the-table)
  - [Creating schemas](#creating-schemas)
  - [Views and schemas](#views-and-schemas)
  - [Dropping schemas](#dropping-schemas)
  - [Schema dependencies](#schema-dependencies)
  - [Finally …](#finally-)
  - [References](#references)

<!-- markdown-toc end -->

## Concept in Depth

By `Hans-Jürgen Schönig`

- 06.2023 / Category: How To / Tags: development | under the hood
  One way to organize data in PostgreSQL is to make use of schemas. What is a
  schema in PostgreSQL? And more importantly: What is the purpose of a schema and
  how can schemas be used to make your life easier? Let's dive in and find out.

## The purpose of a schema

Before you figure out how to use schemas, you need to know what the purpose of a
schema is in the first place. To understand that, first take a look at how
PostgreSQL is structured:

- Instance
- Database
- Schema
- Table
- Row

An `instance` is basically what you start when you deploy PostgreSQL. The next
layer is a database. In reality this is what you connect to: in PostgreSQL a
connection is always bound to a database inside an instance, which happens early
on, right after user authentication. What is important is the next layer down,
between databases and tables: Schemas.

### Schemas group tables

Basically, schemas are a way to group tables together. Let's assume there's a
fairly large data structure: Having 500 tables in one place is certainly harder
to manage and understand than to have 10 buckets containing 50 tables each. It's
simply like organizing pictures: You wouldn't put all of them into the same
folder, but rather group them by year, location, etc. The same logic can be
applied to tables.

## Schemas and PostgreSQL

Now we can focus on how this concept can be applied to PostgreSQL. The first
thing we have to look at is the public schema.

### Using the “public” schema

The beauty of PostgreSQL is that it doesn't matter much if you know nothing at
all about schemas. The reason is the existence of the public schema, which is
there by default. How can we find out which schemas there are in PostgreSQL?
psql provides the dn command to display this information:

```sql
demo=# dn
      List of schemas
  Name  |       Owner
--------+-------------------
 public | pg_database_owner
(1 row)
```

In a default scenario, a table will end up in the public schema. Here's an example:

```sql
demo=# CREATE TABLE t_product (
id 		serial,
name 	text,
price 	numeric
);
CREATE TABLE
```

This is a basic table. The table can be found in the desired schema. d will reveal the truth:

```sql
demo=# d
              List of relations
 Schema |       Name       |   Type   | Owner
--------+------------------+----------+-------
 public | t_product        | table    | hs
 public | t_product_id_seq | sequence | hs
(2 rows)
```

In this case, both the schema and the sequence are found in the default schema
as expected. As you can see, you don't need any knowledge about schemas to
proceed. If you happen to use the public schema, we also recommend checking out
the new security policy introduced in recent versions of PostgreSQL.

## Basically, there are two ways to query the table.

The first method is:

```sql
demo=# SELECT \* FROM t_product;
id | name | price
----+------+-------
(0 rows)
```

## Another method to query the table

However, you can also explicitly use the schema name as a prefix to the table
name, which constitutes a fully qualified name. I've seen a couple of ORM's do
exactly that-- in order to reduce the risk of accessing the wrong table due to
misconfiguration. We'll also see it later in this post:

```sql
demo=# SELECT \* FROM public.t_product;
id | name | price
----+------+-------
(0 rows)
```

After this brief introduction to the public schema, we can move forward and create our first new schema.

## Creating schemas

How can we create a schema in PostgreSQL? The CREATE SCHEMA command is the answer:

```sql
demo=# h CREATE SCHEMA
Command: CREATE SCHEMA
Description: define a new schema
Syntax:
CREATE SCHEMA schema_name
[ AUTHORIZATION role_specification ]
[ schema_element [ ... ] ]
CREATE SCHEMA AUTHORIZATION role_specification
[ schema_element [ ... ] ]
CREATE SCHEMA IF NOT EXISTS schema_name
[ AUTHORIZATION role_specification ]
CREATE SCHEMA IF NOT EXISTS AUTHORIZATION role_specification

where role_specification can be:

    user_name

| CURRENT_ROLE
| CURRENT_USER
| SESSION_USER

URL: https://www.postgresql.org/docs/15/sql-createschema.html
```

The syntax is quite easy and allows us to define a name as well as the schema
owner. Otherwise, everything is really straightforward:

```sql
demo=# CREATE SCHEMA warehouse;
CREATE SCHEMA
```

Once the schema has been created, we can create a table inside the schema:

```sql
demo=# CREATE TABLE warehouse.t_product (
prod_number text PRIMARY KEY,
d date,
in_stock int
);
CREATE TABLE
```

By using a schema name as a prefix to the table name, you can define the schema
you want to use. Mind that the schema itself does NOT impact the way data is
stored. The data files associated with our table are still in the same
PostgreSQL data directory. Therefore schemas do not impact performance and are
not about storage optimization. The purpose of a schema is simply to group
things together and to help organize a solid security policy by assigning
permissions to schemas:

```sql
demo=# d warehouse.t_product;
              Table 'warehouse.t_product'
   Column    |  Type   | Collation | Nullable | Default
-------------+---------+-----------+----------+---------
 prod_number | text    |           | not null |
 d           | date    |           |          |
 in_stock    | integer |           |          |
Indexes:
    't_product_pkey' PRIMARY KEY, btree (prod_number)
```

There are two things worth pointing out here: First of all, it is possible to
have two tables with the same name in two different schemas. There is a
public.t_product and a warehouse.t_product table. This is perfectly possible and
actually quite common. The second important aspect is that we don’t have to
prefix the table in the public schema. The reason is the following parameter:

```sql
demo=# SHOW search_path;
search_path
```

---

```sql
'$user', public
(1 row)
```

Everything that is to be found in the search_path can be accessed directly
without explicitly providing the name of the schema. We can easily try this out:

```sql
demo=# SET search_path TO warehouse;
SET
```

Note that the parameter is only changed in your session - it does not break your
production system if you are running this in your interactive session.

From now on, the second table called t_product will be displayed, because
PostgreSQL knows in which schema to look:

```sql
demo=# d t_product
              Table 'warehouse.t_product'
   Column    |  Type   | Collation | Nullable | Default
-------------+---------+-----------+----------+---------
 prod_number | text    |           | not null |
 d           | date    |           |          |
 in_stock    | integer |           |          |
Indexes:
    't_product_pkey' PRIMARY KEY, btree (prod_number)
```

Now that the search_path has been changed, we have to prefix the public schema, as it is not in the path any more:

```sql
demo=# d public.t_product
                                Table 'public.t_product'
 Column |  Type   | Collation | Nullable |                   Default
--------+---------+-----------+----------+-----------------...
 id     | integer |           | not null | …
 name   | text    |           |          |
 price  | numeric |           |          |
```

After this basic introduction to schemas, let's figure out what it means to use schemas in combination with views:

## Views and schemas

A view is a good way to allow developers easier access to data. The important
point is that schemas are not normally a barrier (For the nitty-gritty details
about views and permissions, see here). A query can freely join tables from
different schemas, and the view using the query can expose the data in a schema
of your choice (assuming you have the permissions to do that):

```sql
demo=# SET search_path TO default;
SET
demo=# CREATE VIEW public.v AS
SELECT \*
FROM warehouse.t_product ;
CREATE VIEW
```

However, there are implications for people who want to migrate from Oracle to PostgreSQL.

**Hint\***: Check out the CYBERTEC Migrator

Renaming schemas in PostgreSQL
In PostgreSQL, everything that can be created can also be renamed. The same is true for schemas:

```sql
demo=# h ALTER SCHEMA
Command: ALTER SCHEMA
Description: change the definition of a schema
Syntax:
ALTER SCHEMA name RENAME TO new_name
ALTER SCHEMA name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
```

URL: https://www.postgresql.org/docs/15/sql-alterschema.html
Renaming a schema causes repercussions which are outlined in the next listing. Mind what happened to the view:

```sql
demo=# ALTER SCHEMA warehouse RENAME TO inventory;
ALTER SCHEMA
demo=# d+ v
                                 View 'public.v'
   Column    |  Type   | Collation | Nullable | Default | Storage  | …
-------------+---------+-----------+----------+---------+----------+ …
 prod_number | text    |           |          |         | extended |
 d           | date    |           |          |         | plain    |
 in_stock    | integer |           |          |         | plain    |
View definition:
 SELECT t_product.prod_number,
    t_product.d,
    t_product.in_stock
   FROM inventory.t_product;
```

The view does not reference tables directly - it references internal object IDs, which is really important here, because renaming the schema only means attaching a different text label to an internal ID. The actual view definition does not depend on names, so renaming objects does render a view invalid. By contrast, in databases such as Oracle, renaming objects can leave a view in an invalid state.

## Dropping schemas

Dropping schemas in PostgreSQL follows the same logic:

```sql
demo=# h DROP SCHEMA
Command:     DROP SCHEMA
Description: remove a schema
Syntax:
DROP SCHEMA [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]

```

URL: https://www.postgresql.org/docs/15/sql-dropschema.html

## Schema dependencies

We don't want to orphan objects, so we can't just drop them without collateral
damage. PostgreSQL will tell us exactly what would happen, but not really drop
the table - in order to avoid breaking the dependencies on the schema:

```sql
demo=# DROP SCHEMA inventory;
ERROR: cannot drop schema inventory because other objects depend on it
DETAIL: table inventory.t_product depends on schema inventory
view v depends on table inventory.t_product
HINT: Use DROP ... CASCADE to drop the dependent objects too.
```

In case we really want to drop the schema and face all the consequences
associated with it, the CASCADE option can be added:

```sql
demo=# DROP SCHEMA inventory CASCADE;
NOTICE: drop cascades to 2 other objects
DETAIL: drop cascades to table inventory.t_product
drop cascades to view v
DROP SCHEMA
```

As you can see, all dependent objects have been dropped and we're left with a
clean, consistent database which doesn't contain any stale or invalid objects.
For more info, see Laurenz Albe's blog on view dependencies.

## Finally …

Even if you're not aware of it, schemas are always part of the game; they offer
a good way to organize data more clearly, in a way that is easier to understand.
See this blog about ALTER DEFAULT PRIVILEGES for more info on how to allow other
users access to objects in a particular schema.

If you are interested in other PostgreSQL-related topics, we recommend you check
out Ants Aasma's blog post about “Faceting Large Result Sets in PostgreSQL”.

## References

- [What is a chema in PostgreSQL](https://www.cybertec-postgresql.com/en/what-is-a-schema-in-postgresql/)

