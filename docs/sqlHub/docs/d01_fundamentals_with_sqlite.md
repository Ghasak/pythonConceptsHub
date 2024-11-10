# Fundamentals with SQLITE
<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Fundamentals with SQLITE](#fundamentals-with-sqlite)
    - [Changing-log](#changing-log)
    - [Concepts](#concepts)
    - [SQL with nvim buffer](#sql-with-nvim-buffer)
        - [In a NVIM buffer](#in-a-nvim-buffer)
    - [Install necessary dependencies](#install-necessary-dependencies)
        - [Explanation of the fields:](#explanation-of-the-fields)

<!-- markdown-toc end -->

## Changing-log

- `2024-11-08 01:31`: sql with nvim up and running
  - syntax highlighting
  - syntax formatter
  - autocompletion
  - linting
  - SQL Sever Language Protocol (`sql-lsp`)

## Concepts

- As for the sqlite we have the following concepts according to our current worflow.

```sh
                                                 ┌────────────────────────────III┐
                                                 │   ┌────────────────────┐      │
                                               ┌───▶ │ NVIM PLUGIN DADBOD │      │
                                               │ │   └────────────────────┘      │
        ┌──────────────I┐       ┌──────────II┐ │ │   ┌─────────────────────────┐ │
  ┌┬┬┬─▶│  SQL SERVER   ├────▶  │ SQL Client ├─┼───▶ │BEAVER COMMUNITY EDITION │ │◀─────────┐
  ││││  └───────────────┘       └────────────┘ │ │   └─────────────────────────┘ │          ├─┐
  ││││                ▲                        │ │   ┌─────────────────────────┐ │          │V│
  ││││ ┌─────────1┐   └─────┐                  └───▶ │OTHER TYPES OF CLIENTS   │ │          │E│
  │││└─┤ SQLITE   │         │                    │   └─────────────────────────┘ │          │I│
  │││  └──────────┘         │                    └───────────────────────────────┘          │W│
  │││  ┌─────────2┐         │                                                               │ │
  ││└──┤ POSTRESQL│         │                                                               │D│
  ││   └──────────┘         │                                                               │A│
  ││   ┌─────────3┐         │                                ┌──────IV─┐                    │T│
  │└───┤ MYSQL    │         │                                │SQLSCRIPT│                    │A│
  │    └──────────┘         │                                │ -----   │                    ├─┘
  │    ┌─────────4┐         │                                │ -----   │────────────────────┘
  └────┤ ORCAL DB │         │                                │ -----   │
       └──────────┘         │                                └───┬─┬───┘
            ...             │        executing query             │ │
                            └────────────────────────────────────┘ │
                                                                   │
                                            ┌──┬───────────────────┴──────────────┐
                                            │01│synatx highlights                 │
                                            │02│syntax compeletion                │
                                            │03│syntax linting and error checking │
                                            │04│sql language server               │
                                            │05│synatx formatter                  │
                                            └──┴──────────────────────────────────┘
```

## SQL with nvim buffer

### In a NVIM buffer

Assume you have already in a `nvim` buffer. To establish a connection with
Dadbod and DBUI in Neovim, follow these steps:

1. **Ensure the database exists** (e.g., `employee_database.db`).

2. **Open Neovim** and start the DBUI interface with:

   ```vim
   :DBUI
   ```

3. **Set up a connection string** for your SQLite database. In Neovim, use the
   following command format:

   ```vim
   :DB sqlite:///path/to/employee_database.db
   ```

   Replace `/path/to/employee_database.db` with the actual path to your SQLite
   database. For example, if it’s in your current directory, you can use:

   ```vim
   :DB sqlite:///./employee_database.db
   ```

4. **Access the database**: After running the command, you should see your
   database in the DBUI interface, allowing you to explore tables, run queries,
   and interact with the database.

## Install necessary dependencies

**NOTE** : As for our curernt workflow this step is unnecessary.
Let me know if you need help with anything specific in DBUI!

Here's a configuration similar to your `r_language_server` setup, but for the
SQL Language Server (`sqlls`). This will allow the LSP to handle SQL files and
provide features like autocompletion and linting:

```lua
    -- for SQL npm install -g sql-language-server
    ["sqlls"] = function()
      lspconfig.sqlls.setup {
        on_attach = opts.on_attach,
        capabilities = opts.capabilities,
        handlers = opts.handlers,
        filetypes = { "sql" },
        cmd = { "sql-language-server", "up", "--method", "stdio" },
        root_dir = function(fname)
          return lspconfig.util.root_pattern ".git"(fname) or lspconfig.util.path.dirname(fname)
        end,
      }
    end,
```

### Explanation of the fields:

- **`on_attach`**, **`capabilities`**, and **`handlers`** are settings you pass
  to all LSP servers to configure their behavior when attaching to buffers, along
  with capabilities and custom handlers if needed.
- **`filetypes`** restricts the LSP server to only work with `sql` filetypes.
- **`cmd`** specifies the command to start the SQL Language Server. This
  example assumes `sql-language-server` is installed and available in your PATH.

Make sure you have installed `sql-language-server` through Mason or by running:

```bash
npm install -g sql-language-server
```

This setup should add autocompletion, syntax checking, and other LSP-related
features when editing SQL files. Let me know if you need further assistance!
