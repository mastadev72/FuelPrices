#!/bin/sh
flask db upgrade
exec gunicorn -c /config/gunicorn.py manage:application