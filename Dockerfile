FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN apt update -y && apt upgrade -y
WORKDIR /django_app

RUN /usr/local/bin/python -m pip install --upgrade pip
COPY requirements.txt /django_app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /django_app/
WORKDIR /django_app/backend