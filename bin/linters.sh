#!/bin/sh

set -e

echo 'Running flake8....'
flake8 --docstring-convention google src/cbc_sdk
flake8 --docstring-convention google src/tests/
