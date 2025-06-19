.PHONY: install install-dev install-all isort black ruff format lint

DEV_PACKAGES = pytest ruff isort black

# Create venv and install deps, register kernel
setup:
	test -d .venv || uv venv .venv
	uv sync
	uv run python -m ipykernel install --user --name=tm-vctoolbox --display-name "tm-vctoolbox"

# Create venv and install deps with native TLS support, register kernel
setup-native-tls:
	test -d .venv || uv venv .venv
	uv --native-tls sync
	uv run python -m ipykernel install --user --name=tm-vctoolbox --display-name "tm-vctoolbox"

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

# Clean lockfile and __pycache__
clean:
	rm -f uv.lock
	find . -type d -name '__pycache__' -exec rm -rf {} +