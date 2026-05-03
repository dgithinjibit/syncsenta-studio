#!/usr/bin/env bash
# Start both the FastAPI AI agents backend and the Vite dev server.
# The Vite server (port 5000) proxies /agents/* to FastAPI (port 8000).

set -e

# Start FastAPI backend in the background
python3 app.py &
BACKEND_PID=$!

# Wait briefly for backend to be ready
sleep 2

# Start Vite dev server in foreground (port 5000)
cd frontend && npm run dev

# If Vite exits, kill the backend too
kill $BACKEND_PID 2>/dev/null || true
