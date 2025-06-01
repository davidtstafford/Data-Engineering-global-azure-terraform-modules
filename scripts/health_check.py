#!/usr/bin/env python3
"""
Comprehensive system health verification script for Azure Terraform modules project.

This script checks for required tools, validates Azure authentication, checks Terraform
configuration, and provides installation guidance for missing tools.
"""

import json
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple


class ToolStatus(Enum):
    """Status of a tool check."""

    AVAILABLE = "✅ Available"
    MISSING = "❌ Missing"
    VERSION_ISSUE = "⚠️ Version Issue"
    ERROR = "🔥 Error"


@dataclass
class ToolCheck:
    """Result of a tool availability check."""

    name: str
    status: ToolStatus
    version: Optional[str] = None
    message: Optional[str] = None
    install_guidance: Optional[str] = None


class HealthChecker:
    """Comprehensive system health checker for Azure Terraform development."""

    def __init__(self) -> None:
        """Initialize the health checker."""
        self.is_container = self._detect_container_environment()
        self.platform = platform.system().lower()
        self.results: List[ToolCheck] = []

    def _detect_container_environment(self) -> bool:
        """Detect if running inside a container."""
        try:
            # Check for common container indicators
            container_indicators = [
                Path("/.dockerenv").exists(),
                self._check_proc_cgroup(),
                "container" in platform.platform().lower(),
            ]
            return any(container_indicators)
        except Exception:
            return False

    def _check_proc_cgroup(self) -> bool:
        """Safely check /proc/1/cgroup for docker indicators."""
        try:
            cgroup_path = Path("/proc/1/cgroup")
            if cgroup_path.exists():
                return "docker" in cgroup_path.read_text()
            return False
        except Exception:
            return False

    def _run_command(
        self, cmd: List[str], capture_output: bool = True
    ) -> Tuple[int, str, str]:
        """Run a command and return exit code, stdout, stderr."""
        try:
            result = subprocess.run(
                cmd, capture_output=capture_output, text=True, timeout=30
            )
            return result.returncode, result.stdout.strip(), result.stderr.strip()
        except subprocess.TimeoutExpired:
            return 1, "", "Command timed out"
        except FileNotFoundError:
            return 127, "", "Command not found"
        except Exception as e:
            return 1, "", str(e)

    def check_python(self) -> ToolCheck:
        """Check Python installation and version."""
        try:
            version = (
                f"{sys.version_info.major}.{sys.version_info.minor}."
                f"{sys.version_info.micro}"
            )

            if sys.version_info >= (3, 9):
                return ToolCheck(
                    name="Python",
                    status=ToolStatus.AVAILABLE,
                    version=version,
                    message="Compatible version",
                )
            else:
                return ToolCheck(
                    name="Python",
                    status=ToolStatus.VERSION_ISSUE,
                    version=version,
                    message="Python 3.9+ required",
                    install_guidance="Please upgrade to Python 3.9 or higher",
                )
        except Exception as e:
            return ToolCheck(name="Python", status=ToolStatus.ERROR, message=str(e))

    def check_terraform(self) -> ToolCheck:
        """Check Terraform installation and version."""
        if not shutil.which("terraform"):
            install_guide = {
                "windows": "Install via Chocolatey: choco install terraform",
                "darwin": "Install via Homebrew: brew install terraform",
                "linux": "Download from https://terraform.io/downloads",
            }

            return ToolCheck(
                name="Terraform",
                status=ToolStatus.MISSING,
                install_guidance=install_guide.get(
                    self.platform, install_guide["linux"]
                ),
            )

        exit_code, stdout, stderr = self._run_command(["terraform", "version"])
        if exit_code == 0:
            # Parse version from output like "Terraform v1.6.6"
            version_line = stdout.split("\n")[0]
            version = version_line.split("v")[-1] if "v" in version_line else "unknown"

            return ToolCheck(
                name="Terraform",
                status=ToolStatus.AVAILABLE,
                version=version,
                message="Ready for use",
            )
        else:
            return ToolCheck(
                name="Terraform",
                status=ToolStatus.ERROR,
                message=f"Error checking version: {stderr}",
            )

    def check_azure_cli(self) -> ToolCheck:
        """Check Azure CLI installation and authentication."""
        if not shutil.which("az"):
            install_guide = {
                "windows": "Install via MSI: https://aka.ms/installazurecliwindows",
                "darwin": "Install via Homebrew: brew install azure-cli",
                "linux": "curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash",
            }

            return ToolCheck(
                name="Azure CLI",
                status=ToolStatus.MISSING,
                install_guidance=install_guide.get(
                    self.platform, install_guide["linux"]
                ),
            )

        # Check version
        exit_code, stdout, stderr = self._run_command(["az", "version"])
        if exit_code != 0:
            return ToolCheck(
                name="Azure CLI",
                status=ToolStatus.ERROR,
                message=f"Error checking version: {stderr}",
            )

        try:
            version_info = json.loads(stdout)
            version = version_info.get("azure-cli", "unknown")
        except (json.JSONDecodeError, KeyError):
            version = "unknown"

        # Check authentication
        auth_exit_code, auth_stdout, auth_stderr = self._run_command(
            ["az", "account", "show"]
        )
        if auth_exit_code == 0:
            auth_message = "Authenticated and ready"
        else:
            auth_message = "Not authenticated - run 'az login'"

        return ToolCheck(
            name="Azure CLI",
            status=ToolStatus.AVAILABLE,
            version=version,
            message=auth_message,
        )

    def check_git(self) -> ToolCheck:
        """Check Git installation."""
        if not shutil.which("git"):
            install_guide = {
                "windows": (
                    "Install via Git for Windows: https://git-scm.com/download/win"
                ),
                "darwin": "Install via Homebrew: brew install git",
                "linux": "Install via package manager: sudo apt install git",
            }

            return ToolCheck(
                name="Git",
                status=ToolStatus.MISSING,
                install_guidance=install_guide.get(
                    self.platform, install_guide["linux"]
                ),
            )

        exit_code, stdout, stderr = self._run_command(["git", "--version"])
        if exit_code == 0:
            version = stdout.split()[-1] if stdout else "unknown"
            return ToolCheck(
                name="Git",
                status=ToolStatus.AVAILABLE,
                version=version,
                message="Ready for version control",
            )
        else:
            return ToolCheck(
                name="Git",
                status=ToolStatus.ERROR,
                message=f"Error checking version: {stderr}",
            )

    def check_docker(self) -> ToolCheck:
        """Check Docker/containerization tools."""
        docker_cmd = None
        for cmd in ["docker", "podman"]:
            if shutil.which(cmd):
                docker_cmd = cmd
                break

        if not docker_cmd:
            install_guide = {
                "windows": "Install Docker Desktop or Rancher Desktop",
                "darwin": "Install Docker Desktop or Rancher Desktop",
                "linux": "Install Docker via package manager or snap",
            }

            return ToolCheck(
                name="Container Runtime",
                status=ToolStatus.MISSING,
                message="Optional for local development",
                install_guidance=install_guide.get(
                    self.platform, install_guide["linux"]
                ),
            )

        exit_code, stdout, stderr = self._run_command([docker_cmd, "--version"])
        if exit_code == 0:
            version = stdout.split()[-1] if stdout else "unknown"
            return ToolCheck(
                name=f"Container Runtime ({docker_cmd})",
                status=ToolStatus.AVAILABLE,
                version=version,
                message="Available for dev containers",
            )
        else:
            return ToolCheck(
                name="Container Runtime",
                status=ToolStatus.ERROR,
                message=f"Error checking {docker_cmd}: {stderr}",
            )

    def check_nodejs(self) -> ToolCheck:
        """Check Node.js installation (optional)."""
        if not shutil.which("node"):
            return ToolCheck(
                name="Node.js",
                status=ToolStatus.MISSING,
                message="Optional for additional tooling",
                install_guidance="Install via package manager or from nodejs.org",
            )

        exit_code, stdout, stderr = self._run_command(["node", "--version"])
        if exit_code == 0:
            version = stdout.strip("v") if stdout.startswith("v") else stdout
            return ToolCheck(
                name="Node.js",
                status=ToolStatus.AVAILABLE,
                version=version,
                message="Available for additional tooling",
            )
        else:
            return ToolCheck(
                name="Node.js",
                status=ToolStatus.ERROR,
                message=f"Error checking version: {stderr}",
            )

    def check_vscode(self) -> ToolCheck:
        """Check VS Code installation (optional)."""
        vscode_commands = ["code", "code-insiders"]

        for cmd in vscode_commands:
            if shutil.which(cmd):
                exit_code, stdout, stderr = self._run_command([cmd, "--version"])
                if exit_code == 0:
                    version = stdout.split("\n")[0] if stdout else "unknown"
                    return ToolCheck(
                        name="VS Code",
                        status=ToolStatus.AVAILABLE,
                        version=version,
                        message="Recommended IDE available",
                    )

        return ToolCheck(
            name="VS Code",
            status=ToolStatus.MISSING,
            message="Recommended IDE for this project",
            install_guidance="Install from https://code.visualstudio.com/",
        )

    def check_terraform_config(self) -> ToolCheck:
        """Check Terraform configuration in the project."""
        project_root = Path(__file__).parent.parent
        terraform_dir = project_root / "terraform"

        if not terraform_dir.exists():
            return ToolCheck(
                name="Terraform Config",
                status=ToolStatus.MISSING,
                message="Terraform directory not found",
            )

        # Check for at least one module
        module_dirs = [
            d
            for d in terraform_dir.rglob("*")
            if d.is_dir() and any(f.suffix == ".tf" for f in d.iterdir())
        ]

        if not module_dirs:
            return ToolCheck(
                name="Terraform Config",
                status=ToolStatus.MISSING,
                message="No Terraform modules found",
            )

        return ToolCheck(
            name="Terraform Config",
            status=ToolStatus.AVAILABLE,
            message=f"Found {len(module_dirs)} Terraform modules",
        )

    def run_all_checks(self) -> List[ToolCheck]:
        """Run all health checks."""
        self.results = []

        # Required tools
        print("🔍 Checking required tools...")
        self.results.extend(
            [
                self.check_python(),
                self.check_terraform(),
                self.check_azure_cli(),
                self.check_git(),
            ]
        )

        # Optional tools
        print("🔍 Checking optional tools...")
        self.results.extend(
            [
                self.check_docker(),
                self.check_nodejs(),
                self.check_vscode(),
            ]
        )

        # Project configuration
        print("🔍 Checking project configuration...")
        self.results.append(self.check_terraform_config())

        return self.results

    def print_summary(self) -> None:
        """Print a comprehensive summary of all checks."""
        print("\n" + "=" * 80)
        print("🏥 AZURE TERRAFORM MODULES - HEALTH CHECK SUMMARY")
        print("=" * 80)

        print(f"\n📍 Environment: {'Container' if self.is_container else 'Local'}")
        print(f"🖥️  Platform: {platform.system()} {platform.release()}")

        # Group results by category
        required_tools = ["Python", "Terraform", "Azure CLI", "Git"]
        optional_tools = [
            "Container Runtime",
            "Container Runtime (docker)",
            "Container Runtime (podman)",
            "Node.js",
            "VS Code",
        ]
        config_checks = ["Terraform Config"]

        def print_category(title: str, tool_names: List[str]) -> None:
            print(f"\n{title}")
            print("-" * len(title))

            category_results = [
                r for r in self.results if any(name in r.name for name in tool_names)
            ]
            if not category_results:
                print("  No tools in this category")
                return

            for result in category_results:
                status_icon = result.status.value.split()[0]
                print(f"  {status_icon} {result.name}")

                if result.version:
                    print(f"      Version: {result.version}")
                if result.message:
                    print(f"      Status: {result.message}")
                if result.install_guidance and result.status in [
                    ToolStatus.MISSING,
                    ToolStatus.VERSION_ISSUE,
                ]:
                    print(f"      Install: {result.install_guidance}")

        print_category("🔧 REQUIRED TOOLS", required_tools)
        print_category("⚙️  OPTIONAL TOOLS", optional_tools)
        print_category("📁 PROJECT CONFIGURATION", config_checks)

        # Overall status
        critical_issues = [
            r
            for r in self.results
            if r.status in [ToolStatus.MISSING, ToolStatus.ERROR]
            and any(name in r.name for name in required_tools)
        ]

        print(f"\n{'='*80}")
        if not critical_issues:
            print("🎉 SYSTEM READY FOR AZURE TERRAFORM DEVELOPMENT!")
            print("   All required tools are available and configured.")
        else:
            print("⚠️  SETUP REQUIRED")
            print(
                f"   {len(critical_issues)} critical tool(s) need attention "
                f"before development."
            )

        print("=" * 80)

        # Next steps
        print("\n📋 NEXT STEPS:")
        if critical_issues:
            print("1. Install missing required tools (see guidance above)")
            print("2. Re-run this health check: python scripts/health_check.py")
            print("3. Follow the getting started guide: docs/getting-started.md")
        else:
            print("1. Start development with: make setup")
            print("2. Run validation: make validate")
            print("3. See available commands: make help")

        # Environment-specific recommendations
        if not self.is_container:
            docker_available = any(
                "Container Runtime" in r.name and r.status == ToolStatus.AVAILABLE
                for r in self.results
            )
            if docker_available:
                print("4. Consider using dev containers for consistent environment")
                print("   Open this project in VS Code and reopen in container")


def main() -> None:
    """Main entry point."""
    try:
        print("🏥 Azure Terraform Modules - System Health Check")
        print("=" * 50)

        checker = HealthChecker()
        print("Initializing health checker...")

        checker.run_all_checks()
        print("Health checks completed, generating summary...")

        checker.print_summary()

        # Exit with appropriate code
        critical_issues = [
            r
            for r in checker.results
            if r.status in [ToolStatus.MISSING, ToolStatus.ERROR]
            and r.name in ["Python", "Terraform", "Azure CLI", "Git"]
        ]

        sys.exit(1 if critical_issues else 0)

    except Exception as e:
        print(f"Error running health check: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
