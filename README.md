# Portfolio GraphRAG Chatbot

API-first portfolio Q&A over Neo4j GraphRAG, with text mood analysis. Minimal test page for local use.

## Where to run commands

Open **Command Prompt**, **PowerShell**, or the **Cursor/VS Code terminal**.

All `docker compose` commands must be run from the **project root** — the folder that contains `docker-compose.yml`:

```text
c:\AAYUSH\5_College\Projects\rag-based-portfolio-chatbot
```

In PowerShell / Command Prompt:

```powershell
cd c:\AAYUSH\5_College\Projects\rag-based-portfolio-chatbot
```

Check you are in the right place (`docker-compose.yml` should be listed):

```powershell
dir docker-compose.yml
```

Do **not** run these from subfolders like `backend\` or `scripts\` unless you `cd` back to the root first.

## Start the project (Docker Compose)

1. Start **Docker Desktop** and wait until it is running.
2. Go to the project root (see above).
3. First time only — copy env and add your Groq key:

```powershell
copy .env.example .env
notepad .env
```

4. Start everything (API + Neo4j + Redis):

```powershell
docker compose up --build
```

- Leave this terminal open while the app runs (logs stream here).
- Or run in the background:

```powershell
docker compose up --build -d
```

5. First time (or after a full wipe) — load sample portfolios:

```powershell
docker compose exec api python /scripts/ingest_portfolio.py --all
```

6. Open the app:
   - Test chat: http://localhost:8000/
   - Health: http://localhost:8000/health
   - API docs: http://localhost:8000/docs
   - Neo4j Browser: http://localhost:7474

On the test page, set `user_id` to `demo` (or `u_alpha` / `u_beta`) and ask about `ADANIPOWER`.

## Stop / shut down Docker Compose

From the **same project root** folder:

```powershell
docker compose down
```

That stops and removes the containers. Neo4j data usually stays in a Docker volume.

To stop **and** delete Neo4j/Redis data volumes (full reset):

```powershell
docker compose down -v
```

### Quick reference

| Action | Command (from project root) |
|--------|-----------------------------|
| Start (foreground) | `docker compose up` |
| Start (background) | `docker compose up -d` |
| Start + rebuild images | `docker compose up --build` |
| Stop | `docker compose down` |
| Stop + wipe DB volumes | `docker compose down -v` |
| Status | `docker compose ps` |

## Setup (summary)

```powershell
cd c:\AAYUSH\5_College\Projects\rag-based-portfolio-chatbot
copy .env.example .env
# edit .env — set LLM_API_KEY (Groq) and NEO4J_PASSWORD if desired
docker compose up --build
docker compose exec api python /scripts/ingest_portfolio.py --all
```

## Run URLs

- API / health: http://localhost:8000/health  
- Neo4j Browser: http://localhost:7474  
- Test page: http://localhost:8000/  
- OpenAPI: http://localhost:8000/docs  

### Ingest sample portfolio(s)

Portfolios live in `backend/portfolios/{user_id}_portfolio.json` (each file has a top-level `user_id`).

```bash
# all users (demo, u_alpha, u_beta)
docker compose exec api python /scripts/ingest_portfolio.py --all

# single file (user_id read from JSON)
docker compose exec api python /scripts/ingest_portfolio.py --file /app/portfolios/demo_portfolio.json
```

Regenerate variants from the original snapshot (optional):

```bash
python scripts/generate_portfolio_variants.py
```

Verify retrieval isolation:

```bash
docker compose exec api python /scripts/verify_retrieve.py
```

Verify Redis conversation memory:

```bash
docker compose exec api python /scripts/verify_memory.py
```

Verify mood classifier (first run downloads the model; cached afterward):

```bash
docker compose exec api python /scripts/verify_mood.py
```

Verify guardrails (+ live Groq if `LLM_API_KEY` is set):

```bash
docker compose exec api python /scripts/verify_guardrails.py
```

### Chat API

```bash
curl -X POST http://localhost:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"user_id\":\"demo\",\"message\":\"How many ADANIPOWER shares do I hold?\"}"
```

Or:

```bash
docker compose exec api python /scripts/verify_chat.py
docker compose exec api python /scripts/verify_questions.py
```

Natural phrasings supported (examples): holdings count, top performers by PnL, “Adani Power” → ADANIPOWER. Unknown tickers / users get a clarifying refuse, not a fake number.

OpenAPI: http://localhost:8000/docs

In Neo4j Browser:

```cypher
MATCH (u:User)-[:OWNS]->(:Portfolio)-[:HOLDS]->(h:Holding {ticker:'ADANIPOWER'})
RETURN u.id, h.quantity
ORDER BY u.id
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `LLM_API_KEY` | Groq / OpenAI API key |
| `LLM_BASE_URL` | e.g. `https://api.groq.com/openai/v1` or `https://api.openai.com/v1` |
| `LLM_MODEL` | e.g. `llama-3.1-8b-instant` (fast) or `llama-3.3-70b-versatile` |
| `NEO4J_URI` | Bolt URI (`bolt://neo4j:7687` in Compose) |
| `NEO4J_USER` | Neo4j user (default `neo4j`) |
| `NEO4J_PASSWORD` | Neo4j password (must match Compose) |
| `REDIS_URL` | e.g. `redis://redis:6379/0` |
| `MOOD_CONFIDENCE_THRESHOLD` | Mood gate (default `0.5`) |
| `MOOD_MODEL` | Hugging Face emotion model id |
| `CHAT_MEMORY_MAX_TURNS` | Redis history window (default `10`) |
| `CHAT_MEMORY_TTL_SECONDS` | Redis key TTL (default `86400`) |
