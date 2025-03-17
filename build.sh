#!/bin/bash

# filepath: /home/alexmy/SGS/SGS.ai/build.sh

# Step 1: Navigate to the directory containing the Dockerfile for sgs.ai
cd /home/alexmy/SGS/SGS.ai || { echo "Directory /path/to/sgs.ai not found"; exit 1; }

# Step 2: Build the sgs.ai Docker image
echo "Building the sgs.ai Docker image..."
docker build -t alexmy/sgs.ai:latest . || { echo "Failed to build the sgs.ai image"; exit 1; }

# Step 3: Push the sgs.ai image to Docker Hub
echo "Pushing the sgs.ai image to Docker Hub..."
docker push alexmy/sgs.ai:latest || { echo "Failed to push the sgs.ai image"; exit 1; }

# Step 4: Navigate to the directory containing the docker-compose.yml file
cd /home/alexmy/SGS/SGS.ai || { echo "Directory /home/alexmy/SGS/SGS.ai not found"; exit 1; }

# Step 5: Bring down any running containers
echo "Stopping and removing existing containers..."
docker compose down || { echo "Failed to stop containers"; exit 1; }

# Step 6: Start all containers using docker-compose
echo "Starting all containers..."
docker compose up -d || { echo "Failed to start containers"; exit 1; }

# Step 7: Verify the status of running containers
echo "Verifying running containers..."
docker ps

echo "Build and deployment process completed successfully!"