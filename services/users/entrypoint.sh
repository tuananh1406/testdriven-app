#!/bin/sh

echo "Khởi động postgres..."
while ! nc -z users-db 5432; do
    sleep 0.1
done

echo "PostgreSQL đã chạy"


python manage.py run -h 0.0.0.0
