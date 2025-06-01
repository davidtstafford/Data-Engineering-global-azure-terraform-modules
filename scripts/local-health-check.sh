#!/bin/bash
# Local development environment health check script for development setup validation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "PASS")
            echo -e "${GREEN}✓${NC} $message"
            ;;
        "FAIL")
            echo -e "${RED}✗${NC} $message"
            ;;
        "WARN")
            echo -e "${YELLOW}⚠${NC} $message"
            ;;
        "INFO")
            echo -e "${BLUE}ℹ${NC} $message"
            ;;
    esac
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get version of a command
get_version() {
    local cmd=$1

    if command_exists "$cmd"; then
        case $cmd in
            "terraform")
                terraform version | head -n1 | awk '{print $2}'
                ;;
            "az")
                az version --output tsv --query '"azure-cli"' 2>/dev/null || echo "unknown"
                ;;
            "python"|"python3")
                python3 --version | awk '{print $2}'
                ;;
            "poetry")
                poetry --version | awk '{print $3}'
                ;;
            "pre-commit")
                pre-commit --version | awk '{print $2}'
                ;;
            "tflint")
                tflint --version | head -n1 | awk '{print $3}'
                ;;
            "terraform-docs")
                terraform-docs version | awk '{print $3}'
                ;;
            *)
                $cmd --version 2>/dev/null | head -n1 || echo "unknown"
                ;;
        esac
    else
        echo "not installed"
    fi
}

# Main health check function
main() {
    echo -e "${BLUE}🔍 Local Development Environment Health Check${NC}"
    echo "=============================================="

    print_status "INFO" "Running in local development environment"

    # Required tools for basic development
    REQUIRED_TOOLS=("python3" "git" "make")
    # Optional tools that enhance development experience
    OPTIONAL_TOOLS=("poetry" "terraform" "az" "pre-commit" "tflint" "terraform-docs" "jq")

    echo ""

    # Check required tools
    echo -e "${BLUE}Required Tools:${NC}"
    all_required_present=true

    for tool in "${REQUIRED_TOOLS[@]}"; do
        if command_exists "$tool"; then
            version=$(get_version "$tool")
            print_status "PASS" "$tool ($version)"
        else
            print_status "FAIL" "$tool (not found)"
            all_required_present=false
        fi
    done

    # Check optional tools
    echo ""
    echo -e "${BLUE}Optional Tools (recommended for full development experience):${NC}"
    optional_installed=0
    for tool in "${OPTIONAL_TOOLS[@]}"; do
        if command_exists "$tool"; then
            version=$(get_version "$tool")
            print_status "PASS" "$tool ($version)"
            ((optional_installed++))
        else
            case $tool in
                "poetry")
                    print_status "WARN" "$tool (not found - install from https://python-poetry.org)"
                    ;;
                "terraform")
                    print_status "WARN" "$tool (not found - install from https://terraform.io/downloads)"
                    ;;
                "az")
                    print_status "WARN" "$tool (not found - install Azure CLI)"
                    ;;
                *)
                    print_status "WARN" "$tool (not found - will be installed via poetry)"
                    ;;
            esac
        fi
    done

    echo ""

    # Check Python environment
    echo -e "${BLUE}Python Environment:${NC}"
    if command_exists "python3"; then
        python_version=$(python3 --version | awk '{print $2}')
        if [[ "$python_version" =~ ^3\.(9|10|11|12|13) ]]; then
            print_status "PASS" "Python version $python_version (compatible)"
        else
            print_status "WARN" "Python version $python_version (recommend 3.9+)"
        fi

        # Check if we're in a virtual environment
        if [[ -n "${VIRTUAL_ENV:-}" ]] || [[ -n "${CONDA_DEFAULT_ENV:-}" ]]; then
            print_status "PASS" "Virtual environment active: ${VIRTUAL_ENV:-$CONDA_DEFAULT_ENV}"
        else
            print_status "INFO" "No virtual environment (Poetry will manage this)"
        fi
    fi

    # Check Poetry configuration
    if command_exists "poetry"; then
        echo ""
        echo -e "${BLUE}Poetry Configuration:${NC}"

        if [[ -f "pyproject.toml" ]]; then
            print_status "PASS" "pyproject.toml found"
        else
            print_status "FAIL" "pyproject.toml not found"
        fi

        # Check if poetry.lock exists
        if [[ -f "poetry.lock" ]]; then
            print_status "PASS" "poetry.lock found"
        else
            print_status "WARN" "poetry.lock not found (run 'make install')"
        fi
    fi

    # Check Git configuration
    echo ""
    echo -e "${BLUE}Git Configuration:${NC}"
    if command_exists "git"; then
        if git rev-parse --git-dir >/dev/null 2>&1; then
            print_status "PASS" "Git repository detected"

            # Check if pre-commit is installed
            if [[ -f ".pre-commit-config.yaml" ]]; then
                print_status "PASS" "Pre-commit configuration found"

                if command_exists "pre-commit"; then
                    if pre-commit --version >/dev/null 2>&1; then
                        print_status "PASS" "Pre-commit hooks available"
                    fi
                else
                    print_status "INFO" "Pre-commit will be installed via 'make install'"
                fi
            else
                print_status "WARN" "Pre-commit configuration not found"
            fi
        else
            print_status "WARN" "Not in a git repository"
        fi
    fi

    # Summary
    echo ""
    echo -e "${BLUE}Summary:${NC}"
    if $all_required_present; then
        print_status "PASS" "Local environment has required tools"
        if [ $optional_installed -ge 3 ]; then
            echo -e "${GREEN}🎉 Ready for development!${NC}"
        else
            echo -e "${YELLOW}💡 Install optional tools for the best experience${NC}"
        fi
    else
        print_status "FAIL" "Local environment is missing required tools"
        echo -e "${RED}❌ Please install missing required tools${NC}"
    fi

    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    if $all_required_present; then
        echo "• Run 'make help' to see available commands"
        echo "• Run 'make install' to setup Python dependencies"
        echo "• Run 'make demo' to see current environment status"
        if [ $optional_installed -lt 3 ]; then
            echo "• Install optional tools for full functionality"
        fi
    else
        echo "• Install missing required tools"
        echo "• Run this script again to verify installation"
    fi
}

# Run the health check
main "$@"
