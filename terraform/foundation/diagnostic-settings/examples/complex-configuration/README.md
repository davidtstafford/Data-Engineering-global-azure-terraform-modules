# Complex Configuration Example

This example demonstrates a comprehensive diagnostic settings configuration with multiple destinations, mixed log categories, and sophisticated retention policies for enterprise environments.

## What This Example Does

- **Triple destination**: Sends logs to Log Analytics, Storage Account, AND Event Hub simultaneously
- **Mixed log categories**: Combines individual categories with category groups
- **Tiered retention policies**: Different retention periods based on log criticality
- **Comprehensive metrics**: Multiple metric categories for complete visibility

## Architecture Overview

```
Azure Resource (e.g., Key Vault, SQL Database)
                    ↓
            Diagnostic Settings
         ↙        ↓        ↘
Log Analytics  Storage   Event Hub
     ↓         Account      ↓
Interactive     ↓       Real-time
 Queries    Long-term   Streaming
Dashboards   Archive    to SIEM
 Alerts
```

## Retention Strategy

### Individual Categories (High-Value Logs)
- **AuditEvent**: 7 years (2555 days) - Compliance requirement
- **Policy**: 1 year (365 days) - Governance tracking  
- **ServiceHealth**: 90 days - Operational monitoring
- **ResourceHealth**: 30 days - Troubleshooting

### Category Groups (Bulk Logs)
- **audit**: 5 years (1825 days) - Security compliance
- **allLogs**: 6 months (180 days) - General operational logs

## Usage

```bash
# Set all required variables
export TF_VAR_target_resource_id="/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-production/providers/Microsoft.KeyVault/vaults/prod-keyvault"
export TF_VAR_log_analytics_workspace_id="/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-monitoring/providers/Microsoft.OperationalInsights/workspaces/prod-log-analytics"
export TF_VAR_storage_account_id="/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-storage/providers/Microsoft.Storage/storageAccounts/prodlogarchive"
export TF_VAR_eventhub_authorization_rule_id="/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-streaming/providers/Microsoft.EventHub/namespaces/prod-eventhub-ns/authorizationRules/DiagnosticLogsRule"
export TF_VAR_eventhub_name="diagnostic-logs-prod"

terraform init
terraform plan
terraform apply
```

## Enterprise Use Cases

### Compliance & Governance
- **Audit logs**: Long-term retention for regulatory compliance
- **Policy logs**: Track policy violations and compliance status
- **Multiple destinations**: Ensure no single point of failure

### Security Monitoring
- **Real-time streaming**: Immediate SIEM integration via Event Hub
- **Historical analysis**: Deep-dive investigations in Log Analytics
- **Long-term forensics**: Archive access via Storage Account

### Operational Excellence
- **Service health monitoring**: Track service availability and performance
- **Resource health tracking**: Monitor resource-specific health events
- **Comprehensive metrics**: Multiple metric streams for complete visibility

## Configuration Highlights

### Log Redundancy Strategy
```hcl
# Critical logs get both individual category AND group coverage
categories = [
  { name = "AuditEvent", retention_policy = { enabled = true, days = 2555 }},
  # ... other individual categories
]

category_groups = [
  { name = "audit", retention_policy = { enabled = true, days = 1825 }},
  { name = "allLogs", retention_policy = { enabled = true, days = 180 }}
]
```

### Multi-Metric Strategy
```hcl
metrics = [
  "AllMetrics",    # Comprehensive coverage
  "Transaction",   # Transaction-specific metrics  
  "Capacity"       # Capacity planning metrics
]
```

## Cost Optimization

- **Tiered retention**: Longer retention only for critical logs
- **Strategic destinations**: 
  - Log Analytics: Interactive queries (expensive but essential)
  - Storage: Long-term archive (cheap, occasional access)
  - Event Hub: Real-time streaming (moderate cost, high value)

## Monitoring & Alerts

After deployment, configure alerts for:
- High log ingestion costs
- Storage account capacity approaching limits
- Event Hub throughput unit scaling needs
- Log Analytics workspace quota approaching limits

## Compliance Benefits

- **Audit trail completeness**: Multiple log categories ensure comprehensive coverage
- **Retention compliance**: Different retention periods meet various regulatory requirements  
- **Data sovereignty**: Storage account ensures data remains in required regions
- **Redundancy**: Multiple destinations protect against data loss
