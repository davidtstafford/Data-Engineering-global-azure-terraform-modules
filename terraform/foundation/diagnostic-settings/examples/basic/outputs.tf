output "diagnostic_setting_id" {
  description = "The ID of the created diagnostic setting"
  value       = module.diagnostic_settings.id
}

output "diagnostic_setting_name" {
  description = "The name of the created diagnostic setting"
  value       = module.diagnostic_settings.name
}

output "target_resource_id" {
  description = "The ID of the target resource being monitored"
  value       = module.diagnostic_settings.target_resource_id
}

output "log_analytics_workspace_id" {
  description = "The ID of the Log Analytics workspace receiving the logs"
  value       = module.diagnostic_settings.log_analytics_workspace_id
}
