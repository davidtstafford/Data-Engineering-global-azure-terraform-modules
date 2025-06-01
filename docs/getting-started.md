# Getting Started with Azure Terraform Modules

This guide will help you set up your development environment and start using the Azure Terraform modules in your projects.

## 🎯 Prerequisites

### Required Tools

- **Python 3.9+** installed locally
- **Git** for version control
- **Azure CLI** for authentication (optional but recommended)
- **Terraform** 1.0+ for running modules

### Optional Tools

- **Docker/Rancher Desktop** for containerized development
- **VS Code** for enhanced development experience

## 🚀 Quick Start for Module Users

If you just want to **use** these modules in your Terraform projects:

### 1. Reference Modules in Your Terraform

```hcl
# main.tf
module "resource_group" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/resource-group?ref=v1.0.0"
  
  name     = "my-data-platform-rg"
  location = "East US"
  
  tags = {
    Environment = "production"
    Project     = "data-platform"
    ManagedBy   = "terraform"
  }
}

module "storage_account" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/storage-account?ref=v1.0.0"
  
  name                = "mydataplatformsa"
  resource_group_name = module.resource_group.name
  location           = module.resource_group.location
  
  # Enable advanced features
  enable_https_traffic_only = true
  enable_blob_encryption    = true
  
  tags = module.resource_group.tags
}
```

### 2. Initialize and Apply

```bash
# Initialize Terraform
terraform init

# Plan deployment
terraform plan

# Apply changes
terraform apply
```

### 3. Version Pinning

Always pin to specific versions for stability:

```hcl
# Good: Pinned to specific version
source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/resource-group?ref=v1.2.1"

# Avoid: Using latest/main branch
source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/resource-group"
```

## 🛠️ Development Environment Setup

If you want to **contribute** to this repository or develop new modules:

### Option 1: Local Development (Recommended)

#### 1. Clone Repository

```bash
git clone https://github.com/your-org/azure-terraform-modules.git
cd azure-terraform-modules
```

#### 2. Install Poetry

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Verify installation
poetry --version
```

#### 3. Setup Development Environment

```bash
# Install all dependencies in single virtual environment
poetry install

# Activate virtual environment
poetry shell

# Verify tools are available
python --version
black --version
pytest --version
terraform --version  # Must be installed separately
```

#### 4. Install Terraform

```bash
# macOS with Homebrew
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Or download from https://terraform.io/downloads
```

#### 5. Configure Pre-commit Hooks

```bash
# Install pre-commit hooks (runs in virtual environment)
poetry run pre-commit install

# Test hooks
poetry run pre-commit run --all-files
```

## ✅ Verify Your Setup

### Check Python Environment

```bash
# Should show virtual environment path
which python

# Should show all development tools
poetry run pytest --version
poetry run black --version
poetry run flake8 --version
poetry run mypy --version
poetry run checkov --version
```

### Check Terraform

```bash
# Should show Terraform version 1.0+
terraform version

# Test Terraform validation
cd terraform/foundation/resource-group
terraform init
terraform validate
```

### Run Quality Checks

```bash
# Format Python code
poetry run black scripts/
poetry run isort scripts/

# Lint Python code
poetry run flake8 scripts/
poetry run mypy scripts/

# Run tests
poetry run pytest tests/ -v

# Security scan (if modules exist)
poetry run checkov -d terraform/
```

## 🗂️ Project Structure Overview

```
azure-terraform-modules/
├── README.md                    # Main project overview
├── CONTRIBUTING.md              # How to contribute
├── pyproject.toml              # Poetry dependencies and tool config
├── poetry.lock                 # Locked dependency versions
├── .gitignore                  # Git ignore patterns
├── .venv/                      # Virtual environment (created by Poetry)
├── docs/                       # Documentation
│   ├── getting-started.md      # This file
│   ├── module-development.md   # Creating new modules
│   └── examples.md             # Usage examples
├── scripts/                    # Development and validation scripts
│   ├── validate.py            # Terraform validation
│   └── format.py              # Code formatting
├── tests/                      # Python test files
│   └── test_*.py              # Test modules
├── examples/                   # Usage examples and compositions
└── terraform/                 # All Terraform modules
    ├── foundation/            # Core Azure resources
    ├── networking/            # Network-related resources
    ├── data/                  # Data platform resources
    └── databricks/           # Databricks ecosystem
```

## 🔧 Common Development Tasks

### Creating a New Module

```bash
# Create module directory structure
mkdir -p terraform/category/new-module/{examples/basic}

# Create required files
touch terraform/category/new-module/{README.md,main.tf,variables.tf,outputs.tf,versions.tf}
touch terraform/category/new-module/examples/basic/{main.tf,README.md}

# Follow module development guide
# See: docs/module-development.md
```

### Validating Changes

```bash
# Validate specific module
poetry run python scripts/validate.py --module terraform/foundation/resource-group

# Run full validation suite
poetry run python scripts/validate.py --all

# Format all code
poetry run python scripts/format.py
```

### Running Tests

```bash
# Run all tests
poetry run pytest tests/ -v

# Run tests with coverage
poetry run pytest tests/ --cov=scripts --cov-report=html

# Run specific test file
poetry run pytest tests/test_validate.py -v
```

## 🔐 Azure Authentication

For testing modules that interact with Azure:

### Azure CLI (Recommended)

```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "your-subscription-id"

# Verify authentication
az account show
```

### Service Principal (CI/CD)

```bash
# Create service principal
az ad sp create-for-rbac --name "terraform-modules-sp" --role="Contributor"

# Set environment variables
export ARM_CLIENT_ID="your-client-id"
export ARM_CLIENT_SECRET="your-client-secret"
export ARM_SUBSCRIPTION_ID="your-subscription-id"
export ARM_TENANT_ID="your-tenant-id"
```

## 📚 Next Steps

1. **Read the [Module Development Guide](module-development.md)** to learn how to create new modules
2. **Check out [Examples](examples.md)** for usage patterns and compositions
3. **Review [Contributing Guidelines](../CONTRIBUTING.md)** for development standards
4. **Explore existing modules** in the `terraform/` directory

## 🆘 Troubleshooting

### Common Issues

**Poetry not found**
```bash
# Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"
```

**Virtual environment issues**
```bash
# Remove and recreate virtual environment
poetry env remove python
poetry install
```

**Terraform validation fails**
```bash
# Ensure Terraform is installed and in PATH
terraform version

# Check module syntax
cd terraform/path/to/module
terraform validate
```

**Pre-commit hooks fail**
```bash
# Update pre-commit hooks
poetry run pre-commit autoupdate

# Skip hooks temporarily
git commit --no-verify
```

### Getting Help

- **Documentation**: Check the `docs/` folder
- **Issues**: Create a GitHub Issue
- **Discussions**: Use GitHub Discussions for questions
- **Contributing**: See `CONTRIBUTING.md`

---

🚀 **You're ready to start using and contributing to Azure Terraform Modules!**
