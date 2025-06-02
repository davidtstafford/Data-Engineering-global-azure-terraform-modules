# Real-time Streaming Example

This example demonstrates configuring diagnostic settings for **real-time streaming** to Event Hub for immediate processing by external systems.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Azure Resource │───▶│   Event Hub     │───▶│  External       │
│  (Target)       │    │  (Real-time)    │    │  Processing     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                        ┌─────────────────┐
                        │  SIEM, Custom   │
                        │  Analytics, or  │
                        │  3rd Party Tools│
                        └─────────────────┘
```

## Use Cases

### Primary Use Cases
- **Security Information and Event Management (SIEM)**: Stream security logs to Splunk, QRadar, or other SIEM platforms
- **Real-time Analytics**: Feed logs into Apache Kafka, Azure Stream Analytics, or Apache Spark for immediate processing
- **External Compliance Systems**: Stream audit logs to third-party compliance and governance platforms
- **Custom Monitoring Solutions**: Send logs to custom monitoring dashboards or alerting systems

### When to Use This Pattern
- ✅ Need immediate log processing (< 1 minute latency)
- ✅ Integrating with external monitoring/SIEM systems
- ✅ Building custom real-time analytics pipelines
- ✅ Streaming to multiple downstream consumers
- ✅ High-throughput log processing requirements

### When NOT to Use This Pattern
- ❌ Only need historical log analysis (use Log Analytics instead)
- ❌ Cost-sensitive scenarios with low log volume (Event Hub has base costs)
- ❌ Simple alerting needs (Log Analytics alerts are simpler)

## Configuration

### Required Variables
- `diagnostic_setting_name`: Name for the diagnostic setting
- `target_resource_id`: ID of the Azure resource to monitor
- `eventhub_authorization_rule_id`: Event Hub namespace authorization rule
- `eventhub_name`: Name of the specific Event Hub

### Optional Variables
- `category_groups`: Log categories to stream (defaults to ["allLogs"])
- `metrics`: Metrics to stream (defaults to all available metrics)

## Example Usage

```bash
# Set your variables
export TF_VAR_diagnostic_setting_name="storage-streaming-logs"
export TF_VAR_target_resource_id="/subscriptions/.../resourceGroups/.../providers/Microsoft.Storage/storageAccounts/mystorageaccount"
export TF_VAR_eventhub_authorization_rule_id="/subscriptions/.../resourceGroups/.../providers/Microsoft.EventHub/namespaces/myeventhubns/authorizationRules/RootManageSharedAccessKey"
export TF_VAR_eventhub_name="storage-logs-hub"

# Deploy
terraform init
terraform plan
terraform apply
```

## Event Hub Considerations

### Throughput and Partitions
- **Throughput Units**: Each unit provides 1 MB/s ingress, 2 MB/s egress
- **Partitions**: More partitions = higher throughput and parallel processing
- **Recommended**: Start with 4 partitions, scale based on actual throughput

### Message Format
Azure diagnostic logs are streamed as JSON with this structure:
```json
{
  "time": "2024-01-15T10:30:00.000Z",
  "resourceId": "/subscriptions/.../resourceGroups/.../providers/...",
  "category": "StorageRead",
  "operationName": "GetBlob",
  "properties": {
    "statusCode": 200,
    "requestId": "abc123",
    "uri": "https://mystorageaccount.blob.core.windows.net/container/file.txt"
  }
}
```

### Cost Optimization
- **Base Cost**: ~$22/month per Event Hub namespace
- **Throughput Cost**: ~$0.028 per million events
- **Retention**: Keep retention period minimal (1-7 days) since this is for real-time processing
- **Partitioning**: Right-size partitions to avoid over-provisioning

## Integration Examples

### Stream Analytics Query
```sql
SELECT 
    System.Timestamp() AS WindowEnd,
    resourceId,
    category,
    COUNT(*) AS EventCount
FROM EventHubInput
GROUP BY 
    resourceId, 
    category,
    TumblingWindow(minute, 5)
```

### Custom Consumer (Python)
```python
from azure.eventhub import EventHubConsumerClient

def on_event(partition_context, event):
    log_data = json.loads(event.body_as_str())
    # Process log data in real-time
    process_diagnostic_log(log_data)
    
consumer = EventHubConsumerClient.from_connection_string(
    conn_str="Endpoint=sb://...",
    consumer_group="$Default",
    eventhub_name="storage-logs-hub"
)

with consumer:
    consumer.receive(on_event=on_event)
```

## Monitoring the Stream

Monitor your Event Hub streaming with these metrics:
- **Incoming Messages**: Rate of log ingestion
- **Outgoing Messages**: Rate of consumption
- **Throttled Requests**: Indicates need for more throughput units
- **Consumer Lag**: Time between log generation and consumption

## Security

- Use managed identity when possible for Event Hub authentication
- Enable Event Hub network isolation if processing sensitive logs
- Consider customer-managed keys for encryption at rest
- Implement proper access controls on Event Hub namespace

## Troubleshooting

### Common Issues
1. **High latency**: Check throughput units and partition count
2. **Missing logs**: Verify category groups and target resource permissions
3. **Consumer errors**: Check authorization rule permissions and connection strings
4. **Throttling**: Scale up throughput units or optimize consumer logic

### Validation Commands
```bash
# Check diagnostic setting
az monitor diagnostic-settings show --name "$TF_VAR_diagnostic_setting_name" --resource "$TF_VAR_target_resource_id"

# Monitor Event Hub metrics
az monitor metrics list --resource "$TF_VAR_eventhub_authorization_rule_id" --metric "IncomingMessages"
```
