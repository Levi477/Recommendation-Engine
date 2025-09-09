.PHONY: help install install-dev clean test lint format type-check validate build upload
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := pip
PACKAGE_NAME := t2v

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install package in development mode
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

install-dev: ## Install package with development dependencies
	$(PIP) install -r requirements.txt
	$(PIP) install -e ".[dev]"

clean: ## Clean build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test: ## Run tests
	pytest

test-verbose: ## Run tests with verbose output
	pytest -v

test-coverage: ## Run tests with coverage report
	pytest --cov=$(PACKAGE_NAME) --cov-report=html --cov-report=term-missing

lint: ## Run linting checks
	flake8 src/ tests/

format: ## Format code with black
	black src/ tests/

format-check: ## Check code formatting without making changes
	black --check src/ tests/

type-check: ## Run type checking with mypy
	mypy src/$(PACKAGE_NAME)/

validate: ## Run all validation checks (lint, format, type)
	$(MAKE) format-check
	$(MAKE) lint
	$(MAKE) type-check
	$(MAKE) test

pre-commit: ## Run pre-commit checks
	$(MAKE) format
	$(MAKE) validate

build: ## Build distribution packages
	$(PYTHON) -m build

build-wheel: ## Build wheel package only
	$(PYTHON) -m build --wheel

build-sdist: ## Build source distribution only
	$(PYTHON) -m build --sdist

upload-test: ## Upload to test PyPI
	twine upload --repository testpypi dist/*

upload: ## Upload to PyPI
	twine upload dist/*

check-package: ## Check package integrity
	twine check dist/*

dev-setup: ## Set up development environment
	$(MAKE) install-dev
	pre-commit install

init: ## Initialize the T2V system
	$(PACKAGE_NAME) init

status: ## Show T2V system status
	$(PACKAGE_NAME) status

env-validate: ## Validate environment requirements
	$(PACKAGE_NAME) validate

docker-build: ## Build Docker image (if Dockerfile exists)
	@if [ -f Dockerfile ]; then \
		docker build -t $(PACKAGE_NAME):latest .; \
	else \
		echo "No Dockerfile found"; \
	fi

docker-run: ## Run Docker container (if image exists)
	@if docker image inspect $(PACKAGE_NAME):latest >/dev/null 2>&1; then \
		docker run -it --rm $(PACKAGE_NAME):latest; \
	else \
		echo "Docker image not found. Run 'make docker-build' first."; \
	fi

docs: ## Generate documentation (if supported)
	@echo "Documentation available in docs/ directory"
	@echo "See docs/README.md for API reference"

version: ## Show current version
	$(PYTHON) -c "import $(PACKAGE_NAME); print($(PACKAGE_NAME).__version__)"

requirements-update: ## Update requirements.txt with current environment
	pip freeze > requirements.txt

security-check: ## Run security checks (if bandit is available)
	@if command -v bandit >/dev/null 2>&1; then \
		bandit -r src/; \
	else \
		echo "Install bandit for security checks: pip install bandit"; \
	fi