#!/bin/sh

MARKER_DIR="/app/marker"
MARKER_FILE="$MARKER_DIR/started"

if [ ! -d "$MARKER_DIR" ]; then
    echo "Creating marker directory: $MARKER_DIR"
    mkdir -p "$MARKER_DIR"
fi

if [ ! -f "$MARKER_FILE" ]; then
    echo "First time start: waiting 70 seconds..."
    sleep 70
    touch "$MARKER_FILE"
    echo "Running Alembic migrations..."
    alembic upgrade head
    python seed_roles.py

else
    echo "Already started before, no delay."

fi

echo "Starting app..."
exec python main.py