# Meeting 03 — Sprint sync (task progress & process)

- **Date:** Thursday, 19 Feb 2026  
- **Participants:** Garv; Prerana; Ms Mayuri Shahir; students including Aryaa Sharma, Jha Aryan, Atharva Kulkarni, Apoorva Kulkarni; others joining / partial (e.g. Ashish traveling). Rohini ma’am’s group represented for task status; Chatbot faculty may not have been on the full call.  
- **Duration:** ~22 minutes (timestamped transcript)  
- **Objective:** Review domain-task progress and doubts; tighten team communication; confirm readiness before deeper Chatbot build work.

> **Chatbot-team lens:** Treat this as **shared GenAI onboarding / finance literacy** for our team. Chatbot product deep-dives were limited; process and domain clarity are the durable takeaways.

---

## Agenda

1. Updates on GitHub tasks + documentation review  
2. Clarify Task 1 metrics issues (Sharpe, volatility signs)  
3. Clarify alpha / beta / R² confusion (Task 2)  
4. Assign clearer team communication ownership  
5. Status from other GenAI groups; schedule next sync when tasks are done  

---

## Discussion Summary

### Progress

- Students worked through the shared GitHub tasks and documentation; some tried example queries from the prior demo.  
- Task completion uneven across people/groups; need aggregated status rather than ad-hoc individual polling.

### Domain clarifications (Chatbot team should internalize)

- **Sharpe:** risk-adjusted return / volatility. Volatility (σ) cannot be negative; Sharpe can be negative if excess return is negative. Risk-free rate assumed **0** per task repo.  
- Different students’ Sharpe values can differ if Yahoo pull **end dates** differ; small differences OK, order-of-magnitude gaps need formula checks.  
- **Alpha:** excess return vs market (from regression).  
- **Beta:** sensitivity / slope vs market (e.g. if market +1%, how much does the stock move).  
- **R²:** strength / goodness of fit of that relationship — not the same as beta; more “how well does the model explain,” less “how much does it move.”  
- Data caveat: corporate actions (e.g. demerger) can break clean 3-year series — substituting a ticker is acceptable if the repo allows it.

### Chatbot / tooling notes

- A student reported **chatbot crashes** even on simple queries. Clarification in-call: for the **NL Query** playground, use **India** data only for now; **US** data too large for the free server. Wait through latency on free hosting; better hosting later.  
- That crash guidance is for the sibling NL Query app — still a reminder that **hosted demos can be flaky**; document Chatbot stability separately when we have our own URL.

### Process

- Nominate a **team lead / communication person** who aggregates who finished what and what blocked them (optional shared Excel).  
- Industry wants domain training done properly before “real” Chatbot implementation confidence.  
- Next meeting only once there is confidence tasks are done; Prerana to schedule against Garv’s calendar.

---

## Technical Decisions

| Decision | Notes |
|----------|-------|
| Risk-free rate = 0 for Sharpe in Task 1 | Per repo |
| Prefer India market on shared NL Query free server | Sibling tooling; awareness for Chatbot hosting later |
| Appoint student communication lead + status sheet | Process |

---

## Action Items

| Action | Owner | Due |
|--------|-------|-----|
| Elect communication lead; maintain status sheet | Chatbot student team | Immediately / next day |
| Finish remaining domain tasks (incl. Task 3 / alpha where pending) | Each member | Before next sync |
| Aggregate per-member update for mentors | Team lead | Next sync |
| Schedule next meeting when tasks verified | Prerana | TBD |
| Continue MoMs | Students | Ongoing |

---

## Risks / Issues

| Risk / issue | Impact on Chatbot |
|--------------|-------------------|
| Inconsistent task results / incomplete members | Delays start of serious Chatbot implementation |
| Free-tier crashes / latency on demos | Poor first impressions; need stable Chatbot host |
| No single owner for team updates | Mentors cannot see true progress |

---

## Open Questions

- Who is Chatbot team lead (name)?  
- Chatbot remote access / dedicated demo still outstanding from Meeting_01?  
- Exact Task 3 completion criteria for “ready for next meeting”?  

---

## Next Steps

1. Finish domain tasks; nominate lead; sheet updates.  
2. Confirm Chatbot access path with Prerana.  
3. Next sync: member-by-member task status, then Chatbot build plan.  

---

## References

- Fireflies: Thu, 19 Feb (timestamped transcript)  
- Shared GitHub task repository  
- `docs/meetings/Meeting_02.md`  
- `docs/development/Action_Items.md`  
- `docs/development/Decision_Log.md`  
