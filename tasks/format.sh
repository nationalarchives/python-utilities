#!/bin/bash

docker run --rm -v "$(pwd)":/app/ ghcr.io/nationalarchives/tna-python-dev:latest format
npx prettier --write .
