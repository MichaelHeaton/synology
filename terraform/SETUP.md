# Synology Terraform Setup Guide

## Quick Start Checklist

### 1. Create HCP Terraform Cloud Workspace

1. Log in to [HashiCorp Cloud Platform](https://app.terraform.io)
2. Navigate to your organization
3. Click **"New Workspace"**
4. Choose **"CLI-Driven Workflow"** (not VCS-driven)
5. Name the workspace: `homelab-synology`
6. Click **"Create Workspace"**

### 2. Configure Workspace Variables (Recommended)

In your `homelab-synology` workspace:

1. Go to **Variables** tab
2. Add the following variables:
   - `synology_username` (mark as **sensitive**)
   - `synology_password` (mark as **sensitive**)

**Note**: You can also use `terraform.tfvars` locally, but workspace variables are more secure.

### 3. Local Configuration

1. **Copy the example file**:

   ```bash
   cd /Users/michaelheaton/Projects/HomeLab/synology/terraform
   cp terraform.tfvars.example terraform.tfvars
   ```

2. **Edit `terraform.tfvars`** with your values:

   ```hcl
   synology_url      = "https://nas01.specterrealm.com:5001"
   synology_username = "admin"
   synology_password = "your-password"
   synology_insecure = true
   nas_name          = "nas01"
   ```

   **Note**: HCP organization name is set in `main.tf` (currently "SpecterRealm").
   To use a different organization, either:

   - Edit `main.tf` and change the organization name, or
   - Set the `TF_CLOUD_ORGANIZATION` environment variable

### 4. Authenticate with HCP

```bash
terraform login
```

This will:

- Open your browser
- Authenticate with HCP
- Save credentials locally

### 5. Initialize Terraform

```bash
terraform init
```

This will:

- Download the Synology provider
- Connect to HCP Terraform Cloud
- Set up remote state backend

### 6. Verify Configuration

```bash
# Format code
terraform fmt

# Validate configuration
terraform validate
```

### 7. Test Connection (Optional)

You can test the connection by running a plan (even with no resources):

```bash
terraform plan
```

This should connect to HCP and show an empty plan (no resources defined yet).

## Next Steps

Once the basic setup is working:

1. **Import existing resources** (shared folders, NFS exports, etc.)
2. **Add resource definitions** in `resources/` directory
3. **Test with plan** before applying
4. **Apply changes** when ready

## Troubleshooting

### Authentication Issues

If `terraform login` fails:

- Make sure you're logged into HCP in your browser
- Check that you have access to the organization
- Try logging out and back in: `terraform logout` then `terraform login`

### Backend Connection Issues

If `terraform init` fails to connect:

- Verify the workspace name matches: `homelab-synology`
- Check that the organization name is correct
- Ensure you have workspace access permissions

### Provider Issues

If the Synology provider fails:

- Check that your Synology NAS is accessible
- Verify the URL, username, and password
- Check if `synology_insecure = true` is needed for self-signed certificates
- Ensure API access is enabled on your Synology NAS

## Workspace Configuration Summary

- **Workspace Name**: `homelab-synology`
- **Workflow Type**: CLI-Driven
- **Execution Mode**: Local (runs on your machine)
- **State Storage**: Remote (HCP Terraform Cloud)
- **Organization**: Set via variable or environment variable

## Reference

- Full documentation: [README.md](README.md)
- Terraform standards: [`../../specs-homelab/standards/terraform-standards.md`](../../specs-homelab/standards/terraform-standards.md)
- Share definitions: [`../../specs-homelab/storage/nas-share-layout.md`](../../specs-homelab/storage/nas-share-layout.md)
