output "id" {
  description = "The ID of the diagnostic setting"
  value       = azurerm_monitor_diagnostic_setting.this.id
}

output "name" {
  description = "The name of the diagnostic setting"
  value       = azurerm_monitor_diagnostic_setting.this.name
}

output "target_resource_id" {
  description = "The ID of the target resource"
  value       = azurerm_monitor_diagnostic_setting.this.target_resource_id
}

output "log_analytics_workspace_id" {
  description = "The ID of the Log Analytics workspace (if configured)"
  value       = azurerm_monitor_diagnostic_setting.this.log_analytics_workspace_id
}

output "storage_account_id" {
  description = "The ID of the storage account (if configured)"
  value       = azurerm_monitor_diagnostic_setting.this.storage_account_id
}

output "eventhub_authorization_rule_id" {
  description = "The ID of the Event Hub authorization rule (if configured)"
  value       = azurerm_monitor_diagnostic_setting.this.eventhub_authorization_rule_id
}

output "eventhub_name" {
  description = "The name of the Event Hub (if configured)"
  value       = azurerm_monitor_diagnostic_setting.this.eventhub_name
}
