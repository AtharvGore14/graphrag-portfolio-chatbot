The distinction comes down to **what each model was actually trained to detect** — they solve different problems even though both say "sentiment."

## What FinBERT actually does

FinBERT is trained on financial text (earnings calls, analyst reports, financial news) to classify content as **positive / negative / neutral** in a market sense — e.g., "Q3 earnings beat expectations" → positive, "company faces regulatory investigation" → negative.

It's answering: *"Is this financial statement bullish or bearish?"*

That's not your use case anymore. You corrected this earlier — you're not scoring news or market text, you're reading the **user's emotional state** from how they type to the chatbot: "I have no idea what's happening with my portfolio and it's stressing me out" → that's anxiety, not a bearish/bullish financial statement. FinBERT would either misclassify this (it wasn't trained on this kind of text) or force it into a positive/negative/neutral bucket that doesn't capture mood at all.

## Why DistilRoBERTa-emotion fits instead

- **Trained on the right task**: emotion classification (joy, anger, fear, sadness, surprise, neutral, etc.) from conversational/everyday text — not financial documents. This matches "how is the user feeling" directly.
- **Trained on the right domain**: general human expression, not financial jargon — your users are typing casual questions like "why does my portfolio look like this again," not writing earnings reports.
- **Output granularity fits your need**: FinBERT gives you 3 classes (pos/neg/neutral) about *content*; an emotion model gives you multiple mood classes (anxious, frustrated, confident, confused, calm) about the *person* — much richer signal for "strong analyser" of mood.
- **Lighter/faster**: DistilRoBERTa is a distilled model — smaller and faster than full RoBERTa/BERT variants, which directly helps your <2 second latency budget since this runs on every message.

## The one-line rule to keep architecture clean

- **FinBERT** → use if you're scoring sentiment *of financial content* (news, filings, market commentary) — you explicitly said you don't need this anymore.
- **Emotion classifier (DistilRoBERTa or similar)** → use for scoring the *emotional state of the user's own message* — this is your actual requirement.

Using FinBERT here would be the wrong tool for the job — it'd give you confidently wrong mood labels (a hallucination risk in itself, just from a classifier instead of an LLM), which directly conflicts with your "no hallucination, strong analyser" requirement.