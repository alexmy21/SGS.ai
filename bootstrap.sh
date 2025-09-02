#!/bin/bash

# SGS.ai Podman Compose bootstrap script
# Usage: bash <(curl -s https://raw.githubusercontent.com/alexmy21/SGS.ai/main/bootstrap.sh)

set -euo pipefail

# Configuration
COMPOSE_URL="https://raw.githubusercontent.com/alexmy21/SGS.ai/main/docker-compose.yml"
PROJECT_NAME="SGS.ai"

# Check for required commands
for cmd in podman podman-compose curl; do
    if ! command -v $cmd &> /dev/null; then
        echo "Error: $cmd is not installed"
        exit 1
    fi
done

# Cleanup existing containers
echo "Removing any existing containers..."
podman-compose -f <(curl -s "$COMPOSE_URL") down || true
podman rm -f $(podman ps -aq --filter "label=io.podman.compose.project=$PROJECT_NAME") 2>/dev/null || true

# Start new containers
echo "Starting containers..."
podman-compose -f <(curl -s "$COMPOSE_URL") up -d

echo ""
echo "SGS.ai setup complete!"
echo "Containers are running in detached mode."
echo "Use 'podman-compose -f <(curl -s $COMPOSE_URL) logs' to view logs"