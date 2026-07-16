Here's the full picture, pulled together from everything baked into the architecture so far — anti-hallucination isn't one feature, it's enforced at every layer:

## 1. Mood detection — deterministic classifier, not LLM guesswork
The LLM never infers mood on its own. A dedicated emotion classifier (DistilRoBERTa) outputs a structured label + confidence score from the user's text. The LLM's only job downstream is to *phrase* that already-computed label back — it cannot invent a mood that wasn't detected.

**Guardrail**: if the classifier's confidence is below a threshold, respond with something like "not enough signal to read your mood right now" instead of forcing a guess.

## 2. Portfolio answers — grounded retrieval only, never memory recall
Every factual claim about holdings must come from an actual Cypher query result against Neo4j — the LLM is never allowed to answer "from what it knows" about a stock or the user's portfolio.

**Guardrail**: if the graph query returns no relevant nodes, the system returns "I don't have that data" rather than letting the LLM fill the gap from its own training knowledge (which is exactly where hallucination creeps in with financial data — the LLM might "remember" a stock price that's stale or wrong).

## 3. Mandatory citation/source-binding
Every response that states a fact must be traceable back to the specific node(s) it was pulled from. This isn't just a nice-to-have — build it as a **structural requirement**: the prompt template forces the model to only use the retrieved subgraph as context (nothing else), and you can programmatically check that any ticker/number mentioned in the output actually exists in what was retrieved.

## 4. Single retrieval → single generation (no multi-hop agent reasoning)
We already decided against an orchestrator partly for latency, but it's also an anti-hallucination choice: multi-step agent chains give the model more opportunities to reason its way into a wrong or invented conclusion. One clean retrieval, one grounded prompt, one answer — fewer places for drift to creep in.

## 5. "Analyser not suggester" response filter
A post-generation validation step scans the LLM's draft output for advisory/speculative language ("you should," "I recommend," "this will likely go up") and either strips it or forces a regeneration with a stricter system prompt. This catches a specific hallucination failure mode: models tend to *editorialize* even when asked not to — this is a hard architectural check, not just a prompt instruction (prompts alone get ignored under certain phrasings).

## 6. Strict system prompt constraints
The system prompt explicitly instructs the model: only use provided context, never speculate, never give financial advice, and explicitly say "I don't know" or "I don't have that data" when context is insufficient. This alone isn't reliable (models drift), which is why layers 3 and 5 exist as backstops — never rely on prompting alone for a hard requirement.

## 7. Observability — every call is traceable
Using something like **Langfuse** to log every LLM call with its exact input context and output. This doesn't *prevent* hallucination, but it means when one slips through, you can see precisely what context the model had and fix the retrieval or prompt — critical since "no hallucination" is a claim you'll need to keep proving over time, not just at launch.

## 8. Scoped, minimal context window
Only the relevant subgraph for that specific user + question is passed to the model — not their entire portfolio history. Smaller, tightly relevant context reduces the model's opportunity to blend in irrelevant or misremembered details, on top of helping your latency budget.

---

**The core principle tying all of this together**: nowhere in the pipeline does the LLM get to answer from its own "knowledge" — for mood, a classifier decides; for portfolio facts, the graph decides; for tone, a validator decides. The LLM's actual job is narrowed down to *only* language generation over pre-verified inputs, never fact generation or judgment. That's what makes "strong analyser, not suggester" enforceable rather than just a prompt-level hope.