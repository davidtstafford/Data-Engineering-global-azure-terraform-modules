locals {
  # Validate that at least one destination is provided
  destinations = [
    var.log_analytics_workspace_id,
    var.storage_account_id,
    var.eventhub_authorization_rule_id
  ]

  has_destination = length([for dest in local.destinations : dest if dest != null]) > 0
}
