#!/bin/bash

poetry install --with test --no-root
poetry run python -m unittest discover tests
