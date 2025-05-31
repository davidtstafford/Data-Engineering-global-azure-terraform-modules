#!/usr/bin/env python3
"""
Terraform Module Validation Script

This script validates Terraform modules for syntax, security, and formatting.
Designed to run within the Poetry virtual environment.
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()


class TerraformValidator:
    """Validates Terraform modules with multiple checks."""

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_module(self, module_path: Path, run_security: bool = True) -> bool:
        """
        Validate a single Terraform module.

        Args:
            module_path: Path to the module directory
            run_security: Whether to run security scanning

        Returns:
            True if validation passes, False otherwise
        """
        console.print(
            f"\n[bold blue]Validating module:[/bold blue] "
            f"{module_path.relative_to(self.base_path)}"
        )

        success = True

        # Check if module directory exists and has .tf files
        if not self._has_terraform_files(module_path):
            self.errors.append(f"No Terraform files found in {module_path}")
            return False

        # Terraform syntax validation
        if not self._validate_terraform_syntax(module_path):
            success = False

        # Terraform format check
        if not self._check_terraform_format(module_path):
            success = False

        # Security scanning with Checkov
        if run_security and not self._run_security_scan(module_path):
            success = False

        # Documentation check
        if not self._check_documentation(module_path):
            success = False

        return success

    def _has_terraform_files(self, module_path: Path) -> bool:
        """Check if directory contains Terraform files."""
        tf_files = list(module_path.glob("*.tf"))
        return len(tf_files) > 0

    def _validate_terraform_syntax(self, module_path: Path) -> bool:
        """Run terraform validate on the module."""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Running terraform validate...", total=None)

                # Initialize Terraform
                init_result = subprocess.run(
                    ["terraform", "init", "-backend=false"],
                    cwd=module_path,
                    capture_output=True,
                    text=True,
                )

                if init_result.returncode != 0:
                    self.errors.append(f"Terraform init failed: {init_result.stderr}")
                    return False

                # Validate syntax
                validate_result = subprocess.run(
                    ["terraform", "validate"],
                    cwd=module_path,
                    capture_output=True,
                    text=True,
                )

                progress.remove_task(task)

            if validate_result.returncode == 0:
                console.print("  ✅ Terraform syntax validation passed")
                return True
            else:
                self.errors.append(
                    f"Terraform validation failed: {validate_result.stderr}"
                )
                console.print("  ❌ Terraform syntax validation failed")
                console.print(f"     {validate_result.stderr}")
                return False

        except subprocess.CalledProcessError as e:
            self.errors.append(f"Error running terraform validate: {e}")
            console.print(f"  ❌ Error running terraform validate: {e}")
            return False
        except FileNotFoundError:
            self.errors.append("Terraform command not found. Please install Terraform.")
            console.print("  ❌ Terraform command not found. Please install Terraform.")
            return False

    def _check_terraform_format(self, module_path: Path) -> bool:
        """Check if Terraform files are properly formatted."""
        try:
            result = subprocess.run(
                ["terraform", "fmt", "-check=true", "-diff=false"],
                cwd=module_path,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                console.print("  ✅ Terraform formatting check passed")
                return True
            else:
                self.warnings.append(
                    f"Terraform files in {module_path} need formatting"
                )
                console.print(
                    "  ⚠️  Terraform files need formatting (run 'terraform fmt')"
                )
                return False

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            self.warnings.append(f"Could not check Terraform formatting: {e}")
            console.print(f"  ⚠️  Could not check Terraform formatting: {e}")
            return False

    def _run_security_scan(self, module_path: Path) -> bool:
        """Run Checkov security scanning."""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Running security scan...", total=None)

                result = subprocess.run(
                    [
                        "checkov",
                        "-d",
                        str(module_path),
                        "--framework",
                        "terraform",
                        "--quiet",
                    ],
                    capture_output=True,
                    text=True,
                )

                progress.remove_task(task)

            if result.returncode == 0:
                console.print("  ✅ Security scan passed")
                return True
            else:
                # Checkov returns non-zero for findings, check if error or findings
                if "Check:" in result.stdout or "FAILED" in result.stdout:
                    self.warnings.append(f"Security scan found issues in {module_path}")
                    console.print("  ⚠️  Security scan found potential issues")
                    console.print(f"     Run 'checkov -d {module_path}' for details")
                    return False
                else:
                    self.errors.append(f"Security scan error: {result.stderr}")
                    console.print(f"  ❌ Security scan error: {result.stderr}")
                    return False

        except FileNotFoundError:
            self.warnings.append("Checkov not found. Security scanning skipped.")
            console.print("  ⚠️  Checkov not found. Install with 'pip install checkov'")
            return False
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Error running security scan: {e}")
            console.print(f"  ❌ Error running security scan: {e}")
            return False

    def _check_documentation(self, module_path: Path) -> bool:
        """Check if module has proper documentation."""
        readme_path = module_path / "README.md"
        variables_path = module_path / "variables.tf"
        outputs_path = module_path / "outputs.tf"

        issues = []

        # Check for README.md
        if not readme_path.exists():
            issues.append("Missing README.md")

        # Check for variables.tf
        if not variables_path.exists():
            issues.append("Missing variables.tf")

        # Check for outputs.tf
        if not outputs_path.exists():
            issues.append("Missing outputs.tf")

        if issues:
            self.warnings.extend([f"{module_path}: {issue}" for issue in issues])
            console.print(f"  ⚠️  Documentation issues: {', '.join(issues)}")
            return False
        else:
            console.print("  ✅ Documentation check passed")
            return True

    def find_modules(self, terraform_dir: Path) -> List[Path]:
        """Find all Terraform modules in the terraform directory."""
        modules: List[Path] = []

        if not terraform_dir.exists():
            console.print(
                f"[yellow]Warning:[/yellow] Terraform directory {terraform_dir} "
                f"does not exist"
            )
            return modules

        # Look for directories containing .tf files
        for path in terraform_dir.rglob("*"):
            if path.is_dir() and self._has_terraform_files(path):
                # Skip example directories for now
                if "examples" not in path.parts:
                    modules.append(path)

        return sorted(modules)


@click.command()
@click.option(
    "--module",
    type=click.Path(exists=True, path_type=Path),
    help="Path to specific module to validate",
)
@click.option(
    "--all",
    "validate_all",
    is_flag=True,
    help="Validate all modules in terraform/ directory",
)
@click.option(
    "--security/--no-security",
    default=True,
    help="Run security scanning (default: enabled)",
)
@click.option(
    "--format/--no-format",
    default=True,
    help="Check Terraform formatting (default: enabled)",
)
def main(
    module: Optional[Path], validate_all: bool, security: bool, format: bool
) -> None:
    """
    Validate Terraform modules for syntax, security, and best practices.

    Examples:
        python scripts/validate.py --module terraform/foundation/resource-group
        python scripts/validate.py --all
        python scripts/validate.py --all --no-security
    """
    base_path = Path.cwd()
    validator = TerraformValidator(base_path)

    console.print(
        Panel.fit(
            "[bold green]Azure Terraform Modules Validator[/bold green]\n"
            "Checking syntax, security, and documentation standards",
            border_style="green",
        )
    )

    modules_to_validate = []

    if module:
        modules_to_validate = [module]
    elif validate_all:
        terraform_dir = base_path / "terraform"
        modules_to_validate = validator.find_modules(terraform_dir)

        if not modules_to_validate:
            console.print("[yellow]No modules found to validate[/yellow]")
            console.print(f"Searched in: {terraform_dir}")
            sys.exit(0)
    else:
        console.print("[red]Error:[/red] Must specify --module or --all")
        console.print("Use --help for usage information")
        sys.exit(1)

    console.print(
        f"\n[bold]Found {len(modules_to_validate)} module(s) to validate[/bold]"
    )

    # Validate modules
    results = []
    for module_path in modules_to_validate:
        result = validator.validate_module(module_path, run_security=security)
        results.append((module_path, result))

    # Display summary
    console.print("\n" + "=" * 60)
    console.print("[bold]VALIDATION SUMMARY[/bold]")

    # Create results table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Module", style="cyan")
    table.add_column("Status", justify="center")

    passed = 0
    failed = 0

    for module_path, success in results:
        relative_path = module_path.relative_to(base_path)
        if success:
            table.add_row(str(relative_path), "[green]✅ PASSED[/green]")
            passed += 1
        else:
            table.add_row(str(relative_path), "[red]❌ FAILED[/red]")
            failed += 1

    console.print(table)

    # Summary statistics
    console.print(f"\n[bold]Results:[/bold] {passed} passed, {failed} failed")

    # Display errors and warnings
    if validator.errors:
        console.print(f"\n[bold red]Errors ({len(validator.errors)}):[/bold red]")
        for error in validator.errors:
            console.print(f"  • {error}")

    if validator.warnings:
        console.print(
            f"\n[bold yellow]Warnings ({len(validator.warnings)}):[/bold yellow]"
        )
        for warning in validator.warnings:
            console.print(f"  • {warning}")

    # Exit with appropriate code
    if failed > 0:
        console.print("\n[bold red]Validation failed![/bold red]")
        sys.exit(1)
    else:
        console.print("\n[bold green]All validations passed![/bold green]")
        sys.exit(0)


if __name__ == "__main__":
    main()
