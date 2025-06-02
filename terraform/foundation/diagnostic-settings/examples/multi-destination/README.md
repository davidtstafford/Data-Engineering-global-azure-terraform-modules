# Multi-Destination Example

This example demonstrates how to send diagnostic logs to multiple destinations simultaneously: Log Analytics for interactive queries and Event Hub for real-time streaming.

## What This Example Does

- Sends logs to **Log Analytics** for interactive queries, dashboards, and alerting
- Simultaneously streams logs to **Event Hub** for real-time processing
- Uses **dedicated tables** in Log Analytics for better performance
- Captures **all logs and metrics** for comprehensive monitoring

## Architecture

```
Azure Resource
       ↓
Diagnostic Settings
    ↙        ↘
Log Analytics   Event Hub
    ↓             ↓
Dashboards   External Systems
Alerts       (SIEM, Analytics)
```

## Usage

```bash
export TF_VAR_target_resource_id="/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-example/providers/Microsoft.Sql/servers/mysqlserver"
export TF_VAR_log_analytics_workspace_id="/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-monitoring/providers/Microsoft.OperationalInsights/workspaces/my-log-analytics"
export TF_VAR_eventhub_authorization_rule_id="/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-streaming/providers/Microsoft.EventHub/namespaces/my-eventhub-ns/authorizationRules/RootManageSharedAccessKey"
export TF_VAR_eventhub_name="diagnostic-logs"

terraform init
terraform plan
terraform apply
```

## Use Cases

### Log Analytics Benefits
- **Interactive queries** with KQL (Kusto Query Language)
- **Real-time dashboards** and visualizations
- **Alerting rules** for proactive monitoring
- **Built-in retention** and data management

### Event Hub Benefits
- **Real-time streaming** to external systems
- **SIEM integration** (Splunk, QRadar, Sentinel)
- **Custom analytics** pipelines
- **High throughput** event processing

## Common Scenarios

1. **Security Monitoring**: Stream security logs to SIEM while keeping operational queries in Log Analytics
2. **Compliance**: Archive logs via Event Hub while maintaining searchable data in Log Analytics  
3. **Analytics**: Real-time processing via Event Hub + historical analysis in Log Analytics
4. **Integration**: Event-driven architectures consuming diagnostic events

## Configuration Details

- **No retention policies** needed (Log Analytics manages its own retention)
- **AllLogs category group** captures everything for comprehensive monitoring
- **AllMetrics** provides complete performance visibility
- **Dedicated tables** in Log Analytics for optimal query performance

## Cost Considerations

- **Double ingestion costs** (data sent to both destinations)
- **Log Analytics**: Per-GB ingestion + retention costs
- **Event Hub**: Throughput unit costs + message charges
- Consider filtering logs by importance if cost is a concern

## Event Hub Requirements

- Event Hub namespace must exist
- Authorization rule must have Send permissions
- Consider partition count based on expected throughput
- Monitor for throughput unit scaling needs
