# Development Container vs Local Development

This document explains the two ways to develop with this project and when to use each approach.

## 🎯 Quick Decision Guide

### Choose **Dev Container** if:
- ✅ You want **zero setup** - everything just works
- ✅ You're on **Windows, Mac, or Linux** 
- ✅ You want **consistent environment** across team
- ✅ You don't want to install Terraform, Azure CLI, etc. locally
- ✅ You use **VS Code** (recommended)

### Choose **Local Development** if:
- ✅ You already have all tools installed locally
- ✅ You prefer your existing local setup
- ✅ You're using a different editor than VS Code
- ✅ You have specific local configurations you need

## 🐳 Dev Container Approach (Recommended)

### What You Get
- **Terraform** latest version
- **Azure CLI** with Bicep support  
- **Python 3.11** with Poetry
- **All linters, formatters, security tools** pre-configured
- **VS Code extensions** automatically installed
- **Pre-commit hooks** ready to go

### How It Works
1. **Open project in VS Code**
2. **VS Code detects** `.devcontainer/devcontainer.json`
3. **Choose "Reopen in Container"**
4. **VS Code rebuilds interface inside container**
5. **All terminals are now container terminals**
6. **All commands run inside container automatically**

### Example Session
```bash
# This is what you'll see in VS Code terminal after "Reopen in Container"
vscode@container:/workspace$ make demo
🔍 Quick Environment Check
==========================

🐳 You're running in the dev container!
This means all tools are pre-installed and ready to use.

Tool availability:
  ✓ Terraform - Available
  ✓ Azure CLI - Available  
  ✓ Poetry - Available

🎉 All set! You can run:
  • make pre-commit     # Fast validation
  • make check          # Comprehensive checks
  • terraform --version # Check Terraform

vscode@container:/workspace$ terraform --version
Terraform v1.8.0

vscode@container:/workspace$ make pre-commit
# All tools work perfectly!
```

## 💻 Local Development Approach

### What You Need to Install
- **Terraform**: https://terraform.io/downloads
- **Azure CLI**: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
- **Poetry**: `curl -sSL https://install.python-poetry.org | python3 -`

### Setup Steps
```bash
# 1. Install tools above, then:
git clone <repo>
cd azure-terraform-modules
make install        # Install Python deps and pre-commit hooks

# 2. Test everything works:
make demo          # Should show all tools available
make pre-commit    # Should run successfully
```

### Example Session  
```bash
# This is what you'll see in your local terminal after setup
david@macbook azure-terraform-modules % make demo
🔍 Quick Environment Check
==========================

💻 You're running locally on your Mac
Some tools may not be installed.

Tool availability:
  ✓ Terraform - Available      # After you install it
  ✓ Azure CLI - Available      # After you install it
  ✓ Poetry - Available

# vs without installation:
Tool availability:
  ❌ Terraform - Not found
  ❌ Azure CLI - Not found
  ✓ Poetry - Available
```

## 🔄 Command Behavior Differences

### In Dev Container
```bash
# VS Code terminal (inside container)
vscode@container:/workspace$ make check
# ✅ Works perfectly - all tools available
# ✅ Terraform commands work
# ✅ Azure CLI commands work  
# ✅ All validation passes
```

### Local Development
```bash
# Your local terminal
david@macbook azure-terraform-modules % make check
# ❌ Fails if tools not installed
# ❌ "terraform: command not found"
# ❌ "az: command not found"

# ✅ Works after installing tools locally
david@macbook azure-terraform-modules % make check  
# ✅ All validation passes (after setup)
```

## 🧪 Testing Your Setup

Run this to see your current status:
```bash
make demo
```

**In Dev Container:**
- Shows "🐳 You're running in the dev container!"
- All tools show as "✅ Available"
- Ready to develop immediately

**Locally:**  
- Shows "💻 You're running locally"
- Missing tools show as "❌ Not found"
- Gives installation instructions

## 🎯 Workflow Recommendations

### For Dev Container Users
```bash
# 1. Open in VS Code → "Reopen in Container"
# 2. Wait for setup (3-5 minutes first time)
# 3. Start developing immediately:

make demo           # Verify setup
make pre-commit     # Fast checks while coding
make check          # Before committing  
make commit-ready   # Final validation

# Everything just works! 🎉
```

### For Local Development Users
```bash
# 1. Install prerequisites (Terraform, Azure CLI, Poetry)
# 2. Set up project:

make install        # One-time setup
make demo           # Verify all tools found

# 3. Regular development:
make pre-commit     # Fast checks while coding
make check          # Before committing
make commit-ready   # Final validation
```

## 🤔 Common Questions

### Q: "Which approach should I use?"
**A:** Dev Container is recommended unless you already have a local setup you prefer.

### Q: "Will GitHub Copilot work in the container?"
**A:** Yes! All VS Code features including Copilot work perfectly in dev containers.

### Q: "How do I switch approaches?"
**A:** You can use both! The same project works in both environments.

### Q: "What if the container is slow?"
**A:** Ensure Docker Desktop has enough resources (4GB+ RAM). Performance is usually very good.

### Q: "Can I customize the dev container?"
**A:** Yes! Edit `.devcontainer/devcontainer.json` and `.devcontainer/Dockerfile`.

## 🚀 Next Steps

1. **Try the dev container**: Open in VS Code, choose "Reopen in Container"
2. **Run `make demo`** to see the difference
3. **Start with `make pre-commit`** for quick validation
4. **Read [development-workflow.md](development-workflow.md)** for detailed workflow

The key insight is: **both approaches use the same commands**, but the dev container has all tools pre-installed while local development requires you to install them yourself.
