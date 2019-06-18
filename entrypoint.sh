#!/usr/bin/env bash

until python manage.py migrate
do
    echo "Connecting to Postgres Database"
done

python manage.py collectstatic --no-input

python manage.py runserver 0.0.0.0:8000