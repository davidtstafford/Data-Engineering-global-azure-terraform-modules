"""
Test configuration for pytest.
"""

from pathlib import Path
from typing import Any

import pytest


def pytest_configure(config: Any) -> None:
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests that don't require external dependencies"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests that may require external tools"
    )
    config.addinivalue_line("markers", "slow: Tests that take a long time to run")
    config.addinivalue_line("markers", "terraform: Tests that use Terraform CLI")
    config.addinivalue_line("markers", "terraform_plan: Tests that run terraform plan")
    config.addinivalue_line(
        "markers", "terraform_apply: Tests that actually deploy to Azure (dangerous)"
    )


@pytest.fixture
def project_root() -> Path:
    """Fixture providing the project root directory."""
    return Path.cwd()


@pytest.fixture
def sample_terraform_module(tmp_path: Path) -> Path:
    """Fixture creating a sample Terraform module for testing."""
    module_dir = tmp_path / "sample-module"
    module_dir.mkdir()

    # Create basic Terraform files
    (module_dir / "main.tf").write_text(
        """
# Sample Terraform module
resource "azurerm_resource_group" "example" {
  name     = var.resource_group_name
  location = var.location
}
"""
    )

    (module_dir / "variables.tf").write_text(
        """
variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "East US"
}
"""
    )

    (module_dir / "outputs.tf").write_text(
        """
output "resource_group_id" {
  description = "ID of the created resource group"
  value       = azurerm_resource_group.example.id
}
"""
    )

    (module_dir / "versions.tf").write_text(
        """
terraform {
  required_version = ">= 1.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0"
    }
  }
}
"""
    )

    (module_dir / "README.md").write_text(
        """
# Sample Module

This is a sample module for testing.

## Usage

```hcl
module "example" {
  source = "./sample-module"

  resource_group_name = "my-rg"
  location           = "East US"
}
```
"""
    )

    return module_dir


@pytest.fixture
def sample_python_files(tmp_path: Path) -> Path:
    """Fixture creating sample Python files for testing."""
    python_dir = tmp_path / "python_code"
    python_dir.mkdir()

    # Create a sample Python file with formatting issues
    (python_dir / "sample.py").write_text(
        """
import os
import sys
import json

def badly_formatted_function(param1,param2,param3):
    if param1=='test':
        result={'key1':param2,'key2':param3}
        return result
    else:
        return None

class BadlyFormattedClass:
    def __init__(self,name):
        self.name=name

    def get_name(self):
        return self.name
"""
    )

    return python_dir


@pytest.fixture
def terraform_resource_group_module(project_root: Path) -> Path:
    """Fixture providing the path to the resource group Terraform module."""
    return project_root / "terraform" / "foundation" / "resource-group"


@pytest.fixture
def terraform_modules_root(project_root: Path) -> Path:
    """Fixture providing the path to all Terraform modules."""
    return project_root / "terraform"


@pytest.fixture(scope="session")
def terraform_available():
    """Fixture to check if Terraform is available for testing."""
    from tests.terraform.config import TerraformTestConfig

    return not TerraformTestConfig.should_skip_terraform_tests()


@pytest.fixture(scope="session", autouse=True)
def skip_terraform_if_unavailable(terraform_available):
    """Auto-fixture to skip Terraform tests if Terraform is not available."""
    from tests.terraform.config import TerraformTestConfig

    if not terraform_available:
        pytest.skip(
            f"Skipping Terraform tests: {TerraformTestConfig.get_skip_reason()}"
        )
