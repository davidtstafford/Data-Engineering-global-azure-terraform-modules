# Usage Examples

This directory contains practical examples of how to use the Azure Terraform modules in real-world scenarios.

## 📁 Directory Structure

```
examples/
├── README.md                    # This file
├── basic-data-platform/         # Simple data platform setup
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tfvars.example
│   └── README.md
├── enterprise-data-platform/    # Production-grade enterprise setup
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tfvars.example
│   └── README.md
├── databricks-workspace/        # Databricks-focused example
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tfvars.example
│   └── README.md
└── multi-environment/           # Multi-environment setup
    ├── environments/
    │   ├── dev.tfvars
    │   ├── staging.tfvars
    │   └── prod.tfvars
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    └── README.md
```

## 🎯 Example Categories

### Basic Data Platform
A simple data platform setup suitable for:
- Development environments
- Small teams
- Proof of concepts
- Learning the modules

**Features:**
- Resource Group
- Storage Account (Data Lake)
- Key Vault for secrets
- Basic networking

### Enterprise Data Platform
A production-grade setup including:
- Advanced security (private endpoints)
- Multiple data services
- Monitoring and compliance
- Disaster recovery considerations

**Features:**
- Virtual Network with subnets
- Private endpoints for security
- Event Hub for streaming data
- Databricks workspace
- Data Factory for ETL
- Comprehensive monitoring

### Databricks Workspace
Focused on Databricks ecosystem:
- Databricks workspace with custom VNet
- Unity Catalog setup
- Compute cluster configurations
- Notebook management

### Multi-Environment
Demonstrates how to:
- Use the same modules across environments
- Manage environment-specific configurations
- Scale from dev to production

## 🚀 Getting Started

### Prerequisites

1. **Azure CLI** installed and authenticated
2. **Terraform** installed (version 1.0+)
3. **Azure subscription** with appropriate permissions

### Basic Usage

1. **Choose an example** that matches your use case
2. **Navigate to the example directory**
3. **Copy the terraform.tfvars.example file**:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```
4. **Edit terraform.tfvars** with your specific values
5. **Initialize and apply**:
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

### Example Workflow

```bash
# Choose the basic data platform example
cd examples/basic-data-platform

# Copy and customize variables
cp terraform.tfvars.example terraform.tfvars
vim terraform.tfvars  # Edit with your values

# Deploy the infrastructure
terraform init
terraform plan -out=tfplan
terraform apply tfplan

# When done, cleanup
terraform destroy
```

## 🔧 Customization

Each example is designed to be:
- **Modular**: Easy to add/remove components
- **Configurable**: Extensive variable customization
- **Extensible**: Add your own modules and resources

### Common Customizations

1. **Environment-specific settings**:
   ```hcl
   # Different storage tiers by environment
   storage_tier = var.environment == "prod" ? "Premium" : "Standard"
   ```

2. **Regional deployments**:
   ```hcl
   # Deploy to multiple regions
   primary_location   = "East US"
   secondary_location = "West US 2"
   ```

3. **Feature toggles**:
   ```hcl
   # Enable features based on requirements
   enable_databricks = true
   enable_synapse   = false
   ```

## 🏷️ Version Compatibility

All examples are tested with:
- **Terraform**: >= 1.0
- **AzureRM Provider**: >= 3.0
- **Module versions**: Latest stable releases

Always pin module versions in production:
```hcl
module "example" {
  source = "git::https://github.com/org/repo.git//terraform/module?ref=v1.2.0"
  # ... configuration
}
```

## 🔐 Security Considerations

### Default Security Posture
All examples implement security best practices:
- HTTPS-only storage accounts
- Private endpoints where applicable
- Managed identities for authentication
- Network segmentation
- Encryption at rest and in transit

### Environment-Specific Security
- **Development**: Simplified security for ease of use
- **Staging**: Production-like security for testing
- **Production**: Full security controls enabled

## 📊 Cost Optimization

### Development Environments
- Use Basic/Standard tiers
- Smaller capacity settings
- Limited redundancy (LRS instead of GRS)
- Auto-shutdown capabilities

### Production Environments
- Appropriate sizing for workloads
- High availability configurations
- Backup and disaster recovery
- Monitoring and alerting

## 🆘 Troubleshooting

### Common Issues

**Authentication errors**:
```bash
# Ensure you're logged in to Azure
az login
az account show
```

**Module not found**:
```bash
# Ensure you have access to the module repository
terraform init -upgrade
```

**Resource naming conflicts**:
```bash
# Use unique naming patterns
name_prefix = "mycompany-${var.environment}-${random_id.suffix.hex}"
```

### Getting Help

- **Issues**: Check the main repository issues
- **Documentation**: Review the module-specific documentation
- **Examples**: Look at similar examples for patterns
- **Community**: Use GitHub Discussions for questions

## 🔄 Contributing Examples

We welcome contributions of new examples! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

### Example Requirements
- **Clear documentation**: README with purpose and usage
- **Working code**: Tested and validated
- **Best practices**: Security and cost considerations
- **Variables**: Configurable for different scenarios

---

🚀 **Ready to deploy your Azure data platform? Choose an example and get started!**
