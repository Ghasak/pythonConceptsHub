# About PostgresSQl
<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [About PostgresSQl](#about-postgressql)
    - [Requirements](#requirements)
    - [Running a PostgresSQl in Terminal](#running-a-postgressql-in-terminal)
        - [Step 1: Run PostgreSQL in a Docker Container](#step-1-run-postgresql-in-a-docker-container)
        - [Step 2: Access PostgreSQL in the Docker Container](#step-2-access-postgresql-in-the-docker-container)
            - [Accessing with `psql` in Docker](#accessing-with-psql-in-docker)
            - [Accessing with a Client (e.g., DBeaver)](#accessing-with-a-client-eg-dbeaver)
    - [What is the URL commmand for running](#what-is-the-url-commmand-for-running)
        - [PostgreSQL Connection URL](#postgresql-connection-url)
        - [Example with Your Details](#example-with-your-details)
        - [Breaking Down the URL Components](#breaking-down-the-url-components)
    - [PostreSql database](#postresql-database)

<!-- markdown-toc end -->

## Requirements

Let's begin with PostgreSQL after REGRESS.

- Provide me with a Docker command to run a PostgreSQL container using Docker.
- Then, teach me how to access it and
- Provide both a username and password as well as specifying the port number.
- The database should be stored in a directory called databases within the root
  directory of my project located at /.
- Also provide a method to connect to it using clients such as Beaver or any other
  preferred tool.
- I am currently running on an Apple Silicon (M1) chip-based MacOS device.

## Running a PostgresSQl in Terminal

Here’s how you can set up a PostgreSQL container with Docker on your macOS M1
ARM-based system, storing the database files in the `databases/` directory at
the root of your project.

### Step 1: Run PostgreSQL in a Docker Container

First, create the `databases/` directory in your project root if it doesn't exist.

Then, use this command to start the PostgreSQL container:

```bash
docker run -d \
  --name my_postgres_container \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=mydatabase \
  -v $(pwd)/databases:/var/lib/postgresql/data \
  -p 5432:5432 \
  --platform linux/arm64 \
  postgres
```

Here’s what each flag means:

- `-d`: Run the container in detached mode.
- `--name my_postgres_container`: Names the container for easy reference.
- `-e POSTGRES_USER=myuser`: Sets the PostgreSQL username to `myuser`.
- `-e POSTGRES_PASSWORD=mypassword`: Sets the password to `mypassword`.
- `-e POSTGRES_DB=mydatabase`: Initializes the database `mydatabase`.
- `-v $(pwd)/databases:/var/lib/postgresql/data`: Mounts the `databases/`
  directory to store data persistently.
- `-p 5432:5432`: Exposes PostgreSQL on port 5432.
- `--platform linux/arm64`: Specifies the ARM platform for M1 compatibility.

- Or using docker-compose as well

```yml
services:
  postgres:
    image: postgres:latest
    port:
      - 5555:5432
    environment:
      - POSTRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
```

### Step 2: Access PostgreSQL in the Docker Container

To access PostgreSQL within the container, you can use `psql`, the PostgreSQL command-line tool, or a GUI client.

#### Accessing with `psql` in Docker

Run this command to access `psql` directly:

```bash
docker exec -it my_postgres_container psql -U myuser -d mydatabase
```

#### Accessing with a Client (e.g., DBeaver)

1. **Download and Install [DBeaver](https://dbeaver.io/)** if you haven't already.
2. **Set up a New Connection** in DBeaver:
   - **Host**: `localhost`
   - **Port**: `5432`
   - **Database**: `mydatabase`
   - **Username**: `myuser`
   - **Password**: `mypassword`

This setup will allow DBeaver (or any other PostgreSQL client) to connect to
your PostgreSQL container. You should now be able to work with your PostgreSQL
database through DBeaver or any other preferred client tool.

## What is the URL commmand for running

For PostgreSQL, the connection URL format is slightly different from SQLite.
Here’s the general format and how you’d set it up with your specific details:

### PostgreSQL Connection URL

The PostgreSQL connection URL format is:

```sh
postgresql://username:password@host:port/database
```

### Example with Your Details

Based on the setup provided, your connection URL would be:

```sh
postgresql://myuser:mypassword@localhost:5432/mydatabase
```

### Breaking Down the URL Components

- **myuser**: Your PostgreSQL username (`POSTGRES_USER`).
- **mypassword**: The password for the user (`POSTGRES_PASSWORD`).
- **localhost**: The hostname where the PostgreSQL server is running (in this
  case, your local machine, as it’s running in Docker with port forwarding).
- **5432**: The port on which PostgreSQL is exposed.
- **mydatabase**: The name of the initial database created (`POSTGRES_DB`).

This URL can be used in clients like SQLAlchemy, DBeaver, or any other
PostgreSQL-compatible tool for connecting to your PostgreSQL instance.

## PostreSql database

To connect to your PostgreSQL database using **Dadbod** in Neovim, you can use
the connection URL format directly within Neovim. Here’s how:

1. **Format the Connection URL** in the style Dadbod expects:

   ```sh
   db postgres://myuser:mypassword@localhost:5432/mydatabase
   ```

2. **Open Neovim** and use the command to connect:

   ```vim
   :DB postgres://myuser:mypassword@localhost:5432/mydatabase

   ```

   if you run on another port with extra feature

   ```vim
   :DB postgres://user:pass@localhost:5555/mydb?sslmode=disable
   ```

   Dadbod should now connect to your PostgreSQL database. You’ll be able to
   query your database directly within Neovim.

3. **Optional**: To make this connection reusable or faster to access, you can
   add a custom alias in your Neovim configuration:

   ```vim
   let g:db#url = 'postgres://myuser:mypassword@localhost:5432/mydatabase'
   ```

   Then, you can simply use `:DB g:db#url` in Neovim for quick access.

This setup allows you to work directly within Neovim, taking advantage of
Dadbod for your PostgreSQL database interactions.
