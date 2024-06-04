#!/bin/bash

# Docker Hub username
# DOCKER_REPO="piotrsicinski"
DOCKER_REPO="10.141.10.69:5000"

# Loop through each subdirectory
for dir in */ ; do
    # Check if the directory contains a Dockerfile
    if [ -f "$dir/Dockerfile" ]; then
        # Extract the subfolder name (remove trailing slash)
        SUBFOLDER_NAME=$(basename "$dir")
        # Convert the subfolder name to lowercase
        SUBFOLDER_NAME_LOWER=$(echo "$SUBFOLDER_NAME" | tr '[:upper:]' '[:lower:]')

        # Build the Docker image
        IMAGE_NAME="$DOCKER_REPO/$SUBFOLDER_NAME_LOWER"
        echo "Building Docker image $IMAGE_NAME from $dir"
        docker build -t "$IMAGE_NAME" "$dir"

        # Push the Docker image to Docker Hub
        echo "Pushing Docker image $IMAGE_NAME to Docker Hub"
        docker push "$IMAGE_NAME"
    else
        echo "No Dockerfile found in $dir, skipping..."
    fi
done
