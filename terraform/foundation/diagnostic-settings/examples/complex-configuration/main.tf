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

  # Triple destination: Log Analytics + Storage + Event Hub
  log_analytics_workspace_id     = var.log_analytics_workspace_id
  log_analytics_destination_type = var.log_analytics_destination_type
  storage_account_id             = var.storage_account_id
  eventhub_authorization_rule_id = var.eventhub_authorization_rule_id
  eventhub_name                  = var.eventhub_name

  # Mix of individual categories and groups with different retention policies
  categories      = var.categories
  category_groups = var.category_groups
  metrics         = var.metrics
}
