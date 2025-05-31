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
├── .devcontainer/              # VS Code dev container configuration
│   ├── devcontainer.json       # Container settings and extensions
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
- **Python 3.9+** installed locally
- **Docker/Rancher Desktop** for containerized development
- **VS Code** with Dev Containers extension (recommended)

#### Option 1: VS Code Dev Container (Recommended)
1. Clone this repository
2. Open in VS Code
3. When prompted, select "Reopen in Container"
4. Wait for container setup (5-10 minutes first time)
5. Run `make help` to see available commands

#### Option 2: Local Development
1. Clone this repository
2. Install Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
3. Run `make setup` to configure environment
4. Install Terraform locally from [terraform.io](https://terraform.io)

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

## 📚 Documentation

- **[Getting Started](docs/getting-started.md)** - Detailed setup instructions
- **[Module Development](docs/module-development.md)** - How to create new modules
- **[Examples](docs/examples.md)** - Usage patterns and compositions
- **[Contributing](CONTRIBUTING.md)** - Contribution guidelines

## 🔧 Available Modules

### Foundation Modules
| Module | Purpose | Status |
|--------|---------|--------|
| [resource-group](terraform/foundation/resource-group/) | Azure Resource Group | ✅ Available |
| [storage-account](terraform/foundation/storage-account/) | Azure Storage Account | 🚧 Planned |
| [key-vault](terraform/foundation/key-vault/) | Azure Key Vault | 🚧 Planned |

### Networking Modules
| Module | Purpose | Status |
|--------|---------|--------|
| [virtual-network](terraform/networking/virtual-network/) | Virtual Network | 🚧 Planned |
| [private-endpoints](terraform/networking/private-endpoints/) | Private connectivity | 🚧 Planned |

### Data Platform Modules  
| Module | Purpose | Status |
|--------|---------|--------|
| [eventhub](terraform/data/eventhub/) | Event streaming | 🚧 Planned |
| [sql-database](terraform/data/sql-database/) | Relational database | 🚧 Planned |
| [data-factory](terraform/data/data-factory/) | Data integration | 🚧 Planned |
| [synapse](terraform/data/synapse/) | Analytics platform | 🚧 Planned |

### Databricks Modules
| Module | Purpose | Status |
|--------|---------|--------|
| [workspace](terraform/databricks/workspace/) | Workspace foundation | 🚧 Planned |
| [compute](terraform/databricks/compute/) | Compute clusters | 🚧 Planned |
| [unity-catalog](terraform/databricks/unity-catalog/) | Data governance | 🚧 Planned |
| [notebooks](terraform/databricks/notebooks/) | Notebook management | 🚧 Planned |

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