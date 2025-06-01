"""
Common test fixtures and configurations for Terraform tests.
"""

# Common Azure locations for testing
TEST_LOCATIONS = ["East US", "West US 2", "West Europe", "UK South"]

# Common resource group configurations for testing
RESOURCE_GROUP_TEST_CONFIGS = {
    "basic": {
        "name": "test-rg-basic",
        "location": "East US",
        "tags": {"Environment": "test", "Project": "terraform-testing"},
    },
    "minimal": {"name": "test-rg-minimal", "location": "West US 2"},
    "with_extensive_tags": {
        "name": "test-rg-tagged",
        "location": "West Europe",
        "tags": {
            "Environment": "test",
            "Project": "terraform-testing",
            "Owner": "data-engineering-team",
            "CostCenter": "engineering",
            "Application": "data-platform",
        },
    },
}

# Provider configurations for different test scenarios
PROVIDER_CONFIGS = {
    "default": {
        "azurerm": {
            "features": {},
            "skip_provider_registration": True,
            "use_msi": False,
            "use_cli": False,
            "use_oidc": False,
        }
    },
    "with_skip_provider_registration": {
        "azurerm": {
            "features": {},
            "skip_provider_registration": True,
            "use_msi": False,
            "use_cli": False,
            "use_oidc": False,
        }
    },
}

# Common variable validation test cases
VARIABLE_VALIDATION_TESTS = {
    "resource_group": {
        "valid_names": [
            "test-rg",
            "my-resource-group",
            "rg-prod-001",
            "data-platform-rg",
        ],
        "invalid_names": [
            "",  # Empty string
            "a" * 91,  # Too long (max 90 chars)
            "rg.with.dots",  # Invalid characters
            "-starting-with-dash",  # Can't start with dash
            "ending-with-dash-",  # Can't end with dash
        ],
        "valid_locations": TEST_LOCATIONS,
        "invalid_locations": ["InvalidLocation", "Not A Real Location", ""],
    }
}
