#!/bin/bash

# source does not persist, bash run in subshell , so activate venv in terminal.

# Configuration
PYTHON=python3.11
VENV_DIR="venv"
# FOLDER="backend"
REQUIREMENTS_FOLDER="./requirements"
REQUIREMENTS_FILE="./.requirements/requirements.base.txt"
EXPORT_PYTHON_PATH=$(pwd)/..:$(pwd)
SLEEP_AFTER_VENV=5


# # Ensure the script is run from the backend folder
# if [ "$(basename "$PWD")" != $FOLDER ]; then
#     echo "This script must be run from the $FOLDER folder."
#     exit 1
# fi

# Check if Python 3.11 is installed, if not install it
if ! command -v $PYTHON &> /dev/null; then
    echo "$PYTHON not found, installing..."
    sudo apt update
    sudo apt install -y software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install -y $PYTHON
    sudo apt-get install -y $PYTHON-venv
    echo "$PYTHON installed successfully."
else
    echo "$PYTHON is already installed."
fi

# Check if virtual environment exists, if not create it
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON -m venv $VENV_DIR || { echo "Failed to create virtual environment"; exit 1; }
    echo "Virtual environment created. sleeping $SLEEP_AFTER_VENV"
    sleep $SLEEP_AFTER_VENV
else
    echo "Virtual environment already exists."
    # exit 1
fi


if source $VENV_DIR/bin/activate; then
    echo "Virtual environment activated."

    # Check if requirements folder exists and contains .txt files
    if [ -d "$REQUIREMENTS_FOLDER" ] && [ "$(ls $REQUIREMENTS_FOLDER/*.txt 2>/dev/null)" ]; then
        # Loop through all .txt files in the requirements folder
        for req_file in $REQUIREMENTS_FOLDER/*.txt; do
            echo "Installing requirements from $req_file..."
            pip install -r "$req_file" || { echo "Failed to install requirements from $req_file"; exit 1; }
        done
    else
        echo "No requirements files found in folder: $REQUIREMENTS_FOLDER"
        exit 1
    fi

    export PYTHONPATH=$PYTHONPATH:$EXPORT_PYTHON_PATH
    echo "PYTHONPATH is set to: $PYTHONPATH"
else
    echo "Failed to activate virtual environment."
    exit 1
fi
