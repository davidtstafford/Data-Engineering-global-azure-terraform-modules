# Azure Terraform Modules for Data Engineering

A collection of reusable, production-ready Terrafor### Development Setup

Choose the development environment that works best for your platform:

#### Option 1: Dev Container (Recommended for Windows, Alternative for Mac/Linux)

**🎯 Why use the dev container?**
- ✅ **Zero manual setup** - All tools automatically installed and configured
- ✅ **Cross-platform consistency** - Works identically on Windows, Mac, and Linux
- ✅ **Windows compatibility** - Eliminates Linux command issues on Windows
- ✅ **Isolated environment** - No conflicts with your host system
- ✅ **Pre-configured VS Code** - Extensions and settings ready to go

**Prerequisites:**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or [Rancher Desktop](https://rancherdesktop.io/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

**Setup Steps:**
1. **Install prerequisites** (if not already installed)
2. **Clone the repository:**
   ```bash
   git clone https://github.com/davidtstafford/Data-Engineering-global-azure-terraform-modules.git
   cd Data-Engineering-global-azure-terraform-modules
   ```
3. **Open in VS Code:**
   ```bash
   code .
   ```
4. **Reopen in Container:**
   - When prompted, click "Reopen in Container"
   - Or use Command Palette (Ctrl/Cmd+Shift+P): `Dev Containers: Reopen in Container`
5. **Wait for automatic setup** - The container will install:
   - Python 3.11 + Poetry
   - Terraform  
   - Azure CLI
   - Git
   - All VS Code extensions
   - All project dependencies via `make install`

**Ready to develop!** All commands work identically to local development.

#### Option 2: Local Development Setup (Mac/Linux)

For Mac/Linux users who prefer local development:

**Prerequisites:**
- **Terraform** (latest version)
- **Azure CLI** (latest version)
- **Python** (3.11+) with Poetry
- **VS Code** (recommended editor)
- **Git** for version control

**Setup Steps:**
1. **Install dependencies:** building Azure data engineering platforms. These modules are designed to be referenced from other repositories using Git tags for reliable version control.

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
├── .devcontainer/              # Dev container configuration
│   └── devcontainer.json       # Container setup with auto-installed tools
├── .github/                    # GitHub Actions and templates
│   ├── workflows/              
│   │   └── validate.yml        # CI/CD pipeline
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/                       # Documentation
│   ├── getting-started.md      # Setup and usage guide
│   ├── module-development.md   # How to create new modules
│   ├── terraform-testing-framework.md # Testing framework docs
│   └── examples.md             # Usage examples
├── scripts/                    # Development and validation scripts
│   ├── validate.py            # Terraform validation
│   ├── format.py              # Code formatting
│   └── test_changed_modules.py # Smart testing script
├── examples/                   # Usage examples and compositions
│   └── README.md              # Examples documentation
├── tests/                     # Testing framework
│   ├── terraform/             # Terraform module tests
│   └── *.py                   # Python tests
└── terraform/                 # All Terraform modules (CATEGORIZED STRUCTURE)
    ├── README.md              # Terraform modules overview
    ├── foundation/            # Core Azure resources
    │   ├── README.md
    │   ├── resource-group/    # Azure Resource Group
    │   ├── diagnostic-settings/ # Azure Diagnostic Settings
    │   ├── storage-account/   # Azure Storage Account (planned)
    │   └── key-vault/        # Azure Key Vault (planned)
    ├── networking/            # Network-related resources (planned)
    │   ├── README.md
    │   ├── virtual-network/   # Virtual Network and subnets
    │   └── private-endpoints/ # Private connectivity
    ├── data/                  # Data platform resources (planned)
    │   ├── README.md
    │   ├── eventhub/         # Azure Event Hubs
    │   ├── sql-database/     # Azure SQL Database
    │   ├── data-factory/     # Azure Data Factory
    │   └── synapse/          # Azure Synapse Analytics
    └── databricks/           # Databricks ecosystem (planned)
        ├── README.md
        ├── workspace/        # Databricks Workspace (foundation)
        ├── compute/          # Databricks Compute Clusters
        ├── unity-catalog/    # Databricks Unity Catalog
        └── notebooks/        # Databricks Notebook Management
```

## 🚀 Quick Start

**💡 New to development?** Consider our [dev container](#option-1-dev-container-recommended-for-windows-alternative-for-maclinux) for zero-configuration setup that works consistently across Windows, Mac, and Linux.

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

Choose the development environment that works best for your platform:

#### Option 1: Dev Container (Recommended for Windows, Alternative for Mac/Linux)

**🎯 Why use the dev container?**
- ✅ **Zero manual setup** - All tools automatically installed and configured
- ✅ **Cross-platform consistency** - Works identically on Windows, Mac, and Linux
- ✅ **Windows compatibility** - Eliminates Linux command issues on Windows
- ✅ **Isolated environment** - No conflicts with your host system
- ✅ **Pre-configured VS Code** - Extensions and settings ready to go

**Prerequisites:**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or [Rancher Desktop](https://rancherdesktop.io/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

**Setup Steps:**
1. **Install prerequisites** (if not already installed)
2. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/azure-terraform-modules.git
   cd azure-terraform-modules
   ```
3. **Open in VS Code:**
   ```bash
   code .
   ```
4. **Reopen in Container:**
   - When prompted, click "Reopen in Container"
   - Or use Command Palette (Ctrl/Cmd+Shift+P): `Dev Containers: Reopen in Container`
5. **Wait for automatic setup** - The container will install:
   - Python 3.11 + Poetry
   - Terraform  
   - Azure CLI
   - Git
   - All VS Code extensions
   - All project dependencies via `make install`

**Ready to develop!** All commands work identically to local development.

#### Option 2: Local Development Setup (Mac/Linux)

For Mac/Linux users who prefer local development:

**Prerequisites:**
- **Terraform** (latest version)
- **Azure CLI** (latest version)
- **Python** (3.11+) with Poetry
- **VS Code** (recommended editor)
- **Git** for version control

**Setup Steps:**
1. **Install dependencies:**

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

   **On Linux:**
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

2. **Clone and setup:**
   ```bash
   git clone https://github.com/your-org/azure-terraform-modules.git
   cd azure-terraform-modules
   make install        # Install Python dependencies and pre-commit hooks
   ```

3. **Start developing:**
   ```bash
   make help           # See all commands
   make install        # Ensure everything is ready
   make pre-commit     # Quick validation
   ```

#### Which Development Option Should You Choose?

**Choose Dev Container if:**
- 🪟 **You're on Windows** - Eliminates Linux command compatibility issues
- 🚀 **You want zero setup time** - Everything configured automatically
- 🔒 **You prefer isolated environments** - No interference with host system
- 👋 **You're new to the project** - Get started immediately without tool conflicts

**Choose Local Development if:**
- 🍎 **You're on Mac/Linux** and comfortable with local tool management
- ⚡ **You want maximum performance** - No container overhead
**Choose Local Development if:**
- 🍎 **You're on Mac/Linux** and comfortable with local tool management
- ⚡ **You want maximum performance** - No container overhead
- 🔧 **You already have tools installed** - Don't want to change existing setup
- 🤖 **You need OS-level integrations** - Git credentials, system tools, etc.

## 🛠️ Development Commands

**Note:** All commands work identically in both dev container and local environments.

The most commonly used commands for daily development:

```bash
# Environment setup
make health-check       # Check what tools are missing
make install            # Install dependencies and setup environment
make help               # Show all available commands

# Daily development workflow
make pre-commit         # Run quick checks (formatting, linting)
make test-terraform     # Run Terraform tests (smart: changed modules only)
make check              # Run comprehensive checks before committing

# Testing commands
make test               # Run Python tests only
make test-terraform-all # Run Terraform tests for all modules
make test-all           # Run all tests (Python + Terraform)

# Code quality
make format             # Format Terraform and Python code
make lint               # Run linting checks
make security           # Run security scans

# Cleanup and utilities
make clean              # Clean temporary files
make validate           # Run validation scripts
```

**Recommended workflow:**
1. `make health-check` - Verify your development environment
2. `make install` - One-time setup 
3. `make pre-commit` - Quick checks while developing
4. `make test-terraform` - Test your Terraform changes
5. `make check` - Comprehensive validation before committing

## 🧪 Testing Framework

This repository includes a comprehensive testing framework for validating Terraform modules that are designed to be consumed by other repositories. The framework provides fast, reliable validation of module syntax, structure, and configuration without requiring Azure authentication.

### Testing Approach

Since these modules are **reusable components** consumed by other repositories (not deployed directly), the testing focuses on validation and static analysis rather than deployment testing.

#### **Validation Testing** ✅
Fast validation tests that ensure modules are ready for consumption:

```bash
make test-terraform     # Smart: test only changed modules (~90 seconds)
make test-terraform-all # Comprehensive: test all modules (~90s × modules)
make test-all          # Run both Python and Terraform validation tests
```

**What it validates:**
- ✅ HCL syntax and formatting
- ✅ Module structure (required files, variables, outputs)
- ✅ Provider configuration compatibility
- ✅ Variable usage and validation rules
- ✅ Multiple configuration scenarios
- ✅ Azure region compatibility
- ✅ Module readiness for consumption by other repositories

### Test Structure

### Smart Testing

The framework includes intelligent change detection that dramatically improves scalability:

- **Smart testing**: Only tests modules that have changed
- **Fast feedback**: ~90 seconds regardless of project size
- **CI/CD friendly**: No special setup or credentials required

```bash
# Daily development (smart testing)
make test-terraform        # Tests only changed modules

# Release validation (comprehensive)  
make test-terraform-all    # Tests all modules
```

### Test Structure

The testing framework is organized under `tests/terraform/`:

```
tests/terraform/
├── __init__.py                             # Python module init
├── base_validation.py                      # Core validation testing infrastructure
├── config.py                              # Test configuration and utilities
├── fixtures/                              # Test data and configurations
│   ├── __init__.py
│   └── test_data.py
└── modules/                               # Module-specific tests
    ├── __init__.py
    └── test_resource_group_validation.py    # Resource group validation tests
```

### Why No Plan Testing?

Since these modules are designed to be **consumed by other repositories**, plan testing doesn't make sense here because:

1. **No deployment context** - This repo doesn't know actual deployment scenarios
2. **Different configurations** - Consuming repos will have their own variable values
3. **Different subscriptions** - Each consuming repo may deploy to different Azure subscriptions
4. **False confidence** - Plan tests here don't validate real-world usage

Instead, **consuming repositories** should implement their own integration tests that validate modules in their specific deployment contexts.

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

#### Full Testing (When Needed)
```bash
# Test ALL modules (use sparingly - gets slow with many modules)
make test-terraform-all      # Tests all modules (~90 seconds per module)
```

#### CI/CD Pipeline Configuration

- **Pull Request Checks**: Use `make test-terraform` (validation only, no Azure auth required)
- **Regular Validation**: Include `make check` in all CI/CD pipelines

#### When to Use Each Test Type

| Scenario              | Validation Tests       | Smart Testing          |
| --------------------- | ---------------------- | ---------------------- |
| **Local Development** | ✅ Changed modules only | 🚀 ~30-90 seconds       |
| **Pull Request CI**   | ✅ Changed modules only | 🚀 Scales with changes  |
| **Release Pipeline**  | ✅ All modules          | ⚠️ Use `*-all` commands |

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
make test-terraform-all      # Test ALL modules (use when needed)
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
| [diagnostic-settings](terraform/foundation/diagnostic-settings/) | Azure Diagnostic Settings | ✅ Available |
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