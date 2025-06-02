output "diagnostic_setting_id" {
  description = "The ID of the created diagnostic setting"
  value       = module.diagnostic_settings.id
}

output "log_analytics_workspace_id" {
  description = "The ID of the Log Analytics workspace receiving the logs"
  value       = module.diagnostic_settings.log_analytics_workspace_id
}

output "eventhub_authorization_rule_id" {
  description = "The ID of the Event Hub authorization rule"
  value       = module.diagnostic_settings.eventhub_authorization_rule_id
}

output "eventhub_name" {
  description = "The name of the Event Hub receiving the logs"
  value       = module.diagnostic_settings.eventhub_name
}
