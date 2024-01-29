#! /usr/bin/bash
export $(cat .env | xargs)
source .venv/bin/activate
TWOJEGRY_DEBUG=True python manage.py runserver 8000 --traceback
