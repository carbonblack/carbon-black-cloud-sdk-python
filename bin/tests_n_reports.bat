@echo off

echo "Running tests..."
coverage run -m pytest

echo "Running report and sending to coveralls...."
coverage report -m
coveralls
