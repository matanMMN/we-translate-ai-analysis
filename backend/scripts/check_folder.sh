#!/bin/bash

check_folder() {
    local required_folder="$1"
    local current_folder=$(basename "$PWD")

    # Strip any surrounding quotes from the required folder
    required_folder=$(echo "$required_folder" | sed 's/^"//;s/"$//')

    # Check if the current folder matches the required folder
    if [ "$current_folder" != "$required_folder" ]; then
        echo "Current folder: $current_folder"
        echo "This script must be run from the $required_folder folder."
        exit 1
    fi
}