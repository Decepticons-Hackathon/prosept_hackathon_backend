#!/bin/sh

python manage.py makemigrations

python manage.py migrate --no-input

python manage.py collectstatic --no-input

python manage.py loaddata test_data.json

cp -r /app/static/. /backend_static/static/

exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000