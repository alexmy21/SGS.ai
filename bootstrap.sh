#!/bin/bash

# Define container images
SGS_CORE_IMAGE="alpine:latest"  # Dummy image for SGS.core
REDIS_IMAGE="redis:latest"      # Official Redis image
HDF5_IMAGE="hdfgroup/hdf5:latest"  # Official HDF5 image (from Docker Hub)

# Generate a unique installation ID using the latest GitHub commit SHA
INSTALLATION_ID=$(curl -fsSL https://api.github.com/repos/alexmy21/SGS.ai/commits/main | grep -oP '"sha": "\K[0-9a-f]+' | head -n 1)
if [ -z "$INSTALLATION_ID" ]; then
    echo "Failed to fetch GitHub commit ID. Using timestamp as fallback."
    INSTALLATION_ID=$(date +%s)
fi

# Define Pod and container names with unique installation ID
POD_NAME="sgs-pod-$INSTALLATION_ID"
SGS_CORE_CONTAINER="sgs-core-container-$INSTALLATION_ID"
REDIS_CONTAINER="redis-container-$INSTALLATION_ID"
HDF5_CONTAINER="hdf5-container-$INSTALLATION_ID"

# Stop and remove existing containers (if any)
echo "Stopping and removing existing containers..."
podman stop $SGS_CORE_CONTAINER $REDIS_CONTAINER $HDF5_CONTAINER 2>/dev/null
podman rm $SGS_CORE_CONTAINER $REDIS_CONTAINER $HDF5_CONTAINER 2>/dev/null

# Remove the existing Pod (if any)
echo "Removing existing Pod..."
podman pod rm -f $POD_NAME 2>/dev/null

# Check if port 6379 is in use
if lsof -i :6379 >/dev/null 2>&1; then
    echo "Port 6379 is already in use. It seems Redis is running locally."
    echo "You can either:"
    echo "1. Stop the local Redis server and let the script start a containerized Redis."
    echo "2. Use a different port for the containerized Redis."
    read -p "Enter your choice (1 or 2): " choice

    case $choice in
        1)
            echo "Stopping local Redis server..."
            sudo systemctl stop redis
            ;;
        2)
            read -p "Enter a new port for Redis (e.g., 6380): " REDIS_PORT
            ;;
        *)
            echo "Invalid choice. Exiting."
            exit 1
            ;;
    esac
else
    REDIS_PORT=6379  # Default Redis port
fi

# Create the Pod
echo "Creating Pod $POD_NAME..."
podman pod create --name $POD_NAME -p $REDIS_PORT:6379 -p 8888:8888

# Start the Redis container
echo "Starting Redis container on port $REDIS_PORT..."
podman run -d --pod $POD_NAME --name $REDIS_CONTAINER $REDIS_IMAGE

# Start the HDF5 container
echo "Starting HDF5 container..."
podman run -d --pod $POD_NAME --name $HDF5_CONTAINER $HDF5_IMAGE

# Start the SGS.core container (dummy for now)
echo "Starting SGS.core container..."
podman run -d --pod $POD_NAME --name $SGS_CORE_CONTAINER $SGS_CORE_IMAGE

# Print Pod status
echo "Pod and containers created successfully!"
podman pod ps
podman ps --all