# Query existing shared folders to verify they exist
# These resources query the current state and can be used as a baseline
# IMPORTANT: These are READ-ONLY queries - they do not modify anything

# Query all shared folders (general list)
resource "synology_api" "list_all_shares" {
  api     = "SYNO.Core.Share"
  method  = "list"
  version = 1
  parameters = {
    additional = "[\"share_rights\",\"encryption\",\"is_support_acl\",\"volume_status\"]"
    limit      = "1000"
    offset     = "0"
  }
}

# Query individual existing shared folders (Volume 1)
resource "synology_api" "get_docker" {
  api     = "SYNO.Core.Share"
  method  = "get"
  version = 1
  parameters = {
    name       = "docker"
    additional = "[\"share_rights\",\"encryption\",\"volume_status\"]"
  }
}

resource "synology_api" "get_web" {
  api     = "SYNO.Core.Share"
  method  = "get"
  version = 1
  parameters = {
    name       = "web"
    additional = "[\"share_rights\",\"encryption\",\"volume_status\"]"
  }
}

resource "synology_api" "get_web_packages" {
  api     = "SYNO.Core.Share"
  method  = "get"
  version = 1
  parameters = {
    name       = "web_packages"
    additional = "[\"share_rights\",\"encryption\",\"volume_status\"]"
  }
}

# Query individual existing shared folders (Volume 3)
resource "synology_api" "get_homes" {
  api     = "SYNO.Core.Share"
  method  = "get"
  version = 1
  parameters = {
    name       = "homes"
    additional = "[\"share_rights\",\"encryption\",\"volume_status\"]"
  }
}

resource "synology_api" "get_logs" {
  api     = "SYNO.Core.Share"
  method  = "get"
  version = 1
  parameters = {
    name       = "Logs"
    additional = "[\"share_rights\",\"encryption\",\"volume_status\"]"
  }
}

resource "synology_api" "get_unas" {
  api     = "SYNO.Core.Share"
  method  = "get"
  version = 1
  parameters = {
    name       = "UNAS"
    additional = "[\"share_rights\",\"encryption\",\"volume_status\"]"
  }
}
