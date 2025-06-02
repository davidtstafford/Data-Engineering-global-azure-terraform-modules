terraform {
  required_version = ">= 1.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

module "diagnostic_settings" {
  source = "../../"

  name               = var.diagnostic_setting_name
  target_resource_id = var.target_resource_id

  storage_account_id = var.storage_account_id

  categories      = var.categories
  category_groups = var.category_groups
  metrics         = var.metrics
}
