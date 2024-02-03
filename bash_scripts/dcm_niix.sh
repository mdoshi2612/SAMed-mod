#!/bin/bash

# Specify the directory containing the folders
parent_directory="data/scan_data/manifest/NSCLC-Radiomics"

# Iterate through each folder in the specified directory
for folder_path in "$parent_directory"/*/; do
    # Check if the current item is a directory
    if [ -d "$folder_path" ]; then
        # Execute dcm2niix command on the current folder
        dcm2niix "$folder_path"
    fi
done
