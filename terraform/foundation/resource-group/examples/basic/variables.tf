variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
  default     = "rg-example-dev"
}

variable "location" {
  description = "The Azure region where resources will be created"
  type        = string
  default     = "East US"
}

variable "tags" {
  description = "A mapping of tags to assign to the resources"
  type        = map(string)
  default = {
    Environment = "dev"
    Project     = "terraform-modules-example"
    ManagedBy   = "terraform"
  }
}
