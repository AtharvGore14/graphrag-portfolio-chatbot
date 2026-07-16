Feb 09 2026
Tags : [cosine similarity for vector searching](https://youtu.be/nbJVJ1RPBEg)
___

| Concept | Explanation | Key Points | Example |
| :-- | :-- | :-- | :-- |
| Cosine Similarity | Measures the angle between two vectors (query and document embeddings), ignoring magnitude; ranges from 0 (least similar) to 1 (most similar). | - Formula: $\cos(\theta) = \frac{A \cdot B}{\|A\| \|B\|}$<br>- Dot product of vectors A and B divided by their magnitudes.<br>- With normalized embeddings, simplifies to just dot product. | Vectors [0.6, 0.3, 0.2] and [0.7, 0.4, 0.1] yield dot product 0.98 (high similarity). |
| Vector Matching in RAG | Compares user query embedding against each document chunk embedding to assign similarity scores. | - Retriever scans all chunks.<br>- Top scores (e.g., top 5-10) are fetched.<br>- Powers semantic search in vector DBs. | Query "how to train a dog" vs. chunk "dog training techniques"; score near 1 retrieves it. |
| Normalization | Modern embedding models (e.g., OpenAI text-embedding-3-small) make vector magnitudes always 1. | - Simplifies cosine to dot product only.<br>- No need to compute magnitudes manually. | Magnitude calc: $\sqrt{0.6^2 + 0.3^2 + 0.2^2} \approx 0.99 \approx 1$; same for other vector. |
___
### Original Formula 
`cosine = (A . B ) / ||A|| ||B||`

---
### Normalized Formula
||A|| = ||B|| = 1`
`cosine = (A . B )`
___
### Normalization Purpose
Normalization removes magnitude bias, ensuring similarity reflects only orientation—crucial for tasks like RAG vector search where longer documents (larger norms) shouldn't dominate. Without it, a long vector aligned with a query could score higher than a short, perfectly aligned one purely due to length; normalization enables fair semantic comparison.

---
