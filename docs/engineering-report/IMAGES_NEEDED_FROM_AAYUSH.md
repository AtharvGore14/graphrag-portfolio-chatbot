# Images needed from Aayush (Lathi)

**Repo:** https://github.com/AtharvGore14/graphrag-portfolio-chatbot  
**LaTeX path:** `docs/engineering-report/latex/` → drop PNGs in `images/`  
**Overleaf:** https://www.overleaf.com/1656157384wxcgqvgpkpdx#c9a2af  

**Total: 22 files** (logo already done). Exact filenames only. PNG. No API keys / passwords.

---

## Done (skip)

| File |
|------|
| `01_college_logo.png` |

---

## Batch 1 — Screenshots (you run the app) — **10 files**

Priority first. After `docker compose up --build` + ingest `--all`:

| File | Capture |
|------|---------|
| `S01_compose_healthy.png` | Compose healthy (`docker compose ps`) |
| `S02_health_json.png` | `http://localhost:8000/health` |
| `S03_swagger_docs.png` | `http://localhost:8000/docs` |
| `S05_ui_grounded_answer.png` | UI: `user_id=demo`, ask ADANIPOWER holdings (answer + citations) |
| `S06_ui_refuse.png` | UI: unknown ticker → refuse |
| `S08_neo4j_subgraph.png` | Neo4j Browser `localhost:7474`, `demo` subgraph |
| `S09_ingest_cli.png` | Ingest CLI success (`ingest_portfolio.py --all`) |
| `S10_pytest.png` | `docker compose exec api pytest /tests -q` |
| `S11_verify_scripts.png` | `verify_chat.py` or `verify_questions.py` success |
| `S13_env_example_redacted.png` | `.env.example` with secrets blurred |

---

## Batch 2 — Diagrams (draw → export PNG) — **12 files**

Clean boxes/arrows, white/light background, readable at page width.

| File | Show |
|------|------|
| `fig_08_tech_stack.png` | Layers: Client → FastAPI → Neo4j / Redis / Mood / LLM / Compose |
| `fig_09_logical_architecture.png` | Client, FastAPI, Neo4j, Redis, Mood, LLM |
| `fig_09_chat_sequence.png` | One `POST /chat` turn sequence |
| `fig_09_ingest_flow.png` | JSON → ingest script → Neo4j |
| `fig_10_graph_schema.png` | User → Portfolio → Sector/Holding → Stock (+ MoodEvent) |
| `fig_10_dual_memory.png` | Redis short-term vs Neo4j long-term |
| `fig_11_graphrag_pipeline.png` | Intent → Cypher → citations → generate → guardrails |
| `fig_11_guardrails_flow.png` | Empty / advice / ungrounded → refuse |
| `fig_12_module_collab.png` | `chat.py` + services around it |
| `fig_14_api_anatomy.png` | `/chat` request + response fields |
| `fig_15_feature_map.png` | F01–F12 grid |
| `fig_16_test_strategy.png` | Unit / verify scripts / manual UI |

---

## Do **not** make these (cut from report)

`S04`, `S07`, `S12`, `S14`, Swagger try-it, and all old `fig_01`…`fig_07` / json_mapping / mood_pipeline / J1–J2 flowcharts.

---

## Paste to Lathi (short)

```text
Bhai — SEDD images only (22 total). Exact PNG names below.
Put in Overleaf images/ OR repo: docs/engineering-report/latex/images/

Already done: 01_college_logo.png

SCREENSHOTS (10) — run Compose + ingest:
S01_compose_healthy.png
S02_health_json.png
S03_swagger_docs.png
S05_ui_grounded_answer.png   (demo + ADANIPOWER)
S06_ui_refuse.png
S08_neo4j_subgraph.png
S09_ingest_cli.png
S10_pytest.png
S11_verify_scripts.png
S13_env_example_redacted.png  (blur keys)

DIAGRAMS (12) — draw/export:
fig_08_tech_stack.png
fig_09_logical_architecture.png
fig_09_chat_sequence.png
fig_09_ingest_flow.png
fig_10_graph_schema.png
fig_10_dual_memory.png
fig_11_graphrag_pipeline.png
fig_11_guardrails_flow.png
fig_12_module_collab.png
fig_14_api_anatomy.png
fig_15_feature_map.png
fig_16_test_strategy.png

Full detail: docs/engineering-report/IMAGES_NEEDED_FROM_AAYUSH.md
Repo: https://github.com/AtharvGore14/graphrag-portfolio-chatbot
```
