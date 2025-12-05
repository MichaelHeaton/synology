# Create new shared folders
# These resources will create the planned shares from nas-share-layout.md

# Create lxcs-iops share (Volume 1 - High IOPS)
# Purpose: High IOPS LXC container storage for Proxmox
# Note: synology_api resources may need to be applied to execute
resource "synology_api" "create_lxcs_iops" {
  api     = "SYNO.Core.Share"
  method  = "create"
  version = 1
  when    = "always" # Force execution
  parameters = {
    name               = "lxcs-iops"
    vol_path           = "/volume1"
    description        = "High IOPS LXC container storage for Proxmox Cluster 1"
    enable_share_quota = "false"
    enable_encryption  = "false"
  }
}

