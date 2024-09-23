#! /bin/bash

set -e

echo 'Running tests....'
coverage run -m pytest

echo 'Running report....'
coverage report -m
