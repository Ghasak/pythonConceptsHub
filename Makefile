.PHONY: help install jupyter jupyter_server run lock

# Colors for fancy output
YELLOW=\033[33m
GREEN=\033[32m
CYAN=\033[36m
RESET=\033[0m

# Default target: help
help:
	@echo ""
	@echo "$(YELLOW)===================================================$(RESET)"
	@echo "$(CYAN)                Project Management Commands$(RESET)"
	@echo "$(YELLOW)===================================================$(RESET)"
	@echo "$(GREEN)install$(RESET)         - Initialize the project environment. Installs all dependencies using Pipenv, ensuring the environment is set up according to the Pipfile."
	@echo "                  $(CYAN)Usage: make install$(RESET)"
	@echo ""
	@echo "$(GREEN)jupyter$(RESET)         - Run Jupyter Lab in the current directory. Opens Jupyter Lab without launching a browser. Uses port 9999."
	@echo "                  $(CYAN)Usage: make jupyter$(RESET)"
	@echo "                  $(CYAN)Details:$(RESET) Run Jupyter Lab with autoreload enabled, allowing for real-time code changes. Useful for working in Jupyter notebooks."
	@echo ""
	@echo "$(GREEN)jupyter_server$(RESET)  - List all active Jupyter servers running on the system. Useful for identifying active sessions."
	@echo "                  $(CYAN)Usage: make jupyter_server$(RESET)"
	@echo ""
	@echo "$(GREEN)run$(RESET)             - Run the main Python script. Executes the Python script located at src/main.py using the Pipenv virtual environment."
	@echo "                  $(CYAN)Usage: make run$(RESET)"
	@echo ""
	@echo "$(GREEN)lock$(RESET)            - Lock the Pipenv environment. Generates a Pipfile.lock file to ensure reproducibility of the environment across systems."
	@echo "                  $(CYAN)Usage: make lock$(RESET)"
	@echo "                  $(CYAN)Details:$(RESET) the current versions of all installed dependencies are captured, helping to avoid future dependency conflicts."
	@echo ""
	@echo "$(YELLOW)===================================================$(RESET)"
	@echo "$(CYAN)                End of Help$(RESET)"
	@echo "$(YELLOW)===================================================$(RESET)"
	@echo ""

# Run to initialize the project - only once
install:
	@echo "$(GREEN)Initializing the project environment...$(RESET)"
	@pipenv install --ignore-pipfile

# Run Jupyter Lab
jupyter:
	@echo "$(GREEN)Starting Jupyter Lab on port 9999...$(RESET)"
	@pipenv run jupyter lab --no-browser --allow-root --port=9999 --autoreload --notebook-dir="$(pwd)" -y

# List active Jupyter servers
jupyter_server:
	@echo "$(GREEN)Listing active Jupyter servers...$(RESET)"
	@jupyter server list

# Run Python main script
run:
	@echo "$(GREEN)Running the main Python script...$(RESET)"
	@pipenv run python -m src.main

# Lock Pipenv dependencies
lock:
	@echo "$(GREEN)Locking the Pipenv environment...$(RESET)"
	@pipenv lock

