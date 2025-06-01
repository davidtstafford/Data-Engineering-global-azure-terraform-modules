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
	@if [ -f /.dockerenv ]; then \
		echo "$(GREEN)🐳 Running in Dev Container$(RESET)"; \
		echo ""; \
	fi
	@echo "$(GREEN)Quick Start:$(RESET)"
	@if [ -f /.dockerenv ]; then \
		echo "  $(BLUE)🐳 You're in the dev container!$(RESET)"; \
		echo "  make health-check  # Verify all tools are working"; \
		echo "  make install       # Ensure dependencies are installed"; \
		echo "  make pre-commit    # Run fast checks"; \
		echo "  make check         # Run comprehensive checks"; \
	else \
		echo "  $(YELLOW)💻 Local development:$(RESET)"; \
		echo "  make health-check  # Check what tools are missing"; \
		echo "  make install       # Set up development environment"; \
		echo "  make pre-commit    # Run fast checks"; \
		echo "  $(BLUE)🐳 Or use dev container (recommended):$(RESET)"; \
		echo "  1. Open in VS Code"; \
		echo "  2. 'Dev Containers: Reopen in Container'"; \
	fi
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

# Development Container helpers
container-info: ## Show development container information
	@echo "$(BLUE)Development Container Info:$(RESET)"
	@if [ -f /.dockerenv ]; then \
		echo "$(GREEN)✓ Running in container$(RESET)"; \
		echo "Container OS: $$(cat /etc/os-release | grep PRETTY_NAME | cut -d'=' -f2 | tr -d '\"')"; \
		echo "Container User: $$(whoami)"; \
		echo "Working Directory: $$(pwd)"; \
		echo "Available Tools:"; \
		echo "  - Terraform: $$(terraform version -json | jq -r '.terraform_version' 2>/dev/null || echo 'not available')"; \
		echo "  - Azure CLI: $$(az version --output tsv --query 'azure-cli' 2>/dev/null || echo 'not available')"; \
		echo "  - Pre-commit: $$(pre-commit --version 2>/dev/null || echo 'not available')"; \
		echo "  - Checkov: $$(checkov --version 2>/dev/null || echo 'not available')"; \
	else \
		echo "$(YELLOW)⚠️  Not running in development container$(RESET)"; \
		echo "To use the dev container:"; \
		echo "  1. Open project in VS Code"; \
		echo "  2. Install Dev Containers extension"; \
		echo "  3. Command Palette → 'Dev Containers: Reopen in Container'"; \
	fi

health-check: ## Run comprehensive development environment health check
	@echo "$(BLUE)Running development environment health check...$(RESET)"
	@if [ -f scripts/health_check.py ]; then \
		poetry run python scripts/health_check.py; \
	else \
		bash scripts/container-health-check.sh; \
	fi

demo: ## Quick demo showing local vs container environment
	@echo "$(BLUE)🔍 Quick Environment Check$(RESET)"
	@echo "=========================="
	@echo ""
	@if [ -f /.dockerenv ]; then \
		echo "$(GREEN)🐳 You're running in the dev container!$(RESET)"; \
		echo "This means all tools are pre-installed and ready to use."; \
	else \
		echo "$(YELLOW)💻 You're running locally on your Mac$(RESET)"; \
		echo "Some tools may not be installed."; \
	fi
	@echo ""
	@echo "Tool availability:"
	@if command -v terraform >/dev/null 2>&1; then \
		echo "  $(GREEN)✓ Terraform$(RESET) - Available"; \
	else \
		echo "  $(RED)❌ Terraform$(RESET) - Not found"; \
	fi
	@if command -v az >/dev/null 2>&1; then \
		echo "  $(GREEN)✓ Azure CLI$(RESET) - Available"; \
	else \
		echo "  $(RED)❌ Azure CLI$(RESET) - Not found"; \
	fi
	@if command -v poetry >/dev/null 2>&1; then \
		echo "  $(GREEN)✓ Poetry$(RESET) - Available"; \
	else \
		echo "  $(RED)❌ Poetry$(RESET) - Not found"; \
	fi
	@echo ""
	@if [ -f /.dockerenv ]; then \
		echo "$(GREEN)🎉 All set! You can run:$(RESET)"; \
		echo "  • make pre-commit     # Fast validation"; \
		echo "  • make check          # Comprehensive checks"; \
		echo "  • terraform --version # Check Terraform"; \
	else \
		echo "$(BLUE)💡 To get all tools instantly:$(RESET)"; \
		echo "  1. Open this project in VS Code"; \
		echo "  2. Install 'Dev Containers' extension"; \
		echo "  3. Command Palette → 'Dev Containers: Reopen in Container'"; \
		echo "  4. Wait for setup (3-5 minutes first time)"; \
		echo "  5. Run 'make demo' again!"; \
	fi

azure-login: ## Login to Azure CLI (for container development)
	@echo "$(BLUE)Logging into Azure CLI...$(RESET)"
	@if command -v az >/dev/null 2>&1; then \
		az login --use-device-code; \
		echo "$(GREEN)✓ Azure login complete!$(RESET)"; \
	else \
		echo "$(RED)❌ Azure CLI not found$(RESET)"; \
	fi

container-reset: ## Reset development container environment (clear caches, reinstall)
	@echo "$(BLUE)Resetting development container environment...$(RESET)"
	$(MAKE) clean
	poetry cache clear pypi --all || true
	poetry install --no-interaction
	poetry run pre-commit clean
	poetry run pre-commit install --install-hooks
	@echo "$(GREEN)✓ Container environment reset complete!$(RESET)"
