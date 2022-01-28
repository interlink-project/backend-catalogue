#! /usr/bin/env bash
# https://raw.githubusercontent.com/tiangolo/uvicorn-gunicorn-docker/master/docker-images/gunicorn_conf.py

HOST=${HOST:-0.0.0.0}
PORT=${PORT}
LOG_LEVEL=${LOG_LEVEL:-info}

git clone https://github.com/interlink-project/interlinkers-data /app/interlinkers-data

# Let the DB start
python /app/app/pre_start.py

# Run and apply migrations
# https://blog.jerrycodes.com/multiple-heads-in-alembic-migrations/
alembic revision --autogenerate -m "First for catalogue"
alembic upgrade head
echo MIGRATIONS DONE

# Start Fastapi app
exec gunicorn -k "uvicorn.workers.UvicornWorker" -c "gunicorn_conf.py" "app.main:app"
