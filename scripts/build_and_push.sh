#!/bin/bash

# Docker Hub username
DOCKER_USERNAME="piotrsicinski"

# Loop through each subdirectory
for dir in */ ; do
    # Check if the directory contains a Dockerfile
    if [ -f "$dir/Dockerfile" ]; then
        # Extract the subfolder name (remove trailing slash)
        SUBFOLDER_NAME=$(basename "$dir")

        # Build the Docker image
        IMAGE_NAME="$DOCKER_USERNAME/$SUBFOLDER_NAME"
        echo "Building Docker image $IMAGE_NAME from $dir"
        docker build -t "$IMAGE_NAME" "$dir"

        # Push the Docker image to Docker Hub
        echo "Pushing Docker image $IMAGE_NAME to Docker Hub"
        docker push "$IMAGE_NAME"
    else
        echo "No Dockerfile found in $dir, skipping..."
    fi
done
