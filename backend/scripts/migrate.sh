#!/bin/bash

echo "Running Alembic migrations..."

alembic upgrade head

echo "Migrations complete."
