"""
Validation-only tests for Terraform diagnostic-settings module.

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

# Test data for diagnostic settings configurations
DIAGNOSTIC_SETTINGS_TEST_CONFIGS = {
    "log_analytics_only": {
        "name": "test-diagnostic-setting",
        "target_resource_id": (
            "/subscriptions/12345678-1234-1234-1234-123456789012"
            "/resourceGroups/test-rg/providers/Microsoft.KeyVault/"
            "vaults/test-kv"
        ),
        "log_analytics_workspace_id": (
            "/subscriptions/12345678-1234-1234-1234-123456789012"
            "/resourceGroups/test-rg/providers/"
            "Microsoft.OperationalInsights/workspaces/test-law"
        ),
        "category_groups": [{"name": "allLogs"}],
        "metrics": ["AllMetrics"],
    },
    "storage_with_retention": {
        "name": "test-storage-diagnostic",
        "target_resource_id": (
            "/subscriptions/12345678-1234-1234-1234-123456789012"
            "/resourceGroups/test-rg/providers/Microsoft.Sql/servers/test-sql"
        ),
        "storage_account_id": (
            "/subscriptions/12345678-1234-1234-1234-123456789012"
            "/resourceGroups/test-rg/providers/"
            "Microsoft.Storage/storageAccounts/teststore"
        ),
        "categories": [
            {
                "name": "SQLInsights",
                "retention_policy": {"enabled": True, "days": 90},
            }
        ],
        "metrics": ["AllMetrics"],
    },
    "eventhub_streaming": {
        "name": "test-eventhub-diagnostic",
        "target_resource_id": (
            "/subscriptions/12345678-1234-1234-1234-123456789012"
            "/resourceGroups/test-rg/providers/Microsoft.Web/sites/test-app"
        ),
        "eventhub_authorization_rule_id": (
            "/subscriptions/12345678-1234-1234-1234-123456789012"
            "/resourceGroups/test-rg/providers/Microsoft.EventHub/"
            "namespaces/test-eh/authorizationRules/RootManageSharedAccessKey"
        ),
        "eventhub_name": "diagnostics-hub",
        "category_groups": [{"name": "allLogs"}],
        "metrics": ["AllMetrics"],
    },
    "multi_destination": {
        "name": "test-multi-destination",
        "target_resource_id": (
            "/subscriptions/12345678-1234-1234-1234-123456789012"
            "/resourceGroups/test-rg/providers/Microsoft.Network/"
            "applicationGateways/test-agw"
        ),
        "log_analytics_workspace_id": (
            "/subscriptions/12345678-1234-1234-1234-123456789012"
            "/resourceGroups/test-rg/providers/"
            "Microsoft.OperationalInsights/workspaces/test-law"
        ),
        "storage_account_id": (
            "/subscriptions/12345678-1234-1234-1234-123456789012"
            "/resourceGroups/test-rg/providers/"
            "Microsoft.Storage/storageAccounts/teststore"
        ),
        "eventhub_authorization_rule_id": (
            "/subscriptions/12345678-1234-1234-1234-123456789012"
            "/resourceGroups/test-rg/providers/Microsoft.EventHub/"
            "namespaces/test-eh/authorizationRules/RootManageSharedAccessKey"
        ),
        "eventhub_name": "diagnostics-hub",
        "category_groups": [{"name": "allLogs"}, {"name": "audit"}],
        "metrics": ["AllMetrics"],
    },
    "minimal": {
        "name": "minimal-diagnostic",
        "target_resource_id": (
            "/subscriptions/12345678-1234-1234-1234-123456789012"
            "/resourceGroups/test-rg/providers/"
            "Microsoft.Storage/storageAccounts/teststore"
        ),
        "log_analytics_workspace_id": (
            "/subscriptions/12345678-1234-1234-1234-123456789012"
            "/resourceGroups/test-rg/providers/"
            "Microsoft.OperationalInsights/workspaces/test-law"
        ),
    },
}

# Test Azure resource types that support diagnostic settings
TEST_RESOURCE_TYPES = [
    "Microsoft.KeyVault/vaults",
    "Microsoft.Storage/storageAccounts",
    "Microsoft.Sql/servers",
    "Microsoft.Web/sites",
    "Microsoft.Network/applicationGateways",
    "Microsoft.Compute/virtualMachines",
    "Microsoft.Network/loadBalancers",
    "Microsoft.EventHub/namespaces",
]


@pytest.mark.terraform
class TestDiagnosticSettingsModuleValidation:
    """
    Validation tests for the diagnostic-settings module that don't require
    Azure auth.
    """

    @pytest.fixture
    def terraform_diagnostic_settings_module(self) -> Path:
        """Get the path to the diagnostic-settings module."""
        project_root = Path(__file__).parent.parent.parent
        return project_root / "terraform" / "foundation" / "diagnostic-settings"

    def test_module_has_required_files(
        self, terraform_diagnostic_settings_module: Path
    ):
        """Test that the module has all required files."""
        analyzer = TerraformModuleAnalyzer(terraform_diagnostic_settings_module)
        files_check = analyzer.check_required_files()

        # Core files should exist
        assert files_check["main.tf"], "Module must have main.tf"
        assert files_check["variables.tf"], "Module must have variables.tf"
        assert files_check["outputs.tf"], "Module must have outputs.tf"

        # Additional files expected for this module
        locals_tf = terraform_diagnostic_settings_module / "locals.tf"
        assert (
            locals_tf.exists()
        ), "Module should have locals.tf for destination validation"

        # Documentation should exist
        assert files_check["README.md"], "Module should have README.md documentation"

    def test_module_has_expected_variables(
        self, terraform_diagnostic_settings_module: Path
    ):
        """Test that the module defines expected variables."""
        analyzer = TerraformModuleAnalyzer(terraform_diagnostic_settings_module)
        variables = analyzer.get_variables()

        # Required variables
        required_vars = ["name", "target_resource_id"]
        for var_name in required_vars:
            assert var_name in variables, f"Module must define variable '{var_name}'"

        # Destination variables (at least one required)
        destination_vars = [
            "log_analytics_workspace_id",
            "storage_account_id",
            "eventhub_authorization_rule_id",
        ]
        destination_vars_found = [var for var in destination_vars if var in variables]
        assert len(destination_vars_found) > 0, (
            "Module must define at least one destination variable: "
            f"{destination_vars}"
        )

        # Configuration variables
        config_vars = ["categories", "category_groups", "metrics"]
        for var_name in config_vars:
            assert var_name in variables, f"Module should define variable '{var_name}'"

    def test_module_has_expected_outputs(
        self, terraform_diagnostic_settings_module: Path
    ):
        """Test that the module defines expected outputs."""
        analyzer = TerraformModuleAnalyzer(terraform_diagnostic_settings_module)
        outputs = analyzer.get_outputs()

        expected_outputs = ["id", "name", "target_resource_id"]
        for output_name in expected_outputs:
            assert output_name in outputs, f"Module must define output '{output_name}'"

    def test_module_syntax_is_valid(self, terraform_diagnostic_settings_module: Path):
        """Test that Terraform files have valid syntax."""
        if TerraformTestConfig.should_skip_terraform_tests():
            pytest.skip("Terraform validation tests are disabled")

        with TerraformConfigValidator(
            terraform_diagnostic_settings_module
        ) as validator:
            validator.setup_test_workspace()
            test_config = DIAGNOSTIC_SETTINGS_TEST_CONFIGS["log_analytics_only"]
            validator.create_test_tfvars(test_config)

            ret_code, stdout, stderr = validator.terraform_validate()
            assert ret_code == 0, f"Terraform validation failed: {stderr}"

    def test_module_formatting(self, terraform_diagnostic_settings_module: Path):
        """Test that Terraform files are properly formatted."""
        if TerraformTestConfig.should_skip_terraform_tests():
            pytest.skip("Terraform formatting tests are disabled")

        with TerraformConfigValidator(
            terraform_diagnostic_settings_module
        ) as validator:
            validator.setup_test_workspace()

            ret_code, stdout, stderr = validator.terraform_fmt_check()
            assert ret_code == 0, (
                f"Terraform files need formatting. Run 'terraform fmt' "
                f"in {terraform_diagnostic_settings_module}. Output: {stdout}"
            )

    @pytest.mark.parametrize(
        "config_name,config_data",
        [(name, config) for name, config in DIAGNOSTIC_SETTINGS_TEST_CONFIGS.items()],
    )
    def test_configuration_is_valid(
        self,
        terraform_diagnostic_settings_module: Path,
        config_name: str,
        config_data: dict,
    ):
        """Test different configuration scenarios are valid."""
        if TerraformTestConfig.should_skip_terraform_tests():
            pytest.skip("Terraform configuration tests are disabled")

        with TerraformConfigValidator(
            terraform_diagnostic_settings_module
        ) as validator:
            validator.setup_test_workspace()
            validator.create_test_tfvars(config_data)

            ret_code, stdout, stderr = validator.terraform_validate()
            assert (
                ret_code == 0
            ), f"Configuration '{config_name}' failed validation: {stderr}"

    def test_complex_retention_configuration(
        self, terraform_diagnostic_settings_module: Path
    ):
        """Test complex retention policy configurations."""
        if TerraformTestConfig.should_skip_terraform_tests():
            pytest.skip("Terraform retention tests are disabled")

        complex_config = {
            "name": "complex-retention-test",
            "target_resource_id": (
                "/subscriptions/12345678-1234-1234-1234-123456789012"
                "/resourceGroups/test-rg/providers/Microsoft.Sql/"
                "servers/test-sql"
            ),
            "storage_account_id": (
                "/subscriptions/12345678-1234-1234-1234-123456789012"
                "/resourceGroups/test-rg/providers/"
                "Microsoft.Storage/storageAccounts/teststore"
            ),
            "categories": [
                {
                    "name": "SQLInsights",
                    "retention_policy": {"enabled": True, "days": 90},
                },
                {
                    "name": "QueryStoreRuntimeStatistics",
                    "retention_policy": {"enabled": True, "days": 30},
                },
                {
                    "name": "Errors",
                    "retention_policy": {"enabled": False, "days": 0},
                },
            ],
            "metrics": [
                {
                    "category": "AllMetrics",
                    "retention_policy": {"enabled": True, "days": 7},
                }
            ],
        }

        with TerraformConfigValidator(
            terraform_diagnostic_settings_module
        ) as validator:
            validator.setup_test_workspace()
            validator.create_test_tfvars(complex_config)

            ret_code, stdout, stderr = validator.terraform_validate()
            assert ret_code == 0, f"Complex retention configuration failed: {stderr}"

    @pytest.mark.parametrize("resource_type", TEST_RESOURCE_TYPES)
    def test_resource_type_compatibility(
        self, terraform_diagnostic_settings_module: Path, resource_type: str
    ):
        """Test that diagnostic settings work with different resource types."""
        if TerraformTestConfig.should_skip_terraform_tests():
            pytest.skip("Terraform resource type tests are disabled")

        # Create a test resource ID for this resource type
        resource_name = resource_type.split("/")[-1].replace("s", "")
        test_config = {
            "name": f"test-{resource_name}-diagnostic",
            "target_resource_id": (
                "/subscriptions/12345678-1234-1234-1234-123456789012"
                f"/resourceGroups/test-rg/providers/{resource_type}/"
                f"test-{resource_name}"
            ),
            "log_analytics_workspace_id": (
                "/subscriptions/12345678-1234-1234-1234-123456789012"
                "/resourceGroups/test-rg/providers/"
                "Microsoft.OperationalInsights/workspaces/test-law"
            ),
            "category_groups": [{"name": "allLogs"}],
            "metrics": ["AllMetrics"],
        }

        with TerraformConfigValidator(
            terraform_diagnostic_settings_module
        ) as validator:
            validator.setup_test_workspace()
            validator.create_test_tfvars(test_config)

            ret_code, stdout, stderr = validator.terraform_validate()
            assert (
                ret_code == 0
            ), f"Resource type '{resource_type}' failed validation: {stderr}"


@pytest.mark.terraform
class TestDiagnosticSettingsExamplesValidation(TerraformValidationTest):
    """Test the diagnostic-settings module examples."""

    @pytest.fixture
    def examples_dir(self) -> Path:
        """Get the path to the examples directory."""
        project_root = Path(__file__).parent.parent.parent
        return (
            project_root
            / "terraform"
            / "foundation"
            / "diagnostic-settings"
            / "examples"
        )

    @pytest.mark.parametrize(
        "example_name",
        [
            "basic",
            "complex-configuration",
            "eventhub-streaming",
            "multi-destination",
            "storage-with-retention",
        ],
    )
    def test_example_syntax_validation(self, examples_dir: Path, example_name: str):
        """Test that example configurations have valid syntax."""
        if TerraformTestConfig.should_skip_terraform_tests():
            pytest.skip("Terraform example tests are disabled")

        example_path = examples_dir / example_name
        assert example_path.exists(), f"Example '{example_name}' not found"

        with TerraformConfigValidator(example_path) as validator:
            validator.setup_test_workspace()

            ret_code, stdout, stderr = validator.terraform_validate()
            assert (
                ret_code == 0
            ), f"Example '{example_name}' failed validation: {stderr}"

    @pytest.mark.parametrize(
        "example_name",
        [
            "basic",
            "complex-configuration",
            "eventhub-streaming",
            "multi-destination",
            "storage-with-retention",
        ],
    )
    def test_example_formatting(self, examples_dir: Path, example_name: str):
        """Test that example configurations are properly formatted."""
        if TerraformTestConfig.should_skip_terraform_tests():
            pytest.skip("Terraform example formatting tests are disabled")

        example_path = examples_dir / example_name
        assert example_path.exists(), f"Example '{example_name}' not found"

        with TerraformConfigValidator(example_path) as validator:
            validator.setup_test_workspace()

            ret_code, stdout, stderr = validator.terraform_fmt_check()
            assert ret_code == 0, (
                f"Example '{example_name}' needs formatting. "
                f"Run 'terraform fmt' in {example_path}. Output: {stdout}"
            )

    def test_all_examples_have_required_files(self, examples_dir: Path):
        """Test that all examples have required documentation."""
        example_dirs = [d for d in examples_dir.iterdir() if d.is_dir()]
        assert len(example_dirs) > 0, "No example directories found"

        for example_dir in example_dirs:
            # Each example should have README.md
            readme_path = example_dir / "README.md"
            assert (
                readme_path.exists()
            ), f"Example '{example_dir.name}' missing README.md"

            # Each example should have main.tf
            main_tf_path = example_dir / "main.tf"
            assert (
                main_tf_path.exists()
            ), f"Example '{example_dir.name}' missing main.tf"
