"""
Test configuration for pytest.
"""

from pathlib import Path

import pytest


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests that don't require external dependencies"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests that may require external tools"
    )
    config.addinivalue_line("markers", "slow: Tests that take a long time to run")


@pytest.fixture
def project_root():
    """Fixture providing the project root directory."""
    return Path.cwd()


@pytest.fixture
def sample_terraform_module(tmp_path):
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
def sample_python_files(tmp_path):
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
