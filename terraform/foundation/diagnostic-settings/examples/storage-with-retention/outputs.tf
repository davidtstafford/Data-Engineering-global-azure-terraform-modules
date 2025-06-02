output "diagnostic_setting_id" {
  description = "The ID of the created diagnostic setting"
  value       = module.diagnostic_settings.id
}

output "diagnostic_setting_name" {
  description = "The name of the created diagnostic setting"
  value       = module.diagnostic_settings.name
}

output "storage_account_id" {
  description = "The ID of the storage account receiving the logs"
  value       = module.diagnostic_settings.storage_account_id
}
