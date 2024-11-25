#!/bin/bash

BASE_BACKEND_IMAGE=base-backend-image:latest
BASE_IMAGE=python:3.11-slim

docker build --build-arg BASE_IMAGE=${BASE_IMAGE} -t ${BASE_BACKEND_IMAGE} .