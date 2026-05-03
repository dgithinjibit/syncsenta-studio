"""SyncSenta Education OS - Main application entry point.

Serves the React-like frontend on port 5000 and mounts the AI agents API
under /agents/* using a single Uvicorn process.

Set SYNCSENTA_OFFLINE_DEMO=1 to run without Ollama (uses deterministic stubs).
"""

import os
import sys

# Ensure the ai-agents source is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "ai-agents", "src"))

# Enable offline demo mode by default in this environment
os.environ.setdefault("SYNCSENTA_OFFLINE_DEMO", "1")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from syncsenta_agents.api.server import app as agents_app

# ---------------------------------------------------------------------------
# Root application
# ---------------------------------------------------------------------------

app = FastAPI(title="SyncSenta Education OS", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount AI agents API
app.mount("/agents", agents_app)

# Serve static frontend files
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/healthz")
async def health():
    return {"status": "ok", "service": "syncsenta-education-os"}


@app.get("/")
async def index():
    return FileResponse("frontend/index.html")


@app.get("/{path:path}")
async def catch_all(path: str):
    """Serve index.html for any unknown path (SPA fallback)."""
    return FileResponse("frontend/index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=5000,
        reload=False,
        log_level="info",
    )
