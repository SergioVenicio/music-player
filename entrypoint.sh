#!/bin/bash

echo "Set up database"
python manage.py makemigrations --noinput
python manage.py migrate --noinput

exec "$@"