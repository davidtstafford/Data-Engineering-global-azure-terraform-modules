variable "diagnostic_setting_name" {
  description = "The name of the diagnostic setting"
  type        = string
  default     = "audit-logs-to-law"
}

variable "target_resource_id" {
  description = "The ID of the target resource for which diagnostic settings are configured (e.g., storage account, key vault, etc.)"
  type        = string
  # No default - user must provide the resource they want to monitor
}

variable "log_analytics_workspace_id" {
  description = "The ID of the Log Analytics workspace to send diagnostic logs to"
  type        = string
  # No default - user must provide their Log Analytics workspace
}

variable "log_analytics_destination_type" {
  description = "The destination type for Log Analytics workspace"
  type        = string
  default     = "Dedicated"
}

variable "category_groups" {
  description = "List of log category groups to enable"
  type = list(object({
    name = string
    retention_policy = optional(object({
      enabled = bool
      days    = number
    }))
  }))
  default = [
    {
      name = "audit"
    }
  ]
}

variable "metrics" {
  description = "List of metric categories to enable"
  type        = list(string)
  default     = ["AllMetrics"]
}
