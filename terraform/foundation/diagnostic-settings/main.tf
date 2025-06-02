resource "azurerm_monitor_diagnostic_setting" "this" {
  name               = var.name
  target_resource_id = var.target_resource_id

  # Validation: Ensure at least one destination is provided
  lifecycle {
    precondition {
      condition     = local.has_destination
      error_message = "At least one destination must be provided: log_analytics_workspace_id, storage_account_id, or eventhub_authorization_rule_id."
    }
  }

  # Only include Log Analytics if workspace ID is provided
  log_analytics_workspace_id     = var.log_analytics_workspace_id != null ? var.log_analytics_workspace_id : null
  log_analytics_destination_type = var.log_analytics_workspace_id != null ? var.log_analytics_destination_type : null

  # Only include Storage Account if ID is provided
  storage_account_id = var.storage_account_id != null ? var.storage_account_id : null

  # Only include Event Hub if authorization rule ID is provided
  eventhub_authorization_rule_id = var.eventhub_authorization_rule_id != null ? var.eventhub_authorization_rule_id : null
  eventhub_name                  = var.eventhub_authorization_rule_id != null ? var.eventhub_name : null


  dynamic "enabled_log" {
    for_each = coalesce(var.categories, [])
    content {
      category = enabled_log.value.name

      dynamic "retention_policy" {
        for_each = enabled_log.value.retention_policy != null ? [enabled_log.value.retention_policy] : []
        content {
          enabled = retention_policy.value.enabled
          days    = retention_policy.value.days
        }
      }
    }
  }

  dynamic "enabled_log" {
    for_each = coalesce(var.category_groups, [])
    content {
      category_group = enabled_log.value.name

      dynamic "retention_policy" {
        for_each = enabled_log.value.retention_policy != null ? [enabled_log.value.retention_policy] : []
        content {
          enabled = retention_policy.value.enabled
          days    = retention_policy.value.days
        }
      }
    }
  }

  dynamic "metric" {
    for_each = coalesce(var.metrics, [])
    content {
      category = metric.value
    }
  }

}
