# Basic Diagnostic Settings Example

This example demonstrates how to configure Azure Diagnostic Settings to send audit logs and metrics to a Log Analytics workspace using dedicated tables.

## What This Example Does

- Configures diagnostic settings for an Azure resource
- Sends **audit logs** to Log Analytics using the `audit` category group
- Sends **all metrics** to Log Analytics
- Uses **dedicated tables** for better query performance and organization

## Usage

1. **Set required variables:**
   ```bash
   export TF_VAR_target_resource_id="/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-example/providers/Microsoft.Storage/storageAccounts/mystorageaccount"
   export TF_VAR_log_analytics_workspace_id="/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-monitoring/providers/Microsoft.OperationalInsights/workspaces/my-log-analytics"
   ```

2. **Initialize and apply:**
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

## Configuration Details

### Log Analytics Destination Type
- **`Dedicated`** - Each log category gets its own table (recommended for better performance)
- Alternative: `AzureDiagnostics` - All logs go into a single table (legacy approach)

### Category Groups
- **`audit`** - Includes audit-related log categories (security events, access logs, etc.)
- Alternative: `allLogs` - Includes all available log categories

### Metrics
- **`AllMetrics`** - Includes all available metrics for the resource type
- Alternative: Specify individual metric categories

## Example Resource Types

This example works with any Azure resource that supports diagnostic settings:

- **Storage Accounts** - Blob, Queue, Table, File service logs
- **Key Vaults** - Access logs, audit events
- **App Services** - Application logs, HTTP logs
- **SQL Databases** - Query performance, deadlocks, security events
- **And many more...**

## Customization

You can customize the configuration by modifying variables:

```hcl
# Enable different category groups
category_groups = [
  {
    name = "allLogs"  # Instead of just audit logs
  }
]

# Add retention policies
category_groups = [
  {
    name = "audit"
    retention_policy = {
      enabled = true
      days    = 90  # Keep audit logs for 90 days
    }
  }
]

# Different metrics
metrics = ["Transaction", "Capacity"]  # Instead of AllMetrics
```

## Output

After successful deployment, you'll be able to query your logs in Log Analytics using KQL:

```kql
// Query audit logs
AuditEvent
| where TimeGenerated > ago(24h)
| limit 100

// Query metrics
AzureMetrics
| where TimeGenerated > ago(1h)
| limit 100
```
