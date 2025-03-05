#!/bin/sh
source $HOME/.local/bin/env
uv run python manage.py runserver $PORT
