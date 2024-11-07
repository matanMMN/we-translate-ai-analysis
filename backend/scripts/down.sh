docker compose -f ./docker-compose/docker-compose.base.yml -f ./docker-compose/docker-compose.dev.yml --env-file ./environments/.env.development down -v
