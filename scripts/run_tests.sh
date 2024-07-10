#!/bin/bash

# Define the Docker Compose file
DOCKER_COMPOSE_FILE=compose.yaml

# Set the command to run pytest from the project root
export SERVER_COMMAND="pytest tests/ -v -s"

# Build and run the tests using Docker Compose
docker-compose -f $DOCKER_COMPOSE_FILE up --build --abort-on-container-exit

# Capture the exit code of the docker compose command
EXIT_CODE=$?

# Bring down the Docker Compose services
docker-compose -f $DOCKER_COMPOSE_FILE down

# Exit with the exit code from the tests
exit $EXIT_CODE
