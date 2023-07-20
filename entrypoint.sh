#!/bin/sh

service postgresql start

python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py command_filter_query
python manage.py command_settings_query
DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_PASSWORD=admin python manage.py createsuperuser --noinput --email admin@admin.com
python manage.py test_command_create_tickets

gunicorn backend.wsgi:application --bind 0.0.0.0:8000