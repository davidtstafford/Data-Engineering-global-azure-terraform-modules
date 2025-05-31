# Terraform Modules

This directory contains reusable Terraform modules for Azure infrastructure components commonly used in data engineering projects.

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

## Available Modules

### Core Infrastructure
- **resource-group** - Azure Resource Group with standardized naming and tagging
- **storage-account** - Azure Storage Account with security best practices
- **key-vault** - Azure Key Vault with access policies and secrets management

### Data Platform
- **data-factory** - Azure Data Factory with managed identity and Git integration
- **synapse-workspace** - Azure Synapse Analytics workspace
- **databricks-workspace** - Azure Databricks workspace

### Networking
- **virtual-network** - Azure Virtual Network with subnets and security groups
- **private-endpoint** - Azure Private Endpoint for secure connectivity

### Security & Monitoring
- **log-analytics-workspace** - Azure Log Analytics workspace
- **application-insights** - Azure Application Insights

## Usage

Each module can be used independently or combined to create complete data platform environments:

```hcl
module "resource_group" {
  source = "./terraform/resource-group"
  
  name     = "rg-data-platform-dev"
  location = "East US"
  
  tags = {
    Environment = "dev"
    Project     = "data-platform"
  }
}

module "storage_account" {
  source = "./terraform/storage-account"
  
  name                = "stdataplatformdev001"
  resource_group_name = module.resource_group.name
  location           = module.resource_group.location
  
  tags = module.resource_group.tags
}
```

## Module Development Guidelines

1. **Naming Conventions**: Follow Azure naming conventions and use descriptive names
2. **Tagging**: All modules should support and propagate tags
3. **Security**: Implement security best practices by default
4. **Documentation**: Include comprehensive README with examples
5. **Testing**: Include validation examples in the examples/ directory

For detailed module development guidelines, see [docs/module-development.md](../docs/module-development.md).
