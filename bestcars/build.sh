#!/usr/bin/env bash
set -o errexit

pip install -r server/requirements.txt

cd server
python manage.py collectstatic --no-input
python manage.py migrate
