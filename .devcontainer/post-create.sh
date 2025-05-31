#!/bin/bash
set -e

echo "🔧 Setting up Azure Terraform Modules development environment..."

# Ensure we're in the workspace directory
cd /workspace

# Install Poetry dependencies if pyproject.toml exists
if [ -f "pyproject.toml" ]; then
    echo "📦 Installing Poetry dependencies..."
    poetry install --no-interaction

    # Install pre-commit hooks
    echo "🪝 Installing pre-commit hooks..."
    poetry run pre-commit install --install-hooks

    # Update pre-commit hooks to latest versions
    echo "⬆️  Updating pre-commit hooks..."
    poetry run pre-commit autoupdate
else
    echo "⚠️  pyproject.toml not found, skipping Poetry setup"
fi

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    echo "🔄 Initializing git repository..."
    git init
    git config --global init.defaultBranch main
fi

# Set up git config if not already set
if [ -z "$(git config --global user.name)" ]; then
    echo "📝 Setting up git configuration..."
    echo "Please run the following commands to set up git:"
    echo "  git config --global user.name 'Your Name'"
    echo "  git config --global user.email 'your.email@example.com'"
fi

# Create useful directories if they don't exist
mkdir -p .vscode/settings.json

# Terraform setup
echo "🔧 Setting up Terraform..."

# Initialize terraform modules if they exist
if [ -d "terraform" ]; then
    echo "🌍 Found Terraform modules, initializing..."
    find terraform -name "*.tf" -exec dirname {} \; | sort -u | while read -r dir; do
        if [ -f "$dir/main.tf" ] || [ -f "$dir/versions.tf" ]; then
            echo "  Initializing $dir..."
            (cd "$dir" && terraform init -backend=false) || echo "    ⚠️  Failed to initialize $dir"
        fi
    done
fi

# Verify installations
echo "✅ Verifying tool installations..."
echo "Python: $(python --version)"
echo "Poetry: $(poetry --version)"
echo "Terraform: $(terraform version -json | jq -r '.terraform_version')"
echo "Azure CLI: $(az --version | head -1)"
echo "Pre-commit: $(pre-commit --version)"
echo "Checkov: $(checkov --version)"

# Show helpful commands
echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "🚀 Quick start commands:"
echo "  make help           # Show all available commands"
echo "  make install        # Install/update dependencies"
echo "  make pre-commit     # Run fast checks"
echo "  make check          # Run comprehensive checks"
echo "  make commit-ready   # Full validation before commit"
echo ""
echo "📚 Documentation:"
echo "  cat docs/development-workflow.md  # Read the workflow guide"
echo ""
echo "🔧 Useful aliases:"
echo "  tf = terraform"
echo "  mk = make"
echo "  ll = ls -la"
echo ""
