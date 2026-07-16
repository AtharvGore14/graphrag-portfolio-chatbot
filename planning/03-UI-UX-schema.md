# 03 — UI/UX Schema

**Product:** Portfolio GraphRAG Chatbot (API-first)  
**Status:** Approved  
**Depends on:** `01-PRD.md`, `02-TRD.md` (approved)  
**Folder:** `planning/`

---

## 1. Scope reminder

MVP UI is a **minimal test page** to exercise the chat API. Product experience lives in a separate host app (out of scope). Design priority: clarity and speed of testing — not branding or marketing polish.

---

## 2. Information architecture / sitemap

```
/                    → Test chat page (only screen)
/docs (optional)     → FastAPI Swagger/OpenAPI (built-in), not a custom UI
```

No signup, settings, portfolio dashboard, or multi-page nav in MVP.

---

## 3. Key screen — Test chat page

### Purpose

Send a message with a `user_id`, see grounded answer + mood + citations, confirm refusals when data is missing.

### Wireframe (desktop)

```
┌─────────────────────────────────────────────────────────┐
│  Portfolio GraphRAG — Test                              │
├─────────────────────────────────────────────────────────┤
│  user_id  [________________]  session_id [____________] │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Conversation                                      │  │
│  │                                                   │  │
│  │  You: How much Adani Power do I hold?             │  │
│  │  Bot: You hold 1661 shares of ADANIPOWER …        │  │
│  │       mood: fear (0.72)                           │  │
│  │       sources: Holding:ADANIPOWER, Stock:…        │  │
│  │                                                   │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  [ Type a portfolio question…              ] [ Send ]   │
│  status: idle | thinking… | error                        │
└─────────────────────────────────────────────────────────┘
```

### Wireframe (mobile)

Same single column: identity fields → transcript → composer. No side panels.

### Layout rules

- One composition: identity strip + transcript + composer (no dashboard cards/stats).  
- No hero marketing, no portfolio charts on this page.  
- Citations and mood shown as plain secondary text under each bot reply (not badges/stickers).

---

## 4. Component inventory

| Component | Behavior |
|-----------|----------|
| **UserIdField** | Required text input; persisted in `localStorage` for reloads |
| **SessionIdField** | Optional; auto-generate UUID if empty; used for Redis short-term memory |
| **Transcript** | Scrollable list of user/bot messages |
| **UserBubble** | Plain message text |
| **BotBubble** | Answer text + mood line + citations list + optional “no data” state |
| **Composer** | Textarea + Send; Enter to send (Shift+Enter newline) |
| **StatusLine** | Idle / loading / error message from API |
| **ClearSession** (optional) | Clears transcript + new `session_id` (does not wipe Neo4j) |

No modals, tabs, nav bars, or charts in MVP.

---

## 5. Content & response presentation

### Bot message structure (UI binding)

```text
{answer}

Mood: {label} ({confidence})   |   or: Mood: not enough signal

Sources:
- {node_type}:{id_or_ticker} …
```

### Empty / refuse states

| Case | UI |
|------|-----|
| Missing `user_id` | Inline validation; do not call API |
| API 4xx/5xx | StatusLine shows error; no fake bot answer |
| “I don’t have that data” | Show as normal bot text (honest refuse) |
| Low mood confidence | Show “not enough signal” — do not invent a label |

### Loading

- Disable Send while request in flight.  
- Optional: show “thinking…” in StatusLine (streaming is v1.1).

---

## 6. Design tokens (test page — keep minimal)

Functional, not brand-led. Avoid purple-gradient / cream-serif AI defaults.

| Token | Value |
|-------|-------|
| `--bg` | `#f7f7f5` |
| `--ink` | `#1a1a1a` |
| `--muted` | `#5c5c5c` |
| `--line` | `#d9d9d4` |
| `--accent` | `#0b6e4f` (actions only) |
| `--danger` | `#9b1c1c` |
| Font | System UI stack OK for test page (`ui-sans-serif, system-ui, …`) |
| Spacing | 8px grid (8 / 16 / 24) |
| Radius | 4px inputs/buttons (no pill clusters) |

Typography: one size for body (~15–16px), slightly smaller for mood/sources (~13px muted).

---

## 7. Interaction notes

| Action | Result |
|--------|--------|
| Send | `POST /chat` with `{ user_id, session_id, message }` |
| Success | Append user + bot bubbles; scroll to bottom |
| Failure | Keep composer text; show StatusLine error |
| Change `user_id` | New queries use new id (warn: transcript may mix users — optional clear on change) |

Keyboard: focus composer on load; Escape cancels nothing in MVP (no abort unless cheap).

---

## 8. Responsive & accessibility

| Topic | MVP bar |
|-------|---------|
| Responsive | Single column; usable ≥320px width |
| Contrast | Ink on light bg; accent for buttons only |
| Focus | Visible focus ring on inputs/button |
| Labels | Visible labels on `user_id` / `session_id` (not placeholder-only) |
| Screen readers | Bot mood/sources as text in the same message region |
| Motion | None required; no decorative animation |

---

## 9. Out of scope for UI

- Portfolio tables, sector charts, login screens  
- Mood history timeline UI  
- Admin ingest UI (CLI script only)  
- Dark mode, design system library, component frameworks (vanilla or one thin page is enough)

---

## 10. Mapping to API (UI contract)

| UI field | API field |
|----------|-----------|
| UserIdField | `user_id` |
| SessionIdField | `session_id` |
| Composer text | `message` |
| Bot answer | `answer` |
| Mood line | `mood.label`, `mood.confidence`, `mood.insufficient_signal` |
| Sources | `citations[]` |

Exact JSON shapes in `05-backend-schema.md`.

---

**Review checkpoint:** Edit this doc or reply **“UI/UX approved”** to proceed to `04-app-flow.md`.
