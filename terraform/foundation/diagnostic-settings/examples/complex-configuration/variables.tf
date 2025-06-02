variable "diagnostic_setting_name" {
  description = "The name of the diagnostic setting"
  type        = string
  default     = "comprehensive-monitoring"
}

variable "target_resource_id" {
  description = "The ID of the target resource for which diagnostic settings are configured"
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

variable "storage_account_id" {
  description = "The ID of the storage account to send diagnostic logs to"
  type        = string
  # No default - user must provide their storage account
}

variable "eventhub_authorization_rule_id" {
  description = "The ID of the Event Hub authorization rule to send diagnostic logs to"
  type        = string
  # No default - user must provide their Event Hub authorization rule
}

variable "eventhub_name" {
  description = "The name of the Event Hub to send diagnostic logs to"
  type        = string
  # No default - user must provide their Event Hub name
}

variable "categories" {
  description = "List of individual log categories with specific retention policies"
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
        days    = 2555 # 7 years for compliance (audit logs)
      }
    },
    {
      name = "Policy"
      retention_policy = {
        enabled = true
        days    = 365 # 1 year for policy compliance logs
      }
    },
    {
      name = "ServiceHealth"
      retention_policy = {
        enabled = true
        days    = 90 # 90 days for service health monitoring
      }
    },
    {
      name = "ResourceHealth"
      retention_policy = {
        enabled = true
        days    = 30 # 30 days for resource health events
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
      name = "audit"
      retention_policy = {
        enabled = true
        days    = 1825 # 5 years for audit category group
      }
    },
    {
      name = "allLogs"
      retention_policy = {
        enabled = true
        days    = 180 # 6 months for all other logs
      }
    }
  ]
}

variable "metrics" {
  description = "List of metric categories to enable"
  type        = list(string)
  default = [
    "AllMetrics",
    "Transaction",
    "Capacity"
  ]
}
