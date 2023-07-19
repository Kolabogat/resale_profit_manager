#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py command_filter_query
python manage.py command_settings_query

gunicorn backend.wsgi:application --bind 0.0.0.0:8000