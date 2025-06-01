#!/bin/sh

echo "⏳ Waiting for MySQL to be ready at $DB_HOST:3306..."

while ! nc -z "$DB_HOST" 3306; do
  sleep 1
done

echo "✅ MySQL is up. Starting Flask..."
exec flask run --host=0.0.0.0 --port=5000 --no-reload
