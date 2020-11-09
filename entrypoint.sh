#!/bin/bash

cd code

echo "Set up database"
python manage.py makemigrations
python manage.py migrate

echo "Running server"
python manage.py runserver 0.0.0.0:8000