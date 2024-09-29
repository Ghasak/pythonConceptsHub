# JupyterLab 4.0 config
<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [JupyterLab 4.0 config](#jupyterlab-40-config)
    - [How to pass your user configurations to Jupyterlab](#how-to-pass-your-user-configurations-to-jupyterlab)
    - [Passing User's configurations of Jupyberlab 4.0](#passing-users-configurations-of-jupyberlab-40)

<!-- markdown-toc end -->

## How to pass your user configurations to Jupyterlab

There are two ways, but both assume you already copied your configurations (directory ~/.jupyter) to your root project.

1. Using the environment variable for example using the following in `.envrc` and load the prior to excute your code.

```sh
export JUPYTERLAB_SETTINGS_DIR=./.jupyter/lab/user-settings
export JUPYTERLAB_WORKSPACES_DIR=./.jupyter/lab/workspaces

```

2. Passing the config usign the flag --config as following

```Makefile
@pipenv run jupyter lab --no-browser --allow-root --port=9999 --autoreload --notebook-dir="$(pwd)" -y --config=$(pwd)/.jupyter/lab/user-settings
```

## Passing User's configurations of Jupyberlab 4.0

This is the method that I used in most of python projects.

1. You can check the current configurations using:

```sh
jupyter lab path
```

2. You have to provide three types of environment variables to get fully
   cusomizable jupyter without affecting the global jupyter.

- Assume I am in my root project with `.envrc` having the following:
- The `Application directory` is based on which jupyterlab you are using.

```sh
export JUPYTERLAB_SETTINGS_DIR=./.jupyter/lab/user-settings
export JUPYTERLAB_WORKSPACES_DIR=./.jupyter/lab/workspaces

```

3. I have copied `cp -r ~/.jupyter` entierly to my current root project. Now I get
   Assume I already inside the virtualenv.

```sh
Application directory:   ~/.local/share/virtualenvs/carWebScripping-KFoIZYbp/share/jupyter/lab
User Settings directory: ~/Desktop/devCode/pythonHub/carWebScripping/.jupyter/lab/user-settings
Workspaces directory: ~/Desktop/devCode/pythonHub/carWebScripping/.jupyter/lab/workspaces

```
