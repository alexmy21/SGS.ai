#!/bin/bash

# Define container images
SGS_CORE_IMAGE="alpine:latest"  # Dummy image for SGS.core
REDIS_IMAGE="redis:latest"      # Official Redis image
HDF5_IMAGE="hdfgroup/hdf5:latest"  # Official HDF5 image

# Create the Pod
POD_NAME="sgs-pod"
podman pod create --name $POD_NAME -p 6379:6379 -p 8888:8888

# Start the Redis container
podman run -d --pod $POD_NAME --name redis-container $REDIS_IMAGE

# Start the HDF5 container
podman run -d --pod $POD_NAME --name hdf5-container $HDF5_IMAGE

# Start the SGS.core container (dummy for now)
podman run -d --pod $POD_NAME --name sgs-core-container $SGS_CORE_IMAGE

# Print Pod status
echo "Pod and containers created successfully!"
podman pod ps
podman ps --all