# Finance Portfolio Chatbot – System Architecture

![[finance_portfolio_chatbot_architecture.svg]]
Here's a comprehensive architecture for a RAG-based portfolio Q&A chatbot (similar to Rufus, but scoped to personal/institutional finance portfolios):Here's a breakdown of each layer and the key design decisions that keep the chatbot strictly within the user's portfolio:

**User interface** — standard chat surface (web or mobile). Nothing special here, but every request carries the authenticated user's identity token.

**API gateway** — two jobs: (1) authenticate the user and enforce rate limits; (2) attach the conversation history so the LLM always has context about what's been asked before. Both components enforce user-level scoping at the earliest possible point.

**NLU layer** — this is where the "scope guard" lives, which is the most important component for a portfolio-only bot. It classifies the intent (holdings query, P&L, risk, allocation), extracts entities (ticker symbols, date ranges, account IDs), and then hard-rejects any query that falls outside portfolio scope before it ever reaches the retrieval layer.

**Retrieval engine (RAG)** — three-stage pipeline:

- The query builder converts parsed intent + entities into structured filters (user_id, date, asset class)
- Vector search finds semantically similar chunks from the user's embedded portfolio documents
- The context assembler ranks and merges the retrieved chunks into the final prompt context

**LLM inference** — the system prompt is the second enforcement layer: it explicitly instructs the model that it has no access to external market data, news feeds, or anything outside the injected context. This prevents the LLM from using its training knowledge to answer "what's Apple's stock price today."

**Guardrail filter + formatter** — the output is checked to catch hallucinated ticker prices or positions that don't appear in the source data, then formatted into tables, charts, or plain text with citations pointing back to the portfolio records.

**Data layer** — four stores, all portfolio-scoped and user-isolated: a holdings DB (current positions, cost basis), a transactions DB (buy/sell history, dividends), a snapshot store (end-of-day valuations for P&L queries), and a vector DB containing pre-embedded chunks of the user's portfolio data for semantic search.