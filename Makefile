# Azure Terraform Modules - Development Makefile
# =================================================
# This Makefile provides simple commands for common development tasks
# Run 'make help' to see all available commands

.PHONY: help install clean test lint format security check validate all pre-commit terraform-check terraform-format

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

help: ## Show this help message
	@echo "$(BLUE)Azure Terraform Modules - Development Commands$(RESET)"
	@echo "================================================="
	@echo ""
	@echo "$(GREEN)Quick Start:$(RESET)"
	@echo "  make install       # Set up development environment"
	@echo "  make pre-commit    # Run pre-commit hooks (fast, essential checks)"
	@echo "  make check         # Run comprehensive checks (slower, includes tests)"
	@echo "  make commit-ready  # Full validation before committing"
	@echo ""
	@echo "$(YELLOW)Development Workflow:$(RESET)"
	@echo "  1. make install           # One-time setup"
	@echo "  2. make pre-commit        # Quick checks while developing"
	@echo "  3. make check             # Before committing (comprehensive)"
	@echo ""
	@echo "$(GREEN)Available commands:$(RESET)"
	@awk 'BEGIN {FS = ":.*##"; printf ""} /^[a-zA-Z_-]+:.*?##/ { printf "  $(BLUE)%-15s$(RESET) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install: ## Install all dependencies and set up development environment
	@echo "$(BLUE)Installing Poetry dependencies...$(RESET)"
	poetry install --no-interaction
	@echo "$(BLUE)Installing pre-commit hooks...$(RESET)"
	poetry run pre-commit install
	@echo "$(GREEN)✓ Development environment ready!$(RESET)"

clean: ## Clean up cache files and temporary directories
	@echo "$(BLUE)Cleaning up cache files...$(RESET)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -f audit-report.json 2>/dev/null || true
	rm -f .coverage 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete!$(RESET)"

format: ## Format code using black and isort
	@echo "$(BLUE)Formatting Python code...$(RESET)"
	poetry run black .
	poetry run isort .
	@echo "$(GREEN)✓ Code formatting complete!$(RESET)"

lint: ## Run linting checks (flake8, mypy)
	@echo "$(BLUE)Running linting checks...$(RESET)"
	poetry run flake8 .
	poetry run mypy scripts/ tests/
	@echo "$(GREEN)✓ Linting checks passed!$(RESET)"

security: ## Run security checks (bandit, safety)
	@echo "$(BLUE)Running security scans...$(RESET)"
	poetry run bandit -c .bandit -r scripts/ tests/
	poetry run safety check --continue-on-error
	@echo "$(GREEN)✓ Security checks complete!$(RESET)"

test: ## Run all Python tests with coverage
	@echo "$(BLUE)Running Python tests...$(RESET)"
	poetry run pytest --cov=scripts --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)✓ All tests passed!$(RESET)"

terraform-check: ## Validate and check Terraform modules
	@echo "$(BLUE)Validating Terraform modules...$(RESET)"
	@for dir in $$(find terraform -name "*.tf" -exec dirname {} \; | sort -u); do \
		echo "$(YELLOW)Checking $$dir...$(RESET)"; \
		cd $$dir && terraform init -backend=false && terraform validate && cd - > /dev/null; \
	done
	@echo "$(GREEN)✓ Terraform validation complete!$(RESET)"

terraform-format: ## Format Terraform files
	@echo "$(BLUE)Formatting Terraform files...$(RESET)"
	terraform fmt -recursive terraform/
	@echo "$(GREEN)✓ Terraform formatting complete!$(RESET)"

checkov: ## Run Checkov security scans on Terraform
	@echo "$(BLUE)Running Checkov security scans...$(RESET)"
	poetry run checkov -d terraform/ --framework terraform
	@echo "$(GREEN)✓ Checkov security scan complete!$(RESET)"

validate: ## Run validation scripts
	@echo "$(BLUE)Running validation scripts...$(RESET)"
	poetry run python scripts/validate.py
	@echo "$(GREEN)✓ Validation complete!$(RESET)"

pre-commit: ## Run pre-commit hooks (fast checks - same as git commit will run)
	@echo "$(BLUE)Running pre-commit hooks (formatting, linting, basic security)...$(RESET)"
	poetry run pre-commit run --all-files
	@echo "$(GREEN)✓ Pre-commit checks complete! (This is what git commit runs)$(RESET)"

quick-check: pre-commit ## Alias for pre-commit (quick formatting and linting)

check: ## Run comprehensive checks (format, lint, security, test, terraform)
	@echo "$(BLUE)Running comprehensive checks (this may take a while)...$(RESET)"
	@echo "$(YELLOW)Step 1/5: Running pre-commit hooks...$(RESET)"
	$(MAKE) pre-commit
	@echo "$(YELLOW)Step 2/5: Running dependency security check...$(RESET)"
	poetry run safety check --continue-on-error
	@echo "$(YELLOW)Step 3/5: Running tests with coverage...$(RESET)"
	$(MAKE) test
	@echo "$(YELLOW)Step 4/5: Checking Terraform...$(RESET)"
	$(MAKE) terraform-check terraform-format
	@echo "$(YELLOW)Step 5/5: Running validation scripts...$(RESET)"
	$(MAKE) validate
	@echo "$(GREEN)✓ All comprehensive checks passed! 🚀$(RESET)"

commit-ready: check ## Ensure code is ready for commit (comprehensive validation)
	@echo "$(GREEN)✓ Code is ready for commit!$(RESET)"
	@echo "$(BLUE)To commit your changes:$(RESET)"
	@echo "  git add ."
	@echo "  git commit -m 'Your commit message'"
	@echo ""
	@echo "$(YELLOW)Note: Git commit will automatically run the fast pre-commit hooks$(RESET)"

all: clean check ## Clean and run all checks

ci: ## Run CI-like checks (what GitHub Actions will run)
	@echo "$(BLUE)Running CI-like checks...$(RESET)"
	@echo "$(YELLOW)Checking Poetry lock file...$(RESET)"
	poetry check
	@echo "$(YELLOW)Installing dependencies...$(RESET)"
	poetry install --no-interaction
	@echo "$(YELLOW)Running all checks...$(RESET)"
	$(MAKE) check
	@echo "$(GREEN)✓ CI checks complete!$(RESET)"

dev-setup: install ## Alias for install (more intuitive name)

# Documentation
docs: ## Generate/update documentation
	@echo "$(BLUE)Documentation tasks...$(RESET)"
	@echo "$(YELLOW)Documentation generation not yet implemented$(RESET)"
	@echo "$(GREEN)✓ Documentation task complete!$(RESET)"

# Release helpers
version: ## Show current version
	@echo "$(BLUE)Current version:$(RESET)"
	@poetry version --short

# Debugging helpers
debug-env: ## Show development environment info
	@echo "$(BLUE)Development Environment Info:$(RESET)"
	@echo "Python version: $$(python --version)"
	@echo "Poetry version: $$(poetry --version)"
	@echo "Current directory: $$(pwd)"
	@echo "Virtual environment: $$(poetry env info --path)"
	@echo "Installed packages:"
	@poetry show --tree
