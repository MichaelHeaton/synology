# NAS01 Shares Verification

**Date**: 2025-12-04
**Verified via**: Python API script (`python/synology_api.py`)

## ✅ All Required Shares Created

### Volume 1 (High IOPS - SSD Cache)

| Share Name        | Volume   | Description                     | UUID                                 | Quota (from UI) | Status     |
| ----------------- | -------- | ------------------------------- | ------------------------------------ | --------------- | ---------- |
| `lxcs-iops`       | /volume1 | High IOPS LXC container storage | 40a2c825-63c3-4cf5-9246-4414903c2c08 | 1 TB            | ✅ Created |
| `dockers-iops`    | /volume1 | High IOPS Docker storage        | b333f659-c443-4df9-a084-2c3b04bdb9b8 | 2 TB            | ✅ Created |
| `vmdks-iops`      | /volume1 | High IOPS VM disk images        | a866bb13-1566-40be-ad36-4cf2c98ee628 | 5 TB            | ✅ Created |
| `kubernetes-iops` | /volume1 | High IOPS Kubernetes storage    | 9a1c3337-8bab-4392-8ceb-08d7473f96b8 | 2 TB            | ✅ Created |
| `ai`              | /volume1 | AI stack storage                | 52db665f-e65d-402e-9af2-c39a90cb5a8c | 5 TB            | ✅ Created |

**Total Quota Allocated**: 15 TB (within recommended 7-16 TB range)

### Existing Shares (Preserved)

**Volume 1:**

- `docker` - Existing Docker share
- `web` - System default shared folder
- `web_packages` - Web packages

**Volume 3:**

- `homes` - User home directories
- `Logs` - System and application logs
- `UNAS` - UNAS share

## Verification Checklist

- ✅ All 5 planned shares created
- ✅ All shares on Volume 1 (correct volume for high IOPS)
- ✅ Descriptions match requirements
- ✅ Quotas set appropriately:
  - `lxcs-iops`: 1 TB (within 500 GB - 1 TB range)
  - `dockers-iops`: 2 TB (within 1-2 TB range)
  - `vmdks-iops`: 5 TB (within 2-5 TB range)
  - `kubernetes-iops`: 2 TB (within 1-2 TB range)
  - `ai`: 5 TB (within 2-5 TB range)
- ✅ Existing shares preserved (no changes)
- ✅ **Network Access Verified** - Shares accessible from local machine (2025-12-04)

## Next Steps

1. ✅ **Shares Created** - All 5 high IOPS shares created manually
2. ✅ **Network Access Verified** - Shares accessible from local machine
3. [ ] **NFS Exports** - Configure NFS exports for each share (for Proxmox/K8s access)
4. [ ] **Proxmox Integration** - Test mounting shares in Proxmox as NFS storage
5. [ ] **Permissions** - Configure NFS permissions for Proxmox clusters
6. [ ] **Documentation** - Document NFS mount points and configurations

## NFS Export Requirements

Based on `specs-homelab/storage/nas-share-layout.md`:

- `/lxcs-iops` → NFS for Proxmox Cluster 1 (Content: Container)
- `/dockers-iops` → NFS for Docker Swarm 1
- `/vmdks-iops` → NFS for Proxmox Cluster 1 (Content: Disk image)
- `/kubernetes-iops` → NFS for Kubernetes Cluster 1
- `/ai` → NFS for AI stack services

All shares should be configured as read-write NFS exports.
