# SyncSenta Education OS

A Web4-first education platform for Kenya's CBC curriculum — AI-powered, offline-first, built for 100,000+ concurrent users.

## Architecture

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + TypeScript + Vite + Tailwind CSS |
| AI Agents API | Python FastAPI (port 8000, localhost) |
| Agent Orchestration | LangGraph + LangChain (offline demo stub available) |
| Rust Backend | Axum + PostgreSQL + Redis (backend/ — requires external DB) |
| Blockchain | Polygon smart contracts (Hardhat — backend/syncsenta-blockchain/) |

## Project Structure

```
/
├── start.sh                         # Dev entrypoint: starts backend + Vite
├── app.py                           # FastAPI AI agents server (port 8000)
│
├── frontend/                        # React + TypeScript + Vite + Tailwind
│   ├── vite.config.ts               # Port 5000, host 0.0.0.0, proxy /agents/* → :8000
│   ├── src/
│   │   ├── App.tsx                  # Route definitions
│   │   ├── main.tsx                 # App entry point
│   │   ├── index.css                # Tailwind base styles
│   │   ├── components/
│   │   │   └── Layout.tsx           # Nav + API health indicator
│   │   └── pages/
│   │       ├── HomePage.tsx         # Landing page with feature overview
│   │       ├── TutorPage.tsx        # AI Tutor chat interface
│   │       └── QuizPage.tsx         # Quiz generator + grading
│   └── package.json
│
└── ai-agents/                       # Python AI agents service
    └── src/syncsenta_agents/
        ├── api/
        │   ├── server.py            # FastAPI: /agents/chat, /agents/assessment/*
        │   └── demo_stub.py         # Offline deterministic stubs (no Ollama needed)
        ├── agents/
        │   ├── assessment.py        # CBC quiz generation + grading
        │   └── tutoring.py          # Socratic tutoring agent
        ├── orchestrator/
        │   ├── main.py              # SyncSentaOrchestrator
        │   └── workflow.py          # LangGraph workflow graph
        └── core/
            ├── config.py            # AgentConfig
            ├── models.py            # Pydantic models
            └── exceptions.py        # Custom exceptions
```

## Running the App

```bash
bash start.sh
```

This starts:
- **FastAPI backend** on `localhost:8000` (AI agents API)
- **Vite dev server** on `0.0.0.0:5000` (frontend with HMR + proxy)

## API Endpoints (all via Vite proxy → port 8000)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/healthz` | Health check |
| POST | `/agents/chat` | AI Tutor (Teacher Agent) |
| POST | `/agents/assessment/quiz` | Generate CBC quiz |
| POST | `/agents/assessment/grade` | Grade a quiz submission |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SYNCSENTA_OFFLINE_DEMO` | `1` | Use deterministic stubs — no Ollama needed |

Set `SYNCSENTA_OFFLINE_DEMO=0` to use a real Ollama server at `http://localhost:11434`.

## Developer Workflow (Multiple Devs)

- **Frontend** lives entirely in `frontend/src/` — React + TypeScript + Tailwind
  - Add new pages in `frontend/src/pages/`
  - Add shared components in `frontend/src/components/`
  - Vite hot-module-reload means changes appear instantly
- **AI Agents** live in `ai-agents/src/syncsenta_agents/`
  - Add new agents in `agents/`
  - Register them in `orchestrator/main.py`
  - Test with `SYNCSENTA_OFFLINE_DEMO=1` (no Ollama needed)
- **Rust backend** in `backend/` — requires PostgreSQL + Redis
- Backend and frontend are fully decoupled — teams can work independently

## Workflow

- **Start application**: `bash start.sh` → port 5000 (webview)

## Deployment

- Target: autoscale
- Run: `python3 app.py` (API only — build frontend separately with `cd frontend && npm run build`)
