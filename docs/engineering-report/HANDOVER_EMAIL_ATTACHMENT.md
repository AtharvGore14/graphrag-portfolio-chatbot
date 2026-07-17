# Portfolio GraphRAG Chatbot — Documentation handover notes

**From:** Atharv  
**Date:** 17 July 2026  

---

## Status

A draft of our industry project documentation (LaTeX) is ready. Most of the writing is done. What remains is mainly **adding images / screenshots**, and a quick check of a few content details.

**Overleaf:** https://www.overleaf.com/1656157384wxcgqvgpkpdx#c9a2af  

**`latex.zip`** is attached with the mail as well. Please upload images into the Overleaf **`images/`** folder using the **exact filenames** listed below.

---

## Kindly help with

1. **Screenshots** after running the project (list in Section A).  
2. **Diagrams** where needed (list in Section B) — draw/export as PNG.  
3. A quick re-check of **Chapter 2** — AlgoFabric stakeholder names and timeline. Those details may need a second look; please correct if anything looks off.  
4. Once images are in Overleaf, a short compile check so figures show properly (not “Image pending”).

Thanks in advance for helping close this out.

---

## Section A — Screenshots (after running the project)

Please capture as **PNG**. Avoid showing real API keys or passwords.

| Filename (exact) | What to capture |
|------------------|-----------------|
| `S01_compose_healthy.png` | Docker Compose healthy (API, Neo4j, Redis) |
| `S02_health_json.png` | Browser: `http://localhost:8000/health` |
| `S03_swagger_docs.png` | Browser: `http://localhost:8000/docs` |
| `S04_ui_empty.png` | Test UI empty / ready — `http://localhost:8000/` |
| `S05_ui_grounded_answer.png` | Grounded answer + citations (`user_id=demo`, e.g. ADANIPOWER) |
| `S06_ui_refuse.png` | Refuse / clarify (unknown ticker or missing fact) |
| `S07_ui_multiturn.png` | Multi-turn chat, same session |
| `S08_neo4j_subgraph.png` | Neo4j Browser subgraph for user `demo` (`http://localhost:7474`) |
| `S09_ingest_cli.png` | Successful ingest CLI output |
| `S10_pytest.png` | Unit test pass summary |
| `S11_verify_scripts.png` | Success output from `verify_chat.py` / `verify_questions.py` |
| `S13_env_example_redacted.png` | `.env.example` with secrets redacted / blurred |

### Optional (nice to have)

| Filename (exact) | What to capture |
|------------------|-----------------|
| `S03_swagger_try_chat.png` | Swagger “Try it out” for `/chat` |
| `S12_qa_excel.png` | Crop from `chat_qa_results.xlsx` (no secrets) |
| `S14_excel_task1.png` | Excel domain Task 1 excerpt (if available) |

### Suggested steps

```text
1. docker compose up --build
2. docker compose exec api python /scripts/ingest_portfolio.py --all
3. Open UI / health / docs / Neo4j and capture
4. docker compose exec api pytest /tests -q
5. docker compose exec api python /scripts/verify_chat.py
```

**Priority:** S01–S11 and S13 first; optional ones if time allows.

---

## Section B — Diagrams (draw + export PNG)

These are diagrams (not live UI). Export with the exact names:

| Filename (exact) | Content |
|------------------|---------|
| `fig_01_genai_tracks.png` | Chatbot vs NL Query vs Backtesting |
| `fig_01_project_timeline.png` | Project timeline |
| `fig_01_impl_phases.png` | Implementation phases |
| `fig_02_engagement_context.png` | Engagement / company context |
| `fig_03_portfolio_concept.png` | Portfolio / holdings concept |
| `fig_03_domain_to_graph.png` | Domain → graph |
| `fig_04_scope_boundary.png` | MVP scope boundary |
| `fig_05_actors_context.png` | Actors / system context |
| `fig_05_journeys_overview.png` | Journeys J1–J5 |
| `fig_06_feature_tiers.png` | MVP / Planned / Future |
| `fig_07_trd_architecture.png` | TRD architecture |
| `fig_07_chat_sequence.png` | TRD chat sequence |
| `fig_08_tech_stack.png` | Tech stack layers |
| `fig_09_logical_architecture.png` | Logical architecture |
| `fig_09_chat_sequence.png` | As-built chat sequence |
| `fig_09_ingest_flow.png` | Ingest flow |
| `fig_10_graph_schema.png` | Neo4j schema |
| `fig_10_json_mapping.png` | JSON → graph mapping |
| `fig_10_dual_memory.png` | Redis + Neo4j dual memory |
| `fig_11_graphrag_vs_vector.png` | GraphRAG vs vector RAG |
| `fig_11_graphrag_pipeline.png` | GraphRAG pipeline |
| `fig_11_guardrails_flow.png` | Guardrails flow |
| `fig_12_module_collab.png` | Backend modules |
| `fig_12_mood_pipeline.png` | Mood pipeline |
| `fig_13_j1_ingest.png` | Journey J1 |
| `fig_13_j2_chat.png` | Journey J2 |
| `fig_14_api_anatomy.png` | `/chat` API anatomy |
| `fig_15_feature_map.png` | Features F01–F12 |
| `fig_16_test_strategy.png` | Test strategy |

**Already present:** `01_college_logo.png` — no need to redo.

---

## Quick checklist

- [ ] Section A screenshots captured  
- [ ] Files uploaded to Overleaf `images/` with exact names  
- [ ] Section B diagrams added where possible  
- [ ] Chapter 2 stakeholder names + timeline reviewed  
- [ ] Overleaf compiles and figures look fine  

---

Thank you — feel free to ping if anything in the draft is unclear.

Atharv
