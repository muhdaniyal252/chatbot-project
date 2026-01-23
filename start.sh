#!/usr/bin/env bash
set -e

# 1️⃣ Wait for Postgres
echo "Waiting for Postgres..."
/wait-for-it.sh ${POSTGRES_HOST}:5432 -- echo "Postgres is ready"

# 2️⃣ Run Django (no autoreload to avoid forking issues)
echo "Starting Django..."
python myproject/manage.py migrate --noinput
python myproject/manage.py runserver 0.0.0.0:8000 --noreload &

# 3️⃣ Run FastAPI
echo "Starting FastAPI..."
(
  cd myproject/asyncapis
  python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
) &

# 4️⃣ Wait for both processes
wait
