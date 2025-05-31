#!/usr/bin/env python3
"""
Code Formatting Script

This script formats Python and Terraform code using the tools installed
in the Poetry virtual environment.
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class CodeFormatter:
    """Handles formatting of Python and Terraform code."""

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.errors: List[str] = []

    def format_python_code(self, paths: List[Path]) -> bool:
        """Format Python code using black and isort."""
        console.print("\n[bold blue]Formatting Python Code[/bold blue]")

        success = True

        # Run black formatter
        if not self._run_black(paths):
            success = False

        # Run isort for import sorting
        if not self._run_isort(paths):
            success = False

        return success

    def format_terraform_code(self, paths: List[Path]) -> bool:
        """Format Terraform code using terraform fmt."""
        console.print("\n[bold blue]Formatting Terraform Code[/bold blue]")

        success = True

        for path in paths:
            if not self._run_terraform_fmt(path):
                success = False

        return success

    def _run_black(self, paths: List[Path]) -> bool:
        """Run black Python formatter."""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Running black formatter...", total=None)

                path_strings = [str(p) for p in paths if p.exists()]
                if not path_strings:
                    progress.remove_task(task)
                    console.print("  ⚠️  No Python paths found to format")
                    return True

                result = subprocess.run(
                    ["black", "--line-length", "88"] + path_strings,
                    capture_output=True,
                    text=True,
                )

                progress.remove_task(task)

            if result.returncode == 0:
                console.print("  ✅ Black formatting completed")
                if result.stdout.strip():
                    console.print(f"     {result.stdout.strip()}")
                return True
            else:
                self.errors.append(f"Black formatting failed: {result.stderr}")
                console.print("  ❌ Black formatting failed")
                console.print(f"     {result.stderr}")
                return False

        except FileNotFoundError:
            self.errors.append("Black not found. Install with Poetry.")
            console.print("  ❌ Black not found. Run 'poetry install'")
            return False
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Error running black: {e}")
            console.print(f"  ❌ Error running black: {e}")
            return False

    def _run_isort(self, paths: List[Path]) -> bool:
        """Run isort import sorter."""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Running isort...", total=None)

                path_strings = [str(p) for p in paths if p.exists()]
                if not path_strings:
                    progress.remove_task(task)
                    console.print("  ⚠️  No Python paths found to sort imports")
                    return True

                result = subprocess.run(
                    ["isort", "--profile", "black"] + path_strings,
                    capture_output=True,
                    text=True,
                )

                progress.remove_task(task)

            if result.returncode == 0:
                console.print("  ✅ Import sorting completed")
                return True
            else:
                self.errors.append(f"Isort failed: {result.stderr}")
                console.print("  ❌ Import sorting failed")
                console.print(f"     {result.stderr}")
                return False

        except FileNotFoundError:
            self.errors.append("Isort not found. Install with Poetry.")
            console.print("  ❌ Isort not found. Run 'poetry install'")
            return False
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Error running isort: {e}")
            console.print(f"  ❌ Error running isort: {e}")
            return False

    def _run_terraform_fmt(self, path: Path) -> bool:
        """Run terraform fmt on a directory."""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task(f"Formatting {path.name}...", total=None)

                result = subprocess.run(
                    ["terraform", "fmt", "-recursive"],
                    cwd=path,
                    capture_output=True,
                    text=True,
                )

                progress.remove_task(task)

            if result.returncode == 0:
                console.print(f"  ✅ Terraform formatting completed for {path.name}")
                if result.stdout.strip():
                    # Show which files were formatted
                    formatted_files = result.stdout.strip().split("\n")
                    for file in formatted_files:
                        if file.strip():
                            console.print(f"     Formatted: {file}")
                return True
            else:
                self.errors.append(f"Terraform fmt failed for {path}: {result.stderr}")
                console.print(f"  ❌ Terraform formatting failed for {path.name}")
                console.print(f"     {result.stderr}")
                return False

        except FileNotFoundError:
            self.errors.append("Terraform not found. Please install Terraform.")
            console.print("  ❌ Terraform not found. Please install Terraform.")
            return False
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Error running terraform fmt: {e}")
            console.print(f"  ❌ Error running terraform fmt: {e}")
            return False

    def find_python_paths(self) -> List[Path]:
        """Find Python directories and files to format."""
        paths = []

        # Add scripts directory
        scripts_dir = self.base_path / "scripts"
        if scripts_dir.exists():
            paths.append(scripts_dir)

        # Add tests directory
        tests_dir = self.base_path / "tests"
        if tests_dir.exists():
            paths.append(tests_dir)

        # Add any Python files in root
        for py_file in self.base_path.glob("*.py"):
            paths.append(py_file)

        return paths

    def find_terraform_paths(self) -> List[Path]:
        """Find Terraform directories to format."""
        paths = []

        # Add terraform directory
        terraform_dir = self.base_path / "terraform"
        if terraform_dir.exists():
            paths.append(terraform_dir)

        # Add any .tf files in root
        if list(self.base_path.glob("*.tf")):
            paths.append(self.base_path)

        return paths


@click.command()
@click.option("--python-only", is_flag=True, help="Format only Python code")
@click.option("--terraform-only", is_flag=True, help="Format only Terraform code")
@click.option("--check", is_flag=True, help="Check formatting without making changes")
@click.option(
    "--path",
    type=click.Path(exists=True, path_type=Path),
    multiple=True,
    help="Specific paths to format (can be used multiple times)",
)
def main(python_only: bool, terraform_only: bool, check: bool, path: Tuple[Path, ...]):
    """
    Format Python and Terraform code using black, isort, and terraform fmt.

    Examples:
        python scripts/format.py                    # Format all code
        python scripts/format.py --python-only     # Format only Python
        python scripts/format.py --terraform-only  # Format only Terraform
        python scripts/format.py --check           # Check without changes
        python scripts/format.py --path scripts/   # Format specific path
    """
    base_path = Path.cwd()
    formatter = CodeFormatter(base_path)

    console.print(
        Panel.fit(
            "[bold green]Code Formatter[/bold green]\n"
            "Formatting Python and Terraform code to project standards",
            border_style="green",
        )
    )

    success = True

    # Determine what to format
    format_python = not terraform_only
    format_terraform = not python_only

    if check:
        console.print("[yellow]Check mode: No files will be modified[/yellow]")

    # Get paths to format
    if path:
        python_paths = [
            p
            for p in path
            if p.suffix == ".py" or (p.is_dir() and any(p.rglob("*.py")))
        ]
        terraform_paths = [p for p in path if any(p.rglob("*.tf"))]
    else:
        python_paths = formatter.find_python_paths()
        terraform_paths = formatter.find_terraform_paths()

    # Format Python code
    if format_python and python_paths:
        if check:
            console.print("\n[yellow]Would format Python paths:[/yellow]")
            for p in python_paths:
                console.print(f"  • {p}")
        else:
            if not formatter.format_python_code(python_paths):
                success = False
    elif format_python:
        console.print("\n[yellow]No Python code found to format[/yellow]")

    # Format Terraform code
    if format_terraform and terraform_paths:
        if check:
            console.print("\n[yellow]Would format Terraform paths:[/yellow]")
            for p in terraform_paths:
                console.print(f"  • {p}")
        else:
            if not formatter.format_terraform_code(terraform_paths):
                success = False
    elif format_terraform:
        console.print("\n[yellow]No Terraform code found to format[/yellow]")

    # Display summary
    console.print("\n" + "=" * 50)
    if check:
        console.print("[bold]FORMAT CHECK COMPLETE[/bold]")
    else:
        console.print("[bold]FORMATTING COMPLETE[/bold]")

    # Display errors
    if formatter.errors:
        console.print(f"\n[bold red]Errors ({len(formatter.errors)}):[/bold red]")
        for error in formatter.errors:
            console.print(f"  • {error}")

    # Exit with appropriate code
    if not success:
        console.print("\n[bold red]Formatting failed![/bold red]")
        sys.exit(1)
    else:
        if check:
            console.print("\n[bold green]All code is properly formatted![/bold green]")
        else:
            console.print("\n[bold green]All code has been formatted![/bold green]")
        sys.exit(0)


if __name__ == "__main__":
    main()
