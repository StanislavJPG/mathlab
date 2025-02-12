#!/bin/bash
set -e

# Function to start Gunicorn with dynamic reload-extra-file options
start_gunicorn() {
    if [ "$DJANGO_ENV" = "dev" ]; then
        echo "Starting Gunicorn in development mode..."
        extra_files=$(find server -name "*.html" -printf "--reload-extra-file %p ")
        gunicorn --config config/gunicorn-cfg.py --reload --reload-engine=poll $extra_files server.settings.wsgi
    else
        echo "Starting Gunicorn in production mode..."
        gunicorn --config config/gunicorn-cfg.py server.settings.wsgi
    fi
}

# Start Gunicorn
start_gunicorn