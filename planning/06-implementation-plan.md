# 06 — Implementation Plan

**Product:** Portfolio GraphRAG Chatbot (API-first)  
**Status:** Approved  
**Depends on:** `01`–`05`  
**Folder:** `planning/`

---

## 1. Build order (why this sequence)

Dependencies force this order: **infra → graph/ingest → retrieval → mood → LLM/guardrails → API → test UI → harden**.

| Phase | Deliverable | Depends on |
|-------|-------------|------------|
| 0 | Repo skeleton, Compose, env, README stub | — |
| 1 | Neo4j schema + ingest from sample JSON | 0 |
| 2 | Cypher retrieval helpers (`user_id` scoped) | 1 |
| 3 | Redis short-term memory | 0 |
| 4 | Mood classifier service | 0 |
| 5 | LLM wrapper + prompt + guardrails | 2, 4 |
| 6 | `POST /chat` orchestration (parallel) | 2–5 |
| 7 | Minimal test webpage | 6 |
| 8 | Latency/negative tests + polish polish | 6–7 |

Do not start Phase 5 until retrieval returns real citation payloads from the sample file.

---

## 2. Target folder structure

```
rag-based-portfolio-chatbot/
├── planning/                 # this doc set
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app
│   │   ├── config.py
│   │   ├── api/
│   │   │   └── routes_chat.py
│   │   ├── services/
│   │   │   ├── llm_client.py
│   │   │   ├── mood.py
│   │   │   ├── graph.py
│   │   │   ├── memory.py
│   │   │   ├── retrieve.py
│   │   │   ├── guardrails.py
│   │   │   └── chat.py       # orchestrate one turn
│   │   ├── models/
│   │   │   └── schemas.py    # Pydantic request/response
│   │   └── prompts/
│   │       └── system.txt
│   ├── portfolio_data (27).json
│   ├── Dockerfile
│   └── requirements.txt
├── scripts/
│   └── ingest_portfolio.py
├── web/                      # minimal test page
│   ├── index.html
│   └── app.js
├── docker-compose.yml
├── .env.example
├── README.md                 # Setup / Run / Environment Variables
└── tests/
    ├── test_guardrails.py
    ├── test_ingest_mapping.py
    └── test_chat_contract.py
```

Keep flat; no LangChain project layout.

---

## 3. Phase details & done criteria

### Phase 0 — Skeleton

- [ ] `docker-compose.yml`: `api`, `neo4j`, `redis`  
- [ ] `.env.example` with all vars from TRD  
- [ ] FastAPI hello + `GET /health`  
- [ ] README: Setup / Run / Env only  

**Done:** `docker compose up` → health OK against Neo4j + Redis.

### Phase 1 — Ingest

- [ ] Constraints/indexes applied on startup or ingest  
- [ ] `scripts/ingest_portfolio.py` loads `backend/portfolio_data (27).json`  
- [ ] Idempotent re-run for same `user_id`  
- [ ] Manual Cypher check: User → holdings count ≈ JSON  

**Done:** `demo` user queryable in Neo4j Browser/Cypher with ADANIPOWER qty matching JSON.

### Phase 2 — Retrieval

- [ ] Helpers: portfolio metrics, sectors, holding-by-ticker, list holdings (capped)  
- [ ] Always `user_id`-anchored  
- [ ] Return structured citation candidates  

**Done:** Unit/integration test: unknown user → empty; known ticker → fields present.

### Phase 3 — Redis memory

- [ ] Get/append/truncate N turns  
- [ ] Key = `chat:{user_id}:{session_id}`  

**Done:** Two turns persist; new session_id empty.

### Phase 4 — Mood

- [ ] DistilRoBERTa emotion load at startup (warm)  
- [ ] Threshold gate → `insufficient_signal`  
- [ ] Optional `MoodEvent` write  

**Done:** Sample anxious sentence → non-null label above threshold; low-signal path works.

### Phase 5 — LLM + guardrails

- [ ] `llm_client.py` only place that talks to OpenAI SDK  
- [ ] System prompt: context-only, no advice  
- [ ] Citation entity check + advice phrase filter  
- [ ] Empty retrieval → fixed refuse (no fact LLM)  

**Done:** Ungrounded ticker cannot appear in answer; “you should buy” stripped/blocked.

### Phase 6 — Chat API

- [ ] `POST /chat` per `05-backend-schema.md`  
- [ ] `asyncio.gather` mood + retrieve + redis  
- [ ] One LLM call; `max_tokens` cap  
- [ ] Persist memory + mood  

**Done:** Contract test green; typical question &lt; 2s on warm stack (measure & note).

### Phase 7 — Test page

- [ ] `web/` fields: user_id, session_id, transcript, composer  
- [ ] Renders mood + citations  

**Done:** Manual demo: ADANIPOWER question shows qty + sources.

### Phase 8 — Harden

- [ ] Negative tests (Neo4j down → 503, no invent)  
- [ ] Latency smoke script  
- [ ] README final pass  

**Done:** Ready for company handoff checklist (Compose + env + ingest + README).

---

## 4. Testing strategy

| Layer | What |
|-------|------|
| Unit | Guardrails, mood threshold, citation subset check |
| Integration | Ingest → retrieve by `user_id`; Redis round-trip |
| Contract | `/chat` schema + refuse flag |
| Manual | Test page against sample portfolio |
| Non-goals MVP | Full load test to 10k (architecture only); E2E browser suite |

**Lazy senior rule:** one small runnable check per non-trivial module (guardrails + ingest mapping minimum).

---

## 5. Milestones

| Milestone | Exit criteria |
|-----------|----------------|
| M1 Graph live | Ingest + Cypher proof on sample JSON |
| M2 Safe answers | `/chat` grounded + refuse + mood |
| M3 Demoable | Test page + README handoff path |
| M4 Perf bar | Documented &lt;2s on warm typical turn (or gap listed) |

Pause after each milestone for go-ahead before the next (per kickoff rule).

---

## 6. Open risks / unknowns

| Item | Plan |
|------|------|
| Mood model size / cold start | Bake weights in image; warm on startup |
| LLM latency | Fast model env; token cap; template fallback if needed |
| Filename spaces | Quote paths; optional rename later |
| Raw `user_id` trust | Document; JWT later |
| 76 holdings in prompt | Retrieve slice by intent/ticker; don’t dump all every turn |
| Advice filter false positives | Start with small phrase list; tune |

---

## 7. Explicit non-work (do not build yet)

- LangChain / LlamaIndex  
- Postgres / vector DB  
- Live market APIs  
- Host SSO  
- Semantic cache / streaming / Langfuse (v1.1)  
- Fancy UI  

---

## 8. Handoff checklist (definition of done for MVP)

- [ ] `docker compose up`  
- [ ] `.env.example` complete  
- [ ] Ingest script + sample JSON  
- [ ] `/chat` + test page  
- [ ] README: Setup / Run / Environment Variables  
- [ ] Planning docs `01`–`06` aligned with shipped behavior  

---

**Review checkpoint:** After you approve `05` + `06`, reply **`approved, start building`** to begin Phase 0. No application code until that sign-off.
