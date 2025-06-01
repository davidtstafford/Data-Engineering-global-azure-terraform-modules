"""
Configuration and utilities for Terraform testing framework.
"""

import os
from pathlib import Path


class TerraformTestConfig:
    """Configuration settings for Terraform tests."""

    # Test timeout settings
    TERRAFORM_INIT_TIMEOUT = 300  # 5 minutes
    TERRAFORM_PLAN_TIMEOUT = 300  # 5 minutes

    # Test markers
    TERRAFORM_MARKERS = ["terraform", "terraform_plan", "terraform_apply", "slow"]

    # Skip conditions
    SKIP_TERRAFORM_TESTS = os.getenv("SKIP_TERRAFORM_TESTS", "false").lower() == "true"
    TERRAFORM_AVAILABLE = bool(os.popen("which terraform").read().strip())

    @classmethod
    def should_skip_terraform_tests(cls) -> bool:
        """Determine if Terraform tests should be skipped."""
        if cls.SKIP_TERRAFORM_TESTS:
            return True
        if not cls.TERRAFORM_AVAILABLE:
            return True
        return False

    @classmethod
    def get_skip_reason(cls) -> str:
        """Get reason why Terraform tests are being skipped."""
        if cls.SKIP_TERRAFORM_TESTS:
            return "SKIP_TERRAFORM_TESTS environment variable is set"
        if not cls.TERRAFORM_AVAILABLE:
            return "Terraform CLI not available in PATH"
        return "Unknown reason"


def get_terraform_modules_path() -> Path:
    """Get the path to the Terraform modules directory."""
    # Assuming we're in tests/ directory
    project_root = Path(__file__).parent.parent.parent
    return project_root / "terraform"


def get_module_path(module_category: str, module_name: str) -> Path:
    """Get the path to a specific Terraform module."""
    modules_root = get_terraform_modules_path()
    return modules_root / module_category / module_name
