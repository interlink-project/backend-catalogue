#! /usr/bin/env bash
# https://raw.githubusercontent.com/tiangolo/uvicorn-gunicorn-docker/master/docker-images/gunicorn_conf.py

HOST=${HOST:-0.0.0.0}
PORT=${PORT}
LOG_LEVEL=${LOG_LEVEL:-info}

rm -rf /app/interlinkers-data || true
git clone https://github.com/interlink-project/interlinkers-data /app/interlinkers-data

# Let the DB start
python /app/app/pre_start.py

# Create models in DB automatically without migrations
python /app/app/create_models.py

# Start Uvicorn with live reload IF DEVELOPMENT
exec uvicorn --reload --host $HOST --port $PORT --log-level $LOG_LEVEL "app.main:app"

# Start Gunicorn if PRODUCTION 
# exec gunicorn -k "uvicorn.workers.UvicornWorker" -c "app/gunicorn_conf.py" "app.main:app"