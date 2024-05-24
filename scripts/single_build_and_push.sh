#!/bin/bash

# Docker Hub username
DOCKER_USERNAME="piotrsicinski"

# Check if the path is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <path-to-folder>"
    exit 1
fi

# Set the base directory to the provided argument
BASE_DIR="$1"

# Ensure the provided path is a directory
if [ ! -d "$BASE_DIR" ]; then
    echo "Error: $BASE_DIR is not a directory."
    exit 1
fi

# Loop through each subdirectory in the provided base directory
for dir in "$BASE_DIR"/*/ ; do
    # Check if the directory contains a Dockerfile
    if [ -f "$dir/Dockerfile" ]; then
        # Extract the subfolder name (remove trailing slash)
        SUBFOLDER_NAME=$(basename "$dir")
        # Convert the subfolder name to lowercase
        SUBFOLDER_NAME_LOWER=$(echo "$SUBFOLDER_NAME" | tr '[:upper:]' '[:lower:]')

        # Build the Docker image
        IMAGE_NAME="$DOCKER_USERNAME/$SUBFOLDER_NAME_LOWER"
        echo "Building Docker image $IMAGE_NAME from $dir"
        docker build -t "$IMAGE_NAME" "$dir"

        # Push the Docker image to Docker Hub
        echo "Pushing Docker image $IMAGE_NAME to Docker Hub"
        docker push "$IMAGE_NAME"
    else
        echo "No Dockerfile found in $dir, skipping..."
    fi
done
