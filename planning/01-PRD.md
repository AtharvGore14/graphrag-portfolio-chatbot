# 01 — Product Requirements Document (PRD)

**Product:** Portfolio GraphRAG Chatbot (API-first)  
**Status:** Approved  

**Folder:** `planning/`

---

## 1. Problem statement

Investors struggle to quickly understand **what they hold** and keep track of it without repeatedly opening a portfolio app. Asking natural-language questions about their own holdings is harder than it should be.

Separately, when users chat about their portfolio, the product should **analyse the emotional tone of their message** (mood/sentiment of the person) so the system can reflect that signal — not invent it and not give advice.

## 2. Goals

| # | Goal |
|---|------|
| G1 | Answer portfolio questions from **ingested graph data only**, scoped by `user_id` |
| G2 | Detect user **mood from chat text** via a dedicated classifier (not the LLM) |
| G3 | Ship an **API-first** chatbot that another platform can integrate; minimal web page for testing |
| G4 | Enforce **no hallucination** and **analyser-not-suggester** behavior |
| G5 | Keep the system **simple**, reproducible (Docker), and scalable toward **~10k users** |
| G6 | Respond with **sub-2-second** latency (target) |

## 3. Non-goals

- Host-app UI/auth product work (identity is assumed present as `user_id` on every request)
- Live market data / prices / news feeds
- Buy/sell recommendations, predictions, or speculative language
- Multi-agent orchestrators (LangChain / LlamaIndex)
- Full branded consumer UI (test page only in MVP)
- PostgreSQL or a second primary DB (single Neo4j graph)
- Vector DB in MVP (graph retrieval + dual memory as defined below)

## 4. Target users / personas

| Persona | Need |
|---------|------|
| **Retail / platform investor** | Ask “what do I hold / how is my allocation” without digging through app screens |
| **Integrating platform** | Call a chat API with `user_id` + message; get grounded answer + mood label |
| **Internal / company engineering** | Clone repo, `docker compose up`, ingest sample JSON, hand off cleanly |

## 5. Value proposition

> **Portfolio GraphRAG** analyses *your* holdings graph and *your* message mood — dual memory for conversation context and lasting portfolio/mood state — so you get facts you can trust, not invented market knowledge or advice.

## 6. Feature prioritization

### MVP (v1)

1. **Chat API** — accept `user_id` + message; return grounded answer + mood payload  
2. **Neo4j portfolio graph** — User → Portfolio → Holdings → Stock; MoodEvent linked to User  
3. **GraphRAG retrieval** — Cypher scoped by `user_id`; no cross-user traversal  
4. **Text-only mood detection** — DistilRoBERTa emotion model → label + confidence; LLM only rephrases  
5. **Anti-hallucination stack** — retrieval-only facts, citations/source-binding, empty-result refusal, advice filter  
6. **Dual memory** — Redis short-term conversation context; Neo4j long-term holdings + mood events  
7. **Minimal test webpage** — exercise the API  
8. **Ingest script** — load sample portfolio JSON into Neo4j (idempotent)  
9. **Docker Compose** — API + Neo4j + Redis; `.env.example` + short README  

### v1.1 (nice next)

- Semantic cache for repeat questions  
- Streaming responses  
- Langfuse (or similar) observability for LLM I/O audit  
- Horizontal API scale (`--scale` / managed containers) behind a simple LB  

### Future

- Host-platform SSO/JWT deep integration  
- Richer portfolio entity types (transactions, snapshots)  
- Read replicas / managed Neo4j Aura & Redis cluster if needed at scale  

## 7. User stories & acceptance criteria

### US-1 — Ask about my holdings

**As** an authenticated user (`user_id`),  
**I want** to ask what I hold / sector exposure / qty / avg price,  
**so that** I don’t reopen the portfolio app.

**Acceptance**

- [ ] Every query starts with `MATCH (u:User {id: $user_id})` (or equivalent scoped pattern)  
- [ ] Answer facts appear only if present in Cypher results  
- [ ] If graph has no match → explicit “I don’t have that data” (no LLM fill-in)  
- [ ] Response includes citation/source binding to retrieved node(s)  

### US-2 — Mood analysed from my message

**As** a user chatting about my portfolio,  
**I want** the system to detect my current emotional tone from my text,  
**so that** mood is analysed consistently and audibly (label + confidence).

**Acceptance**

- [ ] Mood comes from DistilRoBERTa (or agreed emotion model), not LLM invention  
- [ ] Response exposes structured `{ label, confidence }`  
- [ ] Below confidence threshold → “not enough signal…” (no forced mood)  
- [ ] MoodEvent can be persisted on the User in Neo4j  
- [ ] LLM may only phrase the precomputed label  

### US-3 — Integrate via API

**As** a platform engineer,  
**I want** a stable HTTP chat API,  
**so that** our UI can embed portfolio Q&A without owning the RAG stack.

**Acceptance**

- [ ] Documented request/response contract (see later backend schema doc)  
- [ ] `user_id` required; missing/invalid → 4xx  
- [ ] Test webpage can call the same API successfully  

### US-4 — No advice / no hallucination

**As** a product owner,  
**I want** answers limited to facts + mood analysis,  
**so that** we never invent prices, positions, or recommendations.

**Acceptance**

- [ ] System prompt + post-filter block advisory language (“you should”, “I recommend”, etc.)  
- [ ] Programmatic check: tickers/numbers in output ⊆ retrieved context  
- [ ] Single retrieval → single LLM generation (no agent loops)  
- [ ] No live market data used  

### US-5 — Dual memory

**As** a user in a multi-turn chat,  
**I want** the bot to remember recent turns and my lasting portfolio/mood graph,  
**so that** follow-ups work without re-stating everything.

**Acceptance**

- [ ] Short-term: Redis holds recent conversation turns for the session  
- [ ] Long-term: Neo4j holds portfolio + mood events  
- [ ] Clearing Redis does not wipe portfolio graph data  

### US-6 — Handoff / reproduce

**As** a company engineer,  
**I want** one-command local bring-up,  
**so that** I can run and extend the system without tribal setup knowledge.

**Acceptance**

- [ ] `docker compose up` starts API + Neo4j + Redis  
- [ ] `.env.example` lists all required vars  
- [ ] `scripts/ingest_portfolio.py` loads `backend/portfolio_data (27).json` (or path override) idempotently under `user_id`  
- [ ] README has Setup / Run / Environment Variables only (MVP)  

## 8. Success metrics

| Metric | Target (MVP) |
|--------|----------------|
| Hallucination / ungrounded facts | **Zero tolerance** in design: refuse if not in graph; citation binding enforced |
| Latency | **&lt; 2 seconds** end-to-end for typical chat turn (target) |
| Scope | Facts from ingested data + mood label only |
| Scale readiness | Stateless API; architecture supports ~**10k users** (single Neo4j + Redis initially) |
| Simplicity | No orchestrator; one graph DB; Docker-first |

*No separate accuracy % target beyond groundedness + mood confidence gating for MVP.*

## 9. Constraints & principles (locked)

- **Graph security boundary:** never traverse without `user_id` anchor  
- **LLM role:** language over pre-verified inputs only (not fact or mood generation)  
- **LLM provider:** OpenAI-SDK-compatible wrapper (Groq now → OpenAI later via env)  
- **Mood:** text-only DistilRoBERTa emotion; not FinBERT financial sentiment  
- **Data:** canonical sample at `backend/portfolio_data (27).json`; ingest is the only MVP data path (no live market APIs)  
- **Latency tactics:** parallel mood + retrieval; one LLM call; capped tokens; indexed Cypher; minimal subgraph  

## 10. Canonical data source (locked)

**File:** `backend/portfolio_data (27).json`

Ingest maps this snapshot into Neo4j under a given `user_id`. Prices/PnL in the file are **snapshot values at ingest time**, not live fetches.

### Top-level shape

| Key | Role |
|-----|------|
| `metrics` | Portfolio-level aggregates (investment, current value, PnL, counts, day change, T1 stats) |
| `sectors[]` | Sector rollups (allocation, investment/current value, PnL) |
| `holdings[]` | Per-instrument positions |

### Holding fields used for GraphRAG (MVP)

Primary identity / position:

- `tradingsymbol`, `exchange`, `isin`, `instrument_token`, `product`
- `quantity`, `average_price`, `t1_quantity`, `realised_quantity`, `total_quantity`

Valuation / PnL (from snapshot only):

- `last_price`, `close_price`, `investment_value`, `current_value`, `pnl` / `profit_loss`, `profit_loss_percent`
- `day_change`, `day_change_percent` / `day_change_percentage`

Classification:

- `sector`, `industry`, `market_cap`, `market_cap_category`

Optional / lower priority for MVP ingest (store if cheap, do not require for answers):

- `mtf`, `momentum*`, `value*`, collateral/authorisation fields

### Graph mapping (intent)

```
(:User {id}) -[:OWNS]-> (:Portfolio {metrics...})
(:Portfolio) -[:HAS_SECTOR]-> (:Sector {name, allocation, ...})
(:Portfolio) -[:HOLDS]-> (:Holding {qty, avg_price, ...}) -[:OF]-> (:Stock {ticker, exchange, isin, sector, ...})
(:User) -[:HAD_MOOD]-> (:MoodEvent {label, confidence, timestamp})
```

Full Cypher property lists land in `05-backend-schema.md`.

## 11. Open items (non-blocking for PRD)

- Confidence threshold numeric default for mood  
- Timeline / team size (not provided — treat as solo/learning + company handoff)  
- Prefer renaming `portfolio_data (27).json` → e.g. `portfolio_sample.json` for cleaner paths (optional)

---

**Review checkpoint:** Edit this PRD or reply **“PRD approved”** to proceed to `02-TRD.md`.
