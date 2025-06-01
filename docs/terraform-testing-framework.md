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

**Run with**: `make test-terraform`

**Benefits**:
- Works in any environment without Azure credentials
- Fast execution (runs in ~90 seconds)
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

**Run with**: `make test-terraform-plan`

**Requirements**:
- Azure CLI authentication (`az login`)
- Valid Azure subscription
- Takes longer to execute due to provider initialization

## Quick Start

### Run Validation Tests (Recommended for daily development)

```bash
# Run validation tests only (no Azure auth required)
make test-terraform

# Or run specific validation tests
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
make test-terraform-plan
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

The testing framework integrates seamlessly with the development workflow:

```bash
# Fast checks during development
make pre-commit           # Format, lint, basic security

# Module validation during development  
make test-terraform       # Validate Terraform modules (90s)

# Comprehensive validation before commit
make check               # All checks including Terraform validation

# Full testing with Azure (optional)
make test-terraform-plan # Requires Azure authentication
```

This approach ensures high confidence in module quality while maintaining fast development cycles.
