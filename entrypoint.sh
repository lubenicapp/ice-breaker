#!/bin/bash

if [ $# -gt 0 ]; then
    # Execute the command passed as an argument
    "$@"
else
    # Default action if no arguments are provided
    gunicorn app.wsgi:application --bind 0.0.0.0:8000
fi
