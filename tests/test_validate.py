"""
Tests for the validate.py script.
"""

import sys
from pathlib import Path

import pytest

# Add scripts directory to Python path before importing from validate module
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# This import must come after sys.path modification  # noqa: E402
from validate import TerraformValidator


class TestTerraformValidator:
    """Test cases for TerraformValidator class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.base_path = Path.cwd()
        self.validator = TerraformValidator(self.base_path)

    def test_validator_initialization(self) -> None:
        """Test that validator initializes correctly."""
        assert self.validator.base_path == self.base_path
        assert self.validator.errors == []
        assert self.validator.warnings == []

    def test_has_terraform_files_with_tf_files(self, tmp_path: Path) -> None:
        """Test detecting Terraform files in directory."""
        # Create a temporary directory with .tf files
        tf_file = tmp_path / "main.tf"
        tf_file.write_text("# Test terraform file")

        assert self.validator._has_terraform_files(tmp_path) is True

    def test_has_terraform_files_without_tf_files(self, tmp_path: Path) -> None:
        """Test detecting no Terraform files in directory."""
        # Create a temporary directory without .tf files
        txt_file = tmp_path / "readme.txt"
        txt_file.write_text("Not a terraform file")

        assert self.validator._has_terraform_files(tmp_path) is False

    def test_find_modules_empty_directory(self, tmp_path: Path) -> None:
        """Test finding modules in empty directory."""
        modules = self.validator.find_modules(tmp_path)
        assert modules == []

    def test_find_modules_with_terraform_files(self, tmp_path: Path) -> None:
        """Test finding modules with Terraform files."""
        # Create module directory structure
        module_dir = tmp_path / "test-module"
        module_dir.mkdir()

        # Add terraform files
        (module_dir / "main.tf").write_text("# Main terraform file")
        (module_dir / "variables.tf").write_text("# Variables file")

        modules = self.validator.find_modules(tmp_path)
        assert len(modules) == 1
        assert modules[0] == module_dir

    def test_check_documentation_complete(self, tmp_path: Path) -> None:
        """Test documentation check with all required files."""
        # Create all required documentation files
        (tmp_path / "README.md").write_text("# Module Documentation")
        (tmp_path / "variables.tf").write_text("# Variables")
        (tmp_path / "outputs.tf").write_text("# Outputs")

        result = self.validator._check_documentation(tmp_path)
        assert result is True
        assert len(self.validator.warnings) == 0

    def test_check_documentation_missing_files(self, tmp_path: Path) -> None:
        """Test documentation check with missing files."""
        # Only create README, missing variables and outputs
        (tmp_path / "README.md").write_text("# Module Documentation")

        result = self.validator._check_documentation(tmp_path)
        assert result is False
        assert len(self.validator.warnings) == 2  # Missing variables.tf and outputs.tf

    def test_check_documentation_no_files(self, tmp_path: Path) -> None:
        """Test documentation check with no documentation files."""
        result = self.validator._check_documentation(tmp_path)
        assert result is False
        assert len(self.validator.warnings) == 3  # Missing all three files


@pytest.mark.integration
class TestIntegrationValidation:
    """Integration tests for validation functions."""

    @pytest.mark.skipif(
        not Path("terraform").exists(), reason="Terraform directory not found"
    )
    def test_find_real_modules(self) -> None:
        """Test finding modules in actual terraform directory."""
        base_path = Path.cwd()
        validator = TerraformValidator(base_path)
        terraform_dir = base_path / "terraform"

        modules = validator.find_modules(terraform_dir)
        # This should not fail even if no modules exist yet
        assert isinstance(modules, list)


if __name__ == "__main__":
    pytest.main([__file__])
