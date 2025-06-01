"""
Tests for the resource group Terraform module using terraform plan.
"""

from pathlib import Path

import pytest

from tests.terraform.base import TerraformPlanAnalyzer, TerraformTestBase
from tests.terraform.fixtures.test_data import (
    PROVIDER_CONFIGS,
    RESOURCE_GROUP_TEST_CONFIGS,
    VARIABLE_VALIDATION_TESTS,
)


@pytest.mark.terraform
@pytest.mark.terraform_plan
class TestResourceGroupModule:
    """Test suite for the resource group Terraform module."""

    def test_basic_resource_group_plan(self, terraform_resource_group_module: Path):
        """Test basic resource group creation with minimal configuration."""
        with TerraformTestBase(terraform_resource_group_module) as terraform_test:
            # Setup test workspace
            terraform_test.setup_test_workspace()

            # Create test configuration
            test_config = RESOURCE_GROUP_TEST_CONFIGS["basic"]
            terraform_test.create_test_configuration(
                variables=test_config, providers=PROVIDER_CONFIGS["default"]
            )

            # Run terraform init
            ret_code, stdout, stderr = terraform_test.terraform_init()
            assert ret_code == 0, f"Terraform init failed: {stderr}"

            # Run terraform validate
            ret_code, stdout, stderr = terraform_test.terraform_validate()
            assert ret_code == 0, f"Terraform validate failed: {stderr}"

            # Run terraform plan
            ret_code, stdout, stderr = terraform_test.terraform_plan()
            assert ret_code == 0, f"Terraform plan failed: {stderr}"

            # Analyze plan output
            plan_json = terraform_test.terraform_plan_json()
            analyzer = TerraformPlanAnalyzer(plan_json)

            # Verify resource group will be created
            assert analyzer.has_resource_type("azurerm_resource_group")

            # Verify exactly one resource group
            resource_groups = analyzer.get_resource_by_type("azurerm_resource_group")
            assert len(resource_groups) == 1

            # Verify resource group attributes
            rg = resource_groups[0]
            values = rg["values"]
            assert values["name"] == test_config["name"]
            assert values["location"] == test_config["location"]
            assert values["tags"] == test_config["tags"]

    def test_minimal_resource_group_plan(self, terraform_resource_group_module: Path):
        """Test resource group creation with minimal configuration (no tags)."""
        with TerraformTestBase(terraform_resource_group_module) as terraform_test:
            terraform_test.setup_test_workspace()

            test_config = RESOURCE_GROUP_TEST_CONFIGS["minimal"]
            terraform_test.create_test_configuration(
                variables=test_config, providers=PROVIDER_CONFIGS["default"]
            )

            # Run through terraform workflow
            ret_code, _, stderr = terraform_test.terraform_init()
            assert ret_code == 0, f"Init failed: {stderr}"

            ret_code, _, stderr = terraform_test.terraform_validate()
            assert ret_code == 0, f"Validate failed: {stderr}"

            # Analyze plan
            plan_json = terraform_test.terraform_plan_json()
            analyzer = TerraformPlanAnalyzer(plan_json)

            # Verify resource creation
            resource_groups = analyzer.get_resource_by_type("azurerm_resource_group")
            assert len(resource_groups) == 1

            rg = resource_groups[0]
            values = rg["values"]
            assert values["name"] == test_config["name"]
            assert values["location"] == test_config["location"]
            # Tags should be empty/null when not provided
            assert values.get("tags") in [None, {}]

    def test_resource_group_with_extensive_tags(
        self, terraform_resource_group_module: Path
    ):
        """Test resource group creation with extensive tags."""
        with TerraformTestBase(terraform_resource_group_module) as terraform_test:
            terraform_test.setup_test_workspace()

            test_config = RESOURCE_GROUP_TEST_CONFIGS["with_extensive_tags"]
            terraform_test.create_test_configuration(
                variables=test_config, providers=PROVIDER_CONFIGS["default"]
            )

            # Run terraform workflow
            ret_code, _, stderr = terraform_test.terraform_init()
            assert ret_code == 0, f"Init failed: {stderr}"

            # Analyze plan
            plan_json = terraform_test.terraform_plan_json()
            analyzer = TerraformPlanAnalyzer(plan_json)

            # Verify tags are correctly applied
            assert analyzer.validate_resource_attributes(
                "azurerm_resource_group", {"tags": test_config["tags"]}
            )

    def test_module_outputs_are_defined(self, terraform_resource_group_module: Path):
        """Test that the module defines expected outputs."""
        with TerraformTestBase(terraform_resource_group_module) as terraform_test:
            terraform_test.setup_test_workspace()

            test_config = RESOURCE_GROUP_TEST_CONFIGS["basic"]
            terraform_test.create_test_configuration(
                variables=test_config, providers=PROVIDER_CONFIGS["default"]
            )

            ret_code, _, stderr = terraform_test.terraform_init()
            assert ret_code == 0, f"Init failed: {stderr}"

            # Get plan and analyze outputs
            plan_json = terraform_test.terraform_plan_json()
            analyzer = TerraformPlanAnalyzer(plan_json)

            outputs = analyzer.get_outputs()

            # Verify module outputs are available
            assert "module_outputs" in outputs
            module_outputs = outputs["module_outputs"]["value"]

            # Check for expected resource group outputs
            # (These should match what's defined in the module's outputs.tf)
            expected_output_keys = ["id", "name", "location", "tags"]
            for key in expected_output_keys:
                assert key in module_outputs, f"Expected output '{key}' not found"

    @pytest.mark.parametrize(
        "location", VARIABLE_VALIDATION_TESTS["resource_group"]["valid_locations"]
    )
    def test_valid_locations(
        self, terraform_resource_group_module: Path, location: str
    ):
        """Test that all valid Azure locations work correctly."""
        with TerraformTestBase(terraform_resource_group_module) as terraform_test:
            terraform_test.setup_test_workspace()

            test_config = {"name": "test-rg-location", "location": location}
            terraform_test.create_test_configuration(
                variables=test_config, providers=PROVIDER_CONFIGS["default"]
            )

            ret_code, _, stderr = terraform_test.terraform_init()
            assert ret_code == 0, f"Init failed: {stderr}"

            ret_code, _, stderr = terraform_test.terraform_validate()
            assert ret_code == 0, f"Validate failed for location '{location}': {stderr}"

            # Plan should succeed for valid locations
            ret_code, _, stderr = terraform_test.terraform_plan()
            assert ret_code == 0, f"Plan failed for location '{location}': {stderr}"

    def test_missing_required_variables_fails(
        self, terraform_resource_group_module: Path
    ):
        """Test that missing required variables cause plan to fail."""
        with TerraformTestBase(terraform_resource_group_module) as terraform_test:
            terraform_test.setup_test_workspace()

            # Create configuration missing required variables
            incomplete_config = {}  # No name or location
            terraform_test.create_test_configuration(
                variables=incomplete_config, providers=PROVIDER_CONFIGS["default"]
            )

            ret_code, _, stderr = terraform_test.terraform_init()
            assert ret_code == 0, f"Init failed: {stderr}"

            # Plan should fail due to missing required variables
            ret_code, stdout, stderr = terraform_test.terraform_plan()
            assert ret_code != 0, "Plan should fail with missing required variables"

            # Check that error mentions missing variables
            error_output = stderr.lower()
            assert "variable" in error_output or "required" in error_output

    def test_resource_count_is_correct(self, terraform_resource_group_module: Path):
        """Test that the module creates exactly the expected number of resources."""
        with TerraformTestBase(terraform_resource_group_module) as terraform_test:
            terraform_test.setup_test_workspace()

            test_config = RESOURCE_GROUP_TEST_CONFIGS["basic"]
            terraform_test.create_test_configuration(
                variables=test_config, providers=PROVIDER_CONFIGS["default"]
            )

            ret_code, _, stderr = terraform_test.terraform_init()
            assert ret_code == 0, f"Init failed: {stderr}"

            plan_json = terraform_test.terraform_plan_json()
            analyzer = TerraformPlanAnalyzer(plan_json)

            # Resource group module should create exactly 1 resource
            assert analyzer.resource_count() == 1

            # And it should be a resource group
            resources_to_create = analyzer.resources_to_create()
            assert len(resources_to_create) == 1
            assert resources_to_create[0]["type"] == "azurerm_resource_group"

    def test_no_destructive_changes(self, terraform_resource_group_module: Path):
        """Test that initial plan doesn't include any destructive changes."""
        with TerraformTestBase(terraform_resource_group_module) as terraform_test:
            terraform_test.setup_test_workspace()

            test_config = RESOURCE_GROUP_TEST_CONFIGS["basic"]
            terraform_test.create_test_configuration(
                variables=test_config, providers=PROVIDER_CONFIGS["default"]
            )

            ret_code, _, stderr = terraform_test.terraform_init()
            assert ret_code == 0, f"Init failed: {stderr}"

            plan_json = terraform_test.terraform_plan_json()
            analyzer = TerraformPlanAnalyzer(plan_json)

            # Should only be creating resources, not updating or deleting
            assert len(analyzer.resources_to_update()) == 0
            assert len(analyzer.resources_to_delete()) == 0
            assert len(analyzer.resources_to_create()) >= 1
