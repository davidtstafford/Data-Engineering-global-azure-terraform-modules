variable "diagnostic_setting_name" {
  description = "The name of the diagnostic setting"
  type        = string
  default     = "streaming-to-eventhub"
}

variable "target_resource_id" {
  description = "The ID of the target resource for which diagnostic settings are configured"
  type        = string
  # No default - user must provide the resource they want to monitor
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

variable "category_groups" {
  description = "List of log category groups to stream"
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
      # No retention policy needed for Event Hub (streaming only)
    }
  ]
}

variable "metrics" {
  description = "List of metric categories to stream"
  type        = list(string)
  default     = ["AllMetrics"]
}
