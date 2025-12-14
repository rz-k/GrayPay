#!/bin/sh

python manage.py migrate
python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL
python manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:8000 --workers 4 --bind unix:evaluation.sock config.wsgi

