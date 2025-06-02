# Storage Account with Retention Policies Example

This example demonstrates how to configure Azure Diagnostic Settings to send logs to a storage account with different retention policies for different log types.

## What This Example Does

- Sends logs to an **Azure Storage Account** for long-term archival
- Configures **different retention policies** for different log types:
  - **Audit logs**: 7 years (2555 days) for compliance
  - **Service health logs**: 30 days for operational purposes  
  - **All other logs**: 90 days via category group
- Demonstrates **mixing individual categories with category groups**

## Usage

```bash
export TF_VAR_target_resource_id="/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-example/providers/Microsoft.KeyVault/vaults/my-keyvault"
export TF_VAR_storage_account_id="/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-storage/providers/Microsoft.Storage/storageAccounts/mylogstorage"

terraform init
terraform plan
terraform apply
```

## Configuration Highlights

### Individual Categories with Specific Retention
```hcl
categories = [
  {
    name = "AuditEvent"
    retention_policy = {
      enabled = true
      days    = 2555  # 7 years for compliance requirements
    }
  },
  {
    name = "ServiceHealth"
    retention_policy = {
      enabled = true
      days    = 30  # 30 days for operational monitoring
    }
  }
]
```

### Category Groups with Default Retention
```hcl
category_groups = [
  {
    name = "allLogs"
    retention_policy = {
      enabled = true
      days    = 90  # 90 days for everything else
    }
  }
]
```

## Use Cases

- **Compliance**: Long-term retention of audit logs for regulatory requirements
- **Cost optimization**: Different retention periods based on log importance
- **Archival**: Storage accounts are cost-effective for long-term log storage
- **Backup**: Secondary storage destination alongside Log Analytics

## Storage Account Requirements

The storage account must:
- Be in the same region as the target resource (or a supported paired region)
- Have appropriate access permissions configured
- Have sufficient storage capacity for the expected log volume

## Cost Considerations

- **Storage costs** increase with retention period and log volume
- **Access costs** apply when retrieving archived logs
- Consider using **storage tiers** (Hot/Cool/Archive) for cost optimization
- Monitor storage usage and adjust retention policies as needed
