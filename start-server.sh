#!/usr/bin/env bash
# start-server.sh
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('cyrilhokage', 'cyrilhokagen@yahoo.fr', 'pass')" | python manage.py shell
fi
(python manage.py makemigrations ; python manage.py migrate; python manage.py collectstatic --no-input; gunicorn cnouboue_portfolio.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) & nginx -g "daemon off;"