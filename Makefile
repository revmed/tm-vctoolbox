.PHONY: install install-dev install-all isort black ruff format lint

DEV_PACKAGES = pytest ruff isort black

# Install main dependencies + your package in editable mode
install:
	uv --native-tls pip install -e .


# Install dev dependencies
install-dev:
	uv --native-tls pip install $(DEV_PACKAGES)

# Install all dependencies (main + dev)
install-all: install install-dev

# Sort imports with isort (using black profile)
isort:
	isort --profile black .

# Format code with black
black:
	black .

# Run ruff to lint and fix
ruff:
	ruff check . --fix

# Run all formatting tools: isort, black, ruff
format: isort black ruff

# Just lint without fixing (ruff)
lint:
	ruff check .
