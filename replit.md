# SyncSenta Education OS

A Web4-first education platform for Kenya's CBC curriculum — AI-powered, built for 100,000+ concurrent users.

## Architecture

| Layer | Technology |
|-------|-----------|
| Frontend | Single-page HTML/CSS/JS served by FastAPI |
| Backend | Python FastAPI (ai-agents service) on port 5000 |
| AI Agents | LangGraph orchestration + LangChain (offline demo stub available) |
| Blockchain | Rust + Polygon smart contracts (backend/syncsenta-blockchain) |
| Rust Backend | Axum API + PostgreSQL + Redis (backend/syncsenta-backend) — requires external DB |

## Project Structure

```
/
├── app.py                          # Main entry point — serves frontend + AI agents API on port 5000
├── frontend/
│   └── index.html                  # SPA frontend (AI Tutor, Quiz Generator tabs)
├── ai-agents/
│   └── src/syncsenta_agents/
│       ├── api/
│       │   ├── server.py           # FastAPI routes (/agents/chat, /agents/assessment/*)
│       │   └── demo_stub.py        # Deterministic offline stub (no Ollama needed)
│       ├── agents/
│       │   ├── assessment.py       # Assessment & quiz generation agent
│       │   └── tutoring.py         # Socratic tutoring agent
│       ├── orchestrator/
│       │   ├── main.py             # SyncSentaOrchestrator
│       │   └── workflow.py         # LangGraph workflow
│       └── core/
│           ├── config.py           # AgentConfig (Ollama, Stellar, DB settings)
│           ├── models.py           # Pydantic data models
│           └── exceptions.py       # Custom exceptions
├── backend/                        # Rust workspace (Axum + PostgreSQL)
│   ├── syncsenta-backend/          # Main API server
│   ├── syncsenta-blockchain/       # Smart contract tooling (Hardhat)
│   └── syncsenta-common/           # Shared types
└── repos/                          # External ecosystem repos (submodules/clones)
```

## Running the App

```bash
python3 app.py
```

The app starts on **port 5000** and serves:
- `GET /` — Frontend SPA
- `GET /healthz` — Health check
- `POST /agents/chat` — AI Tutor (Teacher Agent)
- `POST /agents/assessment/quiz` — Quiz generation
- `POST /agents/assessment/grade` — Quiz grading

## Environment

- `SYNCSENTA_OFFLINE_DEMO=1` (default) — Use deterministic stubs; no Ollama needed
- Set `SYNCSENTA_OFFLINE_DEMO=0` to use a real Ollama server at `http://localhost:11434`

## AI Agents (Offline Demo Mode)

The `DemoStubLLM` in `demo_stub.py` provides canned CBC-aligned responses for:
- Quiz generation (fractions, general knowledge)
- Short-answer grading with rubric scores
- Tutoring replies with Kenyan context

## Key Dependencies

- `fastapi`, `uvicorn` — Web framework
- `langchain`, `langchain-community`, `langgraph` — Agent orchestration
- `structlog` — Structured logging
- `pydantic` — Data validation

## Workflow

- **Start application**: `python3 app.py` → port 5000 (webview)

## Deployment

- Target: autoscale
- Run command: `python3 app.py`
