#!/bin/bash

poetry install --with test
poetry run python -m unittest discover tests
