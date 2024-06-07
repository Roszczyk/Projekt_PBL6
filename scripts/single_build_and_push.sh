#!/bin/bash

# Docker Hub username
# DOCKER_REPO="piotrsicinski"
DOCKER_REPO="piotrsicinski"

# Check if the path is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <path-to-folder>"
    exit 1
fi

# Set the target directory to the provided argument
TARGET_DIR="$1"

# Ensure the provided path is a directory
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: $TARGET_DIR is not a directory."
    exit 1
fi

# Check if the directory contains a Dockerfile
if [ -f "$TARGET_DIR/Dockerfile" ]; then
    # Extract the folder name (remove trailing slash if any)
    FOLDER_NAME=$(basename "$TARGET_DIR")
    # Convert the folder name to lowercase
    FOLDER_NAME_LOWER=$(echo "$FOLDER_NAME" | tr '[:upper:]' '[:lower:]')

    # Build the Docker image
    IMAGE_NAME="$DOCKER_REPO/$FOLDER_NAME_LOWER"
    echo "Building Docker image $IMAGE_NAME from $TARGET_DIR"
    docker build -t "$IMAGE_NAME" "$TARGET_DIR"

    # Push the Docker image to Docker Hub
    echo "Pushing Docker image $IMAGE_NAME to Docker Hub"
    docker push "$IMAGE_NAME"
else
    echo "No Dockerfile found in $TARGET_DIR, skipping..."
fi
