# Foundation Modules

Foundation modules provide core Azure resources that other modules depend on. These are typically the first modules deployed in any Azure environment.

## Available Modules

### resource-group
- **Purpose**: Create and manage Azure Resource Groups with standardized naming and tagging
- **Status**: ✅ Complete - Ready for production use
- **Dependencies**: None
- **Usage**: See [resource-group/README.md](./resource-group/README.md)

### storage-account
- **Purpose**: Create and manage Azure Storage Accounts with security best practices
- **Status**: 🚧 Planned
- **Dependencies**: resource-group
- **Features**: Encryption, network rules, private endpoints

### key-vault
- **Purpose**: Create and manage Azure Key Vault for secrets management
- **Status**: 🚧 Planned  
- **Dependencies**: resource-group
- **Features**: Access policies, private endpoints, purge protection

## Usage Patterns

Foundation modules are typically used together to establish the baseline infrastructure:

```hcl
# Example: Basic foundation setup
module "resource_group" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/resource-group?ref=v1.0.0"
  
  name     = "my-project"
  location = "East US"
  environment = "production"
}

module "storage_account" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/storage-account?ref=v1.0.0"
  
  resource_group_name = module.resource_group.name
  location           = module.resource_group.location
  # ... other variables
}
```

## Development Guidelines

When creating new foundation modules:

1. **Minimal Dependencies**: Foundation modules should have minimal external dependencies
2. **Security First**: Include security best practices by default
3. **Flexible Configuration**: Support both simple and advanced use cases
4. **Comprehensive Testing**: Include examples and validation tests
5. **Clear Documentation**: Provide usage examples and parameter descriptions

See [../../docs/module-development.md](../../docs/module-development.md) for detailed development guidelines.
