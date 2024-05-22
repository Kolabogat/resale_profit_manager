#!/bin/bash

echo "Building the project..."
python3.10 -m pip install -r requirements.txt

echo "Make Migration..."
python3.10 manage.py makemigrations --no-input
python3.10 manage.py migrate --no-input

echo "Collect Static..."
python3.10 manage.py collectstatic --no-input

echo "Add Settings to Model..."
python3.10 manage.py command_settings_query
