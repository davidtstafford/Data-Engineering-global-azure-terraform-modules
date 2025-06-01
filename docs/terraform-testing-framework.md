# Terraform Testing Framework

This project includes a comprehensive Terraform testing framework that validates modules for use as reusable components in other repositories.

## Testing Approach

Since these Terraform modules are designed to be **consumed by other repositories** (not deployed directly from this repo), the testing framework focuses on validation and static analysis rather than deployment testing.

### Validation-Only Testing ✅

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
- Validates modules are ready for consumption by other repositories

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

| Command                   | Scope                | Use Case              | Time (1 module) | Time (20 modules) |
| ------------------------- | -------------------- | --------------------- | --------------- | ----------------- |
| `make test-terraform`     | Changed modules only | Daily development     | ~90 seconds     | ~90 seconds*      |
| `make test-terraform-all` | ALL modules          | Release validation    | ~90 seconds     | ~30 minutes       |

*Assuming only 1 module changed

## Why No Plan Testing?

This repository contains **reusable Terraform modules** that are consumed by other repositories. Plan testing doesn't make sense here because:

1. **No deployment context** - This repo doesn't know the actual deployment scenarios
2. **Different subscriptions** - Each consuming repo may deploy to different Azure subscriptions  
3. **Different configurations** - Consuming repos will have their own variable values
4. **False confidence** - Plan tests here don't validate real-world usage

Instead, **consuming repositories** should implement their own integration tests that validate the modules in their specific deployment contexts.

## Quick Start

### Run Validation Tests (Recommended for all development)

```bash
# Run validation tests for changed modules only (FAST)
make test-terraform

# Run validation tests for ALL modules (COMPREHENSIVE)
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

## Test Structure

```
tests/terraform/
├── base_validation.py                     # Validation-only test framework
├── config.py                              # Configuration and utilities
├── fixtures/
│   └── test_data.py                       # Test data and configurations
└── modules/
    └── test_resource_group_validation.py  # Validation tests ✅
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

The testing framework provides validation that ensures modules are ready for consumption by other repositories:

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

#### 2. Release Validation (Comprehensive Testing)
```bash
# For major releases, test everything
make test-terraform-all      # ~90 seconds × number of modules
```

#### 3. CI/CD Pipeline Integration

**Pull Request Pipeline (Recommended)**:
```yaml
# Fast validation without any special setup
- make test-terraform    # Smart: only tests changed modules
- make check            # All formatting/linting/security checks
```

**Release Pipeline (Full Validation)**:
```yaml
# Complete validation for major releases
- make test-terraform-all     # Test ALL modules
```

### Testing Strategy by Environment

| Environment           | Validation Tests  | Commands              | Rationale                  |
| --------------------- | ----------------- | --------------------- | -------------------------- |
| **Local Development** | ✅ Changed modules | `make test-terraform` | Fast feedback loop         |
| **Feature Branch**    | ✅ Changed modules | `make test-terraform` | Quick validation in PR     |
| **Main Branch**       | ✅ Changed modules | `make test-terraform` | Pre-merge validation       |
| **Release**           | ✅ All modules     | `make test-terraform-all` | Maximum confidence     |

### Performance Considerations

| Test Type            | Smart Commands         | Full Commands            | Scalability                    |
| -------------------- | ---------------------- | ------------------------ | ------------------------------ |
| **Validation Tests** | ~90 seconds per change | ~90 seconds × modules    | 🚀 Scales linearly with changes |
| **Full Check**       | ~2 minutes             | ~2 minutes               | ✅ Always fast                  |

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

#### Debugging Workflow

```bash
# Step 1: Run validation tests first (fast)
make test-terraform

# Step 2: Debug specific issues
poetry run pytest tests/terraform/modules/test_resource_group_validation.py::test_specific_test -v -s
```

This approach ensures high confidence in module quality while maintaining fast development cycles and preparing modules for consumption by other repositories.
