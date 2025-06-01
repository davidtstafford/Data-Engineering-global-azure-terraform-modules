#!/bin/bash
# Quick Demo: Local Development Environment Status
# This script shows the current status of the local development environment

echo "🔍 Quick Environment Check"
echo "=========================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in a local environment
echo -e "${YELLOW}💻 You're running locally$(RESET)"
echo "Checking what tools are available..."
echo ""

# Quick tool check
echo "Tool availability:"

tools_to_check=(
    "terraform:Terraform"
    "az:Azure CLI"
    "poetry:Poetry"
    "make:Make"
)

for tool_info in "${tools_to_check[@]}"; do
    tool=$(echo "$tool_info" | cut -d: -f1)
    name=$(echo "$tool_info" | cut -d: -f2)

    if command -v "$tool" >/dev/null 2>&1; then
        echo -e "  ${GREEN}✓ $name${NC} - Available"
    else
        echo -e "  ${RED}❌ $name${NC} - Not found"
    fi
done

echo ""

echo ""
echo -e "${GREEN}🎉 Ready to start! Common commands:${NC}"
echo "  • make pre-commit     # Fast validation"
echo "  • make check          # Comprehensive checks"
echo "  • terraform --version # Check Terraform"
echo ""
echo -e "${BLUE}💡 If any tools are missing, install them locally:${NC}"
echo "  • Terraform: https://terraform.io/downloads"
echo "  • Azure CLI: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
echo "  • Poetry: curl -sSL https://install.python-poetry.org | python3 -"
echo ""
echo -e "${YELLOW}💻 For full health check run:${NC} make container-info"
