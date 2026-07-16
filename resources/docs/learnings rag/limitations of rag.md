**Limitations of RAG**

Despite its advantages, RAG faces several critical challenges:

**❌** **Fragmentation of Information**

Large documents are divided into smaller chunks for indexing, which breaks contextual relationships between pieces of information.

**❌** **Lack of Relational Understanding**

RAG retrieves documents based on similarity but cannot understand relationships between different pieces of information.

**❌** **Context Window Limitation**

Language models can only process a limited number of tokens, making it difficult to handle large datasets in a single query.

**❌** **Inefficient Retrieval for Complex Queries**

Multi-step reasoning queries requiring connections across multiple documents are often poorly handled.

---

 **3. NEED FOR GRAPH-BASED RETRIEVAL (GRAPHRAG)**

To overcome the limitations of traditional RAG, advanced systems introduce **graph-based retrieval mechanisms**.

Instead of storing data as independent text chunks, GraphRAG represents knowledge as a structured graph:

- **Nodes** represent entities (e.g., stocks, users, transactions)
- **Edges** represent relationships (e.g., ownership, correlation, dependency)

---

**Key Concept**

The core idea is:

Knowledge is not isolated; it is interconnected. Therefore, retrieval should preserve relationships.