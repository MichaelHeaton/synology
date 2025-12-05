# Synology Terraform Outputs

output "nas_name" {
  description = "NAS identifier"
  value       = var.nas_name
}

output "synology_url" {
  description = "Synology DSM URL"
  value       = var.synology_url
  sensitive   = false
}

# Output shared folders query results
# Temporarily commented out to test if resources are recognized
# Uncomment after resources are working
# output "all_shared_folders_raw" {
#   description = "Raw API response for all shared folders"
#   value       = try(synology_api.list_all_shares.result, "not_available")
#   sensitive   = false
# }
