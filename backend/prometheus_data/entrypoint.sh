#!/bin/sh
echo "APP_CONTAINER_NAME: $APP_CONTAINER_NAME"
echo "APP_PORT: $APP_PORT"

# envsubst < /etc/prometheus/prometheus.yml > /prometheus.yml && mv /prometheus.yml /etc/prometheus/prometheus.yml

exec prometheus --config.file=/etc/prometheus/prometheus.yml --web.enable-remote-write-receiver --enable-feature=native-histograms


