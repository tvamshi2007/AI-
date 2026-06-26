#!/usr/bin/env bash
# Render build script — runs once during each deploy

set -o errexit   # exit on any error

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput
