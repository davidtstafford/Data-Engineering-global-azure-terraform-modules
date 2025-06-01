# Terraform Testing Framework

This project includes a comprehensive Terraform testing framework that validates modules without requiring Azure authentication.

## Testing Approach

The testing framework uses two complementary approaches:

### 1. Validation-Only Testing (No Azure Auth Required) ✅

**Location**: `tests/terraform/modules/test_resource_group_validation.py`

**What it tests**:
- HCL syntax validation using `terraform validate`
- Module structure (required files: main.tf, variables.tf, outputs.tf)
- Variable and output definitions
- Terraform formatting with `terraform fmt`
- Static analysis of module structure
- Configuration validation with different variable sets

**Run with**: `make test-terraform` (smart: changed modules only)

**Benefits**:
- Works in any environment without Azure credentials
- Fast execution (runs in ~90 seconds per module)
- **Smart testing**: Only tests modules that have changed
- Scales efficiently as project grows (20 modules = still ~90 seconds if only 1 changed)
- Catches syntax errors, structural issues, and basic configuration problems
- Perfect for CI/CD pipelines and local development

### 2. Plan-Based Testing (Requires Azure Auth) ⚠️

**Location**: `tests/terraform/modules/test_resource_group_terraform.py`

**What it tests**:
- Full terraform plan execution
- Resource creation validation
- Tag verification
- Output value checking
- Resource count validation

**Run with**: `make test-terraform-plan` (smart: changed modules only)

**Requirements**:
- Azure CLI authentication (`az login`)
- Valid Azure subscription
- Takes longer to execute due to provider initialization (~5 minutes per module)

## Smart Testing Architecture

The testing framework includes intelligent change detection that dramatically improves scalability:

### How Smart Testing Works

1. **Change Detection**: Automatically detects modified files by comparing:
   - Current branch vs. `main` branch
   - Uncommitted changes (staged and unstaged)
   - New untracked files in `terraform/` directory

2. **Module Mapping**: Maps changed files to affected Terraform modules
   - `terraform/foundation/resource-group/main.tf` → Test `resource-group` module
   - Test files themselves don't trigger module testing

3. **Selective Execution**: Runs tests only for affected modules
   - 1 module changed = ~90 seconds
   - 0 modules changed = ~5 seconds (no tests needed)

### Smart vs. Full Testing Commands

| Command                        | Scope                | Use Case           | Time (1 module) | Time (20 modules) |
| ------------------------------ | -------------------- | ------------------ | --------------- | ----------------- |
| `make test-terraform`          | Changed modules only | Daily development  | ~90 seconds     | ~90 seconds*      |
| `make test-terraform-all`      | ALL modules          | Release validation | ~90 seconds     | ~30 minutes       |
| `make test-terraform-plan`     | Changed modules only | Pre-deployment     | ~5 minutes      | ~5 minutes*       |
| `make test-terraform-plan-all` | ALL modules          | Full validation    | ~5 minutes      | ~100 minutes      |

*Assuming only 1 module changed

## Azure Authentication Setup

### Prerequisites

Before running plan-based tests, ensure you have:

1. **Azure CLI installed**:
   ```bash
   az --version  # Should show Azure CLI version
   ```

2. **Azure subscription access** with permissions to:
   - Read subscription details
   - Create/plan resource groups
   - Access Azure Resource Manager APIs

### Authentication Process

1. **Login to Azure**:
   ```bash
   az login
   ```
   This opens a browser window for authentication. Complete the login process.

2. **Verify authentication**:
   ```bash
   az account show
   ```
   Should display your subscription details including:
   - Subscription ID
   - Subscription name
   - User/service principal information

3. **Set subscription (if you have multiple)**:
   ```bash
   # List available subscriptions
   az account list --output table
   
   # Set the desired subscription
   az account set --subscription "Your-Subscription-Name-or-ID"
   ```

4. **Test Azure connectivity**:
   ```bash
   az group list --output table
   ```
   Should list resource groups (or show empty if none exist).

### Running Plan Tests

Once authenticated, you can run the full plan-based tests:

```bash
# Run plan tests for all modules
make test-terraform-plan

# Run plan tests for specific module
poetry run pytest tests/terraform/modules/test_resource_group_terraform.py -v -m "terraform"
```

### Troubleshooting Authentication Issues

#### Error: `subscription_id` is a required provider property

**Symptoms**:
```
Error: `subscription_id` is a required provider property when performing a plan/apply operation
  with provider["registry.terraform.io/hashicorp/azurerm"]
```

**Solution**:
1. Run `az login` to authenticate
2. Verify with `az account show`
3. Ensure your session hasn't expired

#### Error: Please run 'az login' to setup account

**Symptoms**:
```
ERROR: Please run 'az login' to setup account.
```

**Solution**:
1. Your Azure CLI session has expired
2. Run `az login` again
3. Re-run the tests

#### Error: Insufficient permissions

**Symptoms**:
```
Error: You do not have permission to perform this operation
```

**Solution**:
1. Verify your account has appropriate permissions in the subscription
2. Contact your Azure administrator to grant necessary permissions
3. Minimum required permissions:
   - Reader access to subscription
   - Ability to create resource groups (for actual deployment)

#### Error: Subscription not found

**Symptoms**:
```
Error: The subscription 'xyz' could not be found
```

**Solution**:
1. Check available subscriptions: `az account list`
2. Set the correct subscription: `az account set --subscription "correct-name"`
3. Verify: `az account show`

### Plan Test Execution Time

Plan-based tests take significantly longer than validation tests:

- **Validation tests**: ~90 seconds (no Azure calls)
- **Plan tests**: ~5-10 minutes (includes Azure provider initialization and API calls)

This is why validation tests are recommended for daily development and CI/CD pipelines.

### Plan Test Coverage Details

The plan-based testing suite includes **11 comprehensive tests** that validate actual Azure resource planning:

#### Core Functionality Tests (7 tests)

1. **test_basic_resource_group_plan**
   - Tests resource group creation with full configuration (name, location, tags)
   - Validates that exactly one resource group is planned for creation
   - Verifies all attributes match expected values

2. **test_minimal_resource_group_plan**
   - Tests resource group creation with minimal configuration (no tags)
   - Ensures the module works with only required parameters
   - Validates that tags are handled correctly when not provided

3. **test_resource_group_with_extensive_tags**
   - Tests complex tagging scenarios with multiple tags
   - Validates that all tags are correctly applied to the resource
   - Ensures tag validation logic works properly

4. **test_module_outputs_are_defined**
   - Verifies that the module exposes expected outputs (id, name, location, tags)
   - Tests output value propagation through Terraform plan
   - Ensures output structure matches module specification

5. **test_missing_required_variables_fails**
   - Tests error handling when required variables are missing
   - Validates that Terraform plan fails gracefully with appropriate errors
   - Ensures input validation is working correctly

6. **test_resource_count_is_correct**
   - Verifies that exactly one resource is created (no more, no less)
   - Tests resource planning accuracy
   - Ensures module doesn't create unexpected resources

7. **test_no_destructive_changes**
   - Validates that initial planning only creates resources
   - Ensures no updates or deletions are planned unexpectedly
   - Tests safe resource planning behavior

#### Parameterized Location Tests (4 tests)

8-11. **test_valid_locations** (parametrized across 4 Azure regions)
   - Tests module compatibility with different Azure regions:
     - East US
     - West US 2  
     - West Europe
     - UK South
   - Validates location parameter handling
   - Ensures geographic flexibility

#### Why These Tests Require Azure Authentication

All plan-based tests require Azure authentication because they:

- **Initialize the AzureRM provider**: Requires valid Azure credentials
- **Query Azure APIs**: To validate locations, subscription access, and resource planning
- **Generate resource plans**: Terraform needs to contact Azure to create execution plans
- **Validate provider configuration**: Azure provider requires subscription context

**Expected Failure Without Authentication**:
```
Error: `subscription_id` is a required provider property when performing a plan/apply operation
```

This is why validation tests are recommended for daily development and CI/CD pipelines.

**Requirements**:
- Azure CLI authentication (`az login`)
- Valid Azure subscription
- Takes longer to execute due to provider initialization

## Quick Start

### Run Validation Tests (Recommended for daily development)

```bash
# Run validation tests for changed modules only (FAST)
make test-terraform

# Run validation tests for ALL modules (SLOW - use sparingly)
make test-terraform-all

# Or run specific validation tests manually
poetry run pytest tests/terraform/modules/test_resource_group_validation.py -v
```

### Run All Tests

```bash
# Run both Python and Terraform validation tests
make test-all

# Run comprehensive checks (formatting, linting, security, tests)
make check
```

### Run Plan Tests (if you have Azure access)

```bash
# Requires: az login
# Test changed modules only (RECOMMENDED)
make test-terraform-plan

# Test ALL modules (SLOW - only for full validation)  
make test-terraform-plan-all
```

## Test Structure

```
tests/terraform/
├── base_validation.py          # Validation-only test framework
├── base.py                     # Plan-based test framework (original)
├── config.py                   # Configuration and utilities
├── fixtures/
│   └── test_data.py           # Test data and configurations
└── modules/
    ├── test_resource_group_validation.py  # Validation tests ✅
    └── test_resource_group_terraform.py   # Plan tests (requires Azure)
```

## Test Coverage

The validation framework includes **18 tests** covering:

### Module Structure Tests
- ✅ Required files exist (main.tf, variables.tf, outputs.tf)
- ✅ Expected variables are defined
- ✅ Expected outputs are defined
- ✅ Azure resources are properly defined
- ✅ All variables are used in the module
- ✅ Version constraints are specified

### Syntax Validation Tests
- ✅ HCL syntax validation with different configurations
- ✅ Multiple Azure location support
- ✅ Terraform formatting compliance
- ✅ Complex tags configuration
- ✅ Multiple module instances

### Static Analysis Tests
- ✅ Module structure scoring
- ✅ Variable usage validation
- ✅ Provider configuration validation
- ✅ Comprehensive module health checks

## Key Features

### 🚀 Fast Feedback
- Validation tests run in ~90 seconds
- No Azure authentication required
- Perfect for rapid development cycles

### 🔒 CI/CD Ready
- Works in any CI environment
- No cloud credentials needed for basic validation
- Comprehensive syntax and structure checking

### 📊 Comprehensive Coverage
- Tests module structure and best practices
- Validates HCL syntax and formatting
- Checks variable definitions and usage
- Supports parameterized testing for multiple scenarios

### 🛠 Extensible Framework
- Easy to add new modules
- Reusable test utilities
- Clear separation of validation vs. plan testing

## Adding Tests for New Modules

To add tests for a new Terraform module:

1. **Create validation tests** (recommended):
   ```python
   # tests/terraform/modules/test_your_module_validation.py
   from tests.terraform.base_validation import TerraformValidationTest
   # Add your validation tests here
   ```

2. **Create plan tests** (optional, requires Azure):
   ```python
   # tests/terraform/modules/test_your_module_terraform.py
   from tests.terraform.base import TerraformTestBase
   # Add your plan tests here
   ```

3. **Add test configurations**:
   ```python
   # tests/terraform/fixtures/test_data.py
   YOUR_MODULE_TEST_CONFIGS = {
       "basic": {"param1": "value1"},
       # Add your test scenarios
   }
   ```

## Integration with Development Workflow

The testing framework provides a multi-layered approach to validation that supports different development workflows:

### Recommended Development Workflow

#### 1. Daily Development Loop (Fast Feedback)
```bash
# Make code changes to Terraform modules
vim terraform/foundation/resource-group/main.tf

# Run smart validation tests (only tests changed modules)
make test-terraform       # ~30-90 seconds (scales with project size!)

# Run all formatting and basic checks
make pre-commit          # Format, lint, basic security (~30 seconds)

# Before committing: run comprehensive validation
make check              # All checks including smart Terraform validation (~2 minutes)
```

#### 2. Pre-Deployment Validation (Comprehensive)
```bash
# Authenticate with Azure
az login

# Run smart plan-based tests for changed modules
make test-terraform-plan # ~2-5 minutes (only affected modules)

# Deploy with confidence
terraform apply
```

#### 3. Release Validation (Full Testing)
```bash
# For major releases, test everything
make test-terraform-all      # ~90 seconds × number of modules
make test-terraform-plan-all # ~5 minutes × number of modules (requires Azure)
```

#### 3. CI/CD Pipeline Integration

**Pull Request Pipeline (Recommended)**:
```yaml
# Fast validation without Azure credentials
- make test-terraform    # Smart: only tests changed modules
- make check            # All formatting/linting/security checks
```

**Deployment Pipeline (Optional)**:
```yaml
# Smart validation with Azure authentication
- az login --service-principal ...
- make test-terraform-plan    # Smart: only tests changed modules
- terraform apply
```

**Release Pipeline (Full Validation)**:
```yaml
# Complete validation for major releases
- make test-terraform-all     # Test ALL modules
- make test-terraform-plan-all # Plan test ALL modules (if Azure auth available)
```

### Testing Strategy by Environment

| Environment           | Validation Tests  | Plan Tests    | Commands              | Rationale                  |
| --------------------- | ----------------- | ------------- | --------------------- | -------------------------- |
| **Local Development** | ✅ Changed modules | ⚠️ Optional    | `make test-terraform` | Fast feedback loop         |
| **Feature Branch**    | ✅ Changed modules | ❌ Skip        | `make test-terraform` | No Azure credentials in PR |
| **Main Branch**       | ✅ Changed modules | ✅ Optional    | Smart commands        | Pre-deployment validation  |
| **Production Deploy** | ✅ All modules     | ✅ All modules | `make *-all` commands | Maximum confidence         |

### Performance Considerations

| Test Type            | Smart Commands             | Full Commands               | Scalability                    |
| -------------------- | -------------------------- | --------------------------- | ------------------------------ |
| **Validation Tests** | ~90 seconds/changed module | ~90 seconds × total modules | 🚀 Scales linearly with changes |
| **Plan Tests**       | ~5 minutes/changed module  | ~5 minutes × total modules  | 🚀 Scales linearly with changes |
| **Full Check**       | ~2 minutes                 | ~2 minutes                  | ✅ Always fast                  |

**Example Scaling:**
- **Small project (3 modules)**: Smart vs. Full = same performance
- **Medium project (10 modules)**: 1 module changed = 90s vs. 15 minutes  
- **Large project (20 modules)**: 1 module changed = 90s vs. 30 minutes

### Error Handling and Debugging

#### Common Development Issues

1. **Validation test failures** (fast to debug):
   - HCL syntax errors
   - Module structure issues
   - Variable definition problems

2. **Plan test failures** (requires Azure access):
   - Authentication issues
   - Provider configuration problems
   - Azure API connectivity issues

#### Debugging Workflow

```bash
# Step 1: Run validation tests first (fast)
make test-terraform

# Step 2: If validation passes, check plan tests
az login
make test-terraform-plan

# Step 3: Debug specific issues
poetry run pytest tests/terraform/modules/test_resource_group_validation.py::test_specific_test -v -s
```

This approach ensures high confidence in module quality while maintaining fast development cycles.
