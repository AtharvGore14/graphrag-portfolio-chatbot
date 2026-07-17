# Meeting 02 — Sprint sync (demos & domain tasks)

- **Date:** Wednesday, 4 Feb 2026  
- **Participants:** Garv; Prerana; Radhika; faculty mentors present for GenAI groups; students (NL Query / Backtesting teams confirmed present; Chatbot group expected to follow shared task / MoM process)  
- **Duration:** ~ (extended; transcript covers demos + Task 1 review)  
- **Objective:** Demo current agents, clarify motivation, circulate domain task list, set MoM / closed-loop expectations.

> **Chatbot-team lens:** This call was dominated by **NL Query** and **Backtesting** demos. For Chatbot we capture shared process, domain training, and what was *not* covered yet for our track.

---

## Agenda

1. Confirm students received GitHub / task materials  
2. Demo NL Query Agent  
3. Demo Backtesting Agent  
4. (Planned) Chat part — not the focus of the recorded walkthrough  
5. Explain domain Task 1 (Excel-first finance literacy)  
6. Review early Task 1 attempts; Q&A  

---

## Discussion Summary

### Process (applies to Chatbot team)

- GitHub repo / task list shared via Prerana; students to study over the weekend.  
- Faculty expectation: **every student sends MoM / short reflection** after meetings so industry mentors see understanding early (closed loop). Mentors should check MoMs.  
- Agenda order mentioned: NL Query → Backtesting → **chat part**; the detailed demo time was spent on the first two.

### Sibling demos (context only)

- **NL Query:** market select (India / US), natural-language filters on many ratios, chain-of-thought → code gen → execute → plots/summary. Motivation: produce stock lists for historical “what if I invested in these fundamentals” workflows. Later: memory, confidence, fewer useless plots, misspelling / clarification. Integrate with Backtesting later via orchestrator/API — not Chatbot MVP.  
- **Backtesting:** strategy + stock list → plan/interpret → fetch history → indicators → trades → plots + portfolio metrics (annualized return, volatility, drawdown, etc.).

### Domain Task 1 (shared literacy — Chatbot team should complete)

- Prefer **Excel** for formulas (not ChatGPT-written Python), except Yahoo Finance download may use Python.  
- Suggested tickers for comparability: **TCS, M&M, ITC**; **3 years**; **daily OHLC**; metrics on **close**.  
- Compute: normal & log returns; annualized return / volatility; max drawdown; Sharpe; stock-level and **portfolio-level** (covariance); theory on ROE/ROCE, PE/PB, alpha/beta (linear regression).  
- Early student review (ITC): formula sanity, negative annualized return when end &lt; start, volatility as risk, drawdown as peak-to-trough (report as positive magnitude).  

### Chatbot-specific content in this meeting

- No dedicated Chatbot product demo captured in the transcript portion provided.  
- Chatbot team still accountable for MoMs, domain tasks, and waiting on / requesting Chatbot access & demo (see Meeting_01 actions).

---

## Technical Decisions

| Decision | Notes |
|----------|-------|
| MoM after every meeting | Closed-loop feedback |
| Domain Task 1 in Excel-first style | Shared across GenAI students |
| Focus robustness of sibling agents before integration | Does not change Chatbot MVP unless later agreed |

---

## Action Items

| Action | Owner | Due |
|--------|-------|-----|
| Study GitHub task repo; finish Task 1 (and follow-ons) | Chatbot students | Weekend / ongoing |
| Send MoM / reflection after this meeting | Each Chatbot student | Promptly |
| Mentors verify MoMs | Faculty mentors | Ongoing |
| Still owed from kickoff: Chatbot remote access + demo + sample queries | Industry | Open |

---

## Risks / Issues

| Risk / issue | Impact on Chatbot |
|--------------|-------------------|
| Chatbot demo / access not yet in this sync | Domain work proceeds; product exploration blocked or delayed |
| Students may not open tasks until explained | Mitigated by live walkthrough of Task 1 |

---

## Open Questions

- When is the dedicated **Chatbot** demo and access link?  
- Which Chatbot sample queries (good/bad) should we run first once access exists?  

---

## Next Steps

1. Complete domain tasks; keep MoMs flowing.  
2. Chase Chatbot access / demo via Prerana.  
3. Next sync: bring task results and any Chatbot exploration notes if access is live.  

---

## References

- Fireflies: Wed, 4 Feb  
- Shared GitHub task repository (via Prerana)  
- `docs/meetings/Meeting_01_Kickoff.md`  
- `docs/development/Action_Items.md`  
