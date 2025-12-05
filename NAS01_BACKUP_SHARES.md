# NAS01 Backup Shares Plan

**Status**: ✅ Created (2025-12-04)
**NAS**: NAS01 (Synology DS1621+)
**Volume**: Volume 3 (15.7 TB total, 8.3 TB used, ~7.4 TB available)
**Rationale**: Better offsite backup integration, Synology backup features

## Backup Shares for NAS01 Volume 3

| Share Name            | Volume   | Description            | UUID                                 | Status     |
| --------------------- | -------- | ---------------------- | ------------------------------------ | ---------- |
| `backup-proxmox`      | /volume3 | Proxmox Backup Server  | 352c01d5-a826-463c-b910-6a3e649b3a07 | ✅ Created |
| `backups-lvm-proxmox` | /volume3 | LVM pool backups       | dd96864d-200e-4e72-8f0b-a984d0baf437 | ✅ Created |
| `backup`              | /volume3 | General backup storage | cf2744fa-fa63-43a0-bff5-167aeb0d2881 | ✅ Created |

**Note**: Share names use singular `backup` instead of plural `backups` (as created in DSM)

## Current Volume 3 Status

**Existing Shares** (preserve):

- `homes` - User home directories
- `Logs` - System and application logs
- `UNAS` - UNAS share

**Available Space**: ~7.4 TB (can expand as needed)

## Benefits of NAS01 for Backups

1. **Synology Backup Features**: Better integration with Synology backup tools
2. **Offsite Backup**: Easier to configure offsite backup to cloud services
3. **Snapshot Replication**: Synology snapshot features for backup protection
4. **Hyper Backup**: Native Synology backup solution support
5. **Volume 3 Capacity**: 15.7 TB total provides room for growth

## NFS Export Requirements

All backup shares should be configured with:

- **Hostname/IP**: `172.16.30.0/24`
- **Privilege**: Read/Write
- **Squash**: No mapping
- **Security**: sys
- **Enable asynchronous**: Yes

## Verification

✅ **All 3 backup shares created on Volume 3** (2025-12-04)

- `backup-proxmox` - For Proxmox Backup Server
- `backups-lvm-proxmox` - For LVM pool backups
- `backup` - For general backup storage

## Next Steps

1. ✅ **Shares Created** - All 3 backup shares created
2. [ ] **NFS Exports** - Configure NFS exports for each share
3. [ ] **Proxmox Configuration** - Update Proxmox Backup Server to use `backup-proxmox`
4. [ ] **Migration** - Move data from NAS02 `pve_Backups` if needed

## Migration Notes

- Move from NAS02 `pve_Backups` → NAS01 `backup-proxmox`
- Configure Proxmox Backup Server to use NAS01 instead of NAS02
- Update Proxmox storage configurations

> **Note**: NAS02 (UniFi UNAS Pro) documentation is in the `unifi` repository.
