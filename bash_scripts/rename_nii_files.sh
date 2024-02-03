#!/bin/bash

# Source directory
source_dir="./cleaned_effusion_masks"

# Move to the source directory
cd "$source_dir" || exit

# Rename every .nii file in the directory
for file in *.nii; do
    if [ -e "$file" ]; then
        new_name=$(echo "$file" | cut -c 1-18)
        mv "$file" "$new_name.nii"
        echo "Renamed: $file to $new_name.nii"
    fi
done

echo "Rename operation complete."
