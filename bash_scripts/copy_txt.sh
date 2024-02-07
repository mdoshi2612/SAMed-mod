#!/bin/bash

source_file="../Pleural-Effusion/lists/test.txt"
target_directory="/home/manav/SAMed-mod/Pleural-Effusion/lists"

for folder in "$target_directory"/*/; do
    cp "$source_file" "$folder"
    echo "File copied to $target_path"
done
