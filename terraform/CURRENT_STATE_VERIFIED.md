# Current Synology Configuration - Verified via API

## Verification

✅ **Verified via API**: All data retrieved using `scripts/synology_api.py`
**Date**: 2025-12-04
**Source**: Direct API query to Synology DSM

## Shared Folders (Current State - Verified)

### Volume 1

| Share Name     | Volume   | Description                  | UUID                                 | Status    |
| -------------- | -------- | ---------------------------- | ------------------------------------ | --------- |
| `docker`       | /volume1 | (empty)                      | 415c0da0-b11c-4ae9-a487-c60b68c6e7d6 | ✅ Exists |
| `web`          | /volume1 | System default shared folder | 8f670e18-3a41-4d15-aaff-e953db62ad01 | ✅ Exists |
| `web_packages` | /volume1 | (empty)                      | 14e3f8b9-cfdd-44c8-90e2-43141968ff54 | ✅ Exists |

**Notes**:

- All Volume 1 shares support ACL
- None are USB shares
- None have encryption enabled

### Volume 3

| Share Name | Volume   | Description                    | UUID                                 | Status    |
| ---------- | -------- | ------------------------------ | ------------------------------------ | --------- |
| `homes`    | /volume3 | homes contains all users' home | 20773af0-825f-4298-9741-fc09517053be | ✅ Exists |
| `Logs`     | /volume3 | (empty)                        | 57414830-9fc4-4134-8b99-49fad496f766 | ✅ Exists |
| `UNAS`     | /volume3 | (empty)                        | f6fce0b7-e770-4c26-8a7f-1b362c823cd8 | ✅ Exists |

**Notes**:

- All Volume 3 shares support ACL
- None are USB shares
- None have encryption enabled

## New High IOPS Shares (Created 2025-12-04)

### Volume 1 (High IOPS - All Created):

| Share Name        | Volume   | Description                     | UUID                                 | Status     |
| ----------------- | -------- | ------------------------------- | ------------------------------------ | ---------- |
| `lxcs-iops`       | /volume1 | High IOPS LXC container storage | 40a2c825-63c3-4cf5-9246-4414903c2c08 | ✅ Created |
| `dockers-iops`    | /volume1 | High IOPS Docker storage        | b333f659-c443-4df9-a084-2c3b04bdb9b8 | ✅ Created |
| `vmdks-iops`      | /volume1 | High IOPS VM disk images        | a866bb13-1566-40be-ad36-4cf2c98ee628 | ✅ Created |
| `kubernetes-iops` | /volume1 | High IOPS Kubernetes storage    | 9a1c3337-8bab-4392-8ceb-08d7473f96b8 | ✅ Created |
| `ai`              | /volume1 | AI stack storage                | 52db665f-e65d-402e-9af2-c39a90cb5a8c | ✅ Created |

**Note**: All shares created manually via DSM UI. Quotas configured:

- `lxcs-iops`: 1 TB
- `dockers-iops`: 2 TB
- `vmdks-iops`: 5 TB
- `kubernetes-iops`: 2 TB
- `ai`: 5 TB

## Important Notes

⚠️ **CRITICAL**: Do not remove or modify existing shares:

- `docker` (UUID: 415c0da0-b11c-4ae9-a487-c60b68c6e7d6)
- `homes` (UUID: 20773af0-825f-4298-9741-fc09517053be)
- `Logs` (UUID: 57414830-9fc4-4134-8b99-49fad496f766)
- `UNAS` (UUID: f6fce0b7-e770-4c26-8a7f-1b362c823cd8)
- `web` (UUID: 8f670e18-3a41-4d15-aaff-e953db62ad01)
- `web_packages` (UUID: 14e3f8b9-cfdd-44c8-90e2-43141968ff54)

These are production shares that are currently in use.

## API Script

The Python script `scripts/synology_api.py` provides:

- ✅ **Authentication** - Login/logout with session management
- ✅ **List Shares** - Get all shared folders with details
- ✅ **Get Share** - Get details of specific share
- ✅ **Create Share** - Create new shared folders (ready to test)
- ✅ **JSON Export** - Save current state to `current_shares.json`

## Usage

```bash
cd /Users/michaelheaton/Projects/HomeLab/synology/terraform

# Set password (if not using default)
export SYNOLOGY_PASS='your-password'

# Run the script
python3 scripts/synology_api.py
```

This will:

- Authenticate with DSM
- List all shares with details
- Show formatted output
- Save data to `current_shares.json`

## Next Steps

1. [x] ✅ Verify current shares via API
2. [ ] Create `lxcs-iops` share via API
3. [ ] Configure NFS exports for `lxcs-iops`
4. [ ] Test Proxmox can mount the share
5. [ ] Document NFS/SMB settings

## Data Export

The script saves a complete snapshot to `current_shares.json` including:

- Timestamp
- Share names and UUIDs
- Volume paths
- Descriptions
- Encryption status
- Raw API response data

This file is gitignored but can be used for documentation and reference.
