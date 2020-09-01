#!/bin/bash
set -e

if [ "$1" = "prepare" ] ; then

    python manage.py collectstatic --no-input
    wait-for mariadb:3306 -- python manage.py migrate
    python manage.py check --deploy

    shift

elif [ "$1" = "celery" ] ; then

    wait-for mariadb:3306 rabbitmq:5672

elif [ "$1" = "gunicorn" ] ; then

    wait-for mariadb:3306 rabbitmq:5672

fi

exec "$@"
