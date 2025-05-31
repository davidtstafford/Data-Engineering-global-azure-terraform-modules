# Module Development Guide

This guide covers how to create, structure, and maintain high-quality Terraform modules for Azure data engineering platforms.

## 🎯 Module Design Principles

### Core Principles

1. **Single Responsibility**: Each module should have one clear purpose
2. **Composability**: Modules should work well together
3. **Flexibility**: Support common use cases while allowing customization
4. **Security**: Apply security best practices by default
5. **Documentation**: Clear usage examples and comprehensive docs

### Design Patterns

- **Foundation modules**: Core Azure resources (Resource Groups, Storage Accounts)
- **Platform modules**: Higher-level abstractions (Data Factory with pipelines)
- **Composition modules**: Multiple resources working together
- **Utility modules**: Helper functions and data sources

## 🏗️ Module Structure

### Standard Module Layout

```
terraform/category/module-name/
├── README.md           # Module documentation
├── main.tf            # Primary resources
├── variables.tf       # Input variables  
├── outputs.tf         # Output values
├── versions.tf        # Provider version constraints
├── locals.tf          # Local values (optional)
├── data.tf            # Data sources (optional)
└── examples/          # Usage examples
    ├── basic/         # Simple usage example
    │   ├── main.tf
    │   ├── variables.tf
    │   ├── outputs.tf
    │   └── README.md
    └── advanced/      # Complex usage example
        ├── main.tf
        ├── variables.tf
        ├── outputs.tf
        └── README.md
```

### File Organization

**main.tf** - Primary resource definitions
```hcl
# Azure Storage Account resource
resource "azurerm_storage_account" "this" {
  name                = var.storage_account_name
  resource_group_name = var.resource_group_name
  location           = var.location
  
  account_tier             = var.account_tier
  account_replication_type = var.replication_type
  
  # Security defaults
  enable_https_traffic_only = var.enable_https_traffic_only
  min_tls_version          = var.min_tls_version
  
  # Apply tags
  tags = var.tags
}
```

**variables.tf** - Input parameter definitions
```hcl
variable "storage_account_name" {
  description = "Name of the Azure Storage Account. Must be globally unique."
  type        = string
  
  validation {
    condition     = can(regex("^[a-z0-9]{3,24}$", var.storage_account_name))
    error_message = "Storage account name must be 3-24 characters, lowercase letters and numbers only."
  }
}

variable "resource_group_name" {
  description = "Name of the Azure Resource Group where the storage account will be created."
  type        = string
}

variable "location" {
  description = "Azure region where the storage account will be deployed."
  type        = string
}

variable "account_tier" {
  description = "Performance tier of the storage account (Standard or Premium)."
  type        = string
  default     = "Standard"
  
  validation {
    condition     = contains(["Standard", "Premium"], var.account_tier)
    error_message = "Account tier must be either 'Standard' or 'Premium'."
  }
}

variable "tags" {
  description = "Tags to apply to the storage account."
  type        = map(string)
  default     = {}
}
```

**outputs.tf** - Return values
```hcl
output "id" {
  description = "The ID of the storage account."
  value       = azurerm_storage_account.this.id
}

output "name" {
  description = "The name of the storage account."
  value       = azurerm_storage_account.this.name
}

output "primary_blob_endpoint" {
  description = "The primary blob service endpoint URL."
  value       = azurerm_storage_account.this.primary_blob_endpoint
}

output "primary_access_key" {
  description = "The primary access key for the storage account."
  value       = azurerm_storage_account.this.primary_access_key
  sensitive   = true
}
```

**versions.tf** - Provider requirements
```hcl
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0, < 4.0"
    }
  }
}
```

## 📝 Documentation Standards

### Module README Template

```markdown
# Storage Account Module

Creates an Azure Storage Account with security best practices enabled by default.

## Features

- ✅ HTTPS traffic only by default
- ✅ TLS 1.2 minimum version
- ✅ Configurable performance tiers
- ✅ Flexible replication options
- ✅ Comprehensive tagging support

## Usage

### Basic Example

```hcl
module "storage_account" {
  source = "git::https://github.com/org/repo.git//terraform/foundation/storage-account?ref=v1.0.0"
  
  storage_account_name = "mydatastorageacct"
  resource_group_name  = "my-resource-group"
  location            = "East US"
  
  tags = {
    Environment = "production"
    Project     = "data-platform"
  }
}
```

### Advanced Example

```hcl
module "premium_storage" {
  source = "git::https://github.com/org/repo.git//terraform/foundation/storage-account?ref=v1.0.0"
  
  storage_account_name = "mypremiumstorage"
  resource_group_name  = "my-resource-group"
  location            = "East US"
  
  # Premium performance tier
  account_tier         = "Premium"
  replication_type     = "LRS"
  
  # Advanced security
  enable_https_traffic_only = true
  min_tls_version          = "TLS1_2"
  
  tags = {
    Environment = "production"
    Tier        = "premium"
  }
}
```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.0 |
| azurerm | >= 3.0, < 4.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| storage_account_name | Name of the Azure Storage Account | `string` | n/a | yes |
| resource_group_name | Name of the Resource Group | `string` | n/a | yes |
| location | Azure region | `string` | n/a | yes |
| account_tier | Performance tier | `string` | `"Standard"` | no |
| tags | Resource tags | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| id | Storage account ID |
| name | Storage account name |
| primary_blob_endpoint | Primary blob endpoint URL |
```

### Variable Documentation

- **Clear descriptions**: Explain what the variable does and how it affects behavior
- **Type specifications**: Use appropriate Terraform types (`string`, `number`, `bool`, `list`, `map`)
- **Default values**: Provide sensible defaults where appropriate
- **Validation rules**: Add validation for critical parameters
- **Examples**: Include example values in descriptions

## 🔒 Security Best Practices

### Default Security Posture

All modules should implement security by default:

```hcl
# Storage Account security defaults
resource "azurerm_storage_account" "this" {
  # ... other configuration ...
  
  # Security settings
  enable_https_traffic_only      = true
  min_tls_version               = "TLS1_2"
  allow_nested_items_to_be_public = false
  shared_access_key_enabled     = true
  
  # Network access
  public_network_access_enabled = var.allow_public_access
  
  # Blob properties
  blob_properties {
    versioning_enabled = true
    
    delete_retention_policy {
      days = var.blob_retention_days
    }
  }
}
```

### Security Checklist

- [ ] **Encryption**: Enable encryption at rest and in transit
- [ ] **Network isolation**: Support private endpoints and network restrictions
- [ ] **Access control**: Implement RBAC and managed identities
- [ ] **Auditing**: Enable diagnostic logging and monitoring
- [ ] **Secrets**: Never hardcode sensitive values
- [ ] **Validation**: Validate security-critical parameters

## 🧪 Testing Strategy

### Validation Levels

1. **Syntax validation**: `terraform validate`
2. **Security scanning**: `checkov -d module/`
3. **Format checking**: `terraform fmt -check`
4. **Documentation**: Ensure all variables/outputs are documented

### Using Validation Script

```bash
# Validate specific module
poetry run python scripts/validate.py --module terraform/foundation/storage-account

# Validate all modules
poetry run python scripts/validate.py --all

# Validate with security scan
poetry run python scripts/validate.py --module terraform/foundation/storage-account --security
```

### Manual Testing

While we don't run live Azure tests in CI, you should manually test:

```bash
# Navigate to module example
cd terraform/foundation/storage-account/examples/basic

# Initialize and validate
terraform init
terraform validate
terraform plan

# If you have Azure access:
terraform apply
terraform destroy
```

## 🔄 Versioning Strategy

### Semantic Versioning

- **Major (v2.0.0)**: Breaking changes to module interface
- **Minor (v1.1.0)**: New features, backwards compatible
- **Patch (v1.0.1)**: Bug fixes, no interface changes

### Breaking Changes

Examples that require major version bump:

- Removing or renaming input variables
- Changing variable types or validation rules
- Removing or changing output values
- Changing resource names (causes recreation)
- Updating minimum provider versions significantly

### Backwards Compatibility

Maintain backwards compatibility when possible:

```hcl
# Good: Add new optional variable
variable "new_feature_enabled" {
  description = "Enable new feature"
  type        = bool
  default     = false
}

# Good: Deprecate old variable but keep working
variable "old_variable" {
  description = "DEPRECATED: Use new_variable instead"
  type        = string
  default     = null
}

# Bad: Remove variable without major version bump
# variable "removed_variable" { ... }
```

## 📊 Common Patterns

### Conditional Resources

```hcl
# Create resource only if enabled
resource "azurerm_private_endpoint" "this" {
  count = var.enable_private_endpoint ? 1 : 0
  
  name                = "${var.name}-pe"
  location           = var.location
  resource_group_name = var.resource_group_name
  subnet_id          = var.private_endpoint_subnet_id
  
  private_service_connection {
    name                           = "${var.name}-psc"
    private_connection_resource_id = azurerm_storage_account.this.id
    is_manual_connection          = false
    subresource_names             = ["blob"]
  }
}
```

### Dynamic Blocks

```hcl
# Dynamic network rules
resource "azurerm_storage_account" "this" {
  # ... other configuration ...
  
  dynamic "network_rules" {
    for_each = var.network_rules != null ? [var.network_rules] : []
    
    content {
      default_action             = network_rules.value.default_action
      bypass                     = network_rules.value.bypass
      ip_rules                   = network_rules.value.ip_rules
      virtual_network_subnet_ids = network_rules.value.virtual_network_subnet_ids
    }
  }
}
```

### Local Values

```hcl
# locals.tf
locals {
  # Common tags applied to all resources
  common_tags = merge(var.tags, {
    Module      = "storage-account"
    ManagedBy   = "terraform"
    CreatedDate = timestamp()
  })
  
  # Computed values
  storage_account_name = var.storage_account_name != null ? var.storage_account_name : "${var.name_prefix}sa${random_id.suffix.hex}"
}
```

## 🎯 Module Categories

### Foundation Modules

Basic Azure building blocks:
- Resource Groups
- Storage Accounts  
- Key Vaults
- Virtual Networks

### Data Platform Modules

Data engineering specific:
- Event Hubs
- Data Factory
- SQL Database
- Synapse Analytics

### Databricks Modules

Databricks ecosystem:
- Workspace
- Compute Clusters
- Unity Catalog
- Notebook Management

### Composition Modules

Higher-level patterns:
- Complete data lakehouse
- Event-driven data pipeline
- Analytics workspace

## ✅ Quality Checklist

Before submitting a new module:

### Code Quality
- [ ] Follows naming conventions
- [ ] Includes input validation
- [ ] Has sensible defaults
- [ ] Uses proper Terraform types
- [ ] No hardcoded values

### Security
- [ ] Implements security by default
- [ ] Supports private networking
- [ ] Enables encryption
- [ ] Includes monitoring/logging
- [ ] Passes security scan

### Documentation
- [ ] Comprehensive README
- [ ] All variables documented
- [ ] All outputs documented
- [ ] Includes usage examples
- [ ] Has both basic and advanced examples

### Testing
- [ ] Terraform validation passes
- [ ] Format check passes
- [ ] Security scan passes
- [ ] Manual testing completed
- [ ] Examples work correctly

---

🚀 **Ready to create amazing Terraform modules for Azure!**
