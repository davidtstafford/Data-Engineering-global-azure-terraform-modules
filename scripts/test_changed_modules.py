#!/usr/bin/env python3
"""
Smart Terraform module testing script that only tests changed modules.

This script detects which Terraform modules have been modified and runs
tests only for those modules.
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Set, Tuple


def run_command(cmd: List[str], cwd: Optional[Path] = None) -> Tuple[int, str, str]:
    """Run a command and return (return_code, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd or Path.cwd(),
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def get_changed_files(base_branch: str = "main") -> Set[str]:
    """Get list of files changed compared to base branch."""
    all_changed_files = set()

    # First, get files changed compared to base branch
    ret_code, stdout, stderr = run_command(
        ["git", "diff", "--name-only", f"{base_branch}...HEAD"]
    )

    if ret_code == 0 and stdout.strip():
        branch_changes = set(stdout.strip().split("\n"))
        all_changed_files.update(branch_changes)

    # Also get uncommitted changes (staged and unstaged)
    ret_code, stdout, stderr = run_command(["git", "diff", "--name-only", "HEAD"])
    if ret_code == 0 and stdout.strip():
        unstaged_changes = set(stdout.strip().split("\n"))
        all_changed_files.update(unstaged_changes)

    # Get staged changes
    ret_code, stdout, stderr = run_command(["git", "diff", "--name-only", "--cached"])
    if ret_code == 0 and stdout.strip():
        staged_changes = set(stdout.strip().split("\n"))
        all_changed_files.update(staged_changes)

    # Get untracked files that are in terraform/ directory
    ret_code, stdout, stderr = run_command(
        ["git", "ls-files", "--others", "--exclude-standard"]
    )
    if ret_code == 0 and stdout.strip():
        untracked_files = set(stdout.strip().split("\n"))
        # Only include untracked files that are in terraform directory
        terraform_untracked = {f for f in untracked_files if f.startswith("terraform/")}
        all_changed_files.update(terraform_untracked)

    return all_changed_files


def find_terraform_modules() -> List[Path]:
    """Find all Terraform modules in the project."""
    terraform_root = Path("terraform")
    modules = []

    for tf_file in terraform_root.rglob("main.tf"):
        module_dir = tf_file.parent
        # Skip example directories
        if "examples" not in module_dir.parts:
            modules.append(module_dir)

    return sorted(modules)


def get_affected_modules(changed_files: Set[str]) -> Set[Path]:
    """Determine which Terraform modules are affected by the changed files."""
    terraform_modules = find_terraform_modules()
    affected_modules = set()

    for changed_file in changed_files:
        changed_path = Path(changed_file)

        # Check if the changed file is within a Terraform module
        for module_path in terraform_modules:
            try:
                # Check if the changed file is within this module
                changed_path.relative_to(module_path)
                affected_modules.add(module_path)
            except ValueError:
                # File is not within this module
                continue

    return affected_modules


def get_module_test_file(module_path: Path, test_type: str = "validation") -> Path:
    """Get the test file path for a given module."""
    # Convert module path to test file name
    # e.g., terraform/foundation/resource-group -> test_resource_group_validation.py

    module_name = module_path.name.replace("-", "_")

    if test_type == "validation":
        test_file = f"test_{module_name}_validation.py"
    else:
        test_file = f"test_{module_name}_terraform.py"

    test_path = Path("tests/terraform/modules") / test_file
    return test_path


def run_tests_for_modules(modules: Set[Path], test_type: str = "validation") -> bool:
    """Run tests for the specified modules."""
    if not modules:
        print("No Terraform modules to test.")
        return True

    print(f"Testing {len(modules)} Terraform module(s):")
    for module in sorted(modules):
        print(f"  - {module}")

    test_files = []
    missing_tests = []

    for module in modules:
        test_file = get_module_test_file(module, test_type)
        if test_file.exists():
            test_files.append(str(test_file))
        else:
            missing_tests.append((module, test_file))

    if missing_tests:
        print("\nWarning: Missing test files for some modules:")
        for module, test_file in missing_tests:
            print(f"  - {module} -> {test_file} (not found)")

    if not test_files:
        print("No test files found for changed modules.")
        return True

    # Run pytest on the test files
    cmd = ["poetry", "run", "pytest"] + test_files + ["-v", "-m", "terraform"]

    print(f"\nRunning tests: {' '.join(cmd)}")
    ret_code, stdout, stderr = run_command(cmd)

    if stdout:
        print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)

    return ret_code == 0


def main() -> int:
    """Main function to run smart Terraform testing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Run Terraform tests for changed modules only"
    )
    parser.add_argument(
        "--base-branch",
        default="main",
        help="Base branch to compare against (default: main)",
    )
    parser.add_argument(
        "--test-type",
        choices=["validation", "plan"],
        default="validation",
        help="Type of tests to run (default: validation)",
    )
    parser.add_argument(
        "--all", action="store_true", help="Test all modules regardless of changes"
    )

    args = parser.parse_args()

    if args.all:
        print("Testing ALL Terraform modules...")
        modules = set(find_terraform_modules())
    else:
        print(f"Detecting changed files compared to {args.base_branch}...")
        changed_files = get_changed_files(args.base_branch)

        if not changed_files:
            print("No changed files detected.")
            return 0

        print(f"Changed files ({len(changed_files)}):")
        for file in sorted(changed_files):
            print(f"  - {file}")

        modules = get_affected_modules(changed_files)

        if not modules:
            print("No Terraform modules affected by changes.")
            return 0

    success = run_tests_for_modules(modules, args.test_type)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
