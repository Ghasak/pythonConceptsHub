# SQLITE3 IN TERMINAL
<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [SQLITE3 IN TERMINAL](#sqlite3-in-terminal)
    - [-](#-)
    - [Enhance sqlite3 in Terminal](#enhance-sqlite3-in-terminal)
    - [USEFUL UTILITIES](#useful-utilities)

<!-- markdown-toc end -->

For fast checking the help file of `sqlite3` you can use

```sh
echo .help | sqlite3 2>&1 | fzf
```

### In Terminal

Let's dive into SQLite using command-line commands. First, ensure SQLite is
installed. You can check by typing `sqlite3` in the terminal. If it's not
installed, you can usually add it with:

```bash
sudo apt-get install sqlite3      # for Ubuntu/Debian
brew install sqlite               # for macOS with Homebrew
```

Once SQLite is ready, follow these steps:

1. **Open the SQLite command-line interface** by typing:

   ```bash
   sqlite3
   ```

2. **Create a new database** (or open one if it exists) with the `.open` command:

   ```sql
   .open employee_database.db
   ```

3. **Create the `employee` table**:

   ```sql
   CREATE TABLE employee (
       id INTEGER PRIMARY KEY,
       first_name TEXT,
       last_name TEXT,
       timestamp DATE,
       age INTEGER,
       salary REAL
   );
   ```

4. **Insert sample data** one by one. Here are five sample entries:

   ```sql
   INSERT INTO employee (id, first_name, last_name, timestamp, age, salary)
   VALUES (1, 'Alice', 'Johnson', '2024-11-01', 28, 55000.00);

   INSERT INTO employee (id, first_name, last_name, timestamp, age, salary)
   VALUES (2, 'Bob', 'Smith', '2024-11-02', 32, 62000.00);

   INSERT INTO employee (id, first_name, last_name, timestamp, age, salary)
   VALUES (3, 'Charlie', 'Brown', '2024-11-03', 45, 75000.00);

   INSERT INTO employee (id, first_name, last_name, timestamp, age, salary)
   VALUES (4, 'Diana', 'Green', '2024-11-04', 29, 58000.00);

   INSERT INTO employee (id, first_name, last_name, timestamp, age, salary)
   VALUES (5, 'Ethan', 'White', '2024-11-05', 40, 67000.00);
   ```

5. **Verify the data** by querying the table:

   ```sql
   SELECT * FROM employee;
   ```

This will display all records from the `employee` table. Let me know if you encounter any issues!

6. Use (;) always to end your query, and to close the session use `.exit` or `.quit`.

## Enhance sqlite3 in Terminal

To display SQLite table data with enhanced readability in your macOS Terminal,
you can use the `sqlite-utils` command-line tool, which offers colorized and
well-formatted output. Here's how to set it up:

**1. Install `sqlite-utils`:**

First, ensure you have Python and `pip` installed on your system. Then, install
`sqlite-utils` using `pip`:

```bash
pip install sqlite-utils
```

**2. Use `sqlite-utils` to Query and Display Data:**

With `sqlite-utils` installed, you can query your SQLite database and display
the results in a colorized, tabular format. For example:

```bash
sqlite-utils rows your_database.db your_table_name
```

Replace `your_database.db` with the path to your SQLite database file and
`your_table_name` with the name of the table you wish to view.

**3. Alternative: Use `sqlite3` with `.mode column`:**

If you prefer to use the built-in `sqlite3` command-line tool, you can set the
output mode to `column` for a more readable display:

```bash
sqlite3 your_database.db
sqlite> .mode column
sqlite> SELECT * FROM your_table_name;
```

This will format the output in aligned columns, improving readability.

**Note:** While the `sqlite3` tool doesn't natively support colorized output,
using the `column` mode enhances the clarity of the displayed data.

By utilizing `sqlite-utils` or configuring `sqlite3` appropriately, you can
achieve a more readable and organized display of your SQLite table data in the
macOS Terminal.

## USEFUL UTILITIES

To display SQLite table data with enhanced readability and colorized output in
your macOS Terminal, you can utilize Rust-based command-line tools. One such
tool is `qsv`, a fast CSV data-wrangling toolkit written in Rust.

**1. Install `qsv`:**

First, ensure you have Rust installed on your system. Then, you can install `qsv` using Cargo:

```bash
cargo install qsv
```

**2. Export SQLite Data to CSV:**

Use the `sqlite3` command-line tool to export your table data to a CSV file:

```bash
sqlite3 your_database.db -header -csv "SELECT * FROM your_table_name;" > output.csv
```

Replace `your_database.db` with the path to your SQLite database file and
`your_table_name` with the name of the table you wish to export.

**3. Display the CSV Data with `qsv`:**

Now, use `qsv` to display the CSV data in a colorized, tabular format:

```bash
qsv table output.csv
```

This command will render the CSV data in a neatly formatted table with colorized output, enhancing readability.

**Alternative: Use `xsv`**

Another Rust-based tool is `xsv`, a fast CSV command-line toolkit. You can install it via Cargo:

```bash
cargo install xsv
```

After exporting your SQLite data to CSV as shown earlier, you can display it using:

```bash
xsv table output.csv
```

---

This will also provide a formatted and colorized table view of your data.

By leveraging these Rust-based command-line tools, you can achieve a more
readable and visually appealing display of your SQLite table data directly in
the macOS Terminal.

The warning you're encountering indicates that the `qsv` package requires
specific features to be enabled during installation to build its binaries. To
resolve this, you can specify the desired features using the `--features` flag
with `cargo install`.

**Understanding `qsv` Variants and Features:**

The `qsv` toolkit offers different variants, each tailored with specific features:

- **`qsv`**: The full-featured version with all capabilities enabled.
- **`qsvlite`**: A lightweight version with minimal features, resulting in a
  smaller binary size.
- **`qsvdp`**: Optimized for use with DataPusher+, including only relevant
  commands and excluding the self-update engine.

**Installation Steps:**

1. **Install the Full-Featured `qsv`:**

   To install `qsv` with all features enabled, use:

   ```bash
   cargo install qsv --locked --features all_features
   ```

   This command ensures that all necessary features are included during installation.

2. **Install `qsvlite`:**

   For a lightweight version with minimal features:

   ```bash
   cargo install qsv --locked --bin qsvlite --features lite
   ```

3. **Install `qsvdp`:**

   To install the DataPusher+ optimized version:

   ```bash
   cargo install qsv --locked --bin qsvdp --features datapusher_plus
   ```

**Additional Information:**

- **Feature Flags:** The `qsv` package uses feature flags to include or exclude
  specific functionalities. Enabling the appropriate feature flag during
  installation ensures that the desired binary is built.

- **Pre-built Binaries:** Alternatively, pre-built binaries for various
  platforms are available on the [qsv GitHub Releases
  page](https://github.com/jqnatividad/qsv/releases). These binaries come with
  the self-update feature enabled, allowing for easy updates.

By specifying the appropriate features during installation, you can ensure that
the `qsv` binaries are built according to your requirements.
