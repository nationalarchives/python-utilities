#!/bin/bash

# TODO: Change ruff version back to preview once the Docker image has been released
docker run --rm -v "$(pwd)":/app/ ghcr.io/nationalarchives/tna-python-dev:ruff format
