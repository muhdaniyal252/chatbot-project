#!/usr/bin/env bash
set -e

echo "Waiting for Postgres..."
/wait-for-it.sh ${POSTGRES_HOST}:5432 -- echo "Postgres is ready"

echo "Running migrations..."
python myproject/manage.py migrate --noinput

echo "Creating superuser if not exists..."
python myproject/manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpass"
    )

if not User.objects.filter(username="user").exists():
    User.objects.create_user("user", password="user")
EOF

echo "Creating agent if not exists..."
python myproject/manage.py shell <<EOF
from core.models import Agent
from django.contrib.auth import get_user_model

User = get_user_model()
u = User.objects.get(username="admin")

Agent.objects.get_or_create(
    name="personal assistant",
    defaults={
        "prompt": "I am your personal assistant. How can I help you today?",
        "user": u
    }
)
EOF

echo "Starting servers..."
exec "$@"
