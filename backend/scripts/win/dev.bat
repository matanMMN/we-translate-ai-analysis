#!/bin/bash

docker compose -f ./docker-compose/docker-compose.base.yml -f ./docker-compose/docker-compose.dev.yml --env-file ./environments/.env.development up --build --force-recreate  --remove-orphans

# docker compose -f ./docker-compose/docker-compose.base.yml -f ./docker-compose/docker-compose.dev.yml --env-file ./environments/.env.development restart backend


# docker compose -f ./docker-compose/docker-compose.base.yml -f ./docker-compose/docker-compose.dev.yml --env-file ./environments/.env.development down -v

