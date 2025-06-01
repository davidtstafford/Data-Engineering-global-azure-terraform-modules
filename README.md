# Azure Terraform Modules for Data Engineering

A collection of reusable, production-ready Terraform modules for building Azure data engineering platforms. These modules are designed to be referenced from other repositories using Git tags for reliable version control.

## 🎯 Purpose

This repository provides standardized Terraform modules that data engineering teams can use to quickly deploy consistent, secure Azure infrastructure. Each module follows best practices and can be composed together to build complete data platforms.

## 🏗️ Module Philosophy

- **Reusable**: Modules can be used across multiple projects and environments
- **Versioned**: Git tags ensure stability and controlled updates
- **Secure**: Built-in security best practices and compliance
- **Documented**: Clear usage examples and parameter documentation
- **Tested**: Automated validation and testing

## 📁 Repository Structure

```
azure-terraform-modules/
├── README.md                    # Main project overview
├── PROJECT_PLAN.md             # Implementation plan with checkboxes
├── CONTRIBUTING.md              # Contribution guidelines  
├── pyproject.toml              # Poetry dependencies and Python config
├── Makefile                    # Development commands and workflows
├── .gitignore                  # Git ignore patterns

│   └── Dockerfile              # Development environment image
├── .github/                    # GitHub Actions and templates
│   ├── workflows/              
│   │   └── validate.yml        # CI/CD pipeline
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/                       # Documentation
│   ├── getting-started.md      # Setup and usage guide
│   ├── module-development.md   # How to create new modules
│   └── examples.md             # Usage examples
├── scripts/                    # Development and validation scripts
│   ├── validate.py            # Terraform validation
│   └── format.py              # Code formatting
├── examples/                   # Usage examples and compositions
│   └── README.md              # Examples documentation
└── terraform/                 # All Terraform modules (CATEGORIZED STRUCTURE)
    ├── README.md              # Terraform modules overview
    ├── foundation/            # Core Azure resources
    │   ├── README.md
    │   ├── resource-group/    # Azure Resource Group
    │   ├── storage-account/   # Azure Storage Account
    │   └── key-vault/        # Azure Key Vault
    ├── networking/            # Network-related resources
    │   ├── README.md
    │   ├── virtual-network/   # Virtual Network and subnets
    │   └── private-endpoints/ # Private connectivity
    ├── data/                  # Data platform resources
    │   ├── README.md
    │   ├── eventhub/         # Azure Event Hubs
    │   ├── sql-database/     # Azure SQL Database
    │   ├── data-factory/     # Azure Data Factory
    │   └── synapse/          # Azure Synapse Analytics
    └── databricks/           # Databricks ecosystem
        ├── README.md
        ├── workspace/        # Databricks Workspace (foundation)
        ├── compute/          # Databricks Compute Clusters
        ├── unity-catalog/    # Databricks Unity Catalog
        └── notebooks/        # Databricks Notebook Management
```

## 🚀 Quick Start

### Using Modules in Your Project

Reference modules in your Terraform configuration using Git tags:

```hcl
module "resource_group" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/resource-group?ref=v1.0.0"
  
  name     = "my-data-platform-rg"
  location = "East US"
  tags = {
    Environment = "production"
    Project     = "data-platform"
  }
}

module "storage_account" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/storage-account?ref=v1.0.0"
  
  name                = "mydataplatformsa"
  resource_group_name = module.resource_group.name
  location           = module.resource_group.location
  # ... other configuration
}
```

### Development Setup

#### Prerequisites
- **Terraform** (latest version)
- **Azure CLI** (latest version)
- **Python** (3.11+) with Poetry
- **VS Code** (recommended editor)
- **Git** for version control

#### Local Development Setup
Setup your development environment locally:

1. **Install dependencies**:

   **On macOS (using Homebrew):**
   ```bash
   # Install Homebrew if not already installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install Azure CLI
   brew install azure-cli
   
   # Install Terraform (Note: Due to licensing changes, consider OpenTofu as alternative)
   brew install terraform
   
   # Install Poetry for Python dependency management
   curl -sSL https://install.python-poetry.org | python3 -
   ```

   **On other platforms:**
   - **Terraform**: Download from https://terraform.io/downloads
   - **Azure CLI**: Follow instructions at https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
   - **Poetry**: Follow instructions at https://python-poetry.org/docs/#installation

   **Verify installations:**
   ```bash
   az --version          # Should show Azure CLI version
   terraform --version   # Should show Terraform version  
   poetry --version      # Should show Poetry version
   ```

   **⚠️ Note about Terraform Licensing:**
   HashiCorp changed Terraform's license to Business Source License (BUSL) starting from version 1.6+. For production environments, consider using [OpenTofu](https://opentofu.org/) (the open-source fork) instead:
   ```bash
   # Alternative: Install OpenTofu (fully compatible with Terraform)
   brew install opentofu
   ```

2. **Clone and setup**:
   ```bash
   git clone https://github.com/your-org/azure-terraform-modules.git
   cd azure-terraform-modules
   make install        # Install Python dependencies and pre-commit hooks
   ```

3. **Start developing**:
   ```bash
   make help           # See all commands
   make install        # Ensure everything is ready
   make pre-commit     # Quick validation
   ```

## 🛠️ Development Commands

```bash
# Environment setup
make setup              # Setup local development environment
make help               # Show all available commands

# Code quality
make validate           # Validate all Terraform modules
make format             # Format Terraform and Python code
make lint               # Run code linting

# Development workflow
make test               # Run full test suite (container required)
make clean              # Clean temporary files
```

## 🧪 Testing Framework

This repository includes a comprehensive testing framework for validating Terraform modules without requiring Azure authentication or actual resource deployment. The framework provides fast, reliable validation of module syntax, structure, and configuration.

### Testing Types

#### 1. **Validation Testing** (Recommended for CI/CD)
Fast validation tests that check module syntax, structure, and configuration without requiring Azure authentication:

```bash
make test-terraform     # Run all validation tests (~90 seconds)
make test-all          # Run both Python and Terraform validation tests
```

**What it validates:**
- ✅ HCL syntax and formatting
- ✅ Module structure (required files, variables, outputs)
- ✅ Provider configuration compatibility
- ✅ Variable usage and validation rules
- ✅ Multiple configuration scenarios
- ✅ Azure region compatibility

#### 2. **Plan Testing** (Optional - Requires Azure Auth)
Full resource planning tests that validate actual Azure resource configurations:

```bash
make test-terraform-plan    # Run plan tests (requires Azure CLI login)
```

### Test Structure

The testing framework is organized under `tests/terraform/`:

```
tests/terraform/
├── __init__.py                           # Python module init
├── base_validation.py                    # Core validation testing infrastructure
├── config.py                            # Test configuration and utilities
├── fixtures/                            # Test data and configurations
│   ├── __init__.py
│   └── test_data.py
└── modules/                             # Module-specific tests
    ├── __init__.py
    └── test_resource_group_validation.py  # Resource group validation tests
```

### Azure Authentication for Plan Testing

The plan-based tests require Azure CLI authentication to validate actual resource configurations. Here's how to set it up:

#### Prerequisites
- Azure CLI installed (`az --version`)
- Access to an Azure subscription
- Appropriate permissions to create resources

#### Authentication Steps

1. **Login to Azure CLI:**
   ```bash
   az login
   ```
   This will open a browser window for authentication.

2. **Set the correct subscription (if you have multiple):**
   ```bash
   az account list --output table
   az account set --subscription "Your-Subscription-Name-or-ID"
   ```

3. **Verify authentication:**
   ```bash
   az account show
   ```

4. **Run plan-based tests:**
   ```bash
   make test-terraform-plan
   ```

#### Common Authentication Errors

**Error: `subscription_id` is a required provider property**
- **Solution**: Run `az login` and ensure you're authenticated
- **Verify**: `az account show` should display your subscription details

**Error: Please run 'az login' to setup account**
- **Solution**: Your Azure CLI session has expired, run `az login` again

**Error: You do not have permission to perform this operation**
- **Solution**: Ensure your account has appropriate permissions in the Azure subscription

#### Plan Testing vs Validation Testing

| Feature            | Validation Testing        | Plan Testing                 |
| ------------------ | ------------------------- | ---------------------------- |
| **Authentication** | ❌ Not required            | ✅ Azure CLI required         |
| **Speed**          | ⚡ Fast (~90 seconds)      | 🐌 Slower (~5-10 minutes)     |
| **Coverage**       | Syntax, structure, config | Full resource planning       |
| **CI/CD Ready**    | ✅ Yes                     | ⚠️ Requires Azure credentials |
| **Use Case**       | Daily development         | Pre-deployment validation    |

### Adding Tests for New Modules

When creating a new Terraform module, add corresponding validation tests:

1. **Create test file**: `tests/terraform/modules/test_<module_name>_validation.py`
2. **Inherit from base class**: Use `TerraformValidationTest` for structure
3. **Add test scenarios**: Include various configuration combinations
4. **Update Makefile**: Add module-specific test targets if needed

**Example test structure:**
```python
from tests.terraform.base_validation import TerraformValidationTest

class TestMyModuleValidation(TerraformValidationTest):
    def setup_method(self):
        super().setup_method()
        self.module_path = self.terraform_root / "path" / "to" / "my-module"
    
    def test_module_validation_basic(self):
        """Test basic module validation."""
        self.run_terraform_validation(self.module_path)
```

### Recommended Testing Workflow

Follow this workflow for efficient Terraform module development and validation:

#### Daily Development (Fast Loop)
```bash
# 1. Make code changes to your Terraform module
# 2. Run fast validation tests (only tests changed modules)
make test-terraform          # Smart: only tests affected modules (~30-90 seconds)

# 3. Run comprehensive checks before committing
make check                   # Includes formatting, linting, security, and validation
```

#### Pre-Deployment Validation (Optional)
```bash
# 1. Authenticate with Azure
az login

# 2. Run comprehensive plan-based tests (only for changed modules)
make test-terraform-plan     # Smart: only tests affected modules (~2-5 minutes)

# 3. Verify all tests pass before deployment
```

#### Full Testing (When Needed)
```bash
# Test ALL modules (use sparingly - gets slow with many modules)
make test-terraform-all      # Tests all modules (~90 seconds per module)
make test-terraform-plan-all # Plan tests for all modules (~5 minutes per module)
```

#### CI/CD Pipeline Configuration
- **Pull Request Checks**: Use `make test-terraform` (validation only, no Azure auth)
- **Pre-Deployment**: Optionally run `make test-terraform-plan` with Azure service principal
- **Regular Validation**: Include `make check` in all CI/CD pipelines

#### When to Use Each Test Type

| Scenario              | Validation Tests       | Plan Tests               | Smart Testing          |
| --------------------- | ---------------------- | ------------------------ | ---------------------- |
| **Local Development** | ✅ Changed modules only | ⚠️ Optional               | 🚀 ~30-90 seconds       |
| **Pull Request CI**   | ✅ Changed modules only | ❌ Skip (auth complexity) | 🚀 Scales with changes  |
| **Pre-Deployment**    | ✅ Changed modules only | ✅ Changed modules only   | ⚡ Fast feedback        |
| **Release Pipeline**  | ✅ All modules          | ✅ All modules            | ⚠️ Use `*-all` commands |

### Smart Testing (Changed Modules Only)

The testing framework automatically detects which Terraform modules have been modified and runs tests only for those modules. This provides:

**🚀 Scalability Benefits:**
- **1 module changed** = ~90 seconds (instead of testing all modules)
- **10 modules in project** = Still ~90 seconds if only 1 changed
- **20 modules in project** = Still ~90 seconds if only 1 changed

**🔍 Change Detection:**
- Detects changes compared to `main` branch
- Includes uncommitted local changes
- Supports staged and unstaged files
- Automatically maps file changes to affected modules

**📁 Available Commands:**
```bash
make test-terraform          # Smart: test changed modules only
make test-terraform-plan     # Smart: plan test changed modules only  
make test-terraform-all      # Test ALL modules (use when needed)
make test-terraform-plan-all # Plan test ALL modules (very slow)
```

**When to Use Each:**
- **Daily development**: Use smart commands (`test-terraform`)
- **Before major releases**: Use full commands (`test-terraform-all`) 
- **CI/CD pipelines**: Use smart commands for fast feedback
- **Troubleshooting**: Use full commands to validate everything

### Framework Benefits

- **🚀 Fast**: Validation tests run in ~90 seconds without Azure authentication
- **🔒 Secure**: No Azure credentials required for basic validation
- **🏗️ Extensible**: Easy to add tests for new modules
- **🔄 CI/CD Ready**: Perfect for automated testing in pipelines
- **📊 Comprehensive**: Covers syntax, structure, and configuration validation

### Technical Details

For comprehensive information about the testing framework architecture, configuration options, and advanced usage, see the [Terraform Testing Framework Documentation](docs/terraform-testing-framework.md).

## 📚 Documentation

- **[Getting Started](docs/getting-started.md)** - Detailed setup instructions
- **[Module Development](docs/module-development.md)** - How to create new modules
- **[Terraform Testing Framework](docs/terraform-testing-framework.md)** - Testing infrastructure documentation
- **[Examples](docs/examples.md)** - Usage patterns and compositions
- **[Contributing](CONTRIBUTING.md)** - Contribution guidelines

## 🔧 Available Modules

### Foundation Modules
| Module                                                   | Purpose               | Status      |
| -------------------------------------------------------- | --------------------- | ----------- |
| [resource-group](terraform/foundation/resource-group/)   | Azure Resource Group  | ✅ Available |
| [storage-account](terraform/foundation/storage-account/) | Azure Storage Account | 🚧 Planned   |
| [key-vault](terraform/foundation/key-vault/)             | Azure Key Vault       | 🚧 Planned   |

### Networking Modules
| Module                                                       | Purpose              | Status    |
| ------------------------------------------------------------ | -------------------- | --------- |
| [virtual-network](terraform/networking/virtual-network/)     | Virtual Network      | 🚧 Planned |
| [private-endpoints](terraform/networking/private-endpoints/) | Private connectivity | 🚧 Planned |

### Data Platform Modules  
| Module                                       | Purpose             | Status    |
| -------------------------------------------- | ------------------- | --------- |
| [eventhub](terraform/data/eventhub/)         | Event streaming     | 🚧 Planned |
| [sql-database](terraform/data/sql-database/) | Relational database | 🚧 Planned |
| [data-factory](terraform/data/data-factory/) | Data integration    | 🚧 Planned |
| [synapse](terraform/data/synapse/)           | Analytics platform  | 🚧 Planned |

### Databricks Modules
| Module                                               | Purpose              | Status    |
| ---------------------------------------------------- | -------------------- | --------- |
| [workspace](terraform/databricks/workspace/)         | Workspace foundation | 🚧 Planned |
| [compute](terraform/databricks/compute/)             | Compute clusters     | 🚧 Planned |
| [unity-catalog](terraform/databricks/unity-catalog/) | Data governance      | 🚧 Planned |
| [notebooks](terraform/databricks/notebooks/)         | Notebook management  | 🚧 Planned |

## 🏷️ Versioning

This repository uses semantic versioning with Git tags:

- **v1.0.0** - Major version (breaking changes)
- **v1.1.0** - Minor version (new features, backwards compatible)
- **v1.1.1** - Patch version (bug fixes)

Always reference specific versions in your projects for stability:
```hcl
source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/resource-group?ref=v1.0.0"
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for:

- How to propose new modules
- Development workflow and standards
- Testing requirements
- Documentation standards

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and general discussion
- **Documentation**: Check the [docs/](docs/) folder for detailed guides

---

**🚀 Ready to get started?** Check out our [Getting Started Guide](docs/getting-started.md) or jump into the [examples](examples/) folder!