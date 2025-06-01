"""
Validation-only Terraform testing framework.

This module provides testing capabilities that work without Azure authentication
by focusing on syntax validation, structure checking, and static analysis.
"""

import json
import logging
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class TerraformValidationTest:
    """
    Terraform validation testing that works without provider authentication.

    This class focuses on:
    - HCL syntax validation
    - Module structure validation
    - Variable/output definition checking
    - Basic static analysis
    """

    def __init__(self, module_path: Path):
        """Initialize with path to Terraform module."""
        self.module_path = Path(module_path)
        self.test_dir: Optional[Path] = None
        self.terraform_cmd = self._find_terraform()

        if not self.terraform_cmd:
            raise RuntimeError("Terraform CLI not found in PATH")

        if not self.module_path.exists():
            raise ValueError(f"Module path does not exist: {self.module_path}")

    def _find_terraform(self) -> Optional[str]:
        """Find terraform executable in PATH."""
        result = subprocess.run(["which", "terraform"], capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup."""
        self.cleanup()

    def cleanup(self):
        """Clean up temporary test directory."""
        if self.test_dir and self.test_dir.exists():
            shutil.rmtree(self.test_dir, ignore_errors=True)
            self.test_dir = None

    def setup_test_workspace(self):
        """Set up test workspace with module files."""
        if self.test_dir:
            self.cleanup()

        self.test_dir = Path(tempfile.mkdtemp(prefix="terraform-validation-"))
        logger.info(f"Created test workspace: {self.test_dir}")

        # Copy module files
        for item in self.module_path.iterdir():
            if item.is_file() and item.suffix in [".tf", ".tfvars"]:
                dest = self.test_dir / item.name
                shutil.copy2(item, dest)
                logger.debug(f"Copied {item} to {dest}")

    def create_minimal_config(self, variables: Dict[str, Any]):
        """Create minimal test configuration for validation."""
        if not self.test_dir:
            raise RuntimeError("Test workspace not set up")

        # Create terraform.tfvars
        tfvars_content = self._generate_tfvars(variables)
        tfvars_file = self.test_dir / "terraform.tfvars"
        tfvars_file.write_text(tfvars_content)

        # Create versions.tf for provider requirements only
        versions_content = """terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}"""
        versions_file = self.test_dir / "versions.tf"
        versions_file.write_text(versions_content)

    def _generate_tfvars(self, variables: Dict[str, Any]) -> str:
        """Generate terraform.tfvars content."""
        lines = []
        for key, value in variables.items():
            if isinstance(value, str):
                lines.append(f'{key} = "{value}"')
            elif isinstance(value, bool):
                lines.append(f"{key} = {str(value).lower()}")
            elif isinstance(value, (dict, list)):
                formatted_value = json.dumps(value)
                lines.append(f"{key} = {formatted_value}")
            else:
                lines.append(f"{key} = {value}")

        return "\n".join(lines) + "\n"

    def _run_terraform_command(self, args: List[str]) -> Tuple[int, str, str]:
        """Run terraform command and return result."""
        if not self.test_dir:
            raise RuntimeError("Test workspace not set up")

        cmd = [self.terraform_cmd] + args
        logger.debug(f"Running: {' '.join(cmd)} in {self.test_dir}")

        try:
            result = subprocess.run(
                cmd,
                cwd=self.test_dir,
                capture_output=True,
                text=True,
                timeout=120,  # 2 minute timeout
            )

            return result.returncode, result.stdout, result.stderr

        except subprocess.TimeoutExpired as e:
            raise RuntimeError(f"Terraform command timed out: {' '.join(cmd)}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to run terraform command: {e}") from e

    def terraform_init_backend_false(self) -> Tuple[int, str, str]:
        """Run terraform init with -backend=false to avoid state/provider issues."""
        return self._run_terraform_command(["init", "-backend=false", "-no-color"])

    def terraform_validate(self) -> Tuple[int, str, str]:
        """Run terraform validate."""
        return self._run_terraform_command(["validate", "-no-color"])

    def terraform_fmt_check(self) -> Tuple[int, str, str]:
        """Check terraform formatting."""
        return self._run_terraform_command(["fmt", "-check", "-no-color"])


class TerraformModuleAnalyzer:
    """Analyze Terraform module structure and content."""

    def __init__(self, module_path: Path):
        self.module_path = Path(module_path)

    def check_required_files(self) -> Dict[str, bool]:
        """Check for required Terraform files."""
        return {
            "main.tf": (self.module_path / "main.tf").exists(),
            "variables.tf": (self.module_path / "variables.tf").exists(),
            "outputs.tf": (self.module_path / "outputs.tf").exists(),
            "versions.tf": (self.module_path / "versions.tf").exists(),
            "README.md": (self.module_path / "README.md").exists(),
        }

    def get_defined_variables(self) -> List[str]:
        """Extract variable names from variables.tf."""
        variables = []
        variables_file = self.module_path / "variables.tf"

        if variables_file.exists():
            content = variables_file.read_text()
            var_pattern = r'variable\s+"([^"]+)"'
            variables = re.findall(var_pattern, content)

        return variables

    def get_defined_outputs(self) -> List[str]:
        """Extract output names from outputs.tf."""
        outputs = []
        outputs_file = self.module_path / "outputs.tf"

        if outputs_file.exists():
            content = outputs_file.read_text()
            output_pattern = r'output\s+"([^"]+)"'
            outputs = re.findall(output_pattern, content)

        return outputs

    def get_resources_defined(self) -> List[str]:
        """Get list of resource types defined in the module."""
        resources = []

        for tf_file in self.module_path.glob("*.tf"):
            content = tf_file.read_text()
            # Find resource blocks
            resource_pattern = r'resource\s+"([^"]+)"\s+"[^"]+"'
            matches = re.findall(resource_pattern, content)
            resources.extend(matches)

        return list(set(resources))  # Remove duplicates

    def validate_variable_usage(self) -> Dict[str, bool]:
        """Check if all defined variables are used in the module."""
        defined_vars = self.get_defined_variables()
        usage_results = {}

        # Read all .tf files except variables.tf
        all_content = ""
        for tf_file in self.module_path.glob("*.tf"):
            if tf_file.name != "variables.tf":
                all_content += tf_file.read_text() + "\n"

        # Check usage of each variable
        for var_name in defined_vars:
            var_usage_pattern = rf"var\.{re.escape(var_name)}\b"
            is_used = bool(re.search(var_usage_pattern, all_content))
            usage_results[var_name] = is_used

        return usage_results

    def check_terraform_version_constraints(self) -> Dict[str, Any]:
        """Check terraform and provider version constraints."""
        versions_file = self.module_path / "versions.tf"

        if not versions_file.exists():
            return {"has_versions_file": False}

        content = versions_file.read_text()

        # Extract terraform version constraint
        terraform_version_pattern = r'required_version\s*=\s*"([^"]+)"'
        terraform_version_match = re.search(terraform_version_pattern, content)

        # Extract provider constraints
        provider_pattern = (
            r'(\w+)\s*=\s*\{[^}]*source\s*=\s*"([^"]+)"[^}]*version\s*=\s*"([^"]+)"'
        )
        provider_matches = re.findall(provider_pattern, content)

        return {
            "has_versions_file": True,
            "terraform_version": (
                terraform_version_match.group(1) if terraform_version_match else None
            ),
            "providers": {
                match[0]: {"source": match[1], "version": match[2]}
                for match in provider_matches
            },
        }


class TerraformConfigValidator:
    """Validate Terraform configuration against best practices."""

    def __init__(self, module_path: Path):
        self.module_path = Path(module_path)
        self.analyzer = TerraformModuleAnalyzer(module_path)

    def validate_module_structure(self) -> Dict[str, Any]:
        """Validate overall module structure."""
        files_check = self.analyzer.check_required_files()

        return {
            "has_main_tf": files_check["main.tf"],
            "has_variables_tf": files_check["variables.tf"],
            "has_outputs_tf": files_check["outputs.tf"],
            "has_versions_tf": files_check["versions.tf"],
            "has_readme": files_check["README.md"],
            "structure_score": sum(files_check.values()) / len(files_check),
        }

    def validate_variables(self) -> Dict[str, Any]:
        """Validate variable definitions and usage."""
        defined_vars = self.analyzer.get_defined_variables()
        usage_check = self.analyzer.validate_variable_usage()

        unused_vars = [var for var, used in usage_check.items() if not used]

        return {
            "total_variables": len(defined_vars),
            "unused_variables": unused_vars,
            "all_variables_used": len(unused_vars) == 0,
            "variable_names": defined_vars,
        }

    def validate_outputs(self) -> Dict[str, Any]:
        """Validate output definitions."""
        defined_outputs = self.analyzer.get_defined_outputs()

        return {
            "total_outputs": len(defined_outputs),
            "has_outputs": len(defined_outputs) > 0,
            "output_names": defined_outputs,
        }

    def validate_providers(self) -> Dict[str, Any]:
        """Validate provider configurations."""
        version_info = self.analyzer.check_terraform_version_constraints()

        return {
            "has_version_constraints": version_info["has_versions_file"],
            "terraform_version": version_info.get("terraform_version"),
            "providers": version_info.get("providers", {}),
            "has_azurerm_provider": "azurerm" in version_info.get("providers", {}),
        }
