variable "diagnostic_setting_name" {
  description = "The name of the diagnostic setting"
  type        = string
  default     = "logs-to-storage-with-retention"
}

variable "target_resource_id" {
  description = "The ID of the target resource for which diagnostic settings are configured"
  type        = string
  # No default - user must provide the resource they want to monitor
}

variable "storage_account_id" {
  description = "The ID of the storage account to send diagnostic logs to"
  type        = string
  # No default - user must provide their storage account
}

variable "categories" {
  description = "List of individual log categories with retention policies"
  type = list(object({
    name = string
    retention_policy = optional(object({
      enabled = bool
      days    = number
    }))
  }))
  default = [
    {
      name = "AuditEvent"
      retention_policy = {
        enabled = true
        days    = 2555 # 7 years for compliance
      }
    },
    {
      name = "ServiceHealth"
      retention_policy = {
        enabled = true
        days    = 30 # 30 days for operational logs
      }
    }
  ]
}

variable "category_groups" {
  description = "List of log category groups with retention policies"
  type = list(object({
    name = string
    retention_policy = optional(object({
      enabled = bool
      days    = number
    }))
  }))
  default = [
    {
      name = "allLogs"
      retention_policy = {
        enabled = true
        days    = 90 # 90 days for all other logs
      }
    }
  ]
}

variable "metrics" {
  description = "List of metric categories to enable"
  type        = list(string)
  default     = ["AllMetrics"]
}
