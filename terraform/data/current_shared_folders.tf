# Resource to query current shared folders
# This will help us discover what exists before importing
# Note: synology_api is a resource, not a data source

resource "synology_api" "list_shared_folders" {
  api     = "SYNO.Core.Share"
  method  = "list"
  version = 1
  parameters = jsonencode({
    additional = "[\"share_rights\",\"encryption\",\"is_support_acl\",\"is_support_acl_enable\",\"is_support_apply_group_quota\",\"is_support_apply_user_quota\",\"is_support_share_quota\",\"is_support_snapshot\",\"is_support_snapshot_share\",\"is_support_snapshot_share_quota\",\"is_support_snapshot_share_size\",\"is_support_snapshot_size\",\"is_support_time_machine\",\"is_support_vss\",\"owner\",\"time_machine_quota\",\"volume_status\"]"
    limit      = 1000
    offset     = 0
  })
}

