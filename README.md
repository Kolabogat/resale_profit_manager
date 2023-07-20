# resale_profit_manager
Operating system: Ubuntu 22.04.2

**resale_profit_manager** - it's an application that allows you to account your resales, for example: digital goods, stocks, bonds, cryptocurrencies, other goods.
## How does this work?
1. Login or Register
2. Add ticket on Home page
3. You can add ticket with or without field `Sold`
4. If `Sold` field filled then ticket is complete
5. If `Sold` field not filled then your ticket will be in `Waiting` filter
6. You can edit ticket by clicking on it
7. Profit calculated after `Sold` field filled
## PostgreSQL
Check users and databases in Terminal:
```
sudo -i -u postgres
\du
q
\l
```
If you don't have superuser `postgres`:
```
sudo -i -u postgres
ALTER USER postgres WITH PASSWORD 'postgres';
```
If you don't have database `postgres`:
```
sudo -i -u postgres
CREATE DATABASE postgres WITH OWNER postgres;
```
## Docker-compose
Open Terminal in app directory and execute these commands:
```
sudo docker-compose build
```
```
sudo docker-compose up
```
If ports 5432 and 80 are busy:
```
sudo lsof -t -i tcp:80 -s tcp:listen | sudo xargs kill
```
```
sudo lsof -t -i tcp:5432 -s tcp:listen | sudo xargs kill
```
## Commands
When you up the server the following commands are executed in `entrypoint.sh` file:

```
python manage.py migrate
```
Migrations for database.

---

```
python manage.py collectstatic
```
Collects all static files.

---

```
python manage.py command_filter_query
```
Execute custom command that creates tickets filters in database

---

```
python manage.py command_settings_query
```
Execute custom command that creates choices settings for currency and pagination fields.

---

```
DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD python manage.py createsuperuser --noinput --email $DJANGO_SUPERUSER_EMAIL
```
Creating a superuser with username, password and email initialized in the .env file.

---

```
python manage.py test_command_create_tickets
```
An optional command that creates 200 tickets using a custom command. Only one user should be in database.

---

```
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
```
Starts the server with `gunicorn`.
