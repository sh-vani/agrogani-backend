#!/bin/bash
echo "🔁 Running Migrations..."
python manage.py migrate

echo "🚀 Starting Gunicorn server..."
gunicorn agrogani_backend.wsgi:application --bind 0.0.0.0:8080
