#!/bin/bash

set -x;

/bin/bash /entrypoint.sh mysqld > /dev/null 2>&1 &

python manage.py flush --no-input
python manage.py migrate
python manage.py runserver 8000