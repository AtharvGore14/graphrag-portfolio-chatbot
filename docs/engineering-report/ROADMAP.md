# Chapter Roadmap & Page Budget (**80+ pages**)

**Target:** **at least 80 pages** (comfortable band **80–95**; aim ~**85–90**).  
Full per-chapter writing instructions live in each phase `README.md`.

---

## Status labels

| Label | Meaning |
|-------|---------|
| **Implemented** | In repo / runnable |
| **Planned** | Approved next increment (not built) |
| **Future Scope** | PRD Future / production beyond Compose / sibling orchestration |

---

## How we hit 80+ (without fluff)

1. Full figures + screenshots (placeholders already wired)  
2. Deeper Ch 3 finance + Excel narrative  
3. Richer Ch 9–12 architecture (diagrams + module detail)  
4. Ch 15 feature sheets ~½–¾ page each (F01–F12)  
5. Ch 16 with real test outputs pasted  
6. Appendix with full screenshot set + API samples  

Avoid: repeating the same paragraph in PRD and TRD chapters — expand with tables, flows, and evidence instead.

---

## Front matter (~5–7 pages) — Phase 1 / 6

| Part | Pages | Phase |
|------|------:|------:|
| Cover + Document Control | 2–3 | 1 |
| Acknowledgement | 1 | 1 |
| Executive Summary | 1.5–2 | **6** (write last) |
| TOC / LoF / LoT / Abbreviations | 2–3 | auto + finalize in 6 |

---

## Chapters (expanded budget)

| Ch | Title | Pages | Phase | Primary sources |
|---:|-------|------:|------:|-----------------|
| 1 | Project Background and Development Journey | 5–6 | 1 | meetings, development logs, `planning/06` |
| 2 | Company Overview | 2.5–3.5 | 1 | Meeting_01, design notes — **no invented company facts** |
| 3 | Finance Domain Learning | 5–7 | 1 | Meeting_02/03, finance learnings, PRD §10 |
| 4 | Problem Statement | 3–3.5 | 2 | `planning/01-PRD.md` |
| 5 | Requirement Analysis | 4–5 | 2 | PRD, TRD, `04-app-flow`, `intent.py` |
| 6 | Product Requirement Document | 4–5 | 2 | `planning/01-PRD.md` |
| 7 | Technical Requirement Document | 4–5 | 2 | `planning/02-TRD.md`, `.env.example` |
| 8 | Technology Stack | 3–3.5 | 2 | TRD, `requirements.txt`, Compose |
| 9 | System Architecture | 5–6 | 3 | `main.py`, `chat.py`, TRD |
| 10 | Database Design | 4.5–5.5 | 3 | `05-backend-schema`, `schema.py`, `ingest.py` |
| 11 | GraphRAG Architecture | 4.5–5.5 | 3 | `retrieve.py`, `guardrails.py`, `system.txt` |
| 12 | Backend Architecture | 5–6 | 3 | `backend/app/services/*` |
| 13 | Application Workflow | 4–5 | 4 | `04-app-flow.md`, `chat.py` |
| 14 | API Documentation | 3–4 | 4 | `schemas.py`, routes, Swagger |
| 15 | Features Implemented | 6–8 | 4 | PRD MVP + code evidence |
| 16 | Testing and Validation | 5–6 | 5 | `tests/`, `scripts/verify_*` |
| 17 | Deployment | 3.5–4.5 | 5 | `README.md`, Compose, Dockerfile |
| 18 | Challenges and Solutions | 3–3.5 | 6 | meetings, TRD risks, Action_Items |
| 19 | Learning Outcomes | 3–3.5 | 6 | cross-cutting |
| 20 | Future Scope | 2–2.5 | 6 | PRD §6, TRD §8 |
| 21 | Conclusion | 1.5–2 | 6 | goals + handoff |
| A | Appendices | 7–10 | 6 | screenshots, API samples, meetings |

**Sum estimate:** ~**83–100** pages with figures filled.  
**Floor:** **80**. Soft ceiling ~**100** (trim appendix if needed).

### If under 80 after compile
- Expand Ch 3, 9–12, 15, 16 first  
- Add missing screenshots/diagrams  
- Lengthen Executive Summary with outcome metrics  

### If over ~100
- Move long code/API dumps to Appendix only  
- Cap feature sheets; avoid PRD/TRD duplication  

---

## Phase page rollup

| Phase | Focus | Target pages (cumulative after phase) |
|------:|-------|--------------------------------------:|
| 1 | Front + Ch 1–3 | ~18–24 |
| 2 | Ch 4–8 | ~38–48 |
| 3 | Ch 9–12 | ~57–70 |
| 4 | Ch 13–15 | ~70–87 |
| 5 | Ch 16–17 | ~79–98 |
| 6 | Ch 18–21 + App + Exec Summary | **80–100+** |

---

## Chapter files (LaTeX)

```text
docs/engineering-report/latex/
  main.tex
  chapters/ch01_journey.tex … ch21_conclusion.tex
  chapters/appendix.tex
  images/
```
