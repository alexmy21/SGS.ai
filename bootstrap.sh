#!/bin/bash

# Stop and remove existing containers (if any)
echo "Stopping and removing existing containers..."
docker compose down

# Build and start the containers
echo "Building and starting containers..."
docker compose up -d

# Print status
echo "Containers are up and running!"
echo "Redis: localhost:6379"
echo "HDF5 API: http://localhost:5000"
echo "SGS Core: http://localhost:8888"