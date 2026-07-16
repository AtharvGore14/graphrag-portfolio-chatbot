## Single Graph DB — user_id as the entry node

Since the user is already authenticated (session persists into the chatbot), model it like this in Neo4j:

```
(:User {id: "user_123"}) -[:OWNS]-> (:Portfolio) -[:HOLDS]-> (:Holding {qty, avg_price}) -[:OF]-> (:Stock {ticker, sector})
(:User {id: "user_123"}) -[:HAD_MOOD]-> (:MoodEvent {label, confidence, timestamp})
```

Every query is scoped by `user_id` as the anchor node — so retrieval always starts with `MATCH (u:User {id: $user_id})-[:OWNS]->...`. This is also your security boundary: no query should ever traverse the graph without that anchor, or you risk cross-user data leakage.

## Groq API now, swap to OpenAI later

Good news — **Groq's API is OpenAI-SDK-compatible**, so the swap is nearly free if you build it right from day one. Just abstract the client behind one config point instead of hardcoding it:

```python
# llm_client.py
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL")  # Groq: https://api.groq.com/openai/v1 | OpenAI: default
)

def chat_completion(messages, model=os.getenv("LLM_MODEL")):
    return client.chat.completions.create(model=model, messages=messages)
```

`.env` for Groq:
```
LLM_API_KEY=gsk-xxxx
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL=llama-3.1-8b-instant
```

`.env` to switch to OpenAI — just change 3 lines, zero code changes:
```
LLM_API_KEY=sk-xxxx
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```

That's the whole migration. Never call the SDK directly anywhere else in the codebase — always through this wrapper.

## PostgreSQL vs Neo4j

| | **PostgreSQL** | **Neo4j** |
|---|---|---|
| **Best for** | Flat/tabular data: auth, sessions, mood history log, audit trail | Relationship-heavy queries: "what sectors am I overexposed to," multi-hop portfolio reasoning |
| **Query speed on relationships** | Degrades fast with JOINs as depth increases (3+ hop queries get slow/ugly) | Constant-time traversal regardless of depth — this is the whole point of a graph DB |
| **Maturity/tooling** | Extremely mature, huge ecosystem, cheap hosting everywhere | Smaller ecosystem, but purpose-built GraphRAG tooling (`neo4j-graphrag`) is a real advantage for you |
| **Schema flexibility** | Rigid, needs migrations for changes | Flexible, easy to add new node/relationship types as portfolio model grows |
| **Ops complexity** | Simple, well-understood, cheap | Heavier to run/host, steeper learning curve, pricier managed hosting (Aura) |
| **Your use case fit** | Good for user accounts, mood log (simple time-series) | Good for portfolio structure + retrieval — this is your core "brain" |

**Since you said one graph database only** — you can actually collapse everything into Neo4j (users, mood events, holdings all as nodes) and skip Postgres entirely. That's simpler to operate (one DB, one connection pool, one backup strategy) at the cost of Neo4j being mildly worse than Postgres at pure auth/session lookups — but at 10k users that tradeoff is negligible. I'd recommend going single-DB since you asked for "one graph database" — it also matches your "keep it simple" requirement.

## Easiest to reproduce / hand off to the company

This is what makes or breaks a handoff. Priorities:

1. **Docker Compose** — the entire stack (FastAPI + Neo4j + Redis) spins up with one command: `docker compose up`. No "install this, then that" instructions.
2. **`.env.example`** — every required variable listed with dummy values, so anyone can copy → fill in → run.
3. **Seed/ingestion script** — a single script (`scripts/ingest_portfolio.py`) that takes their JSON file and loads it into Neo4j. This is your "data source" pipeline — make it idempotent (safe to re-run).
4. **One README** with exactly 3 sections: Setup, Run, Environment Variables. No sprawling docs — matches your "simple" requirement.
5. **No local-machine dependencies** — nothing should require a specific OS, global pip install, or manual DB setup outside Docker.

That combination (Compose + `.env.example` + seed script + README) is the standard for "clone repo, run one command, it works" — which is exactly what you'd hand to a company's dev team.

## How Docker scaling works here

Since your FastAPI layer is stateless (session state lives in Redis, not in the container), scaling is horizontal and simple:

- **Locally/small scale**: `docker compose up --scale api=4` runs 4 copies of your API container behind a load balancer (e.g., Nginx or Traefik container in the same Compose file).
- **Production at 10k users**: deploy the same image to **AWS ECS/Fargate** or **Railway**, set autoscaling rules (e.g., scale out when CPU > 70%), and let the platform spin up/down containers automatically based on load.
- **Neo4j and Redis don't scale the same way** — they're stateful. Neo4j scales via read-replicas (Neo4j Aura handles this managed) if read load gets heavy; Redis scales via a managed cluster (e.g., AWS ElastiCache) if needed. At 10k users, a single well-sized Neo4j + Redis instance is very likely enough — don't over-engineer this yet.

The key architectural point: **only the API layer needs to scale horizontally** (many stateless copies); the databases scale vertically first, then via replicas only if you actually hit a bottleneck.

## Why no orchestrator (LangChain/LlamaIndex)?

Good instinct to question this — here's the actual reasoning:

- Your data source is one flat JSON structure loaded into a fixed graph schema — you don't need an orchestrator's job (chaining together many heterogeneous tools/sources). You have exactly one retrieval path: Cypher query against Neo4j.
- Orchestrators add **latency** (extra function-calling round-trips, agent-loop overhead) and **abstraction you can't fully see inside** — which directly works against both your "no hallucination" requirement (harder to audit exactly what got retrieved) and your "<2 second response" requirement (every abstraction layer adds milliseconds, and agent loops can add full extra LLM calls).
- A **hand-written Cypher query + a single prompt template** is faster, fully auditable, and easier to unit-test than a LangChain chain. Given your fixed, small toolset, hand-rolling this is genuinely simpler than learning and fighting an orchestrator's abstractions.

Use an orchestrator when you have many tools, many data sources, or complex multi-step agent behavior. You have none of that — so skip it. This is the correct call for your stated requirements.

## Mood detection — confirmed: text-only

Locked in as: user's chat message → emotion classifier (DistilRoBERTa emotion model) → structured label + confidence score → LLM only rephrases the label, never invents one. No behavioral signals, no portfolio volatility mixed in. Simple, auditable, matches your "strong analyser not suggestor" requirement.

## Getting response time under 2 seconds

This is the one that needs the most discipline. Here's what to cut and what to keep:

**Run independent steps in parallel, not sequentially**
Mood classification and graph retrieval don't depend on each other — run them concurrently with `asyncio.gather()` instead of one-after-another. This alone can cut a big chunk of latency.

**Keep the LLM call to exactly one**
No multi-step reasoning, no "let me think then retrieve then think again." One retrieval → one prompt → one completion. Multi-call chains are the #1 latency killer.

**Cap `max_tokens` on the response**
Force short, direct answers (e.g., `max_tokens=300`). Generation time scales directly with output length — this is often the single biggest lever you have.

**Use a fast model tier**
Use the fastest available model variant (e.g., `llama-3.1-8b-instant` on Groq or `gpt-4o-mini`-class) rather than the largest. For grounded, templated Q&A over a known graph, you don't need your biggest model — accuracy comes from good retrieval, not model size.

**Pre-index everything in Neo4j**
Create indexes on `user_id` and `ticker` so lookups are near-instant (`CREATE INDEX ON :User(id)`). Never do a full graph scan per query.

**Limit what you retrieve**
Only pull the specific subgraph relevant to the question (e.g., just this user's holdings + directly connected nodes), not their entire history. Smaller context = faster prompt processing = faster response.

**Cut cold starts**
Keep the API, Neo4j, and Redis in the same region/VPC, with persistent connection pools (don't open a new Neo4j driver connection per request). If deploying serverless, keep containers warm — cold starts alone can blow past 2 seconds.

**Add a semantic cache for repeat questions**
If many users ask similar questions ("how's my portfolio doing"), cache the LLM response for a short TTL keyed by a semantic hash of the question + user state. Skips the LLM call entirely on cache hits.

**Stream the response**
Even if full generation takes ~2s, streaming tokens back as they're generated makes it *feel* instant to the user — worth doing for perceived speed even if not strictly required by "response time."

**What NOT to cut**: don't skip the citation/grounding step to save time — that's your anti-hallucination guardrail and it's cheap (it's a graph lookup, not an LLM call), so it shouldn't meaningfully affect your 2-second budget anyway.