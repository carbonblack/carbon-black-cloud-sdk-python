#!/bin/sh

set -e

echo 'Running flake8....'
flake8 --docstring-convention google --extend-ignore W503 src/cbc_sdk/
flake8 --docstring-convention google --extend-ignore W503 src/tests/
flake8 --docstring-convention google --extend-ignore W503 examples/
