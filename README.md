# Personal-AI-Agent

Telegram-first personal AI agent backend built in testable phases.

## Current phase

Phase 1 focuses on validating the Telegram communication layer:

- FastAPI backend with health and Telegram status endpoints
- Telegram Bot API client
- Long-polling worker for localhost development
- Basic message handler and automated tests
- `.env`-based local configuration

## Planned stack

- Backend: FastAPI
- Agent orchestration target: LangGraph
- Web tools: Crawl4AI
- Database and memory: PostgreSQL + pgvector
- Optional managed DB later: Supabase

LangGraph is the best fit here because the flow will likely become stateful and tool-heavy:
Telegram -> intent routing -> crawler/tool calls -> memory lookup -> LLM response.

## Local setup

1. Create or reuse the local virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -e .[dev]
   ```

3. Copy the environment template if needed and fill in `TELEGRAM_BOT_TOKEN`:

   ```powershell
   Copy-Item .env.example .env
   ```

4. Run the API:

   ```powershell
   python -m uvicorn personal_ai_agent.main:app --app-dir src --reload
   ```

5. Run tests:

   ```powershell
   pytest
   ```

## Roadmap

1. Telegram transport validation
2. Crawl4AI tools for product and key-price search
3. Gemini integration behind an agent workflow
4. PostgreSQL + pgvector memory and persistence
5. Dockerized local stack
6. Deployment
