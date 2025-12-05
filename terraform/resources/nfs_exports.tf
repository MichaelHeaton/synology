# Synology NFS Exports
#
# This file will contain NFS export resources once we start importing/managing them.
#
# Example resource (commented out until ready):
#
# resource "synology_nfs_export" "dockers_iops" {
#   shared_folder = synology_shared_folder.dockers_iops.name
#   network       = "172.16.30.0/24"  # Storage VLAN
#   permission    = "rw"
#   sync          = true
# }
#
# See ../specs-homelab/storage/nas-share-layout.md for NFS export requirements

