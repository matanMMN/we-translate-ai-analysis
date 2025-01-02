#!/bin/bash

# Wait for RabbitMQ
until nc -z rabbitmq 5672; do
    echo "Waiting for RabbitMQ..."
    sleep 1
done

# Clear existing queues
celery -A meditranslate.celery purge -f

# Start Celery worker
exec celery -A meditranslate.celery worker \
    --loglevel=info \
    --pool=prefork \
    --concurrency=4 \
    --max-tasks-per-child=50 \
    --without-heartbeat