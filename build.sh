#!/bin/bash

# Get the current working directory
CURRENT_DIR=$(pwd)

# Step 1: Navigate to the directory containing the Dockerfile for sgs.ai
cd "$CURRENT_DIR" || { echo "Directory $CURRENT_DIR not found"; exit 1; }

# Step 2: Build the sgs.ai Podman image
echo "Building the sgs.ai Podman image..."
podman build -t alexmy/sgs.ai:latest . || { echo "Failed to build the sgs.ai image"; exit 1; }

# Step 3: Push the sgs.ai image to a container registry
echo "Pushing the sgs.ai image to a container registry..."
podman push alexmy/sgs.ai:latest || { echo "Failed to push the sgs.ai image"; exit 1; }

# # Step 4: Navigate to the directory containing the docker-compose.yml file
# cd "$CURRENT_DIR" || { echo "Directory $CURRENT_DIR not found"; exit 1; }

# # Step 5: Stop and remove existing containers
# echo "Stopping and removing existing containers..."
# podman-compose down || { echo "Failed to stop containers"; exit 1; }

# # Step 6: Start all containers using podman-compose
# echo "Starting all containers..."
# podman-compose up -d || { echo "Failed to start containers"; exit 1; }

# # Step 7: Verify the status of running containers
# echo "Verifying running containers..."
# podman ps

echo "Build and deployment process completed successfully!"