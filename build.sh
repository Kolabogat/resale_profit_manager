#!/bin/bash

pyhton3.9 -m pip install -r requirements.txt

python3.9 manage.py makemigrations --no-input
python3.9 manage.py migrate --no-input

python3.9 manage.py collectstatic --no-input

python3.9 manage.py command_settings_query
