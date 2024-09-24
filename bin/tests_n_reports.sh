#! /bin/bash

set -e

echo 'Running tests....'
coverage run -m pytest

echo 'Generating report....'
coverage xml
