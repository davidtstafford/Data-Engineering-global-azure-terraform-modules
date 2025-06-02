"""Test cases for the diagnostic-settings Terraform module."""

from pathlib import Path

import pytest


class TestDiagnosticSettingsModule:
    """Test cases for the diagnostic-settings module structure and content."""

    @pytest.fixture
    def module_path(self) -> Path:
        """Get the path to the diagnostic-settings module."""
        project_root = Path(__file__).parent.parent
        return project_root / "terraform" / "foundation" / "diagnostic-settings"

    def test_module_files_exist(self, module_path: Path) -> None:
        """Test that all required module files exist."""
        required_files = [
            "main.tf",
            "variables.tf",
            "outputs.tf",
            "versions.tf",
            "locals.tf",
            "README.md",
        ]

        for file_name in required_files:
            file_path = module_path / file_name
            assert file_path.exists(), f"Required file {file_name} does not exist"

    def test_example_files_exist(self, module_path: Path) -> None:
        """Test that example files exist."""
        examples = [
            "basic",
            "complex-configuration",
            "eventhub-streaming",
            "multi-destination",
            "storage-with-retention",
        ]

        for example in examples:
            example_path = module_path / "examples" / example
            required_files = ["main.tf", "variables.tf", "outputs.tf", "README.md"]

            for file_name in required_files:
                file_path = example_path / file_name
                assert (
                    file_path.exists()
                ), f"Required example file {file_name} does not exist in {example}"

    def test_main_tf_contains_resource(self, module_path: Path) -> None:
        """Test that main.tf contains the azurerm_monitor_diagnostic_setting resource."""
        main_tf = module_path / "main.tf"
        content = main_tf.read_text()

        assert 'resource "azurerm_monitor_diagnostic_setting" "this"' in content
        assert "name               = var.name" in content
        assert "target_resource_id = var.target_resource_id" in content

    def test_variables_tf_contains_required_vars(self, module_path: Path) -> None:
        """Test that variables.tf contains required variables."""
        variables_tf = module_path / "variables.tf"
        content = variables_tf.read_text()

        # Core required variables
        assert 'variable "name"' in content
        assert 'variable "target_resource_id"' in content

        # Destination variables
        assert 'variable "log_analytics_workspace_id"' in content
        assert 'variable "storage_account_id"' in content
        assert 'variable "eventhub_authorization_rule_id"' in content
        assert 'variable "eventhub_name"' in content

        # Configuration variables
        assert 'variable "categories"' in content
        assert 'variable "category_groups"' in content
        assert 'variable "metrics"' in content

    def test_variables_have_validation(self, module_path: Path) -> None:
        """Test that key variables have validation rules."""
        variables_tf = module_path / "variables.tf"
        content = variables_tf.read_text()

        # Should have validation blocks for critical variables
        assert "validation {" in content
        assert "regex(" in content
        assert "error_message" in content

    def test_outputs_tf_contains_required_outputs(self, module_path: Path) -> None:
        """Test that outputs.tf contains required outputs."""
        outputs_tf = module_path / "outputs.tf"
        content = outputs_tf.read_text()

        assert 'output "id"' in content
        assert 'output "name"' in content
        assert 'output "target_resource_id"' in content

    def test_locals_tf_contains_destination_validation(self, module_path: Path) -> None:
        """Test that locals.tf contains destination validation logic."""
        locals_tf = module_path / "locals.tf"
        content = locals_tf.read_text()

        assert "locals {" in content
        assert "has_destination" in content or "destination" in content

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

        assert "Diagnostic Settings" in content
        assert "## Usage" in content
        assert "## Variables" in content or "## Inputs" in content
        assert "## Outputs" in content

    def test_main_tf_has_dynamic_blocks(self, module_path: Path) -> None:
        """Test that main.tf uses dynamic blocks for flexible configuration."""
        main_tf = module_path / "main.tf"
        content = main_tf.read_text()

        assert "dynamic " in content
        assert "enabled_log" in content or "metric" in content

    def test_main_tf_has_lifecycle_rules(self, module_path: Path) -> None:
        """Test that main.tf has lifecycle validation rules."""
        main_tf = module_path / "main.tf"
        content = main_tf.read_text()

        assert "lifecycle {" in content
        assert "precondition {" in content or "postcondition {" in content

    def test_examples_reference_module_correctly(self, module_path: Path) -> None:
        """Test that examples reference the module correctly."""
        examples = [
            "basic",
            "complex-configuration",
            "eventhub-streaming",
            "multi-destination",
            "storage-with-retention",
        ]

        for example in examples:
            example_main = module_path / "examples" / example / "main.tf"
            if example_main.exists():
                content = example_main.read_text()

                assert 'module "diagnostic_settings"' in content
                assert 'source = "../../"' in content

    def test_variable_types_are_correct(self, module_path: Path) -> None:
        """Test that variables have correct types."""
        variables_tf = module_path / "variables.tf"
        content = variables_tf.read_text()

        # String variables
        assert "type        = string" in content

        # List variables
        assert "type        = list(string)" in content
        assert "list(object(" in content

    def test_variable_defaults_are_appropriate(self, module_path: Path) -> None:
        """Test that variables have appropriate default values."""
        variables_tf = module_path / "variables.tf"
        content = variables_tf.read_text()

        # Optional destination variables should default to null
        assert "default     = null" in content

        # List variables should default to empty lists
        assert "default = []" in content

    def test_outputs_have_descriptions(self, module_path: Path) -> None:
        """Test that all outputs have descriptions."""
        outputs_tf = module_path / "outputs.tf"
        content = outputs_tf.read_text()

        # Count outputs and descriptions
        output_count = content.count('output "')
        description_count = content.count("description =")

        assert output_count > 0, "Module should have outputs"
        assert output_count == description_count, "All outputs should have descriptions"

    def test_variables_have_descriptions(self, module_path: Path) -> None:
        """Test that all variables have descriptions."""
        variables_tf = module_path / "variables.tf"
        content = variables_tf.read_text()

        # Count variables and descriptions
        variable_count = content.count('variable "')
        description_count = content.count("description =")

        assert variable_count > 0, "Module should have variables"
        assert (
            variable_count == description_count
        ), "All variables should have descriptions"

    def test_azure_resource_id_validation_patterns(self, module_path: Path) -> None:
        """Test that Azure resource ID validation patterns are correct."""
        variables_tf = module_path / "variables.tf"
        content = variables_tf.read_text()

        # Should validate Azure resource ID format
        assert "/subscriptions/" in content
        assert "/resourceGroups/" in content
        assert "/providers/" in content

    def test_retention_policy_validation(self, module_path: Path) -> None:
        """Test that retention policy validation is present."""
        variables_tf = module_path / "variables.tf"
        content = variables_tf.read_text()

        # Should validate retention days
        assert "days" in content
        assert "365" in content or "retention" in content.lower()
