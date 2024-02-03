#!/bin/bash

# CT scans directory
ct_scans_dir="./ct_scans"

# Effusion masks directory
effusion_masks_dir="./effusion_masks"

# Iterate through CT scans
for ct_scan_file in "$ct_scans_dir"/*.nii; do
    # Extract the base filename without extension
    base_filename=$(basename "$ct_scan_file" .nii)
    
    # Construct the corresponding effusion mask filename
    effusion_mask_file="$effusion_masks_dir/${base_filename}_effusion.nii"
    
    # Check if the effusion mask file exists
    if [ ! -e "$effusion_mask_file" ]; then
        # Effusion mask does not exist, delete the CT scan file
        rm "$ct_scan_file"
        echo "Deleted: $ct_scan_file"
    fi
done

echo "Cleanup operation complete."
