# Synology Terraform Variables

# Note: hcp_organization is set in main.tf cloud block and can be overridden
# via TF_CLOUD_ORGANIZATION environment variable

variable "synology_url" {
  description = "Synology DSM URL (e.g., https://nas01.specterrealm.com:5001)"
  type        = string
  sensitive   = false
}

variable "synology_username" {
  description = "Synology DSM username"
  type        = string
  sensitive   = true
}

variable "synology_password" {
  description = "Synology DSM password"
  type        = string
  sensitive   = true
}

variable "synology_insecure" {
  description = "Skip TLS verification (not recommended for production)"
  type        = bool
  default     = false
}

variable "nas_name" {
  description = "NAS identifier (e.g., nas01)"
  type        = string
  default     = "nas01"
}

