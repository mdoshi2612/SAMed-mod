#!/bin/bash

# Source directory
source_dir="./effusion_masks"

# Destination directory
destination_dir="./cleaned_effusion_masks"

# Ensure destination directory exists
mkdir -p "$destination_dir"

# Iterate through each unique lung identifier
for lung_id in $(ls "$source_dir" | grep -Eo 'LUNG[0-9]+-[0-9]+' | sort -u); do
    # Find the latest reviewed file for the current lung identifier
    latest_reviewed_file=$(ls "$source_dir/$lung_id"_* | sort -V | tail -n 1)
    
    # Copy the latest reviewed file to the destination directory
    if [ -n "$latest_reviewed_file" ]; then
        cp "$latest_reviewed_file" "$destination_dir"
        echo "Copied: $latest_reviewed_file to $destination_dir"
    fi
done

echo "Copy operation complete."
