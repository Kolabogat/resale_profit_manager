#!/bin/bash


echo "Building the project..."
pyhton -m pip install -r requirements.txt

echo "Make Migration..."
python manage.py makemigrations --no-input
python manage.py migrate --no-input

echo "Collect Static..."
python manage.py collectstatic --no-input

echo "Add Settings to Model..."
python manage.py command_settings_query
