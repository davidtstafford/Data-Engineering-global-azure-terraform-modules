# Azure Terraform Modules - Development Container

This development container provides a consistent, cross-platform development environment for the Azure Terraform Modules project. It includes all necessary tools and dependencies pre-configured.

## 🚀 Quick Start

### Prerequisites
- [Visual Studio Code](https://code.visualstudio.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or compatible container runtime)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) for VS Code

### Getting Started

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/your-org/Data-Engineering-global-azure-terraform-modules.git
   cd Data-Engineering-global-azure-terraform-modules
   ```

2. **Open in VS Code**:
   ```bash
   code .
   ```

3. **Reopen in Container**:
   - VS Code should automatically detect the dev container configuration
   - Click "Reopen in Container" when prompted, or
   - Use Command Palette (`Ctrl+Shift+P`): "Dev Containers: Reopen in Container"

4. **Wait for setup** (first time only):
   - The container will build and install all dependencies automatically
   - This takes 3-5 minutes on first run
   - Subsequent starts are much faster

5. **Start developing**:
   ```bash
   make help           # See all available commands
   make install        # Ensure everything is installed
   make pre-commit     # Run quick checks
   ```

## 🛠️ What's Included

### Core Tools
- **Python 3.11** with Poetry for dependency management
- **Terraform** latest version with provider caching
- **Azure CLI** with Bicep support
- **Git** with helpful aliases and configuration
- **GitHub CLI** for repository management

### Development Tools
- **Pre-commit hooks** with all linters and formatters
- **Testing framework** (pytest) with coverage
- **Code formatting** (black, isort)
- **Linting** (flake8, mypy, bandit)
- **Security scanning** (checkov, safety)
- **Terraform tools** (terraform-docs, tflint)

### VS Code Extensions
- Python development (linting, formatting, debugging)
- Terraform language support
- Azure tools and CLI integration
- GitHub Copilot (if you have access)
- Testing and debugging support
- YAML, TOML, and Makefile support

## 🔧 Container Features

### Environment
- **Base**: Microsoft's official Python dev container
- **User**: `vscode` with sudo access
- **Shell**: Zsh with Oh My Zsh and helpful aliases
- **Working Directory**: `/workspace`

### Port Forwarding
- `8000` - Development server
- `8080` - Alternative development server
- `3000` - Frontend server

### Aliases
- `tf` → `terraform`
- `mk` → `make`
- `ll` → `ls -la`
- `la` → `ls -la`

### Git Integration
- Git repository is bind-mounted for performance
- Pre-commit hooks are automatically installed
- Git configuration is preserved from host

## 💡 Development Workflow

The container includes the same three-tier validation system:

### 1. Fast Checks (30 seconds)
```bash
make pre-commit
```
Runs formatting, linting, and basic security checks.

### 2. Comprehensive Checks (2-5 minutes)
```bash
make check
```
Includes all fast checks plus tests, security scans, and Terraform validation.

### 3. Commit Ready
```bash
make commit-ready
```
Full validation before committing changes.

## 🔄 Container Management

### Rebuilding the Container
If you need to rebuild (after Dockerfile changes):
```bash
# Command Palette: "Dev Containers: Rebuild Container"
```

### Updating Dependencies
```bash
make install  # Updates Poetry dependencies
poetry run pre-commit autoupdate  # Updates pre-commit hooks
```

### Performance Tips
- The container uses bind mounts for the git directory for better performance
- Poetry dependencies are cached in the container image
- Terraform providers are cached between container rebuilds

## 🐛 Troubleshooting

### Container Won't Start
1. Ensure Docker Desktop is running
2. Check Docker has enough resources (4GB+ RAM recommended)
3. Try rebuilding: "Dev Containers: Rebuild Container"

### Slow Performance
1. Ensure Docker Desktop has adequate resources
2. On Windows, ensure the project is in the WSL2 filesystem
3. Consider enabling Docker Desktop's VirtioFS (experimental)

### Git Issues
1. Ensure git is configured in the container:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

### Extension Issues
1. Extensions are automatically installed on container creation
2. If missing, manually install through VS Code extensions panel
3. Some extensions may require container rebuild to work properly

### Terraform Issues
1. Terraform is automatically initialized for modules in post-create script
2. Manual initialization: `terraform init -backend=false` in module directories
3. Provider authentication may require Azure CLI login: `az login`

## 🔒 Security Considerations

- The container runs as the `vscode` user (non-root)
- Git credentials are handled through VS Code's credential manager
- Azure CLI authentication uses device code flow by default
- No secrets are stored in the container image

## 🎯 Agent Mode Support

**Yes!** VS Code's agent mode (GitHub Copilot, IntelliSense, etc.) works perfectly within the dev container:

- **GitHub Copilot**: Full support for code completion and chat
- **IntelliSense**: Python and Terraform language servers work seamlessly
- **Debugging**: Full debugging support for Python and integration tests
- **Extensions**: All extensions function normally within the container
- **Terminal Integration**: All terminal-based tools work as expected

The dev container provides the same (or better) experience as local development with the added benefits of:
- Consistent environment across team members
- No local tool installation required
- Isolated dependencies
- Reproducible builds

## 📝 Customization

### Adding Tools
Edit `.devcontainer/Dockerfile` to add new system packages or tools.

### VS Code Settings
Modify `.devcontainer/devcontainer.json` to customize VS Code settings and extensions.

### Shell Configuration
The `post-create.sh` script can be customized to add additional setup steps.

## 🤝 Contributing

When contributing to the dev container configuration:

1. Test changes thoroughly
2. Document any new tools or requirements
3. Consider impact on container build time
4. Update this README for any significant changes

---

**Need help?** Check the [development workflow guide](../docs/development-workflow.md) or open an issue!
