#!/bin/bash

# sudo apt-get install -y yq

# source ./scripts/load_config.sh
# source ./scripts/check_folder.sh

# check_folder $BASE_FOLDER
# echo "Using Python version: $PYTHON_VERSION"
# echo "folder: $BASE_FOLDER"
docker compose -f ./docker-compose/docker-compose.base.yml -f ./docker-compose/docker-compose.testing.yml up --build --force-recreate  --remove-orphans
