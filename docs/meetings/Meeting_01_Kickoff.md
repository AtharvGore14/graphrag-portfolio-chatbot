# Meeting 01 — Kickoff (GenAI tracks)

- **Date:** Thursday, 29 Jan 2026  
- **Participants:** Aniruddha Pant; Garv; Prerana; Radhika (faculty side); VIT faculty mentors (incl. intro for NL Query / Backtesting mentors; Chatbot faculty mentor named as Dr. Bharadwaj — not present for full intro); student / mentor attendees on the GenAI rows of the project sheet  
- **Duration:** ~ (not recorded precisely in transcript)  
- **Objective:** Align on AlgoFabric GenAI problem statements (NL Query Agent, Backtesting Agent, AlgoFabric Chatbot), remote onboarding plan, communication channels, and first-week expectations.

> **Chatbot-team lens:** Notes below prioritize the **AlgoFabric Chatbot** track. Sibling agents are summarized only for context.

---

## Agenda

1. Confirm GenAI scope (sheet rows for NL Query, Backtesting, Chatbot)  
2. Clarify what each agent does and remote availability  
3. Agree first-week plan: access, starter kit, demos  
4. Communication (WhatsApp vs Google Chat) and mentoring structure  
5. Faculty mentor introductions  
6. Domain material and longer-term technical challenges  

---

## Discussion Summary

### Chatbot definition (our track)

- **AlgoFabric Chatbot** = Q&A over AlgoFabric datasets / databases: ask natural-language questions and get responses grounded in that data.  
- Distinct from:
  - **NL Query Agent** — filter stocks by fundamental criteria (e.g. ROE thresholds over years); produces a stock list.  
  - **Backtesting Agent** — apply a strategy (buy/hold, RSI rules, etc.) on a stock list and evaluate historical performance.  
- Industry note: the Chatbot is **not** the same as treating “AlgoFabric Chatbot” as the current trading / NL / backtest bots; the expansion path is closer to the **existing AlgoFabric website semantic-search chatbot** (ticker-related data), to be extended over time.

### Availability / onboarding

- NL Query and Backtesting were described as already usable remotely (e.g. Streamlit / Algo Analytics hosting).  
- **Chatbot** was described as **not yet public** for student playground use — still part of the AlgoFabric application. Making it available remotely (or clarifying access) is an industry-side prerequisite for our play week.  
- Plan: one-pager + sample queries (good and bad) + demo; students spend ~one week exploring from a **domain** perspective, then feed back good/bad/ugly outputs in the next meeting.  
- After that: either improve from shared codebase or rebuild with provided data — decision deferred.  
- Separate **demo calls per group** (three calls) preferred over one mixed session. Weekly group calls with mentors; Prerana coordinates.

### Mentoring & communication

- Prerana = coordinator / POC; Bharadwaj for escalation.  
- Technical mentors (Garv, Rohit, Chidambarish) may be busy with customer work — Prerana stays in groups to unblock.  
- **Chatbot faculty mentor:** Dr. Bharadwaj.  
- WhatsApp group exists for AlgoFabric admin; **Google Chat** preferred for technical discussion (external-allowed groups; possibly via Amar). Prefer **separate groups per workstream**, merge later if useful.

### Technical direction relevant to Chatbot

- Hard boundaries between the three GenAI projects are soft; students get parallel exposure.  
- Harder queries need correlating **tabular + unstructured** information.  
- **Video** financial sources mentioned as possible later — **not** current scope.  
- Domain training material (returns, log returns, annualized returns, etc.) to be shared — relevant for all AlgoFabric GenAI students, including Chatbot.  
- Side note (not Chatbot delivery): NL Query + Backtesting may later integrate into one chatbot via an orchestrator; develop separately first.

### Other (recorded briefly; not Chatbot delivery)

- Production / strategy internship tracks and hiring interest were discussed for other sheet rows.  
- AI Summit stall / branding offer — take offline.

---

## Technical Decisions

| Decision | Notes |
|----------|-------|
| Chatbot = AlgoFabric data Q&A track | Not NL screening or backtesting |
| Start from semantic-search / AlgoFabric chatbot direction | Expand beyond portfolio-only ticker search over time |
| Tabular + unstructured correlation is a core hard problem | Video deferred |
| Soft boundaries across GenAI teams | Parallel learning intentional |
| Google Chat for tech; WhatsApp for admin | Separate per-group chats |

*(Also logged in `docs/development/Decision_Log.md`.)*

---

## Action Items

| Action | Owner | Due |
|--------|-------|-----|
| Make Chatbot available remotely (or define interim access) + starter kit | Garv / Prerana | Target ~Monday after kickoff |
| One-pager + sample queries (working / failing) for Chatbot | Industry | With access |
| Separate Chatbot demo call | Prerana | Soon after access |
| Domain study material share | Industry | ASAP |
| Google Chat group(s) + add mentors; numbers to Radhika | Prerana / Garv | ASAP |
| Students: explore ~1 week after access; prepare feedback | Chatbot team | +1 week from access |

---

## Risks / Issues

| Risk / issue | Impact on Chatbot |
|--------------|-------------------|
| Chatbot not yet remotely usable | Blocks play-week and sample-query feedback |
| Streamlit / free hosting flakiness (mentioned for other bots) | Expect restarts; prefer stable host later |
| Soft project boundaries | Scope creep if Chatbot team is pulled into NL/backtest delivery |

---

## Open Questions

- Exact remote URL / access path for **Chatbot** (vs app-only)?  
- What datasets (beyond portfolio / ticker semantic search) are in Chatbot scope for this engagement?  
- Improve existing codebase vs greenfield — which path for Chatbot?  
- Who is the named technical mentor for Chatbot day-to-day (Garv / Rohit / Chidambarish)?  

---

## Next Steps

1. Industry: Chatbot access + kit + demo.  
2. Chatbot team: domain material + exploration once access exists.  
3. Next sync: report Chatbot outputs (good / bad / ugly) and agree improvement path.  

---

## References

- Fireflies notebook (source recording): Thu, 29 Jan — AlgoFabric_VIT_GenAI Team  
- Project Google Sheet (GenAI rows)  
- `docs/development/Decision_Log.md`  
- `docs/development/Action_Items.md`  
- `docs/design/AlgoFabric_Chatbot.md`  
