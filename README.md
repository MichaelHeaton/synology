# Synology NAS Management

This repository contains tools and documentation for managing Synology NAS devices (NAS01) in the HomeLab infrastructure.

## Overview

This repository provides:

- **Python API scripts** for managing Synology DSM via API
- **Terraform configurations** for Infrastructure as Code (IaC) management
- **Documentation** for share layouts, NFS configurations, and current state
- **Share management** for NAS01 (Synology DS1621+)

## Repository Structure

```
synology/
├── README.md                    # This file
├── LICENSE                      # License file
├── python/                      # Python API scripts
│   ├── synology_api.py         # Main Synology DSM API client
│   └── requirements.txt        # Python dependencies
├── terraform/                   # Terraform configurations
│   ├── main.tf                 # Main Terraform configuration
│   ├── variables.tf            # Variable definitions
│   ├── outputs.tf              # Output definitions
│   ├── resources/              # Resource definitions
│   ├── data/                   # Data source definitions
│   └── README.md               # Terraform-specific documentation
└── Documentation files:
    ├── SHARES_CREATION_SUMMARY.md    # Summary of all created shares
    ├── SHARES_VERIFICATION.md       # NAS01 shares verification
    ├── NAS01_BACKUP_SHARES.md       # NAS01 backup shares documentation
    └── CLEANUP_SUMMARY.md           # Repository cleanup summary
```

## Quick Start

### Python API Scripts

The Python API scripts provide direct interaction with Synology DSM API for managing shared folders.

#### Prerequisites

```bash
# Install Python dependencies
cd python
pip3 install -r requirements.txt
```

#### Configuration

Create a `.env` file in the repository root:

```bash
SYNOLOGY_URL=https://172.16.15.5:5001
SYNOLOGY_USER=your-username
SYNOLOGY_PASS=your-password
SYNOLOGY_VERIFY_SSL=false
```

#### Usage

```bash
# List all shared folders
python3 python/synology_api.py list

# Get details of a specific share
python3 python/synology_api.py get <share-name>

# Create a new shared folder
python3 python/synology_api.py create <share-name> --volume /volume1 --description "Description"
```

#### Features

- ✅ Authentication with session management
- ✅ List all shared folders with details
- ✅ Get specific share information
- ✅ Create new shared folders
- ✅ JSON export of current state
- ✅ Error handling and detailed output

### Terraform

See `terraform/README.md` for detailed Terraform setup and usage instructions.

## Current State

### NAS01 (Synology DS1621+)

**High IOPS Shares (Volume 1)** - 5 shares:

- `lxcs-iops` (1 TB) - High IOPS LXC container storage
- `dockers-iops` (2 TB) - High IOPS Docker storage
- `vmdks-iops` (5 TB) - High IOPS VM disk images
- `kubernetes-iops` (2 TB) - High IOPS Kubernetes storage
- `ai` (5 TB) - AI stack storage

**Backup Shares (Volume 3)** - 3 shares:

- `backup-proxmox` - Proxmox Backup Server
- `backups-lvm-proxmox` - LVM pool backups
- `backup` - General backup storage

**Total**: 8 new shares created (plus 6 existing shares preserved)

> **Note**: NAS02 (UniFi UNAS Pro) documentation has been moved to the `unifi` repository.

See `SHARES_CREATION_SUMMARY.md` for complete details.

## Synology DSM API Reference

### synology-dsm-api Repository

When working with Synology DSM APIs, we reference the **synology-dsm-api** repository for API documentation and examples:

**Repository**: [pmilano1/synology-dsm-api](https://github.com/pmilano1/synology-dsm-api)

#### Why This Repository?

The `synology-dsm-api` repository provides:

- Comprehensive API documentation for Synology DSM
- Example code for various API endpoints
- Parameter documentation for API calls
- Error code references

#### Key API Endpoints Used

**SYNO.Core.Share** - Shared Folder Management:

- `list` - List all shared folders
- `get` - Get details of a specific share
- `create` - Create a new shared folder
- `delete` - Delete a shared folder (use with caution)

**SYNO.Core.Auth** - Authentication:

- `login` - Authenticate and get session ID
- `logout` - End session

#### Important Notes

1. **API Version**: Most APIs use version 1, but check the repository for specific version requirements
2. **Session Management**: Always login before making API calls, logout when done
3. **HTTP Methods**:
   - `GET` for read operations (list, get)
   - `POST` for write operations (create, delete)
4. **Parameters**:
   - Use `desc` (not `description`) for share descriptions
   - Use `vol_path` (e.g., `/volume1`) for volume specification
5. **Error Codes**:
   - `101` - Invalid credentials
   - `103` - Permission denied
   - `402` - Unknown error (often related to 2FA/MFA)
   - `403` - Permission denied or 2FA required

#### When to Reference

Refer to the `synology-dsm-api` repository when:

- Adding new API functionality
- Troubleshooting API errors
- Understanding parameter requirements
- Finding API endpoint documentation
- Learning about new DSM API features

#### Example Usage

```python
# Based on synology-dsm-api documentation
from synology_api import SynologyAPI

api = SynologyAPI(url, username, password)
api.login()

# Create share (using POST method and 'desc' parameter)
response = api._request(
    api='SYNO.Core.Share',
    method='create',
    version=1,
    params={
        'name': 'new-share',
        'vol_path': '/volume1',
        'desc': 'Share description'  # Note: 'desc', not 'description'
    },
    http_method='POST'
)
```

## Documentation

### Share Documentation

- **`SHARES_CREATION_SUMMARY.md`** - Complete summary of NAS01 created shares
- **`SHARES_VERIFICATION.md`** - NAS01 shares verification details
- **`NAS01_BACKUP_SHARES.md`** - NAS01 backup shares documentation

> **Note**: NAS02 (UniFi UNAS Pro) documentation is in the `unifi` repository.

### Infrastructure Documentation

For complete infrastructure documentation, see:

- **`specs-homelab/storage/nas-share-layout.md`** - Authoritative share layout design
- **`specs-homelab/storage/synology-structure.md`** - Synology structure details
- **`specs-homelab/reference/common-values.md`** - IP addresses and DNS names

## Network Configuration

### NAS01 (Synology DS1621+)

- **Management IP**: `172.16.15.5` (VLAN 15)
- **Storage IP**: `172.16.30.5` (VLAN 30)
- **Family IP**: `172.16.5.5` (VLAN 5)
- **Production IP**: `172.16.10.5` (VLAN 10)
- **DSM URL**: `https://172.16.15.5:5001`

> **Note**: NAS02 (UniFi UNAS Pro) network configuration is documented in the `unifi` repository.

## Next Steps

1. ✅ **Shares Created** - All 8 NAS01 shares created
2. [ ] **NFS Exports** - Configure NFS exports for NAS01 shares
3. [ ] **Proxmox Configuration** - Update Proxmox to use new share names
4. [ ] **Data Migration** - Migrate data from old shares to new shares (if applicable)

## Troubleshooting

### Python API Issues

**Authentication Errors (101, 402, 403)**:

- Verify username and password
- Check if 2FA/MFA is enabled (may require app-specific password)
- Ensure user has administrative privileges
- Verify user is in the `administrators` group

**Permission Errors (403)**:

- Creating shares requires user to be in `administrators` group
- Check application privileges in DSM
- Verify session type is `Core` for administrative operations

**SSL Certificate Errors**:

- Set `SYNOLOGY_VERIFY_SSL=false` for self-signed certificates
- Or add certificate to system trust store

### Common Issues

**Shares not appearing in Terraform**:

- `synology_api` resources may not show in plan (expected behavior)
- Use Python API scripts for direct management
- Terraform provider has limitations with shared folder management

**NFS Mount Issues**:

- Verify NFS exports are configured correctly
- Check network connectivity (VLAN 30)
- Verify IP addresses in NFS export configuration
- Check firewall rules

## Contributing

When making changes:

1. Update relevant documentation files
2. Test Python API scripts before committing
3. Update `SHARES_CREATION_SUMMARY.md` if creating new shares
4. Document any new API endpoints or parameters used
5. Reference `synology-dsm-api` repository for API documentation

## License

See `LICENSE` file for license information.

## References

- **Synology DSM API**: [pmilano1/synology-dsm-api](https://github.com/pmilano1/synology-dsm-api)
- **Terraform Provider**: [synology-community/terraform-provider-synology](https://github.com/synology-community/terraform-provider-synology)
- **Synology DSM API Guide**: [Official Synology API Documentation](https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/FileStation/All/enu/Synology_File_Station_API_Guide.pdf)
- **HomeLab Specs**: `specs-homelab/` repository
