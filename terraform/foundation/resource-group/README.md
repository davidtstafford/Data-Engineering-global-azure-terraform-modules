# Azure Resource Group Module

This module creates an Azure Resource Group with standardized naming conventions and tagging support.

## Usage

```hcl
module "resource_group" {
  source = "./terraform/resource-group"
  
  name     = "rg-data-platform-dev"
  location = "East US"
  
  tags = {
    Environment = "dev"
    Project     = "data-platform"
    Owner       = "data-team"
  }
}
```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.0 |
| azurerm | >= 3.0 |

## Providers

| Name | Version |
|------|---------|
| azurerm | >= 3.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| name | The name of the resource group | `string` | n/a | yes |
| location | The Azure region where the resource group will be created | `string` | n/a | yes |
| tags | A mapping of tags to assign to the resource | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| id | The ID of the Resource Group |
| name | The name of the Resource Group |
| location | The location of the Resource Group |
| tags | The tags applied to the Resource Group |

## Examples

See the [examples](./examples/) directory for complete usage examples.
