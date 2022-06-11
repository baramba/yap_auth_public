#!/bin/sh

flask db upgrade
gunicorn wsgi_app:app