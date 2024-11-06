#!/bin/bash

# Function to load configuration from YAML
load_config() {
    local config_file="$1"
    
    # Check if yq is installed
    if ! command -v yq &> /dev/null; then
        echo "yq is not installed. Please install it first."
        exit 1
    fi
    
    # Check if the config file exists
    if [ ! -f "$config_file" ]; then
        echo "Config file $config_file not found!"
        exit 1
    fi
    
    # Read and export configuration values
    export PYTHON_VERSION=$(yq '.python_version' "$config_file")
    export BASE_FOLDER=$(yq '.base_folder' "$config_file")
    export APP_NAME=$(yq '.app_name' "$config_file")
    

    # Optionally, add more configurations as needed
}

# Call the function with the path to your config.yaml
load_config "config.yaml"
