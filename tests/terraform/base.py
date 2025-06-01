"""
Base classes and utilities for Terraform testing.
"""

import json
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from python_terraform import Terraform


class TerraformTestBase:
    """Base class for Terraform module testing."""

    def __init__(self, module_path: Path):
        """Initialize with the path to the Terraform module to test."""
        self.module_path = module_path
        self.test_dir: Optional[Path] = None
        self.terraform: Optional[Terraform] = None

    def setup_test_workspace(self) -> Path:
        """Create a temporary workspace for testing."""
        self.test_dir = Path(tempfile.mkdtemp(prefix="terraform_test_"))

        # Copy module to test directory
        module_dest = self.test_dir / "module"
        shutil.copytree(self.module_path, module_dest)

        # Initialize Terraform client
        self.terraform = Terraform(working_dir=str(self.test_dir))

        return self.test_dir

    def create_test_configuration(
        self, variables: Dict[str, Any], providers: Optional[Dict[str, Any]] = None
    ) -> Path:
        """Create a test main.tf file that calls the module."""
        if not self.test_dir:
            raise RuntimeError(
                "Test workspace not set up. Call setup_test_workspace() first."
            )

        # Default Azure provider configuration for testing
        if providers is None:
            providers = {"azurerm": {"features": {}}}

        # Generate main.tf content
        main_tf_content = self._generate_main_tf(variables, providers)

        # Write main.tf
        main_tf_path = self.test_dir / "main.tf"
        main_tf_path.write_text(main_tf_content)

        return main_tf_path

    def _generate_main_tf(
        self, variables: Dict[str, Any], providers: Dict[str, Any]
    ) -> str:
        """Generate main.tf content for testing."""
        content = []

        # Add terraform block
        content.append(
            """terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}
"""
        )

        # Add provider configurations
        for provider_name, provider_config in providers.items():
            content.append(f'\nprovider "{provider_name}" {{')
            for key, value in provider_config.items():
                if isinstance(value, dict):
                    content.append(f"  {key} {{")
                    for sub_key, sub_value in value.items():
                        content.append(f"    {sub_key} = {json.dumps(sub_value)}")
                    content.append("  }")
                else:
                    content.append(f"  {key} = {json.dumps(value)}")
            content.append("}")

        # Add module call
        content.append('\nmodule "test_module" {')
        content.append('  source = "./module"')
        content.append("")

        # Add variables
        for var_name, var_value in variables.items():
            content.append(f"  {var_name} = {json.dumps(var_value)}")

        content.append("}")

        # Add outputs
        content.append(
            """
# Output all module outputs for testing
output "module_outputs" {
  value = module.test_module
}
"""
        )

        return "\n".join(content)

    def terraform_init(self) -> tuple[int, str, str]:
        """Run terraform init."""
        if not self.terraform:
            raise RuntimeError(
                "Terraform not initialized. Call setup_test_workspace() first."
            )

        return self.terraform.init()

    def terraform_validate(self) -> tuple[int, str, str]:
        """Run terraform validate."""
        if not self.terraform:
            raise RuntimeError(
                "Terraform not initialized. Call setup_test_workspace() first."
            )

        return self.terraform.validate()

    def terraform_plan(self, var_file: Optional[str] = None) -> tuple[int, str, str]:
        """Run terraform plan and return the result."""
        if not self.terraform:
            raise RuntimeError(
                "Terraform not initialized. Call setup_test_workspace() first."
            )

        plan_kwargs = {}
        if var_file:
            plan_kwargs["var_file"] = var_file

        return self.terraform.plan(**plan_kwargs)

    def terraform_plan_json(self, var_file: Optional[str] = None) -> Dict[str, Any]:
        """Run terraform plan and return JSON output for analysis."""
        if not self.terraform or not self.test_dir:
            raise RuntimeError(
                "Terraform not initialized. Call setup_test_workspace() first."
            )

        # Create plan file
        plan_file = self.test_dir / "plan.tfplan"

        # Run plan with output file
        plan_kwargs = {"out": str(plan_file)}
        if var_file:
            plan_kwargs["var_file"] = var_file

        # Run plan
        ret_code, stdout, stderr = self.terraform.plan(**plan_kwargs)
        if ret_code != 0:
            raise RuntimeError(f"Terraform plan failed: {stderr}")

        # Get JSON representation using show command
        ret_code, json_output, stderr = self.terraform.show(
            str(plan_file), json=True, capture_output=True
        )
        if ret_code != 0:
            raise RuntimeError(f"Terraform show failed: {stderr}")

        return json.loads(json_output)

    def cleanup(self):
        """Clean up test workspace."""
        if self.test_dir and self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir = None
        self.terraform = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.cleanup()


class TerraformPlanAnalyzer:
    """Utility class to analyze Terraform plan JSON output."""

    def __init__(self, plan_json: Dict[str, Any]):
        """Initialize with plan JSON data."""
        self.plan_json = plan_json

    def get_planned_resources(self) -> List[Dict[str, Any]]:
        """Get list of resources that will be created/modified."""
        return (
            self.plan_json.get("planned_values", {})
            .get("root_module", {})
            .get("resources", [])
        )

    def get_resource_changes(self) -> List[Dict[str, Any]]:
        """Get list of resource changes from the plan."""
        return self.plan_json.get("resource_changes", [])

    def resources_to_create(self) -> List[Dict[str, Any]]:
        """Get resources that will be created."""
        return [
            change
            for change in self.get_resource_changes()
            if change.get("change", {}).get("actions") == ["create"]
        ]

    def resources_to_update(self) -> List[Dict[str, Any]]:
        """Get resources that will be updated."""
        return [
            change
            for change in self.get_resource_changes()
            if change.get("change", {}).get("actions") == ["update"]
        ]

    def resources_to_delete(self) -> List[Dict[str, Any]]:
        """Get resources that will be deleted."""
        return [
            change
            for change in self.get_resource_changes()
            if change.get("change", {}).get("actions") == ["delete"]
        ]

    def get_resource_by_type(self, resource_type: str) -> List[Dict[str, Any]]:
        """Get all resources of a specific type."""
        return [
            resource
            for resource in self.get_planned_resources()
            if resource.get("type") == resource_type
        ]

    def get_outputs(self) -> Dict[str, Any]:
        """Get planned output values."""
        return self.plan_json.get("planned_values", {}).get("outputs", {})

    def has_resource_type(self, resource_type: str) -> bool:
        """Check if plan includes resources of a specific type."""
        return len(self.get_resource_by_type(resource_type)) > 0

    def resource_count(self) -> int:
        """Get total number of resources in the plan."""
        return len(self.get_planned_resources())

    def validate_resource_attributes(
        self, resource_type: str, expected_attributes: Dict[str, Any]
    ) -> bool:
        """Validate that resources of a type have expected attributes."""
        resources = self.get_resource_by_type(resource_type)

        for resource in resources:
            values = resource.get("values", {})
            for attr_name, expected_value in expected_attributes.items():
                if values.get(attr_name) != expected_value:
                    return False

        return True
