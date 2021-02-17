#!/bin/sh

echo "Khởi động postgres..."
while ! nc -z users-db 5432; do
    sleep 0.1
done

echo "PostgreSQL đã chạy"


gunicorn -b 0.0.0.0:5000 manage:app
