terraform {
  required_version = ">= 1.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

module "resource_group" {
  source = "../../"

  name     = var.resource_group_name
  location = var.location
  tags     = var.tags
}
