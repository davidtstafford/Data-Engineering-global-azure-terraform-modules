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

  # Event Hub only - for real-time streaming to external systems
  eventhub_authorization_rule_id = var.eventhub_authorization_rule_id
  eventhub_name                  = var.eventhub_name

  category_groups = var.category_groups
  metrics         = var.metrics
}
