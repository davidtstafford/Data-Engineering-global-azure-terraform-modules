# Diagnostic Settings Module

This Terraform module creates Azure Diagnostic Settings to route resource logs and metrics to various destinations including Log Analytics workspaces, Storage Accounts, and Event Hubs.

## Features

- **Multi-destination support**: Log Analytics, Storage Account, Event Hub, or any combination
- **Flexible log configuration**: Support for individual categories, category groups, or both
- **Granular retention policies**: Different retention settings per log category (Storage Account only)
- **Metrics support**: Route platform metrics to destinations
- **Validation**: Ensures at least one destination is configured
- **Azure compliance**: Follows Azure best practices for diagnostic logging

## Supported Destinations

| Destination         | Use Case                       | Retention   | Real-time        | Cost                    |
| ------------------- | ------------------------------ | ----------- | ---------------- | ----------------------- |
| **Log Analytics**   | Queries, dashboards, alerts    | 30-730 days | Near real-time   | Pay per GB ingested     |
| **Storage Account** | Long-term archival, compliance | Unlimited   | Batch (5-15 min) | Storage costs only      |
| **Event Hub**       | Real-time streaming, SIEM      | 1-7 days    | Real-time        | Base + throughput costs |

## Usage

### Basic Usage (Log Analytics)

```hcl
module "diagnostic_settings" {
  source = "path/to/diagnostic-settings"

  name               = "vm-diagnostics"
  target_resource_id = azurerm_virtual_machine.example.id

  # Log Analytics destination
  log_analytics_workspace_id = azurerm_log_analytics_workspace.example.id

  # Use category groups for simplicity
  category_groups = [{
    name    = "allLogs"
    enabled = true
  }]

  # Enable metrics
  metrics = [{
    category = "AllMetrics"
    enabled  = true
  }]
}
```

### Multi-destination with Retention

```hcl
module "diagnostic_settings" {
  source = "path/to/diagnostic-settings"

  name               = "storage-compliance-logs"
  target_resource_id = azurerm_storage_account.example.id

  # Multiple destinations
  log_analytics_workspace_id   = azurerm_log_analytics_workspace.ops.id
  storage_account_id          = azurerm_storage_account.archive.id
  eventhub_authorization_rule_id = azurerm_eventhub_authorization_rule.example.id
  eventhub_name               = azurerm_eventhub.logs.name

  # Specific categories with different retention policies
  categories = [
    {
      name    = "StorageRead"
      enabled = true
      retention_policy = {
        enabled = true
        days    = 90
      }
    },
    {
      name    = "StorageWrite"
      enabled = true
      retention_policy = {
        enabled = true
        days    = 2555  # 7 years for compliance
      }
    }
  ]

  metrics = [{
    category = "Transaction"
    enabled  = true
    retention_policy = {
      enabled = true
      days    = 30
    }
  }]
}
```

## Variables

### Required Variables

| Name                 | Description                    | Type     |
| -------------------- | ------------------------------ | -------- |
| `name`               | Name of the diagnostic setting | `string` |
| `target_resource_id` | ID of the resource to monitor  | `string` |

### Destination Variables (at least one required)

| Name                             | Description                                  | Type     |
| -------------------------------- | -------------------------------------------- | -------- |
| `log_analytics_workspace_id`     | Log Analytics workspace ID                   | `string` |
| `log_analytics_destination_type` | "Dedicated" or "AzureDiagnostics" table mode | `string` |
| `storage_account_id`             | Storage account ID for archival              | `string` |
| `eventhub_authorization_rule_id` | Event Hub authorization rule ID              | `string` |
| `eventhub_name`                  | Event Hub name                               | `string` |

### Log Configuration Variables

| Name              | Description                         | Type           | Default |
| ----------------- | ----------------------------------- | -------------- | ------- |
| `category_groups` | Log category groups to enable       | `list(object)` | `[]`    |
| `categories`      | Individual log categories to enable | `list(object)` | `[]`    |
| `metrics`         | Metrics to enable                   | `list(object)` | `[]`    |

### Category/Category Group Object Structure

```hcl
# Category groups (recommended)
category_groups = [{
  name    = "allLogs"      # or "audit", "allLogs", etc.
  enabled = true
}]

# Individual categories (granular control)
categories = [{
  name    = "AuditEvent"
  enabled = true
  retention_policy = {     # Optional, Storage Account only
    enabled = true
    days    = 90
  }
}]

# Metrics
metrics = [{
  category = "AllMetrics"
  enabled  = true
  retention_policy = {     # Optional, Storage Account only
    enabled = true
    days    = 30
  }
}]
```

## Outputs

| Name                 | Description             |
| -------------------- | ----------------------- |
| `id`                 | Diagnostic setting ID   |
| `name`               | Diagnostic setting name |
| `target_resource_id` | Target resource ID      |

## Examples

The module includes comprehensive examples for different scenarios:

### [Basic Example](./examples/basic/)
- Single destination (Log Analytics)
- Category groups and metrics
- Dedicated tables for better query performance

### [Storage with Retention](./examples/storage-with-retention/)
- Storage Account destination
- Different retention policies for different log types
- Cost-effective long-term archival

### [Multi-destination](./examples/multi-destination/)
- Log Analytics + Event Hub
- Real-time streaming with historical analysis
- Operational and security monitoring

### [Complex Configuration](./examples/complex-configuration/)
- All three destinations
- Sophisticated retention strategies
- Enterprise compliance scenario

### [Event Hub Streaming](./examples/eventhub-streaming/)
- Event Hub only for real-time processing
- SIEM integration and external system feeding
- High-throughput log processing

## Best Practices

### Destination Selection

1. **Log Analytics**: Choose when you need to:
   - Query logs with KQL
   - Create dashboards and alerts
   - Correlate logs across resources
   - Use dedicated tables for better performance

2. **Storage Account**: Choose when you need to:
   - Long-term archival (>2 years)
   - Compliance requirements
   - Cost-effective storage
   - Backup of diagnostic data

3. **Event Hub**: Choose when you need to:
   - Real-time streaming to external systems
   - SIEM integration
   - Custom analytics pipelines
   - High-throughput processing

### Category vs Category Groups

- **Use Category Groups** (recommended): Simpler configuration, automatically includes new categories
- **Use Individual Categories**: When you need granular control or specific retention policies

### Retention Policies

- **Log Analytics**: Set at workspace level (30-730 days)
- **Storage Account**: Set per category/metric (1 day to unlimited)
- **Event Hub**: Set at Event Hub level (1-7 days)

### Cost Optimization

1. **Log Analytics**: 
   - Use Basic logs for high-volume, low-value data
   - Set appropriate retention periods
   - Use dedicated tables for better compression

2. **Storage Account**:
   - Use Cool/Archive tiers for long-term retention
   - Implement lifecycle policies
   - Consider data compression

3. **Event Hub**:
   - Right-size throughput units
   - Use appropriate partition count
   - Keep retention minimal for streaming scenarios

## Limitations

- **Azure Policy**: Some organizations may have policies requiring specific diagnostic configurations
- **Resource Support**: Not all Azure resources support all log categories
- **Regional Availability**: Some features may not be available in all regions
- **Concurrent Settings**: Only one diagnostic setting per resource per destination type

## Validation

The module includes validation to ensure:
- At least one destination is specified
- Retention days are within valid ranges (1-365 for most categories)
- Required fields are provided for each destination type

## Troubleshooting

### Common Issues

1. **No logs appearing**: 
   - Check target resource supports the specified categories
   - Verify destination permissions and configuration
   - Check if resource is generating the expected log types

2. **High costs**:
   - Review retention policies
   - Consider using category groups instead of all categories
   - Evaluate if all destinations are necessary

3. **Missing categories**:
   - Use category groups for automatic inclusion of new categories
   - Check resource documentation for supported categories
   - Verify category names are correct (case-sensitive)

### Debugging Commands

```bash
# List available categories for a resource
az monitor diagnostic-settings categories list --resource <resource-id>

# Check current diagnostic settings
az monitor diagnostic-settings list --resource <resource-id>

# Validate Log Analytics workspace
az monitor log-analytics workspace show --workspace-name <name> --resource-group <rg>
```

## Contributing

When contributing to this module:

1. Add comprehensive examples for new features
2. Update this README with new variables/outputs
3. Include validation rules for new inputs
4. Test with multiple destination combinations
5. Consider cost implications of changes

## Version Compatibility

- **Terraform**: >= 1.0
- **AzureRM Provider**: >= 3.0
- **Azure**: All regions supporting diagnostic settings

## Related Modules

- `terraform/foundation/log-analytics-workspace`: Create Log Analytics workspaces
- `terraform/foundation/storage-account`: Create storage accounts for log archival  
- `terraform/foundation/event-hub`: Create Event Hubs for log streaming
