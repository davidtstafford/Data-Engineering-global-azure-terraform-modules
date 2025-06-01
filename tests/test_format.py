"""
Tests for the format.py script.
"""

import sys
from pathlib import Path

import pytest

# Add scripts directory to Python path before importing from format module
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# This import must come after sys.path modification  # noqa: E402
from format import CodeFormatter


class TestCodeFormatter:
    """Test cases for CodeFormatter class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.base_path = Path.cwd()
        self.formatter = CodeFormatter(self.base_path)

    def test_formatter_initialization(self) -> None:
        """Test that formatter initializes correctly."""
        assert self.formatter.base_path == self.base_path
        assert self.formatter.errors == []

    def test_find_python_paths_includes_scripts(self) -> None:
        """Test that find_python_paths includes scripts directory."""
        paths = self.formatter.find_python_paths()
        scripts_dir = self.base_path / "scripts"

        if scripts_dir.exists():
            assert scripts_dir in paths

    def test_find_python_paths_includes_tests(self) -> None:
        """Test that find_python_paths includes tests directory."""
        paths = self.formatter.find_python_paths()
        tests_dir = self.base_path / "tests"

        if tests_dir.exists():
            assert tests_dir in paths

    def test_find_terraform_paths_includes_terraform_dir(self) -> None:
        """Test that find_terraform_paths includes terraform directory."""
        paths = self.formatter.find_terraform_paths()
        terraform_dir = self.base_path / "terraform"

        if terraform_dir.exists():
            assert terraform_dir in paths

    def test_find_terraform_paths_with_no_terraform_dir(self, tmp_path: Path) -> None:
        """Test finding terraform paths when no terraform directory exists."""
        formatter = CodeFormatter(tmp_path)
        paths = formatter.find_terraform_paths()

        # Should return empty list or just root if .tf files exist
        assert isinstance(paths, list)


@pytest.mark.unit
class TestCodeFormatterMethods:
    """Unit tests for individual formatter methods."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.base_path = Path.cwd()
        self.formatter = CodeFormatter(self.base_path)

    def test_find_python_paths_returns_list(self) -> None:
        """Test that find_python_paths returns a list."""
        paths = self.formatter.find_python_paths()
        assert isinstance(paths, list)

    def test_find_terraform_paths_returns_list(self) -> None:
        """Test that find_terraform_paths returns a list."""
        paths = self.formatter.find_terraform_paths()
        assert isinstance(paths, list)


if __name__ == "__main__":
    pytest.main([__file__])
