#!/bin/bash


nohup gunicorn --bind 0.0.0.0:8000 travel_companion_backend.wsgi:application --workers 3 > gunicorn.log 2>&1 &
