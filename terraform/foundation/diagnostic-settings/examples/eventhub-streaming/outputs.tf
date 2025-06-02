
output "diagnostic_setting_id" {
  description = "The ID of the diagnostic setting"
  value       = module.diagnostic_settings.id
}

output "diagnostic_setting_name" {
  description = "The name of the diagnostic setting"
  value       = module.diagnostic_settings.name
}

output "target_resource_id" {
  description = "The ID of the resource being monitored"
  value       = module.diagnostic_settings.target_resource_id
}

output "eventhub_name" {
  description = "The name of the Event Hub receiving the logs"
  value       = var.eventhub_name
}

output "streaming_configuration" {
  description = "Summary of the streaming configuration"
  value = {
    destination_type    = "eventhub"
    eventhub_name       = var.eventhub_name
    category_groups     = var.category_groups
    metrics_enabled     = length(var.metrics) > 0
    real_time_streaming = true
  }
}
