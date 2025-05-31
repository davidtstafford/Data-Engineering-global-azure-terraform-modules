#!/bin/bash
# Quick Demo: Container vs Local Development
# This script shows the difference between local and container environments

echo "🔍 Quick Environment Check"
echo "=========================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in a container
if [ -f /.dockerenv ]; then
    echo -e "${GREEN}🐳 You're running in the dev container!${NC}"
    echo "This means all tools are pre-installed and ready to use."
else
    echo -e "${YELLOW}💻 You're running locally on your Mac${NC}"
    echo "Some tools may not be installed."
fi
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

if [ -f /.dockerenv ]; then
    echo -e "${GREEN}🎉 All set! You can run:${NC}"
    echo "  • make pre-commit     # Fast validation"
    echo "  • make check          # Comprehensive checks"
    echo "  • terraform --version # Check Terraform"
else
    echo -e "${BLUE}💡 To get all tools instantly:${NC}"
    echo "  1. Open this project in VS Code"
    echo "  2. Install 'Dev Containers' extension"
    echo "  3. Command Palette → 'Dev Containers: Reopen in Container'"
    echo "  4. Wait for setup (3-5 minutes first time)"
    echo "  5. Run this script again!"
    echo ""
    echo -e "${YELLOW}Or install tools locally:${NC}"
    echo "  • Terraform: https://terraform.io/downloads"
    echo "  • Azure CLI: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    echo "  • Poetry: curl -sSL https://install.python-poetry.org | python3 -"
fi
