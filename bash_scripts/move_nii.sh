#!/bin/bash

# Source directory
source_dir="data/Effusions"

# Destination directory
destination_dir="./effusion_masks"

# Ensure destination directory exists
mkdir -p "$destination_dir"

# Find .nii files in the source directory and its subdirectories
find "$source_dir" -type f -name "*.nii" -exec cp {} "$destination_dir" \;

echo "Copy operation complete."
