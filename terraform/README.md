# Terraform Modules

This directory contains reusable Terraform modules for Azure infrastructure components commonly used in data engineering projects.

## Module Organization

Modules are organized by category to make them easy to find and understand dependencies:

### Foundation (`foundation/`)
Core infrastructure modules that other modules depend on:
- **[resource-group](foundation/resource-group/)** - Azure Resource Group with standardized naming and tagging ✅ Available

### Planned Modules

Additional modules will be organized in these categories:

#### Data Platform (`data/`)
- **data-factory** - Azure Data Factory with managed identity and Git integration
- **synapse-workspace** - Azure Synapse Analytics workspace  
- **databricks-workspace** - Azure Databricks workspace

#### Networking (`networking/`)
- **virtual-network** - Azure Virtual Network with subnets and security groups
- **private-endpoint** - Azure Private Endpoint for secure connectivity

#### Security & Monitoring (`security/`)
- **key-vault** - Azure Key Vault with access policies and secrets management
- **log-analytics-workspace** - Azure Log Analytics workspace
- **application-insights** - Azure Application Insights

## Module Structure

Each module follows a standardized structure:

```
module-name/
├── main.tf          # Main resource definitions
├── variables.tf     # Input variables
├── outputs.tf       # Output values
├── versions.tf      # Terraform and provider version constraints
├── README.md        # Module documentation
└── examples/        # Usage examples
    └── basic/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

## Usage

Reference modules using Git tags for version control:

```hcl
module "resource_group" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/resource-group?ref=v1.0.0"
  
  name     = "rg-data-platform-dev"
  location = "East US"
  
  tags = {
    Environment = "dev"
    Project     = "data-platform"
  }
}
```

Or reference locally during development:

```hcl
module "resource_group" {
  source = "./terraform/foundation/resource-group"
  
  name     = "rg-data-platform-dev"
  location = "East US"
  
  tags = {
    Environment = "dev"
    Project     = "data-platform"
  }
}
```

## Module Development Guidelines

1. **Naming Conventions**: Follow Azure naming conventions and use descriptive names
2. **Tagging**: All modules should support and propagate tags
3. **Security**: Implement security best practices by default
4. **Documentation**: Include comprehensive README with examples
5. **Testing**: Include validation examples in the examples/ directory

For detailed module development guidelines, see [docs/module-development.md](../docs/module-development.md).
