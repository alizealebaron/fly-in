# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : Makefile                                                         #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/02/26 12:46:41 by alebaron                                #
# @update   : 2026/02/26 13:44:26 by alebaron                                #
# ************************************************************************** #

# ==========================
#         Variables
# ==========================

VENV_PATH = .venv
VENV_PYTHON = $(VENV_PATH)/bin/python3
VENV_PIP = $(VENV_PATH)/bin/pip
VENV_POETRY = $(VENV_PATH)/bin/poetry

PYTHON = $(if $(wildcard $(VENV_PYTHON)), $(VENV_PYTHON), python3)
PIP = $(if $(wildcard $(VENV_PIP)), $(VENV_PIP), pip)
POETRY = $(if $(wildcard $(VENV_POETRY)), $(VENV_POETRY), poetry)

MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
			 --disallow-untyped-defs --check-untyped-defs

NAME = fly-in
CONFIG = default_config.txt
SRC_FILES = main.py \
			src/

PROJECT_VERSION = $(shell grep -m 1 '^version =' pyproject.toml | cut -d '"' -f 2)
PROJECT_NAME = $(shell grep -m 1 '^name =' pyproject.toml | cut -d '"' -f 2 | tr '-' '_')
TAR_FILE = $(PROJECT_NAME)-$(PROJECT_VERSION).tar.gz

# ==========================
#           Colors
# ==========================

BLACK   := \033[30m
RED     := \033[31m
GREEN   := \033[32m
YELLOW  := \033[33m
BLUE 	:= \033[96m
MAGENTA := \033[38;5;206m
CYAN    := \033[36m
WHITE   := \033[37m
RESET   := \033[0m
BOLD    := \033[1m
DIM     := \033[2m
ITALIC  := \033[3m
UNDER   := \033[4m
BLINK   := \033[5m
REVERSE := \033[7m
HIDDEN  := \033[8m
PINK 	:= \033[35m

# ==========================
#           Rules
# ==========================

# Install the Python packages used in a_maze_ing
install:
	@echo "$(CYAN)Installing ${NAME} packages...$(RESET)"
	@$(PIP) install poetry
	@$(VENV_POETRY) install
	@echo "$(GREEN)✅ Packages installed !$(RESET)"

# Run the main file of a_maze_ing in debug mode
debug:
	@echo "$(YELLOW)Running in DEBUG mode$(RESET)"
	@$(PY_PATH) $(PYTHON) -m pdb a_maze_ing.py

# Cleaning up all unnecessary Python files
clean :
	@echo "$(RED)$(BOLD)[Cleaning useless objects of ${NAME}]$(RESET)"
	@find . | grep -E "__pycache__" | xargs rm -rf
	@rm -rf .mypy_cache
	@rm -rf .pytest_cache
	@rm -rf .coverage

# Run the main file of a_maze_ing
run : a_maze_ing.py
	@python3 a_maze_ing.py $(CONFIG)

# Install the virtual environment.
venv:
	@echo "$(BLUE)Create virtual environment$(RESET)"
	@python3 -m venv $(VENV_PATH)
	@echo "$(BLUE)Run 'source $(VENV_PATH)/bin/activate' to go to the virtual environment."

# Checking flake8 and mypy norm
lint:	
	@echo "$(PINK)$(BOLD)[Checking mypy and flake8 norm]$(RESET)"
	@-flake8 ${SRC_FILES}
	@-mypy ${SRC_FILES} $(MYPY_FLAGS)

# Checking flake8 and mypy norm in strict mode
lint-strict:
	@echo "$(PINK)$(BOLD)[Checking mypy and flake8 norm is strict mode]$(RESET)"
	@-flake8 ${SRC_FILES}
	@-mypy ${SRC_FILES} $(MYPY_FLAGS) --strict

# Update pip requirements
pipfreeze:
	@pip freeze > requirements.txt

# Install virtual environment and all packages
all: venv install
	@echo "$(GREEN)✅ Environment set up ready!$(RESET)"

package:
	@echo "$(PINK)$(BOLD)🔨 Construction du package source (.tar.gz)...$(RESET)"
	@poetry build
	@echo "✅ Archivage terminé : $(TAR_FILE)"

# Prevent rule to be associated with files.
.PHONY: install clean run debug lint lint-strict all pipfreeze run venv package