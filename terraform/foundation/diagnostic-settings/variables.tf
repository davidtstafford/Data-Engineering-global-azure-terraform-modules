variable "name" {
  description = "The name of the diagnostic setting"
  type        = string

  validation {
    condition     = can(regex("^[a-zA-Z0-9._-]+$", var.name))
    error_message = "Diagnostic setting name must contain only alphanumeric characters, periods, underscores, or hyphens."
  }
}

variable "target_resource_id" {
  description = "The ID of the target resource for which diagnostic settings are configured"
  type        = string

  validation {
    condition     = can(regex("^/subscriptions/[a-f0-9-]+/resourceGroups/[^/]+/providers/", var.target_resource_id))
    error_message = "Target resource ID must be a valid Azure resource ID format."
  }
}

variable "log_analytics_workspace_id" {
  description = "The ID of the Log Analytics workspace to send diagnostic logs to (optional)"
  type        = string
  default     = null

  validation {
    condition     = var.log_analytics_workspace_id == null || can(regex("^/subscriptions/[a-f0-9-]+/resourceGroups/[^/]+/providers/Microsoft.OperationalInsights/workspaces/", var.log_analytics_workspace_id))
    error_message = "Log Analytics workspace ID must be a valid Azure workspace resource ID format."
  }
}

variable "log_analytics_destination_type" {
  description = "The destination type for Log Analytics workspace (AzureDiagnostics or Dedicated)"
  type        = string
  default     = null

  validation {
    condition     = var.log_analytics_destination_type == null || (var.log_analytics_destination_type == "AzureDiagnostics" || var.log_analytics_destination_type == "Dedicated")
    error_message = "Log Analytics destination type must be either 'AzureDiagnostics' or 'Dedicated'."
  }
}

variable "storage_account_id" {
  description = "The ID of the storage account to send diagnostic logs to (optional)"
  type        = string
  default     = null

  validation {
    condition     = var.storage_account_id == null || can(regex("^/subscriptions/[a-f0-9-]+/resourceGroups/[^/]+/providers/Microsoft.Storage/storageAccounts/", var.storage_account_id))
    error_message = "Storage account ID must be a valid Azure storage account resource ID format."
  }
}

variable "eventhub_authorization_rule_id" {
  description = "The ID of the Event Hub authorization rule to send diagnostic logs to (optional)"
  type        = string
  default     = null

  validation {
    condition     = var.eventhub_authorization_rule_id == null || can(regex("^/subscriptions/[a-f0-9-]+/resourceGroups/[^/]+/providers/Microsoft.EventHub/namespaces/", var.eventhub_authorization_rule_id))
    error_message = "Event Hub authorization rule ID must be a valid Azure Event Hub authorization rule resource ID format."
  }
}

variable "eventhub_name" {
  description = "The name of the Event Hub to send diagnostic logs to (required when eventhub_authorization_rule_id is specified)"
  type        = string
  default     = null

  validation {
    condition     = var.eventhub_name == null || can(regex("^[a-zA-Z0-9._-]+$", var.eventhub_name))
    error_message = "Event Hub name must contain only alphanumeric characters, periods, underscores, or hyphens."
  }
}

variable "categories" {
  description = "List of log categories to enable with optional retention policies"
  type = list(object({
    name = string
    retention_policy = optional(object({
      enabled = bool
      days    = number
    }))
  }))
  default = []

  validation {
    condition = alltrue([
      for category in var.categories : can(regex("^[a-zA-Z0-9._-]+$", category.name))
    ])
    error_message = "All category names must contain only alphanumeric characters, periods, underscores, or hyphens."
  }

  validation {
    condition = alltrue([
      for category in var.categories :
      category.retention_policy == null || (
        category.retention_policy.days >= 0 && category.retention_policy.days <= 365
      )
    ])
    error_message = "Retention policy days must be between 0 and 365."
  }
}

variable "category_groups" {
  description = "List of log category groups to enable with optional retention policies (e.g., 'allLogs', 'audit')"
  type = list(object({
    name = string
    retention_policy = optional(object({
      enabled = bool
      days    = number
    }))
  }))
  default = []

  validation {
    condition = alltrue([
      for group in var.category_groups : can(regex("^[a-zA-Z0-9._-]+$", group.name))
    ])
    error_message = "All category group names must contain only alphanumeric characters, periods, underscores, or hyphens."
  }

  validation {
    condition = alltrue([
      for group in var.category_groups :
      group.retention_policy == null || (
        group.retention_policy.days >= 0 && group.retention_policy.days <= 365
      )
    ])
    error_message = "Retention policy days must be between 0 and 365."
  }
}

variable "metrics" {
  description = "List of metric categories to enable (e.g., 'AllMetrics')"
  type        = list(string)
  default     = []

  validation {
    condition = alltrue([
      for metric in var.metrics : can(regex("^[a-zA-Z0-9._-]+$", metric))
    ])
    error_message = "All metric names must contain only alphanumeric characters, periods, underscores, or hyphens."
  }
}
