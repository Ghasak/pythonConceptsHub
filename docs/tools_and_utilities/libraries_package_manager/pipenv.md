# Pipenv in Action

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Pipenv in Action](#pipenv-in-action)
    - [Introduction](#introduction)
        - [Summary Table for Pipenv Commands](#summary-table-for-pipenv-commands)
        - [Introduction to Pipenv](#introduction-to-pipenv)
        - [Setting Up a Robust Project with Pipenv](#setting-up-a-robust-project-with-pipenv)
        - [1. Create a Project from Scratch](#1-create-a-project-from-scratch)
        - [2. Pass the Project to a Friend](#2-pass-the-project-to-a-friend)
        - [3. Manage Development, Pre-Release, and Release](#3-manage-development-pre-release-and-release)
            - [Development](#development)
            - [Pre-Release](#pre-release)
            - [Release](#release)
        - [4. Basics Commands for Pipenv (with Complete Workflow)](#4-basics-commands-for-pipenv-with-complete-workflow)
        - [5. Extra Features and Tips](#5-extra-features-and-tips)
    - [Passing a path of python to pipenv](#passing-a-path-of-python-to-pipenv)
        - [Steps to Create a Pipenv Virtual Environment with a Custom Python Version:](#steps-to-create-a-pipenv-virtual-environment-with-a-custom-python-version)
        - [Example:](#example)
        - [Important Notes:](#important-notes)
    - [Development with pipenv](#development-with-pipenv)
        - [Explanation of Each Stage](#explanation-of-each-stage)
        - [Summary of Key Commands:](#summary-of-key-commands)
    - [Project transfer ownership pipenv](#project-transfer-ownership-pipenv)
        - [Explanation of the Project Transfer and Collaboration Workflow:](#explanation-of-the-project-transfer-and-collaboration-workflow)
        - [Summary Table for Commands in Collaborative Development with Pipenv:](#summary-table-for-commands-in-collaborative-development-with-pipenv)
    - [Q1 Does it mean Pipenv.lock file should be maintained using versioning like git right?](#q1-does-it-mean-pipenvlock-file-should-be-maintained-using-versioning-like-git-right)
        - [Why `Pipfile.lock` Should Be Version Controlled:](#why-pipfilelock-should-be-version-controlled)
        - [Best Practices for Versioning `Pipfile.lock`:](#best-practices-for-versioning-pipfilelock)
        - [Summary:](#summary)
    - [Q2 Is there a way to check compatibility of packages before I use pipenv lock ?](#q2-is-there-a-way-to-check-compatibility-of-packages-before-i-use-pipenv-lock-)
        - [1. **Pipenv's Built-In Compatibility Check:**](#1-pipenvs-built-in-compatibility-check)
        - [2. **Manual Version Constraints in `Pipfile`:**](#2-manual-version-constraints-in-pipfile)
        - [3. **Test Installation Before Locking:**](#3-test-installation-before-locking)
        - [4. **Use `pipenv graph` to Inspect Dependencies:**](#4-use-pipenv-graph-to-inspect-dependencies)
        - [5. **Check Package Documentation and Compatibility Tables:**](#5-check-package-documentation-and-compatibility-tables)
        - [6. **Run Tests in the Virtual Environment Before Locking:**](#6-run-tests-in-the-virtual-environment-before-locking)
        - [Steps for Checking Compatibility Before Locking:](#steps-for-checking-compatibility-before-locking)
        - [Conclusion:](#conclusion)
    - [Q3: Everyting to know about --skip-lock - Useful command](#q3-everyting-to-know-about---skip-lock---useful-command)
        - [How the `--skip-lock` Flag Works](#how-the---skip-lock-flag-works)
        - [When to Use `--skip-lock`](#when-to-use---skip-lock)
        - [How to Use `--skip-lock`](#how-to-use---skip-lock)
            - [Syntax:](#syntax)
            - [Examples:](#examples)
        - [The Process of Using `--skip-lock`](#the-process-of-using---skip-lock)
        - [When Not to Use `--skip-lock`](#when-not-to-use---skip-lock)
        - [Summary of Usage](#summary-of-usage)
    - [TroubleShooting](#troubleshooting)
        - [What I have done?](#what-i-have-done)

<!-- markdown-toc end -->

## Introduction

This is the `pipenv` working snippet, worked on and tested based on version:
`pipenv, version 2023.12.1`, which works with my current python version: `Python 3.11.5`.

### Summary Table for Pipenv Commands

| Command                                 | Description                                                  | Syntax Example                    |
| --------------------------------------- | ------------------------------------------------------------ | --------------------------------- |
| **Initialize a project**                | Initializes a new project with specified Python version      | `pipenv --python 3.11.3`          |
| **Install a package**                   | Installs a regular dependency                                | `pipenv install requests`         |
| **Install a dev package**               | Installs a development dependency                            | `pipenv install pytest --dev`     |
| **Install a pre-release package**       | Installs a pre-release version of a package                  | `pipenv install pandas --pre`     |
| **Recreate environment**                | Installs dependencies from `Pipfile.lock` on another machine | `pipenv install --ignore-pipfile` |
| **Run a script in virtual environment** | Runs a Python script within the Pipenv environment           | `pipenv run python my_script.py`  |
| **Activate shell**                      | Activates the Pipenv-managed virtual environment shell       | `pipenv shell`                    |
| **Check for security vulnerabilities**  | Runs a security check for installed dependencies             | `pipenv check`                    |
| **View dependency graph**               | Displays a graph of all installed dependencies               | `pipenv graph`                    |
| **Lock dependencies**                   | Locks the current versions of dependencies to `Pipfile.lock` | `pipenv lock`                     |
| **Uninstall a package**                 | Removes a package and updates `Pipfile`                      | `pipenv uninstall requests`       |
| **Exit virtual environment shell**      | Exits the Pipenv shell                                       | `exit`                            |

With Pipenv, you can easily create and manage robust projects, share them across
machines, and ensure consistent environments. Let me know if you need more
details!

### Introduction to Pipenv

Pipenv is a tool that aims to bring the best features of `pip` and `virtualenv`
together for Python projects. It simplifies dependency management by
automatically creating and managing a virtual environment for your projects and
adding/removing packages from your `Pipfile` as you install or uninstall
packages. It was created to solve the following problems:

1. **Environment Isolation:** To avoid global package installations and manage
   dependencies on a per-project basis.
2. **Dependency Management:** To replace `requirements.txt` with a more robust
   solution (`Pipfile` and `Pipfile.lock`).
3. **Reproducibility:** Ensuring that project environments can be replicated
   exactly on different machines with the same dependencies and versions.

### Setting Up a Robust Project with Pipenv

Let’s go step by step through how to set up a project using Pipenv and how to
transfer it to another machine or a friend, along with managing different stages
(dev, pre-release, and release).

---

### 1. Create a Project from Scratch

Here’s how you start a project using Pipenv.

1. **Install Pipenv:**

   Before using Pipenv, you need to install it:

   ```bash
   pip install pipenv
   ```

2. **Initialize a new project:**

   In an empty directory, you can initialize a new project with:

   ```bash
   pipenv --python 3.11.3
   ```

   This will:

   - Create a `Pipfile` to manage dependencies.
   - Create a virtual environment where all packages will be installed.

3. **Install Dependencies:**

   Now you can install dependencies. For example, for a web scraping project,
   you might install `requests` and `beautifulsoup4`:

   ```bash
   pipenv install requests beautifulsoup4
   ```

   To install a development dependency (such as `pytest` for testing), you can add it like this:

   ```bash
   pipenv install pytest --dev
   ```

   Pipenv will maintain separate sections in the `Pipfile` for regular and development dependencies.

4. **Lock Dependencies:**

   After adding your dependencies, you should lock the dependencies to ensure reproducibility:

   ```bash
   pipenv lock
   ```

   This will create a `Pipfile.lock`, which records the exact versions of all installed dependencies.

---

### 2. Pass the Project to a Friend

To share the project with a friend or move it to another machine, follow these steps:

1. **Share the Files:**

   You need to share these files:

   - `Pipfile`
   - `Pipfile.lock`
   - Any project-specific files (source code, etc.)

2. **Recreate the Environment:**

   On the new machine (or your friend’s machine), after cloning the project
   folder or downloading it, the following command will recreate the
   environment:

   ```bash
   pipenv install --ignore-pipfile
   ```

   This installs the exact versions of the dependencies based on the `Pipfile.lock`.

---

### 3. Manage Development, Pre-Release, and Release

Pipenv allows you to manage different stages of your project’s life cycle easily.

#### Development

In development, you might need extra tools like linters or testing libraries
that won’t be required in production. Use the `--dev` flag to install
development dependencies.

Example:

```bash
pipenv install flake8 --dev
```

You can use `pipenv install --dev` to install all development dependencies specified in the `Pipfile`.

#### Pre-Release

Sometimes, you may want to install pre-release versions of packages. Pipenv has an option for this:

```bash
pipenv install package_name --pre
```

This installs the pre-release version of a package.

#### Release

In the release phase, ensure that the final version is locked and installed using:

```bash
pipenv lock
pipenv install --ignore-pipfile
```

This will ensure that the exact versions specified in the `Pipfile.lock` are used.

---

### 4. Basics Commands for Pipenv (with Complete Workflow)

- **Start a project from scratch:**

  ```bash
  pipenv --python 3.11.3
  ```

  This initializes a project with Python 3.11.3 in a virtual environment.

- **Install a package (regular dependency):**

  ```bash
  pipenv install requests
  ```

  Adds `requests` to the `Pipfile` and installs it in the virtual environment.

- **Install a development package:**

  ```bash
  pipenv install pytest --dev
  ```

  Adds `pytest` to the `dev-packages` section of `Pipfile`.

- **Install a pre-release package:**

  ```bash
  pipenv install pandas --pre
  ```

  Installs the pre-release version of `pandas`.

- **Recreate the environment on another machine:**

  Clone the project, then run:

  ```bash
  pipenv install --ignore-pipfile
  ```

  This installs the exact versions specified in `Pipfile.lock`.

- **Run your project:**

  You can run scripts or programs inside the virtual environment using:

  ```bash
  pipenv run python my_script.py
  ```

  Or you can activate the shell:

  ```bash
  pipenv shell
  ```

  Now, you can run commands in an isolated environment.

- **Check for security vulnerabilities:**

  You can check if there are any security issues with the dependencies using:

  ```bash
  pipenv check
  ```

- **Uninstall a package:**

  If you want to remove a package, use:

  ```bash
  pipenv uninstall requests
  ```

---

### 5. Extra Features and Tips

- **Pipfile and Pipfile.lock:**

  - The `Pipfile` is a declarative configuration file that lists your project's direct dependencies.
  - The `Pipfile.lock` is an exact, resolved list of all dependencies and their versions, ensuring deterministic builds.

- **Locking Dependencies:**

  Always run `pipenv lock` before deploying or sharing your project. This locks the specific versions of your dependencies to ensure consistent environments.

- **Dependency Graph:**

  You can visualize your dependency graph using:

  ```bash
  pipenv graph
  ```

---

## Passing a path of python to pipenv

If you have a specific Python interpreter installed in a directory on your
machine and you want Pipenv to use that exact version (without searching for
it), you can specify the path to the Python binary when creating the virtual
environment.

Here’s how you can create a Pipenv virtual environment with a specific Python
version from a custom directory:

### Steps to Create a Pipenv Virtual Environment with a Custom Python Version:

1. **Find the path to the Python interpreter:**

   First, make sure you know the exact path to the Python binary you want to
   use. For example, let’s assume your Python binary is located at:

   ```bash
   /path/to/python3.11/bin/python3
   ```

2. **Use Pipenv with the custom Python interpreter:**

   To force Pipenv to use this Python version and interpreter, you can specify
   the full path when initializing your project:

   ```bash
   pipenv --python /path/to/python3.11/bin/python3
   ```

   This will instruct Pipenv to use the provided Python interpreter to create
   the virtual environment. It will not search for Python on your machine.

### Example:

If the Python interpreter you want to use is located at
`/usr/local/bin/python3.11`, you can run:

```bash
pipenv --python /usr/local/bin/python3.11
```

### Important Notes:

- This ensures that the virtual environment is created using the specific Python
  version you provided, without relying on whatever version Pipenv might find on
  your system.
- You can confirm the Python version in the virtual environment with:

  ```bash
  pipenv run python --version
  ```

This approach is useful when working with multiple Python versions or custom
installations and guarantees that Pipenv uses the correct interpreter for your
project.

## Development with pipenv

Below is an ASCII diagram illustrating the development lifecycle using `pipenv`,
covering the main stages: development, pre-release, and release, along with the
commands you would use at each stage.

```sh
                           Pipenv Development Lifecycle
--------------------------------------------------------------------------------
                                +------------------+
                                |   Start Project   |
                                +------------------+
                                       |
                                       | pipenv --python 3.11.3
                                       |
                                +------------------+
                                |   Install Deps   |
                                +------------------+
                                |                  |
  pipenv install requests       |                  | pipenv install pytest --dev
      (Regular Package)          |                  | (Development Package)
                                |                  |
                                +------------------+
                                       |
                                       | pipenv lock
                                       | (Lock Dependencies)
                                       |
                                +--------------------+
                                |   Development      |
                                |   Environment      |
                                +--------------------+
                                       |
  -------------------->                 |
  |  Install dev dependencies:          |
  |  pipenv install --dev               |
  |  (Install all dev packages)         |
  -------------------->                 |
                                       |
                                +-------------------+
                                |   Pre-release     |
                                |   Stage           |
                                +-------------------+
                                       |
  pipenv install package_name --pre    |
  (Install pre-release version)        |
                                       |
                                +-------------------+
                                |    Test and Fix   |
                                +-------------------+
                                       |
                                       | pipenv run pytest
                                       | (Run tests)
                                       |
                                +-------------------+
                                |    Final Release  |
                                +-------------------+
                                       |
  pipenv install --ignore-pipfile      |
  (Install exact dependencies)         |
                                       |
                                +--------------------+
                                |   Production       |
                                +--------------------+
                                       |
  pipenv check                         |
  (Check for security vulnerabilities) |
                                       |
  pipenv graph                         |
  (View dependency graph)              |
                                       |
                                +---------------------+
                                |    Distribute       |
                                +---------------------+
                                       |
  Transfer project to friend           |
  Share `Pipfile` & `Pipfile.lock`     |
  Recreate env:                        |
  pipenv install --ignore-pipfile      |
                                       |
  pipenv shell                         |
  (Activate environment shell)         |
                                       |
  pipenv uninstall package_name        |
  (Uninstall a package if needed)      |
--------------------------------------------------------------------------------
```

### Explanation of Each Stage

1. **Start Project:**

   - You begin a project by specifying the Python version you want to use:
     ```bash
     pipenv --python 3.11.3
     ```

2. **Install Dependencies:**

   - Regular dependencies (e.g., `requests`):
     ```bash
     pipenv install requests
     ```
   - Development dependencies (e.g., `pytest`):
     ```bash
     pipenv install pytest --dev
     ```

3. **Lock Dependencies:**

   - Lock your dependencies in the `Pipfile.lock` for reproducibility:
     ```bash
     pipenv lock
     ```

4. **Development Stage:**

   - Install all development dependencies (if not already installed):
     ```bash
     pipenv install --dev
     ```

5. **Pre-release Stage:**

   - Install pre-release versions of packages:
     ```bash
     pipenv install package_name --pre
     ```

6. **Test and Fix:**

   - Run your test suite (e.g., `pytest` for testing):
     ```bash
     pipenv run pytest
     ```

7. **Final Release:**

   - Lock dependencies to ensure exact versions are installed in production:
     ```bash
     pipenv lock
     ```
   - Install exact versions in production:
     ```bash
     pipenv install --ignore-pipfile
     ```

8. **Production Stage:**

   - Check for security vulnerabilities:

     ```bash
     pipenv check
     ```

   - View the dependency graph:
     ```bash
     pipenv graph
     ```

9. **Distribute:**
   - Share the `Pipfile` and `Pipfile.lock` with a friend or colleague.
   - Recreate the environment on another machine:
     ```bash
     pipenv install --ignore-pipfile
     ```
   - Activate the environment shell:
     ```bash
     pipenv shell
     ```

---

### Summary of Key Commands:

| Command                             | Description                                        |
| ----------------------------------- | -------------------------------------------------- |
| `pipenv --python 3.11.3`            | Initialize a new Pipenv project with Python 3.11.3 |
| `pipenv install package_name`       | Install a regular package                          |
| `pipenv install package_name --dev` | Install a development package                      |
| `pipenv install package_name --pre` | Install a pre-release package                      |
| `pipenv lock`                       | Lock current dependencies                          |
| `pipenv install --ignore-pipfile`   | Install exact versions from `Pipfile.lock`         |
| `pipenv run pytest`                 | Run tests within the virtual environment           |
| `pipenv check`                      | Check for security vulnerabilities                 |
| `pipenv graph`                      | View the project’s dependency graph                |
| `pipenv shell`                      | Activate the virtual environment shell             |
| `pipenv uninstall package_name`     | Uninstall a package and update `Pipfile`           |

This diagram and the commands outline a complete workflow for using `pipenv` in
development, pre-release, and release stages, along with handling environment
distribution.

## Project transfer ownership pipenv

Here’s an ASCII diagram showing how to transfer a `pipenv` project to another
machine or a friend’s computer, focusing on collaboration in a development
environment.

```sh
                             Pipenv Project Transfer Workflow
--------------------------------------------------------------------------------
                                +------------------+
                                |   Start Project   |
                                +------------------+
                                       |
                                       | pipenv --python 3.11.3
                                       |
                                +------------------+
                                |   Install Deps   |
                                +------------------+
                                |                  |
  pipenv install requests       |                  | pipenv install pytest --dev
  (Regular Package)              |                  | (Development Package)
                                |                  |
                                +------------------+
                                       |
                                       | pipenv lock
                                       | (Lock Dependencies)
                                       |
                                +--------------------+
                                |   Development      |
                                |   Environment      |
                                +--------------------+
                                       |
    --------------------->             |
    | Transfer the Project:             |
    |   - Share `Pipfile`               |
    |   - Share `Pipfile.lock`          |
    |   - Share code files              |
    --------------------->             |
                                       |
                                +--------------------+
                                | Transfer to Friend  |
                                +--------------------+
                                       |
                                       | Friend clones project repo
                                       |
                                +--------------------+
                                |   Recreate Env     |
                                +--------------------+
                                       |
                                       | pipenv install --ignore-pipfile
                                       | (Install from Pipfile.lock)
                                       |
                                +---------------------+
                                |  Dev Collaboration  |
                                +---------------------+
                                       |
 pipenv shell                          |  Friend activates shell:
 (Activate environment)                |  pipenv shell
                                       |
                                +---------------------+
                                |  Friend Installs    |
                                |  New Dev Packages   |
                                +---------------------+
                                       |
 pipenv install new_dev_pkg --dev      |  pipenv install package --dev
 (Install more dev dependencies)       |  (Install additional dev packages)
                                       |
                                +----------------------+
                                |  Sync & Lock         |
                                +----------------------+
                                       |
 Friend locks dependencies             |  pipenv lock
                                       |
                                +----------------------+
                                |  Push Changes        |
                                |  to Version Control  |
                                +----------------------+
                                       |
                                       | Sync codebase via Git/other VCS
                                       |
                                +----------------------+
                                |  Pull Changes Back   |
                                +----------------------+
                                       |
                                       | Original user pulls the changes,
                                       | including `Pipfile.lock`
                                       |
                                +----------------------+
                                |  Recreate Env Again  |
                                +----------------------+
                                       |
                                       | pipenv install --ignore-pipfile
                                       | (Recreate the same environment)
--------------------------------------------------------------------------------
```

### Explanation of the Project Transfer and Collaboration Workflow:

1. **Start and Lock Dependencies:**

   - Initialize a Pipenv project and install all the necessary dependencies (both regular and dev dependencies).
   - Lock the dependencies using:
     ```bash
     pipenv lock
     ```

2. **Transfer the Project to Another Machine or Friend:**

   - Share the following files:
     - `Pipfile` (specifies dependencies)
     - `Pipfile.lock` (locks exact versions)
     - Any project-specific code files (source code, etc.)

3. **Recreate the Environment on Your Friend's Machine:**

   - Your friend can clone or copy the project directory.
   - To recreate the environment exactly, your friend should run:

     ```bash
     pipenv install --ignore-pipfile
     ```

     This ensures that all dependencies from the `Pipfile.lock` are installed on their machine.

4. **Activate the Virtual Environment:**

   - Both you and your friend should activate the environment for development:
     ```bash
     pipenv shell
     ```

5. **Collaborate on Development:**

   - Your friend can add new development dependencies using:
     ```bash
     pipenv install new_dev_pkg --dev
     ```

6. **Sync Changes and Lock Dependencies:**

   - After installing new dependencies, your friend should lock the new dependency versions:
     ```bash
     pipenv lock
     ```

7. **Push and Pull Changes via Version Control:**

   - Your friend pushes the changes to the version control system (e.g., Git), including the updated `Pipfile` and `Pipfile.lock`.
   - You pull the changes back to your machine.

8. **Recreate the Updated Environment:**
   - After pulling the changes, you run:
     ```bash
     pipenv install --ignore-pipfile
     ```
   - This ensures your environment matches your friend’s, with all new dev dependencies installed.

---

### Summary Table for Commands in Collaborative Development with Pipenv:

| Command                             | Description                                        |
| ----------------------------------- | -------------------------------------------------- |
| `pipenv --python 3.11.3`            | Initialize a new Pipenv project with Python 3.11.3 |
| `pipenv install package_name`       | Install a regular package                          |
| `pipenv install package_name --dev` | Install a development package                      |
| `pipenv lock`                       | Lock current dependencies                          |
| `pipenv install --ignore-pipfile`   | Recreate environment from `Pipfile.lock`           |
| `pipenv shell`                      | Activate the virtual environment shell             |
| `pipenv install new_dev_pkg --dev`  | Install a new development package                  |
| `pipenv uninstall package_name`     | Uninstall a package and update `Pipfile`           |
| `pipenv check`                      | Check for security vulnerabilities                 |
| `pipenv graph`                      | View the project’s dependency graph                |

By following this workflow, you and your friend can collaborate efficiently on
the same project, ensuring that you both have consistent development
environments.

## Q1 Does it mean Pipenv.lock file should be maintained using versioning like git right?

Yes, exactly! The `Pipfile.lock` **should absolutely be maintained in version
control**, like Git. This file is critical for ensuring consistent and
reproducible environments across different machines and for all collaborators.
Here's why:

### Why `Pipfile.lock` Should Be Version Controlled:

1. **Reproducibility:**

   - The `Pipfile.lock` contains exact versions of all the dependencies,
     ensuring that anyone who installs the project later will get the same
     versions as you did, preventing compatibility issues.
   - Without the `Pipfile.lock`, someone installing the project might get
     different versions of the dependencies (if the `Pipfile` allows flexibility
     in versions), which could lead to bugs or unexpected behavior.

2. **Collaboration:**

   - If multiple developers are working on the same project, having the
     `Pipfile.lock` version-controlled ensures that they are all working with
     the same dependencies. This prevents the "works on my machine" problem.

3. **Security:**

   - Locking specific versions helps mitigate security risks. If a dependency is
     flagged for a security vulnerability, you can upgrade that dependency and
     lock it at the secure version, ensuring everyone is using the safe version.

4. **Rollbacks:**

   - If you encounter issues after adding or upgrading dependencies,
     version-controlling the `Pipfile.lock` allows you to revert to a previous
     commit where the environment was working.

5. **Deployment Stability:**
   - For production environments, the `Pipfile.lock` ensures that your
     deployment uses the same package versions that were tested during
     development, minimizing the risk of issues when moving to production.

### Best Practices for Versioning `Pipfile.lock`:

1. **Always Commit the `Pipfile.lock` File:**

   - After running `pipenv lock` (which generates or updates the `Pipfile.lock`), commit the file to version control:
     ```bash
     git add Pipfile.lock
     git commit -m "Update Pipfile.lock after installing new dependencies"
     ```

2. **Keep the `Pipfile` and `Pipfile.lock` in Sync:**

   - If the `Pipfile.lock` is updated due to changes in the `Pipfile`, make sure
     both are committed together to maintain consistency.

3. **Review Changes to `Pipfile.lock`:**

   - When upgrading or changing dependencies, review the diff in `Pipfile.lock`
     to ensure no unintended changes have been introduced.

4. **Lock Before Release:**
   - Before releasing your project or deploying to production, make sure to lock
     all dependencies using `pipenv lock` and commit the updated `Pipfile.lock`.

---

### Summary:

Yes, version-controlling `Pipfile.lock` is essential for maintaining stability,
reproducibility, and security in your project. Every time you or your
collaborators modify dependencies or lock the environment, ensure that the
`Pipfile.lock` is committed to version control. This will guarantee that
everyone working on the project, as well as production environments, will have
the same, predictable setup.

## Q2 Is there a way to check compatibility of packages before I use pipenv lock ?

Yes, there are ways to check the compatibility of your packages before running
`pipenv lock`. Pipenv has built-in tools that can help you check for potential
issues with your package dependencies. Here’s how you can do it:

### 1. **Pipenv's Built-In Compatibility Check:**

Pipenv provides a command to check your current dependency tree for any
compatibility or security issues **before locking the environment**. This is
a quick way to ensure there are no obvious conflicts between the packages
you've installed.

You can use:

```bash
pipenv check
```

This command checks the dependencies in your `Pipfile` for known security
vulnerabilities and for potential issues with the compatibility of the
packages. While this won’t catch all types of compatibility issues (like
deeper version mismatches), it will help identify common problems.

### 2. **Manual Version Constraints in `Pipfile`:**

You can manually specify version constraints for packages in the `Pipfile` to
ensure compatibility before locking the environment. For example:

```toml
[packages]
requests = ">=2.25,<2.26"
pandas = ">=1.2,<1.3"
```

By setting constraints, you prevent Pipenv from installing incompatible
versions of your packages.

### 3. **Test Installation Before Locking:**

You can test installing packages without immediately locking the environment
to see if there are any conflicts. For example:

- Install packages without locking:

  ```bash
  pipenv install --skip-lock
  ```

- After installing the packages, you can check the installed versions and run
  your tests to ensure compatibility **before** running `pipenv lock`.

### 4. **Use `pipenv graph` to Inspect Dependencies:**

Before locking the environment, you can inspect the dependency tree to ensure
there are no conflicts between installed packages. This helps visualize what
versions have been installed and whether there are any mismatches or
conflicting versions.

To check the dependency graph:

```bash
pipenv graph
```

This shows a tree of your installed packages and their dependencies, which
can help you identify potential conflicts.

### 5. **Check Package Documentation and Compatibility Tables:**

While not directly part of Pipenv, it's always a good practice to check the
compatibility tables or release notes for critical packages you're using.
Many libraries document which versions are compatible with others. This can
be important, especially if you're working with major packages like `Django`,
`Flask`, or `pandas`, which may have specific version dependencies.

### 6. **Run Tests in the Virtual Environment Before Locking:**

After installing dependencies (using `pipenv install --skip-lock`), run your
test suite inside the virtual environment to ensure everything works as
expected. This will help identify runtime compatibility issues:

```bash
pipenv run pytest
```

### Steps for Checking Compatibility Before Locking:

1. Install packages without locking:

   ```bash
   pipenv install --skip-lock
   ```

2. Check for known vulnerabilities and issues:

   ```bash
   pipenv check
   ```

3. Inspect the dependency tree for potential conflicts:

   ```bash
   pipenv graph
   ```

4. Run your tests:

   ```bash
   pipenv run pytest
   ```

5. If everything looks good, lock the environment:
   ```bash
   pipenv lock
   ```

### Conclusion:

While `pipenv lock` is necessary for ensuring deterministic builds, it's a good
idea to first install your dependencies without locking, check for compatibility
issues using `pipenv check` and `pipenv graph`, and test your application in the
virtual environment. This allows you to catch potential issues before locking
down the dependency versions.

## Q3: Everyting to know about --skip-lock - Useful command

The `--skip-lock` flag in Pipenv allows you to install packages without
immediately generating or updating the `Pipfile.lock` file. This can be useful
in certain scenarios where you want to test dependencies or quickly install
packages without going through the potentially time-consuming process of
resolving and locking dependencies.

### How the `--skip-lock` Flag Works

By default, when you install a package using Pipenv, it resolves all
dependencies and creates or updates the `Pipfile.lock` to ensure the exact
versions are tracked for reproducibility. However, resolving dependencies and
locking them can take time, especially in large projects or when there are
complex version constraints.

The `--skip-lock` flag tells Pipenv to **install the package(s)** without
updating the `Pipfile.lock` file, thus skipping the dependency resolution
process. This allows you to quickly install and test packages but leaves your
environment in an "unlocked" state, meaning it's not yet fully reproducible
until you later lock it.

### When to Use `--skip-lock`

1. **Quick Testing of Dependencies:**

   - When you're experimenting with different packages and want to quickly
     install them without locking down exact versions. You might be evaluating
     which packages work best or trying out new packages before finalizing your
     dependency setup.

2. **Speeding Up the Install Process:**

   - When you don’t want to wait for Pipenv to resolve and lock all
     dependencies, especially during rapid development or testing. Locking can
     be time-consuming, so using `--skip-lock` can help speed up the process.

3. **Handling Conflicting Dependencies:**

   - If you encounter dependency conflicts during installation, using
     `--skip-lock` allows you to install the packages and manually manage or
     test their compatibility without immediately locking the environment. You
     can manually tweak the versions later.

4. **Development-Only Installs:**

   - During development, if you're frequently adding and removing packages and
     don’t want to lock the dependencies every time, you can use `--skip-lock`
     to avoid repeatedly updating the `Pipfile.lock`.

5. **Installation in a Temporary Environment:**
   - When working in a temporary environment (e.g., running a script or one-time
     task) where you don’t care about locking exact versions but just need the
     packages installed quickly.

### How to Use `--skip-lock`

#### Syntax:

```bash
pipenv install <package_name> --skip-lock
```

#### Examples:

1. **Installing a regular package without locking:**

   ```bash
   pipenv install requests --skip-lock
   ```

   This installs the `requests` package without updating the `Pipfile.lock`
   file. The `Pipfile` is updated with the new package, but no exact versions
   are locked.

2. **Installing a development dependency without locking:**

   ```bash
   pipenv install pytest --dev --skip-lock
   ```

   This installs `pytest` as a development dependency without updating the lock
   file.

3. **Installing multiple packages without locking:**

   ```bash
   pipenv install requests beautifulsoup4 --skip-lock
   ```

   This installs both `requests` and `beautifulsoup4` without resolving and
   locking their dependencies.

4. **Skipping lock while upgrading a package:**

   ```bash
   pipenv update requests --skip-lock
   ```

   This updates the `requests` package but skips locking the exact versions in
   `Pipfile.lock`.

### The Process of Using `--skip-lock`

Here’s a typical process where you would use `--skip-lock`:

1. **Install Packages Quickly Without Locking:**
   You might want to install several packages during development to try them
   out, skipping the locking process to save time:

   ```bash
   pipenv install <package_name> --skip-lock
   ```

2. **Test Compatibility:**
   After installing the packages, you can test them, run your code, and make
   sure the packages are working as expected:

   ```bash
   pipenv run python my_script.py
   ```

3. **Inspect Dependencies:**
   You can inspect the installed packages and their dependencies using `pipenv graph` to see if there are any conflicts:

   ```bash
   pipenv graph
   ```

4. **Lock When Ready:**
   Once you're satisfied with the package setup and you've ensured
   compatibility, you can lock the environment:

   ```bash
   pipenv lock
   ```

   This will update the `Pipfile.lock` file and lock down the exact versions of
   all dependencies for reproducibility.

### When Not to Use `--skip-lock`

- **For Production or Final Deployments:**
  You should avoid using `--skip-lock` when preparing for production or
  deploying your project. Locking the environment ensures that the exact
  versions of packages are used in production, reducing the risk of issues due
  to incompatible package versions. In production, always lock your dependencies
  by running:

  ```bash
  pipenv lock
  ```

- **When Working with Other Developers:**
  If you’re collaborating with others, skipping the lock step can lead to
  inconsistencies between your environment and others. It’s important to ensure
  that the dependencies are locked for reproducibility across different
  machines.

### Summary of Usage

| Scenario                               | Command Example                           | Description                                                                  |
| -------------------------------------- | ----------------------------------------- | ---------------------------------------------------------------------------- |
| Install a regular package without lock | `pipenv install requests --skip-lock`     | Quickly install without updating the lock file                               |
| Install a dev dependency without lock  | `pipenv install pytest --dev --skip-lock` | Add a development dependency without locking                                 |
| Skip locking while upgrading a package | `pipenv update requests --skip-lock`      | Update a package without locking                                             |
| Lock dependencies later                | `pipenv lock`                             | After testing or verifying the environment, lock the dependencies            |
| Check installed dependency graph       | `pipenv graph`                            | View installed dependencies after using `--skip-lock` to check for conflicts |

The `--skip-lock\*\* flag is a useful tool for quick installs, development work,
and testing, but you should always lock your dependencies once you’ve confirmed
the environment is stable and ready for production or sharing.

## TroubleShooting

**NOTE**: It seems that we have to use the `pipenv` command to ensure all the
libraries goes to the `Pipfile.lock`, if you mix commands such as using `pipen install library_name` and `pipenv run pip install library_name`, you will ended
up having some libraries in the `.loc` file while other only for the `pip`.

- [x] We must always use `pipenv` to ensure everyting goes to the `Pipfile.lock`.

### What I have done?

1. First I have all the libraries that I want in my `requiremetns.txt` file so I used

```sh
pipenv install -r requirements.txt

```

This will ensure all the dependencies and passeed to the `Pipfile`. with all the versions of our library-requirements. 
