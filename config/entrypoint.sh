#!/bin/bash
set -e

# Function to start Gunicorn with dynamic reload-extra-file options
start_gunicorn() {
    if [ "$DJANGO_ENV" = "dev" ]; then
        echo "Starting Gunicorn in development mode..."
        extra_files=$(find server -name "*.html" -printf "--reload-extra-file %p " -o -name "*.css" -printf "--reload-extra-file %p ")
        gunicorn --config config/gunicorn-cfg.py --reload --reload-engine=poll $extra_files server.settings.wsgi
    else
        echo "Starting Gunicorn in production mode..."
        gunicorn --config config/gunicorn-cfg.py server.settings.wsgi
    fi
}

if [ "$DJANGO_ENV" = "prod" ]; then
  # Start migrations
  echo "📦 Making migrations..."
  python manage.py migrate --noinput

  echo "Automatically preparing production data..."
  python manage.py loaddata post_categories
  python manage.py loaddata mathlab_carousels

  if [ "$SUPERUSER_CREATE" = "True" ]; then
    echo "Superuser creation..."
    python manage.py createsuperuser --noinput
  fi

  if [ "$COLLECTSTATIC" = "True" ]; then
    echo "Collecting static..."
    python manage.py collectstatic
  fi

  # Starting daphne and celery
  echo "Starting daphne and celery..."
  daphne server.settings.asgi:application -b 0.0.0.0 -p 8099 &

  # uncomment this line to start celery on production
#  celery -A server.settings.celery worker -l INFO &

  wait
fi

# Start Gunicorn
start_gunicorn