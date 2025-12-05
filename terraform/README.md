# Synology Terraform Infrastructure

This directory contains Terraform configurations for managing the Synology NAS infrastructure.

## Structure

```
terraform/
├── main.tf                    # Main configuration
├── variables.tf              # Variable definitions
├── outputs.tf                # Output definitions
├── terraform.tfvars.example  # Example variable values
├── resources/                # Resource definitions (to be created)
│   ├── shared_folders.tf
│   ├── nfs_exports.tf
│   └── smb_shares.tf
├── modules/                  # Reusable Terraform modules (to be created)
└── README.md                # This file
```

## Getting Started

### Prerequisites

1. **HCP Terraform Cloud Account**: You need a HashiCorp Cloud Platform account with a Terraform Cloud organization
2. **Workspace Created**: Create a workspace named `homelab-synology` in HCP Terraform with CLI-driven workflow
3. **Synology API Access**: Ensure your Synology NAS has API access enabled

### Initial Setup

1. **Copy the example variables file**:

   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

2. **Fill in your values** in `terraform.tfvars`:

   - `synology_url`: Your Synology DSM URL (e.g., `https://nas01.specterrealm.com:5001`)
   - `synology_username`: Your Synology username
   - `synology_password`: Your Synology password
   - `synology_insecure`: Set to `true` if using self-signed certificate, `false` otherwise

   **Note**: HCP organization name is set in `main.tf` (currently "SpecterRealm") and can be overridden via `TF_CLOUD_ORGANIZATION` environment variable.

3. **Set workspace variables in HCP** (recommended for sensitive values):

   - Navigate to your `homelab-synology` workspace in HCP Terraform
   - Go to Variables
   - Add the following variables:
     - `synology_username` (mark as sensitive)
     - `synology_password` (mark as sensitive)

4. **Authenticate with HCP**:

   ```bash
   terraform login
   ```

   This will open a browser to authenticate and generate an API token.

5. **Initialize Terraform**:

   ```bash
   terraform init
   ```

   This will:

   - Download the Synology provider
   - Connect to HCP Terraform Cloud backend
   - Configure remote state storage

6. **Validate configuration**:

   ```bash
   terraform fmt
   terraform validate
   ```

7. **Plan changes**:

   ```bash
   terraform plan -out tfplan
   ```

8. **Apply changes** (when ready):
   ```bash
   terraform apply tfplan
   ```

## Workflow

### Always Run

1. **Terraform fmt**: Format code

   ```bash
   terraform fmt
   ```

2. **Terraform validate**: Validate configuration

   ```bash
   terraform validate
   ```

3. **Terraform plan**: Create execution plan
   ```bash
   terraform plan -out tfplan
   ```

### Never Run

- **terraform apply**: Never run without a plan file
  ```bash
  # Always use:
  terraform apply tfplan
  ```

## State Management

### Remote State

- **Backend**: HashiCorp Cloud Platform (Terraform Cloud)
- **Location**: Remote state stored in HCP
- **Encryption**: At rest and in transit (managed by HashiCorp)
- **Locking**: Automatic state locking (managed by Terraform Cloud)
- **Versioning**: Automatic state versioning (managed by Terraform Cloud)
- **Workflow**: CLI-driven (manual runs via `terraform apply`)

### State File Security

- **Never Commit**: State files to Git
- **Backup**: Automatic backups managed by HCP
- **Access**: Restricted to workspace access

## Resources to Manage

### Planned Resources

- **Shared Folders**: NFS and SMB shared folders
- **NFS Exports**: NFS export configuration
- **SMB Shares**: SMB share configuration
- **Users**: User management (if supported by provider)
- **Groups**: Group management (if supported by provider)

### Current State

See `../specs-homelab/storage/nas-share-layout.md` for complete share inventory and desired state.

## Importing Existing Resources

To import existing Synology resources into Terraform:

1. **Identify the resource** in your Synology DSM
2. **Add the resource** to your Terraform configuration
3. **Import the resource**:
   ```bash
   terraform import synology_shared_folder.example_folder example-folder-name
   ```
4. **Verify the import**:
   ```bash
   terraform plan
   ```
   Should show no changes if import was successful

## Provider Documentation

- **Synology Provider**: [synology-community/terraform-provider-synology](https://github.com/synology-community/terraform-provider-synology)
- **Provider Resources**: Check provider documentation for available resources

## Notes

- State is stored remotely in HCP Terraform Cloud
- All runs are executed locally (CLI-driven workflow)
- Sensitive variables should be set in HCP workspace variables, not in tfvars files
- Follow Terraform standards in `../specs-homelab/standards/terraform-standards.md`
- Share definitions are documented in `../specs-homelab/storage/nas-share-layout.md`
