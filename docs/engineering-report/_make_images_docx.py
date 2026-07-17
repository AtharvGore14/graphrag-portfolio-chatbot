"""Generate Word attachment: Images Needed for Documentation."""
from docx import Document
from docx.shared import Pt

doc = Document()
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)

doc.add_heading("Images needed from Aayush (Lathi)", 0)
p = doc.add_paragraph()
run = p.add_run("Portfolio GraphRAG Chatbot — SEDD (22 figures)")
run.italic = True

doc.add_paragraph("Repo: https://github.com/AtharvGore14/graphrag-portfolio-chatbot")
doc.add_paragraph(
    "LaTeX path: docs/engineering-report/latex/images/  |  "
    "Overleaf: https://www.overleaf.com/1656157384wxcgqvgpkpdx#c9a2af"
)
doc.add_paragraph(
    "Exact PNG filenames. No API keys/passwords. "
    "Logo already done — skip 01_college_logo.png."
)

doc.add_heading("Batch 1 — Screenshots (10)", level=1)
shots = [
    ("S01_compose_healthy.png", "Compose healthy (docker compose ps)"),
    ("S02_health_json.png", "http://localhost:8000/health"),
    ("S03_swagger_docs.png", "http://localhost:8000/docs"),
    ("S05_ui_grounded_answer.png", "UI demo + ADANIPOWER holdings + citations"),
    ("S06_ui_refuse.png", "UI unknown ticker → refuse"),
    ("S08_neo4j_subgraph.png", "Neo4j Browser demo subgraph"),
    ("S09_ingest_cli.png", "ingest_portfolio.py --all success"),
    ("S10_pytest.png", "pytest /tests -q"),
    ("S11_verify_scripts.png", "verify_chat / verify_questions success"),
    ("S13_env_example_redacted.png", ".env.example with secrets blurred"),
]
t = doc.add_table(rows=1 + len(shots), cols=2)
t.style = "Table Grid"
t.rows[0].cells[0].text = "Exact filename"
t.rows[0].cells[1].text = "What to capture"
for r, row in enumerate(shots, 1):
    t.rows[r].cells[0].text = row[0]
    t.rows[r].cells[1].text = row[1]

doc.add_heading("Batch 2 — Diagrams (12)", level=1)
figs = [
    ("fig_08_tech_stack.png", "Client → FastAPI → Neo4j/Redis/Mood/LLM/Compose"),
    ("fig_09_logical_architecture.png", "Client, FastAPI, Neo4j, Redis, Mood, LLM"),
    ("fig_09_chat_sequence.png", "One POST /chat turn sequence"),
    ("fig_09_ingest_flow.png", "JSON → ingest → Neo4j"),
    ("fig_10_graph_schema.png", "User→Portfolio→Sector/Holding→Stock (+MoodEvent)"),
    ("fig_10_dual_memory.png", "Redis short-term vs Neo4j long-term"),
    ("fig_11_graphrag_pipeline.png", "Intent→Cypher→cite→generate→guardrails"),
    ("fig_11_guardrails_flow.png", "Empty/advice/ungrounded → refuse"),
    ("fig_12_module_collab.png", "chat.py + services"),
    ("fig_14_api_anatomy.png", "/chat request + response fields"),
    ("fig_15_feature_map.png", "F01–F12 grid"),
    ("fig_16_test_strategy.png", "Unit / verify / manual"),
]
t = doc.add_table(rows=1 + len(figs), cols=2)
t.style = "Table Grid"
t.rows[0].cells[0].text = "Exact filename"
t.rows[0].cells[1].text = "What to show"
for r, row in enumerate(figs, 1):
    t.rows[r].cells[0].text = row[0]
    t.rows[r].cells[1].text = row[1]

doc.add_paragraph(
    "Do NOT make: S04, S07, S12, S14, Swagger try-it, "
    "or old fig_01…fig_07 / json_mapping / mood_pipeline / J1–J2 charts."
)
doc.add_paragraph("Thanks!")

out = (
    r"E:\AlgoFabric_Final\graphrag-portfolio-chatbot"
    r"\docs\engineering-report\Images_Needed_for_Documentation.docx"
)
doc.save(out)
print("Saved:", out)
