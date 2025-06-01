variable "name" {
  description = "The name of the resource group"
  type        = string

  validation {
    condition     = can(regex("^[a-zA-Z0-9._-]+$", var.name))
    error_message = "Resource group name must contain only alphanumeric characters, periods, underscores, or hyphens."
  }
}

variable "location" {
  description = "The Azure region where the resource group will be created"
  type        = string

  validation {
    condition = contains([
      "East US", "East US 2", "West US", "West US 2", "West US 3",
      "Central US", "North Central US", "South Central US", "West Central US",
      "Canada Central", "Canada East",
      "Brazil South",
      "North Europe", "West Europe",
      "UK South", "UK West",
      "France Central", "France South",
      "Germany West Central", "Germany North",
      "Switzerland North", "Switzerland West",
      "Norway East", "Norway West",
      "Sweden Central", "Sweden South",
      "Australia East", "Australia Southeast", "Australia Central", "Australia Central 2",
      "Japan East", "Japan West",
      "Korea Central", "Korea South",
      "Southeast Asia", "East Asia",
      "India Central", "India South", "India West",
      "UAE North", "UAE Central",
      "South Africa North", "South Africa West"
    ], var.location)
    error_message = "Location must be a valid Azure region."
  }
}

variable "tags" {
  description = "A mapping of tags to assign to the resource"
  type        = map(string)
  default     = {}
}
