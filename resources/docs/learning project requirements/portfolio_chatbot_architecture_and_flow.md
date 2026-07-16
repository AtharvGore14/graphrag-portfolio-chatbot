# 🧠 Portfolio Chatbot Architecture (RAG + Memory + Personalization)

---

## 📌 1. System Overview

This system is a **domain-specific, memory-aware financial assistant**.

It combines:
- Structured portfolio data
- Retrieval-Augmented Generation (RAG)
- User memory (short-term + long-term)
- LLM reasoning

---

## ⚙️ 2. End-to-End Data Pipeline

```
Raw JSON → Feature Extraction → LLM Summarization → Embeddings → Storage
```

---

## 🥇 STEP 1: Raw JSON Ingestion

- Input: Portfolio JSON (holdings, sectors, metrics)
- Stored as-is for integrity

**Storage:**
- S3 / Object storage
- `portfolio_snapshots` table

---

## 🥈 STEP 2: Feature Extraction (Deterministic)

No LLM involved.

Extract:
- Sector allocation
- Top gainers/losers
- Diversification level
- Risk proxies

**Example:**
```python
features = {
  "top_sector": "Basic Materials",
  "diversification": "high",
  "top_gainer": "SGB",
}
```

**Storage:**
- Structured DB (`portfolio_features`)

---

## 🥉 STEP 3: LLM Summarization

LLM converts structured data → semantic understanding

### Input to LLM:
- Extracted features
- Key metrics

### Output:
```json
{
  "investor_type": "growth investor",
  "risk_profile": "moderate",
  "strengths": ["diversified", "commodity gains"],
  "risks": ["cyclical exposure"]
}
```

---

## 🧩 STEP 4: Storage Strategy

### 🏦 Structured DB
- Risk profile
- Investor type
- Sector bias

### 🧠 Vector DB
- Embedded summary
- Conversation history
- User interests

### 📁 Object Storage
- Raw JSON snapshots

---

## 🔁 STEP 5: Query Processing Flow

```
User Query → Intent Detection → Retrieval → Context Builder → LLM → Response
```

---

## 🎯 Query Types

### 1. Portfolio-level Query
Example:
> "Am I overexposed to any sector?"

Uses:
- Sector data
- User memory

---

### 2. Stock-level Query
Example:
> "How is my Adani stock performing?"

---

## 📊 Stock Query Flow

### STEP 1: Intent + Entity Detection
```json
{
  "intent": "stock_performance",
  "entity": "ADANIPOWER"
}
```

---

### STEP 2: Structured Retrieval

From holdings:
- Avg price
- Current price
- PnL

---

### STEP 3: Context Enrichment

- Compare with portfolio return
- Add sector context

---

### STEP 4: Response Generation

Good response includes:

1. Direct metric
2. Relative performance
3. Interpretation
4. Suggestion

---

## 🧠 Memory System

### 🟢 Short-Term Memory
- Current conversation

### 🔵 Long-Term Memory
- Risk profile
- Preferences

### 🟣 Episodic Memory
- Past queries and themes

---

## 🔄 Memory Update Loop

After each query:

```json
{
  "interest": "risk",
  "engagement": "stock analysis"
}
```

---

## ⚡ Retrieval Priority

```
1. Structured DB (portfolio data)
2. Portfolio features
3. Vector DB (memory)
4. External APIs (yfinance)
```

---

## 🚀 Optional Enhancements

- Live price data via yfinance
- User embeddings for personalization
- Hybrid search (vector + structured)

---

## 🧠 Key Principle

> The system should remember **what defines the user**, not just raw data.

---

## 🎯 Final Architecture

```
Raw Data (S3)
      ↓
Feature Extraction (Python)
      ↓
LLM Summarization
      ↓
→ Structured DB
→ Vector DB
      ↓
Query Engine (RAG)
      ↓
Personalized Response
```

---

## 🧩 One-Line Summary

A **context-aware, memory-augmented financial intelligence system** that adapts to the user over time.

---

