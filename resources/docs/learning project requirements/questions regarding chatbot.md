Great argument to pressure-test the architecture.
If NL Query + Backtesting were fully sufficient, the chatbot team would be unnecessary — so the right way is to ask decision-driving questions like these:

Core Challenge Questions
- If both agents return outputs, who decides which one to trust when they conflict?
- Who converts technical payloads into a single user-safe answer instead of two raw outputs?
- Who ensures responses never violate finance-safe language (no guarantees, no misleading certainty)?
- Who handles ambiguous prompts like “is this strategy better now?” where intent could be factual + predictive + comparative?
- Who maintains multi-turn context (“as I said earlier use the same stock and window”) across agent calls?
- Orchestration Necessity Questions
- When should a user query hit NL only, Backtesting only, or both in parallel?
- If one service times out and the other succeeds, what is the fallback response policy?
- Who normalizes inputs (entities, time range, assumptions) into a strict interface both services can consume?
- Who combines confidence, assumptions, and evidence into one ranked final output?
- Trust, Safety, and UX Questions
- Who adds citations and “why this answer” trace for auditability?
- Who decides when confidence is too low and escalation to a human is required?
- Who adapts tone for beginner vs investor vs advisor without changing core facts?
- Who asks clarifying questions before running expensive/incorrect backtests?
- Product Ownership Questions
- If users complain “answer was confusing,” which team owns fixing explanation quality?
- If hallucination rate increases, which team tracks groundedness/helpfulness metrics end-to-end?
- Who owns chat latency budget across all downstream agents?
- Who owns user feedback loops and prompt/policy tuning over time?
- Strategic Framing Question (Most Important)
- Are we building two specialist engines, or a reliable decision-assistant product?
- Engines alone: NL + Backtesting may be enough.
- Product-grade assistant: you still need chatbot-team orchestration, safety, grounding, and UX ownership.
- If you want, I can add a section to PROJECT_OVERVIEW.md titled “Why Chatbot Team Is Needed Even With NL + Backtesting” with these questions and clear answers for your project defense/presentation.