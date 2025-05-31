# Usage Examples and Patterns

This guide provides practical examples of how to use Azure Terraform modules effectively in real-world scenarios.

## 🎯 Basic Usage Patterns

### Single Module Usage

The simplest way to use a module:

```hcl
# main.tf
module "resource_group" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/resource-group?ref=v1.0.0"
  
  name     = "my-data-platform-rg"
  location = "East US"
  
  tags = {
    Environment = "production"
    Project     = "data-platform"
    Owner       = "data-team"
  }
}
```

### Module Composition

Combining multiple modules to build a platform:

```hcl
# variables.tf
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "dataplatform"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "East US"
}

# locals.tf
locals {
  name_prefix = "${var.project_name}-${var.environment}"
  
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
    CreatedDate = timestamp()
  }
}

# main.tf
module "resource_group" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/resource-group?ref=v1.0.0"
  
  name     = "${local.name_prefix}-rg"
  location = var.location
  tags     = local.common_tags
}

module "storage_account" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/storage-account?ref=v1.0.0"
  
  storage_account_name = "${replace(local.name_prefix, "-", "")}sa"
  resource_group_name  = module.resource_group.name
  location            = module.resource_group.location
  
  account_tier     = "Standard"
  replication_type = "LRS"
  
  tags = local.common_tags
}

module "key_vault" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/key-vault?ref=v1.0.0"
  
  key_vault_name      = "${local.name_prefix}-kv"
  resource_group_name = module.resource_group.name
  location           = module.resource_group.location
  
  sku_name = "standard"
  
  tags = local.common_tags
}
```

## 🏗️ Real-World Scenarios

### Scenario 1: Development Environment

Small-scale development setup with cost optimization:

```hcl
# dev-environment.tf
module "dev_resource_group" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/resource-group?ref=v1.0.0"
  
  name     = "myproject-dev-rg"
  location = "East US"
  
  tags = {
    Environment = "development"
    Project     = "myproject"
    AutoShutdown = "enabled"
  }
}

module "dev_storage" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/storage-account?ref=v1.0.0"
  
  storage_account_name = "myprojectdevsa"
  resource_group_name  = module.dev_resource_group.name
  location            = module.dev_resource_group.location
  
  # Cost-optimized settings for dev
  account_tier     = "Standard"
  replication_type = "LRS"
  access_tier     = "Cool"
  
  tags = module.dev_resource_group.tags
}

module "dev_eventhub" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/data/eventhub?ref=v1.0.0"
  
  namespace_name      = "myproject-dev-eh"
  resource_group_name = module.dev_resource_group.name
  location           = module.dev_resource_group.location
  
  # Minimal capacity for dev
  sku      = "Basic"
  capacity = 1
  
  event_hubs = [
    {
      name              = "events"
      partition_count   = 2
      message_retention = 1
    }
  ]
  
  tags = module.dev_resource_group.tags
}
```

### Scenario 2: Production Data Platform

Enterprise-grade data platform with security and monitoring:

```hcl
# production-platform.tf

# Core Infrastructure
module "prod_resource_group" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/resource-group?ref=v1.0.0"
  
  name     = "dataplatform-prod-rg"
  location = "East US"
  
  tags = {
    Environment   = "production"
    Project       = "dataplatform"
    CostCenter    = "engineering"
    Compliance    = "required"
    BackupPolicy  = "daily"
  }
}

# Networking
module "virtual_network" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/networking/virtual-network?ref=v1.0.0"
  
  vnet_name           = "dataplatform-prod-vnet"
  resource_group_name = module.prod_resource_group.name
  location           = module.prod_resource_group.location
  
  address_space = ["10.0.0.0/16"]
  
  subnets = [
    {
      name           = "data-subnet"
      address_prefix = "10.0.1.0/24"
    },
    {
      name           = "databricks-public"
      address_prefix = "10.0.2.0/24"
    },
    {
      name           = "databricks-private"
      address_prefix = "10.0.3.0/24"
    }
  ]
  
  tags = module.prod_resource_group.tags
}

# Storage with Advanced Security
module "data_lake_storage" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/storage-account?ref=v1.0.0"
  
  storage_account_name = "dataplatformdatalake"
  resource_group_name  = module.prod_resource_group.name
  location            = module.prod_resource_group.location
  
  # Production-grade settings
  account_tier             = "Standard"
  replication_type         = "GRS"
  is_hns_enabled          = true  # Data Lake Gen2
  enable_https_traffic_only = true
  min_tls_version         = "TLS1_2"
  
  # Network restrictions
  enable_private_endpoint = true
  private_endpoint_subnet_id = module.virtual_network.subnet_ids["data-subnet"]
  
  # Advanced threat protection
  enable_advanced_threat_protection = true
  
  tags = module.prod_resource_group.tags
}

# Key Vault for Secrets
module "key_vault" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/key-vault?ref=v1.0.0"
  
  key_vault_name      = "dataplatform-prod-kv"
  resource_group_name = module.prod_resource_group.name
  location           = module.prod_resource_group.location
  
  sku_name = "premium"
  
  # Security settings
  enabled_for_disk_encryption     = true
  enabled_for_template_deployment = true
  purge_protection_enabled       = true
  soft_delete_retention_days     = 90
  
  # Network access
  enable_private_endpoint = true
  private_endpoint_subnet_id = module.virtual_network.subnet_ids["data-subnet"]
  
  tags = module.prod_resource_group.tags
}

# Event Hub for Streaming Data
module "event_hub_namespace" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/data/eventhub?ref=v1.0.0"
  
  namespace_name      = "dataplatform-prod-eh"
  resource_group_name = module.prod_resource_group.name
  location           = module.prod_resource_group.location
  
  # Production capacity
  sku              = "Standard"
  capacity         = 5
  auto_inflate_enabled = true
  maximum_throughput_units = 10
  
  event_hubs = [
    {
      name              = "raw-events"
      partition_count   = 8
      message_retention = 7
    },
    {
      name              = "processed-events"
      partition_count   = 4
      message_retention = 3
    }
  ]
  
  # Network security
  enable_private_endpoint = true
  private_endpoint_subnet_id = module.virtual_network.subnet_ids["data-subnet"]
  
  tags = module.prod_resource_group.tags
}

# Databricks Workspace
module "databricks_workspace" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/databricks/workspace?ref=v1.0.0"
  
  workspace_name      = "dataplatform-prod-dbx"
  resource_group_name = module.prod_resource_group.name
  location           = module.prod_resource_group.location
  
  # Premium tier for advanced features
  sku = "premium"
  
  # Network injection
  custom_virtual_network_id = module.virtual_network.vnet_id
  public_subnet_id         = module.virtual_network.subnet_ids["databricks-public"]
  private_subnet_id        = module.virtual_network.subnet_ids["databricks-private"]
  
  # Security
  public_network_access_enabled = false
  
  tags = module.prod_resource_group.tags
}
```

### Scenario 3: Multi-Environment Setup

Using workspaces or separate configurations for multiple environments:

```hcl
# environments/dev/main.tf
module "environment" {
  source = "./modules/data-platform"
  
  environment = "dev"
  location   = "East US"
  
  # Development-specific overrides
  databricks_sku = "standard"
  storage_replication = "LRS"
  eventhub_capacity = 1
  
  enable_private_endpoints = false  # Cost saving
  enable_monitoring = false        # Simplified setup
}

# environments/staging/main.tf
module "environment" {
  source = "./modules/data-platform"
  
  environment = "staging"
  location   = "East US"
  
  # Staging-specific overrides
  databricks_sku = "premium"
  storage_replication = "GRS"
  eventhub_capacity = 2
  
  enable_private_endpoints = true
  enable_monitoring = true
}

# environments/prod/main.tf
module "environment" {
  source = "./modules/data-platform"
  
  environment = "prod"
  location   = "East US"
  
  # Production configuration
  databricks_sku = "premium"
  storage_replication = "GRS"
  eventhub_capacity = 5
  
  enable_private_endpoints = true
  enable_monitoring = true
  enable_backup = true
  enable_disaster_recovery = true
}
```

## 🔄 Advanced Patterns

### Pattern 1: For_Each with Module

Deploy multiple similar environments:

```hcl
# Multiple data processing environments
locals {
  environments = {
    dev = {
      location = "East US"
      databricks_sku = "standard"
      storage_tier = "Standard"
    }
    staging = {
      location = "East US"
      databricks_sku = "premium"
      storage_tier = "Standard"
    }
    prod = {
      location = "East US"
      databricks_sku = "premium"
      storage_tier = "Premium"
    }
  }
}

module "data_platform" {
  for_each = local.environments
  
  source = "./modules/data-platform"
  
  environment = each.key
  location   = each.value.location
  
  databricks_sku = each.value.databricks_sku
  storage_tier   = each.value.storage_tier
  
  tags = {
    Environment = each.key
    ManagedBy   = "terraform"
  }
}
```

### Pattern 2: Conditional Module Loading

Load modules based on features:

```hcl
# Feature flags
variable "enable_databricks" {
  description = "Enable Databricks workspace"
  type        = bool
  default     = true
}

variable "enable_synapse" {
  description = "Enable Synapse Analytics"
  type        = bool
  default     = false
}

# Conditional Databricks
module "databricks" {
  count = var.enable_databricks ? 1 : 0
  
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/databricks/workspace?ref=v1.0.0"
  
  # ... configuration
}

# Conditional Synapse
module "synapse" {
  count = var.enable_synapse ? 1 : 0
  
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/data/synapse?ref=v1.0.0"
  
  # ... configuration
}
```

### Pattern 3: Data Source Integration

Using data sources with modules:

```hcl
# Get existing resources
data "azurerm_client_config" "current" {}

data "azurerm_resource_group" "existing" {
  name = "existing-rg"
}

# Use existing resource group
module "storage_account" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/storage-account?ref=v1.0.0"
  
  storage_account_name = "newstorageaccount"
  resource_group_name  = data.azurerm_resource_group.existing.name
  location            = data.azurerm_resource_group.existing.location
  
  tags = data.azurerm_resource_group.existing.tags
}

# Grant current user access to Key Vault
module "key_vault" {
  source = "git::https://github.com/your-org/azure-terraform-modules.git//terraform/foundation/key-vault?ref=v1.0.0"
  
  key_vault_name      = "mykeyvault"
  resource_group_name = data.azurerm_resource_group.existing.name
  location           = data.azurerm_resource_group.existing.location
  
  # Grant access to current user
  access_policies = [
    {
      tenant_id = data.azurerm_client_config.current.tenant_id
      object_id = data.azurerm_client_config.current.object_id
      
      secret_permissions = ["Get", "List", "Set", "Delete"]
      key_permissions   = ["Get", "List", "Create", "Delete"]
    }
  ]
}
```

## 🎛️ Configuration Management

### Using tfvars Files

```hcl
# terraform.tfvars
environment = "production"
location   = "East US"
project_name = "dataplatform"

# Network configuration
address_space = ["10.0.0.0/16"]
subnets = {
  data = {
    address_prefix = "10.0.1.0/24"
    service_endpoints = ["Microsoft.Storage", "Microsoft.KeyVault"]
  }
  databricks_public = {
    address_prefix = "10.0.2.0/24"
  }
  databricks_private = {
    address_prefix = "10.0.3.0/24"
  }
}

# Feature flags
enable_private_endpoints = true
enable_monitoring = true
enable_backup = true

# Storage configuration
storage_replication = "GRS"
storage_access_tier = "Hot"

# Databricks configuration
databricks_sku = "premium"
databricks_public_network_access = false

# Tags
common_tags = {
  Environment = "production"
  Project     = "dataplatform"
  Owner       = "data-team"
  CostCenter  = "engineering"
}
```

### Using Variable Files per Environment

```bash
# Development
terraform apply -var-file="environments/dev.tfvars"

# Staging  
terraform apply -var-file="environments/staging.tfvars"

# Production
terraform apply -var-file="environments/prod.tfvars"
```

## 🔍 Troubleshooting Common Issues

### Module Version Conflicts

```hcl
# Problem: Different modules using incompatible versions
module "storage1" {
  source = "git::https://github.com/org/repo.git//terraform/foundation/storage-account?ref=v1.0.0"
  # ...
}

module "storage2" {
  source = "git::https://github.com/org/repo.git//terraform/foundation/storage-account?ref=v2.0.0"
  # ...
}

# Solution: Use consistent versions
locals {
  module_version = "v1.2.0"
}

module "storage1" {
  source = "git::https://github.com/org/repo.git//terraform/foundation/storage-account?ref=${local.module_version}"
  # ...
}

module "storage2" {
  source = "git::https://github.com/org/repo.git//terraform/foundation/storage-account?ref=${local.module_version}"
  # ...
}
```

### Resource Naming Conflicts

```hcl
# Problem: Duplicate resource names
locals {
  # Add randomness for uniqueness
  random_suffix = random_id.suffix.hex
  
  # Or use consistent naming pattern
  name_prefix = "${var.project}-${var.environment}-${var.location}"
}

resource "random_id" "suffix" {
  byte_length = 4
}

module "storage_account" {
  source = "./modules/storage-account"
  
  # Guaranteed unique name
  storage_account_name = "${local.name_prefix}sa${local.random_suffix}"
  # ...
}
```

### Provider Configuration

```hcl
# Configure providers for modules
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = true
    }
    
    storage {
      prevent_deletion_if_contains_resources = false
    }
  }
}
```

## 📈 Best Practices

### 1. Version Pinning
Always pin module versions for stability:
```hcl
# Good
source = "git::https://github.com/org/repo.git//terraform/foundation/storage-account?ref=v1.2.1"

# Avoid
source = "git::https://github.com/org/repo.git//terraform/foundation/storage-account"
```

### 2. Consistent Tagging
Use consistent tagging across all resources:
```hcl
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
    Owner       = var.owner
    CostCenter  = var.cost_center
  }
}
```

### 3. Resource Dependencies
Use implicit dependencies through outputs:
```hcl
module "resource_group" {
  source = "./modules/resource-group"
  # ...
}

module "storage_account" {
  source = "./modules/storage-account"
  
  # Implicit dependency on resource_group
  resource_group_name = module.resource_group.name
  location           = module.resource_group.location
}
```

### 4. Output Organization
Structure outputs for easy consumption:
```hcl
# outputs.tf
output "resource_ids" {
  description = "Resource IDs for reference"
  value = {
    resource_group  = module.resource_group.id
    storage_account = module.storage_account.id
    key_vault      = module.key_vault.id
  }
}

output "connection_strings" {
  description = "Connection information"
  value = {
    storage_account_url = module.storage_account.primary_blob_endpoint
    key_vault_url      = module.key_vault.vault_uri
  }
  sensitive = true
}
```

---

🚀 **Start building amazing data platforms with these proven patterns!**
