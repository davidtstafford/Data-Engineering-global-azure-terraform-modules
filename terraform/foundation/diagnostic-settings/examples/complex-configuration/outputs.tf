output "diagnostic_setting_id" {
  description = "The ID of the created diagnostic setting"
  value       = module.diagnostic_settings.id
}

output "all_destinations" {
  description = "All configured destinations for the diagnostic setting"
  value = {
    log_analytics_workspace_id     = module.diagnostic_settings.log_analytics_workspace_id
    storage_account_id             = module.diagnostic_settings.storage_account_id
    eventhub_authorization_rule_id = module.diagnostic_settings.eventhub_authorization_rule_id
    eventhub_name                  = module.diagnostic_settings.eventhub_name
  }
}

output "log_configuration_summary" {
  description = "Summary of log categories and groups configured"
  value = {
    individual_categories = length(var.categories)
    category_groups       = length(var.category_groups)
    metrics               = length(var.metrics)
    total_log_streams     = length(var.categories) + length(var.category_groups)
  }
}
