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

  # Log Analytics for interactive queries and alerting
  log_analytics_workspace_id     = var.log_analytics_workspace_id
  log_analytics_destination_type = var.log_analytics_destination_type

  # Event Hub for real-time streaming to external systems
  eventhub_authorization_rule_id = var.eventhub_authorization_rule_id
  eventhub_name                  = var.eventhub_name

  category_groups = var.category_groups
  metrics         = var.metrics
}
