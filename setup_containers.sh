#!/bin/bash

# Set the shared volume name and host path
VOLUME_NAME="the_collective"
HOST_PATH="/mnt/s/the_collective"  # WSL/Linux path for S:/the_collective

# Function to print messages in bold
print_bold() {
  echo -e "\e[1m$1\e[0m"
}

# Function to handle errors and exit
handle_error() {
  echo "Error on line $1"
  exit 1
}

# Set trap to catch errors and call the handle_error function
trap 'handle_error $LINENO' ERR

print_bold "Starting the Open WebUI and Pipelines setup script..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
  echo "Docker is not installed. Please install Docker and try again."
  exit 1
fi

# Ensure the host path exists
if [ ! -d "$HOST_PATH" ]; then
  echo "Host path $HOST_PATH does not exist. Creating it now..."
  mkdir -p "$HOST_PATH" || { echo "Failed to create host path $HOST_PATH."; exit 1; }
else
  echo "Host path $HOST_PATH exists."
fi

# Stop and remove any existing containers if they are running
print_bold "Stopping and removing existing containers..."
docker stop pipelines open-webui 2>/dev/null || true
docker rm pipelines open-webui 2>/dev/null || true

# Check if the volume already exists
print_bold "Checking if the volume $VOLUME_NAME already exists..."
VOLUME_EXISTS=$(docker volume ls -q -f name=$VOLUME_NAME)

# Create the shared volume only if it does not exist
if [ -z "$VOLUME_EXISTS" ]; then
  print_bold "Creating a new shared volume: $VOLUME_NAME"
  docker volume create --driver local \
    --opt type=none \
    --opt device=$HOST_PATH \
    --opt o=bind \
    $VOLUME_NAME
else
  echo "Volume $VOLUME_NAME already exists. Skipping volume creation."
fi

# Pull the latest Docker images with error handling
print_bold "Pulling the latest images for Pipelines and Open WebUI..."
docker pull ghcr.io/open-webui/pipelines:main || { echo "Failed to pull Pipelines image."; exit 1; }
docker pull ghcr.io/open-webui/open-webui:main || { echo "Failed to pull Open WebUI image."; exit 1; }

# Run the Pipelines Container using the Shared `the_collective` Volume
print_bold "Starting the Pipelines container..."
docker run -d \
  --name pipelines \
  -p 9099:9099 \
  --network=bridge \
  --restart always \
  -e ENV=prod \
  -e HOST=0.0.0.0 \
  -e PORT=9099 \
  -e RESET_PIPELINES_DIR=true \
  --add-host=host.docker.internal:host-gateway \
  -v $VOLUME_NAME:/app/pipelines \
  -v $VOLUME_NAME:/app/backend/data \
  ghcr.io/open-webui/pipelines:main || { echo "Failed to start Pipelines container."; exit 1; }

# Check if Pipelines container is running
if [ "$(docker inspect -f '{{.State.Running}}' pipelines)" != "true" ]; then
  echo "Pipelines container failed to start. Check the logs with 'docker logs pipelines'."
  exit 1
fi

# Run the Open WebUI Container using the Shared `the_collective` Volume
print_bold "Starting the Open WebUI container..."
docker run -d \
  --name open-webui \
  -p 3000:8080 \
  --network=bridge \
  --restart always \
  -e PIPELINES_HOST=host.docker.internal \
  -e PIPELINES_PORT=9099 \
  --add-host=host.docker.internal:host-gateway \
  -v $VOLUME_NAME:/app/pipelines \
  -v $VOLUME_NAME:/app/backend/data \
  ghcr.io/open-webui/open-webui:main || { echo "Failed to start Open WebUI container."; exit 1; }

# Check if Open WebUI container is running
if [ "$(docker inspect -f '{{.State.Running}}' open-webui)" != "true" ]; then
  echo "Open WebUI container failed to start. Check the logs with 'docker logs open-webui'."
  exit 1
fi

print_bold "Setup completed successfully!"
echo "Open WebUI is available at http://localhost:3000"
echo "Pipelines API is available at http://localhost:9099"
