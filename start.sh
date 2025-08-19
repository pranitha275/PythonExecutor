#!/bin/bash

# Get the port from Railway environment variable, default to 8080
PORT=${PORT:-8080}

echo "Starting Python Code Execution Service on port $PORT"

# Start the application with gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 60 app:app 