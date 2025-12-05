# Synology Terraform Configuration
# Main entry point for infrastructure management

terraform {
  required_version = ">= 1.0"

  required_providers {
    synology = {
      source  = "synology-community/synology"
      version = "~> 0.6"
    }
  }

  # HCP Terraform Cloud backend (CLI-driven workflow)
  # Organization name can be overridden via TF_CLOUD_ORGANIZATION environment variable
  cloud {
    organization = "SpecterRealm"

    workspaces {
      name = "homelab-synology"
    }
  }
}

# Configure the Synology Provider
provider "synology" {
  host            = var.synology_url
  user            = var.synology_username
  password        = var.synology_password
  skip_cert_check = var.synology_insecure
}

