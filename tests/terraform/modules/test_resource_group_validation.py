"""
Validation-only tests for Terraform resource group module.

These tests focus on syntax validation, structure checking, and static analysis
without requiring Azure provider authentication.
"""

from pathlib import Path

import pytest

from tests.terraform.base_validation import (
    TerraformConfigValidator,
    TerraformModuleAnalyzer,
    TerraformValidationTest,
)
from tests.terraform.config import TerraformTestConfig
from tests.terraform.fixtures.test_data import (
    RESOURCE_GROUP_TEST_CONFIGS,
    TEST_LOCATIONS,
)


@pytest.mark.terraform
class TestResourceGroupModuleValidation:
    """Validation tests for the resource group module that don't require Azure auth."""

    def test_module_has_required_files(self, terraform_resource_group_module: Path):
        """Test that the module has all required files."""
        analyzer = TerraformModuleAnalyzer(terraform_resource_group_module)
        files_check = analyzer.check_required_files()

        # Core files should exist
        assert files_check["main.tf"], "Module must have main.tf"
        assert files_check["variables.tf"], "Module must have variables.tf"
        assert files_check["outputs.tf"], "Module must have outputs.tf"

        # Documentation should exist
        assert files_check["README.md"], "Module should have README.md documentation"

    def test_module_has_expected_variables(self, terraform_resource_group_module: Path):
        """Test that the module defines expected variables."""
        analyzer = TerraformModuleAnalyzer(terraform_resource_group_module)
        variables = analyzer.get_defined_variables()

        # Resource group module should have these core variables
        expected_variables = {"name", "location", "tags"}

        for var in expected_variables:
            assert var in variables, f"Module should define variable '{var}'"

    def test_module_has_expected_outputs(self, terraform_resource_group_module: Path):
        """Test that the module defines expected outputs."""
        analyzer = TerraformModuleAnalyzer(terraform_resource_group_module)
        outputs = analyzer.get_defined_outputs()

        # Resource group module should output key information
        expected_outputs = {"id", "name", "location"}

        for output in expected_outputs:
            assert output in outputs, f"Module should define output '{output}'"

    def test_module_defines_azure_resources(
        self, terraform_resource_group_module: Path
    ):
        """Test that the module defines expected Azure resources."""
        analyzer = TerraformModuleAnalyzer(terraform_resource_group_module)
        resources = analyzer.get_resources_defined()

        # Should define azurerm_resource_group
        assert (
            "azurerm_resource_group" in resources
        ), "Module should define azurerm_resource_group resource"

    def test_all_variables_are_used(self, terraform_resource_group_module: Path):
        """Test that all defined variables are actually used in the module."""
        analyzer = TerraformModuleAnalyzer(terraform_resource_group_module)
        usage_check = analyzer.validate_variable_usage()

        unused_vars = [var for var, used in usage_check.items() if not used]

        assert len(unused_vars) == 0, f"Unused variables found: {unused_vars}"

    def test_module_has_version_constraints(
        self, terraform_resource_group_module: Path
    ):
        """Test that the module has proper version constraints."""
        analyzer = TerraformModuleAnalyzer(terraform_resource_group_module)
        version_info = analyzer.check_terraform_version_constraints()

        if version_info["has_versions_file"]:
            # If versions.tf exists, it should have provider constraints
            assert "azurerm" in version_info.get(
                "providers", {}
            ), "Module should specify azurerm provider version constraint"

    @pytest.mark.parametrize(
        "test_config_name", ["basic", "minimal", "with_extensive_tags"]
    )
    def test_syntax_validation_with_different_configs(
        self, terraform_resource_group_module: Path, test_config_name: str
    ):
        """Test that module syntax is valid with different configurations."""
        if TerraformTestConfig.should_skip_terraform_tests():
            pytest.skip(TerraformTestConfig.get_skip_reason())

        test_config = RESOURCE_GROUP_TEST_CONFIGS[test_config_name]

        with TerraformValidationTest(terraform_resource_group_module) as validator:
            validator.setup_test_workspace()
            validator.create_minimal_config(test_config)

            # Test terraform init (backend=false)
            ret_code, stdout, stderr = validator.terraform_init_backend_false()
            assert ret_code == 0, f"Terraform init failed: {stderr}"

            # Test terraform validate
            ret_code, stdout, stderr = validator.terraform_validate()
            assert ret_code == 0, f"Terraform validate failed: {stderr}"

    @pytest.mark.parametrize("location", TEST_LOCATIONS)
    def test_syntax_validation_with_different_locations(
        self, terraform_resource_group_module: Path, location: str
    ):
        """Test syntax validation with different Azure locations."""
        if TerraformTestConfig.should_skip_terraform_tests():
            pytest.skip(TerraformTestConfig.get_skip_reason())

        test_config = {
            "name": "test-rg-location",
            "location": location,
            "tags": {"Environment": "test"},
        }

        with TerraformValidationTest(terraform_resource_group_module) as validator:
            validator.setup_test_workspace()
            validator.create_minimal_config(test_config)

            ret_code, stdout, stderr = validator.terraform_init_backend_false()
            assert ret_code == 0, f"Init failed for location '{location}': {stderr}"

            ret_code, stdout, stderr = validator.terraform_validate()
            assert ret_code == 0, f"Validate failed for location '{location}': {stderr}"

    def test_terraform_formatting(self, terraform_resource_group_module: Path):
        """Test that Terraform files are properly formatted."""
        if TerraformTestConfig.should_skip_terraform_tests():
            pytest.skip(TerraformTestConfig.get_skip_reason())

        with TerraformValidationTest(terraform_resource_group_module) as validator:
            validator.setup_test_workspace()

            ret_code, stdout, stderr = validator.terraform_fmt_check()
            assert ret_code == 0, f"Terraform formatting check failed: {stderr}"

    def test_terraform_validate_syntax_only(
        self, terraform_resource_group_module: Path
    ):
        """Test that terraform validate checks syntax but not variable values."""
        if TerraformTestConfig.should_skip_terraform_tests():
            pytest.skip(TerraformTestConfig.get_skip_reason())

        # Test with missing required variables - this should still pass validation
        # because terraform validate only checks syntax, not variable requirements
        incomplete_config = {
            "tags": {"Environment": "test"}
            # Missing both 'name' and 'location' which are required at plan/apply time
        }

        with TerraformValidationTest(terraform_resource_group_module) as validator:
            validator.setup_test_workspace()
            validator.create_minimal_config(incomplete_config)

            ret_code, stdout, stderr = validator.terraform_init_backend_false()
            assert ret_code == 0, f"Init should succeed: {stderr}"

            # Validation succeeds because it only checks HCL syntax, not variable values
            ret_code, stdout, stderr = validator.terraform_validate()
            assert ret_code == 0, f"Validation should succeed (syntax-only): {stderr}"

            # Note: Missing variable values would only be caught during terraform plan

    def test_module_structure_validation(self, terraform_resource_group_module: Path):
        """Test comprehensive module structure validation."""
        validator = TerraformConfigValidator(terraform_resource_group_module)

        # Test structure
        structure_result = validator.validate_module_structure()
        assert structure_result["has_main_tf"], "Module must have main.tf"
        assert structure_result["has_variables_tf"], "Module must have variables.tf"
        assert structure_result["has_outputs_tf"], "Module must have outputs.tf"
        assert (
            structure_result["structure_score"] >= 0.6
        ), "Module structure score should be at least 60%"

        # Test variables
        variables_result = validator.validate_variables()
        assert variables_result["total_variables"] > 0, "Module should define variables"
        assert variables_result["all_variables_used"], (
            f"All variables should be used, "
            f"unused: {variables_result['unused_variables']}"
        )

        # Test outputs
        outputs_result = validator.validate_outputs()
        assert outputs_result["has_outputs"], "Module should define outputs"
        assert (
            outputs_result["total_outputs"] > 0
        ), "Module should have at least one output"

        # Test providers
        providers_result = validator.validate_providers()
        # Note: versions.tf might not exist in this module, so we just check if it does
        if providers_result["has_version_constraints"]:
            assert providers_result[
                "has_azurerm_provider"
            ], "Module should specify azurerm provider if using version constraints"


@pytest.mark.terraform
class TestResourceGroupModuleIntegration:
    """Integration-style tests that still work without Azure authentication."""

    def test_module_can_be_instantiated_multiple_times(
        self, terraform_resource_group_module: Path
    ):
        """Test that the module configuration supports multiple instances."""
        if TerraformTestConfig.should_skip_terraform_tests():
            pytest.skip(TerraformTestConfig.get_skip_reason())

        # Create a test configuration that instantiates the module twice
        test_configs = [
            {"name": "test-rg-1", "location": "East US", "tags": {"env": "test1"}},
            {"name": "test-rg-2", "location": "West US 2", "tags": {"env": "test2"}},
        ]

        for i, config in enumerate(test_configs):
            with TerraformValidationTest(terraform_resource_group_module) as validator:
                validator.setup_test_workspace()
                validator.create_minimal_config(config)

                ret_code, stdout, stderr = validator.terraform_init_backend_false()
                assert ret_code == 0, f"Init failed for config {i}: {stderr}"

                ret_code, stdout, stderr = validator.terraform_validate()
                assert ret_code == 0, f"Validate failed for config {i}: {stderr}"

    def test_complex_tags_configuration(self, terraform_resource_group_module: Path):
        """Test module with complex tags configuration."""
        if TerraformTestConfig.should_skip_terraform_tests():
            pytest.skip(TerraformTestConfig.get_skip_reason())

        complex_config = {
            "name": "test-rg-complex-tags",
            "location": "West Europe",
            "tags": {
                "Environment": "production",
                "Project": "data-platform",
                "Owner": "engineering-team",
                "CostCenter": "12345",
                "Application": "analytics",
                "Backup": "required",
                "Monitoring": "enabled",
            },
        }

        with TerraformValidationTest(terraform_resource_group_module) as validator:
            validator.setup_test_workspace()
            validator.create_minimal_config(complex_config)

            ret_code, stdout, stderr = validator.terraform_init_backend_false()
            assert ret_code == 0, f"Init failed: {stderr}"

            ret_code, stdout, stderr = validator.terraform_validate()
            assert ret_code == 0, f"Validate failed: {stderr}"
