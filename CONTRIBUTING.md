# Contributing to Azure Terraform Modules

Thank you for your interest in contributing to this project! This guide will help you understand our development process and standards.

## 🎯 Project Goals

This repository provides **reusable, production-ready Terraform modules** for Azure data engineering platforms. Our modules should be:

- **Reliable**: Thoroughly tested and validated
- **Secure**: Follow Azure security best practices
- **Documented**: Clear usage examples and parameter docs
- **Versioned**: Stable releases using Git tags
- **Composable**: Work well together and with external modules

## 🚀 Getting Started

### Development Environment

We use a **single virtual environment** approach with Poetry for simplicity:

```bash
# Clone and setup
git clone https://github.com/davidtstafford/Data-Engineering-global-azure-terraform-modules.git
cd azure-terraform-modules

# Install dependencies (creates .venv with all tools)
poetry install

# Activate virtual environment
poetry shell

# Verify setup
poetry run pytest --version
poetry run black --version
```

### Development Tools

All development tools are installed in the single `.venv` environment:

- **Testing**: pytest, pytest-cov, pytest-mock
- **Formatting**: black, isort
- **Linting**: flake8, mypy
- **Security**: checkov, bandit
- **Git hooks**: pre-commit

## 📝 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

### 2. Development Standards

#### **Terraform Standards**
- Use consistent variable naming (`snake_case`)
- Include comprehensive variable descriptions
- Add appropriate variable validation
- Use data sources where appropriate
- Follow Azure naming conventions

#### **Python Standards**
- Follow PEP 8 (enforced by black/flake8)
- Use type hints (enforced by mypy)
- Write comprehensive docstrings
- Add unit tests for all functions

#### **Documentation Standards**
- Update README.md for module changes
- Include usage examples
- Document all input/output variables
- Add inline comments for complex logic

### 3. Code Quality Checks

Run all checks before committing:

```bash
# Format code
poetry run black scripts/
poetry run isort scripts/

# Lint code
poetry run flake8 scripts/
poetry run mypy scripts/

# Security scan
poetry run bandit -r scripts/
poetry run checkov -d terraform/

# Run tests
poetry run pytest tests/ -v --cov=scripts
```

### 4. Commit Standards

Use conventional commits for clear history:

```bash
# Feature commits
git commit -m "feat: add storage account module with encryption"

# Bug fixes
git commit -m "fix: resolve resource group naming validation"

# Documentation
git commit -m "docs: update contributing guidelines"

# Testing
git commit -m "test: add unit tests for validation script"
```

### 5. Pre-commit Hooks

Install pre-commit hooks to run checks automatically:

```bash
poetry run pre-commit install
```

This will run formatting, linting, and basic validation on every commit.

## 🏗️ Module Development

### Creating a New Module

1. **Plan the module structure**:
   ```
   terraform/category/module-name/
   ├── README.md           # Module documentation
   ├── main.tf            # Main resources
   ├── variables.tf       # Input variables
   ├── outputs.tf         # Output values
   ├── versions.tf        # Provider requirements
   └── examples/          # Usage examples
       └── basic/
           ├── main.tf
           └── README.md
   ```

2. **Follow naming conventions**:
   - Module names: `kebab-case` (e.g., `storage-account`)
   - Resource names: `snake_case` (e.g., `azurerm_storage_account`)
   - Variable names: `snake_case` (e.g., `storage_account_name`)

3. **Include comprehensive documentation**:
   - Clear module purpose and use cases
   - All input/output variable documentation
   - Basic and advanced usage examples
   - Security considerations

### Module Testing

Test modules thoroughly before submission:

```bash
# Validate Terraform syntax
poetry run python scripts/validate.py --module terraform/foundation/storage-account

# Security scanning
poetry run checkov -d terraform/foundation/storage-account

# Format checking
terraform fmt -check terraform/foundation/storage-account
```

## 🔍 Testing Requirements

### Python Script Testing

All Python scripts must have comprehensive test coverage:

```bash
# Run specific test file
poetry run pytest tests/test_validate.py -v

# Run with coverage
poetry run pytest tests/ --cov=scripts --cov-report=html

# Coverage should be >90%
```

### Terraform Module Testing

While we don't run live Azure tests in CI, modules should be:

- **Syntax validated**: `terraform validate`
- **Security scanned**: `checkov -d <module-path>`
- **Format checked**: `terraform fmt -check`
- **Documentation complete**: All variables/outputs documented

## 📚 Documentation Standards

### Module README Structure

Each module should have a comprehensive README.md:

```markdown
# Module Name

Brief description of what the module does.

## Usage

```hcl
module "example" {
  source = "git::https://github.com/org/repo.git//terraform/category/module?ref=v1.0.0"
  
  # Required variables
  name = "example"
  
  # Optional variables
  tags = {
    Environment = "production"
  }
}
```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.0 |
| azurerm | >= 3.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| name | Resource name | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| id | Resource ID |
```

### Code Comments

- **Terraform**: Comment complex logic and business rules
- **Python**: Use docstrings for functions and classes
- **Configuration**: Explain non-obvious settings

## 🚨 Security Guidelines

### Terraform Security

- **No hardcoded secrets**: Use Azure Key Vault references
- **Least privilege**: Minimal required permissions
- **Network security**: Private endpoints where possible
- **Encryption**: Enable encryption at rest and in transit
- **Monitoring**: Include diagnostic settings

### Python Security

- **Input validation**: Validate all user inputs
- **Error handling**: Don't leak sensitive information
- **Dependencies**: Keep dependencies updated
- **Secrets**: Never commit credentials or keys

## 🎯 Pull Request Process

### Before Submitting

1. **Run all quality checks**: formatting, linting, tests
2. **Update documentation**: README, examples, comments
3. **Test manually**: Verify your changes work
4. **Rebase on main**: Ensure clean history

### PR Requirements

- **Clear title**: Describe what the PR does
- **Detailed description**: Explain why and how
- **Breaking changes**: Call out any breaking changes
- **Testing notes**: How to test the changes
- **Documentation**: Links to updated docs

### Review Process

1. **Automated checks**: CI must pass
2. **Code review**: At least one approval required
3. **Security review**: For new modules or security changes
4. **Documentation review**: Ensure docs are complete

## 🏷️ Release Process

### Versioning

We follow semantic versioning:

- **Major (v2.0.0)**: Breaking changes
- **Minor (v1.1.0)**: New features, backwards compatible
- **Patch (v1.0.1)**: Bug fixes

### Creating Releases

1. **Update version** in relevant files
2. **Update CHANGELOG.md** with changes
3. **Create PR** with version bump
4. **Merge to main** after approval
5. **Create Git tag** with release notes
6. **Update documentation** links if needed

## ❓ Getting Help

- **Questions**: Use GitHub Discussions
- **Bugs**: Create a GitHub Issue
- **Features**: Create a GitHub Issue with feature template
- **Urgent**: Contact maintainers directly

## 🤝 Code of Conduct

Be respectful, inclusive, and professional in all interactions. We welcome contributors from all backgrounds and experience levels.

---

Thank you for contributing to Azure Terraform Modules! 🚀
