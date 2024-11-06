#!/bin/bash

# down --volumes
docker compose -f ./docker-compose/docker-compose.base.yml -f ./docker-compose/docker-compose.debug.yml up --build --force-recreate  --remove-orphans
