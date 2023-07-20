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
## Example of .env file (not safe)
```env
POSTGRES_HOST=postgres_db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin
DJANGO_SUPERUSER_EMAIL=amdin@admin.com

SECRET_KEY=5n(=rwpd^wp4dpv#j@l828nifgqacow%94_!xzof&adzf05cw&

DEBUG=False
```
## PostgreSQL example (not safe)
Check if users and databases are in PostgreSQL database:
```bash
sudo -i -u postgres psql
\du  #List of roles
q  #Exit from list
\l  #List of databases
q  #Exit from list
```
If you don't have role `postgres` with superuser permissions:
```bash
sudo -i -u postgres psql
ALTER USER postgres WITH PASSWORD 'postgres';
```
If you don't have database `postgres`:
```bash
sudo -i -u postgres psql
CREATE DATABASE postgres WITH OWNER postgres;
```
## Docker-compose
Open Terminal in app directory and execute these commands:
```bash
sudo docker-compose build
```
```bash
sudo docker-compose up
```
If ports 5432 and 80 are busy:
```bash
sudo lsof -t -i tcp:80 -s tcp:listen | sudo xargs kill
```
```bash
sudo lsof -t -i tcp:5432 -s tcp:listen | sudo xargs kill
```
## Commands info
When you up the server the following commands are executed in `entrypoint.sh` file:

Migrations for database:

```python manage.py migrate```

Collects all static files:

```python manage.py collectstatic```

Execute custom command that creates tickets filters in database:

```python manage.py command_filter_query```

Execute custom command that creates choices settings for currency and pagination fields:

```python manage.py command_settings_query```

Creating a superuser with username, password and email initialized in the .env file:
```
DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD python manage.py createsuperuser --noinput --email $DJANGO_SUPERUSER_EMAIL
```

An optional command that creates 200 tickets using a custom command. Tickets creates for first user with `id=1`:

```python manage.py test_command_create_tickets```

Starts the server with `gunicorn`:

```gunicorn backend.wsgi:application --bind 0.0.0.0:8000```
