# Force Git Bash on Windows 
SHELL := C:/Program Files/Git/bin/bash.exe

# Linting
lint:
	bash scripts/lint.sh

# Cleaning
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete


# Help command
help:
	@echo "Available commands:"
	@echo "  lint         : Run code formatters and linters"
	@echo "  clean        : Remove Python cache files and build artifacts"
