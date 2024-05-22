#!/bin/bash

mkdir ~/.npm-global
export NPM_CONFIG_PREFIX=~/.npm-global
export PATH=$PATH:~/.npm-global/bin
echo -e "export NPM_CONFIG_PREFIX=~/.npm-global\nexport PATH=$PATH:~/.npm-global/bin" >> ~/.bashrc

pyhton -m pip install -r requirements.txt

python manage.py makemigrations --no-input
python manage.py migrate --no-input

python manage.py collectstatic --no-input

python manage.py command_settings_query
