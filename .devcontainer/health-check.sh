#!/bin/bash
# Development Container Health Check
# This script verifies that all required tools are installed and working

set -e

echo "🔍 Development Container Health Check"
echo "====================================="

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Track overall status
OVERALL_STATUS=0

check_command() {
    local cmd=$1
    local name=$2
    local version_flag=${3:-"--version"}

    echo -n "Checking $name... "

    if command -v "$cmd" >/dev/null 2>&1; then
        local version
        if [ "$version_flag" = "none" ]; then
            version="installed"
        else
            version=$($cmd $version_flag 2>&1 | head -1)
        fi
        echo -e "${GREEN}✓${NC} ($version)"
    else
        echo -e "${RED}✗ Not found${NC}"
        OVERALL_STATUS=1
    fi
}

check_python_package() {
    local package=$1
    local import_name=${2:-$package}

    echo -n "Checking Python package $package... "

    if python -c "import $import_name" >/dev/null 2>&1; then
        local version=$(python -c "import $import_name; print(getattr($import_name, '__version__', 'unknown'))" 2>/dev/null || echo "unknown")
        echo -e "${GREEN}✓${NC} ($version)"
    else
        echo -e "${RED}✗ Not found${NC}"
        OVERALL_STATUS=1
    fi
}

echo
echo "🔧 System Tools"
echo "---------------"
check_command "python" "Python"
check_command "python3" "Python3"
check_command "pip" "pip"
check_command "poetry" "Poetry"
check_command "git" "Git"
check_command "terraform" "Terraform"
check_command "az" "Azure CLI"
check_command "gh" "GitHub CLI"
check_command "jq" "jq"
check_command "curl" "curl"
check_command "wget" "wget"

echo
echo "🐍 Python Development Tools"
echo "---------------------------"
check_python_package "black"
check_python_package "isort"
check_python_package "flake8"
check_python_package "mypy"
check_python_package "bandit"
check_python_package "safety"
check_python_package "pytest"
check_python_package "pre_commit" "pre_commit"
check_python_package "rich"
check_python_package "click"

echo
echo "🔐 Security Tools"
echo "----------------"
check_command "checkov" "Checkov"
check_command "tflint" "TFLint"
check_command "terraform-docs" "terraform-docs"

echo
echo "📁 Environment Check"
echo "--------------------"

# Check if we're in a container
if [ -f /.dockerenv ]; then
    echo -e "Container Environment: ${GREEN}✓ Running in Docker container${NC}"
else
    echo -e "Container Environment: ${YELLOW}⚠ Not in Docker container${NC}"
fi

# Check workspace
if [ -f "pyproject.toml" ]; then
    echo -e "Workspace: ${GREEN}✓ Found pyproject.toml${NC}"
else
    echo -e "Workspace: ${RED}✗ pyproject.toml not found${NC}"
    OVERALL_STATUS=1
fi

# Check Poetry virtual environment
if poetry env info >/dev/null 2>&1; then
    echo -e "Poetry Environment: ${GREEN}✓ Virtual environment active${NC}"
    echo "  Path: $(poetry env info --path)"
else
    echo -e "Poetry Environment: ${YELLOW}⚠ No virtual environment${NC}"
fi

# Check pre-commit hooks
if [ -f ".pre-commit-config.yaml" ]; then
    echo -e "Pre-commit Config: ${GREEN}✓ Found .pre-commit-config.yaml${NC}"

    if [ -d ".git/hooks" ] && [ -f ".git/hooks/pre-commit" ]; then
        echo -e "Pre-commit Hooks: ${GREEN}✓ Installed${NC}"
    else
        echo -e "Pre-commit Hooks: ${YELLOW}⚠ Not installed (run 'make install')${NC}"
    fi
else
    echo -e "Pre-commit Config: ${RED}✗ .pre-commit-config.yaml not found${NC}"
    OVERALL_STATUS=1
fi

# Check Makefile
if [ -f "Makefile" ]; then
    echo -e "Makefile: ${GREEN}✓ Found${NC}"
else
    echo -e "Makefile: ${RED}✗ Not found${NC}"
    OVERALL_STATUS=1
fi

echo
echo "🧪 Quick Tests"
echo "-------------"

# Test Python import
echo -n "Testing Python imports... "
if python -c "
import sys
import os
import pathlib
import json
import yaml
import click
import rich
print('OK')
" >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    OVERALL_STATUS=1
fi

# Test Terraform
echo -n "Testing Terraform... "
if terraform version >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    OVERALL_STATUS=1
fi

# Test Azure CLI
echo -n "Testing Azure CLI... "
if az version >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    OVERALL_STATUS=1
fi

echo
echo "📊 Summary"
echo "----------"

if [ $OVERALL_STATUS -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed! Development environment is ready.${NC}"
    echo
    echo -e "${BLUE}Next steps:${NC}"
    echo "  make help           # See all available commands"
    echo "  make install        # Install/update dependencies"
    echo "  make pre-commit     # Run quick checks"
    echo "  make check          # Run comprehensive validation"
else
    echo -e "${RED}❌ Some checks failed. Please review the output above.${NC}"
    echo
    echo -e "${BLUE}Common fixes:${NC}"
    echo "  make install        # Install missing dependencies"
    echo "  poetry install      # Install Python packages"
    echo "  pre-commit install  # Install pre-commit hooks"
fi

echo
exit $OVERALL_STATUS
