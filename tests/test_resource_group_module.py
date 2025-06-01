"""Test cases for the resource-group Terraform module."""

from pathlib import Path

import pytest


class TestResourceGroupModule:
    """Test cases for the resource-group module structure and content."""

    @pytest.fixture
    def module_path(self) -> Path:
        """Get the path to the resource-group module."""
        project_root = Path(__file__).parent.parent
        return project_root / "terraform" / "foundation" / "resource-group"

    def test_module_files_exist(self, module_path: Path) -> None:
        """Test that all required module files exist."""
        required_files = [
            "main.tf",
            "variables.tf",
            "outputs.tf",
            "versions.tf",
            "README.md",
        ]

        for file_name in required_files:
            file_path = module_path / file_name
            assert file_path.exists(), f"Required file {file_name} does not exist"

    def test_example_files_exist(self, module_path: Path) -> None:
        """Test that example files exist."""
        example_path = module_path / "examples" / "basic"
        required_files = ["main.tf", "variables.tf", "outputs.tf", "README.md"]

        for file_name in required_files:
            file_path = example_path / file_name
            assert (
                file_path.exists()
            ), f"Required example file {file_name} does not exist"

    def test_main_tf_contains_resource(self, module_path: Path) -> None:
        """Test that main.tf contains the azurerm_resource_group resource."""
        main_tf = module_path / "main.tf"
        content = main_tf.read_text()

        assert 'resource "azurerm_resource_group" "this"' in content
        assert "name     = var.name" in content
        assert "location = var.location" in content
        assert "tags     = var.tags" in content

    def test_variables_tf_contains_required_vars(self, module_path: Path) -> None:
        """Test that variables.tf contains required variables."""
        variables_tf = module_path / "variables.tf"
        content = variables_tf.read_text()

        assert 'variable "name"' in content
        assert 'variable "location"' in content
        assert 'variable "tags"' in content

    def test_outputs_tf_contains_required_outputs(self, module_path: Path) -> None:
        """Test that outputs.tf contains required outputs."""
        outputs_tf = module_path / "outputs.tf"
        content = outputs_tf.read_text()

        assert 'output "id"' in content
        assert 'output "name"' in content
        assert 'output "location"' in content
        assert 'output "tags"' in content

    def test_versions_tf_contains_requirements(self, module_path: Path) -> None:
        """Test that versions.tf contains terraform and provider requirements."""
        versions_tf = module_path / "versions.tf"
        content = versions_tf.read_text()

        assert 'required_version = ">= 1.0"' in content
        assert "hashicorp/azurerm" in content
        assert 'version = ">= 3.0"' in content

    def test_readme_exists_and_has_content(self, module_path: Path) -> None:
        """Test that README.md exists and has basic content."""
        readme = module_path / "README.md"
        content = readme.read_text()

        assert "# Azure Resource Group Module" in content
        assert "## Usage" in content
        assert "## Requirements" in content
        assert "## Inputs" in content
        assert "## Outputs" in content

    def test_example_references_module_correctly(self, module_path: Path) -> None:
        """Test that the example references the module correctly."""
        example_main = module_path / "examples" / "basic" / "main.tf"
        content = example_main.read_text()

        assert 'module "resource_group"' in content
        assert 'source = "../../"' in content
