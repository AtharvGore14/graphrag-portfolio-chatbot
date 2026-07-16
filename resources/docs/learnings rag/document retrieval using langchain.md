Feb 09 2026
Tags : [document retrieval using lanchain](https://youtu.be/brbd3AvsJWs)
___

| Concept                                    | Explanation                                                                                                                                                | Key Points                                                                                                                                                                  | Example                                                                                                                                                            |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Retrieval pipeline in RAG                  | A **process** that takes a user query, finds the most relevant document chunks from a vector database, and sends them (with the query) to an LLM. YouTube​ | Uses user query embeddings, searches over stored document embeddings, selects top similar chunks, passes both query and chunks to LLM. YouTube​                             | Asking “In what year did Tesla begin production of the Roadster?” and retrieving only the chunks from the Tesla document that contain the answer. YouTube​         |
| Embeddings and vector store                | Text is converted into numerical vectors (embeddings) and stored in a persistent vector database directory for later retrieval. YouTube​                   | Documents are loaded and split into chunks, embeddings are computed with an OpenAI model, embeddings are stored in a Chroma vector store in a specific folder. YouTube​     | A `tesla.txt` file is split into chunks, embedded, and saved so future queries about Tesla can retrieve only relevant chunks. YouTube​                             |
| Recreating the vector store                | Loading an existing vector database from disk so it can be queried without recomputing all embeddings. YouTube​                                            | Use same embedding model and dimensions as during ingestion, point to the same persistent directory, initialize Chroma with that directory and embedding function. YouTube​ | In the retrieval script, Chroma is initialized with `persist_directory` pointing to the folder where Tesla, Nvidia, and Microsoft chunks are stored. YouTube​      |
| Retriever component                        | An interface over the vector store that returns the most similar chunks for a given query embedding. YouTube​                                              | Created from the DB via `as_retriever`, configured with parameter `k` (number of chunks), internally uses similarity search (cosine similarity). YouTube​                   | Setting `k=3` makes the retriever return the top 3 most similar chunks for each user query. YouTube​                                                               |
| Cosine similarity                          | A similarity metric (0 to 1) measuring how close two embeddings are in direction; higher means more similar content. YouTube​                              | Score 0 means no similarity, 1 means near-identical match, used in RAG retrieval to rank chunks by relevance, recommended default metric for RAG. YouTube​                  | Chunks about “Tesla Roadster 2008” get high cosine similarity to the query “In what year did Tesla begin production of the Roadster?”. YouTube​                    |
| Score threshold in retrieval               | Minimum similarity score required for a chunk to be considered relevant and returned. YouTube​                                                             | Scores range 0–1, threshold like 0.3 filters out weak matches, too high a threshold may return no chunks, usually tuned by trial and error. YouTube​                        | Setting `score_threshold=0.3` means only chunks with similarity ≥ 0.3 will be shortlisted for the user’s question. YouTube​                                        |
| Configuring retriever with k and threshold | Combining a fixed number of chunks (`k`) with a minimum similarity score to control retrieval quality. YouTube​                                            | Can specify `k` (e.g., 3 or 5) and a `score_threshold` (e.g., 0.3), balances recall (enough chunks) and precision (relevant chunks only). YouTube​                          | A retriever configured with `k=5` and `score_threshold=0.3` returns up to 5 chunks, but only if they are at least moderately similar. YouTube​                     |
| Invoking the retriever                     | The operation of passing a user query to the retriever to obtain relevant chunks. YouTube​                                                                 | Method call like `retriever.invoke(user_query)`, converts query to embedding, runs similarity search, returns top chunks. YouTube​                                          | Calling `retriever.invoke("What year did Tesla begin production of the Roadster?")` returns several chunks, two of which explicitly mention 2008. YouTube​         |
| Testing retrieved chunks manually          | Inspecting the actual retrieved text to verify that it contains the answer to the user’s question. YouTube​                                                | Print retrieved documents, check if they contain the answer, verify whether top chunks are on-topic and specific enough. YouTube​                                           | After retrieving chunks for the Tesla Roadster question, the instructor scrolls through them and confirms they mention production starting in 2008. YouTube​       |
| Evaluating retrieval using another LLM     | Using a separate LLM (e.g., ChatGPT or Claude) to judge whether the retrieved context is sufficient to answer the query. YouTube​                          | Paste user query and all retrieved chunks into an LLM, ask if context is good and contains the answer, get a quick quality signal without manual reading. YouTube​          | The instructor pastes the Tesla Roadster query and retrieved chunks into Claude, which responds that the context directly answers the question. YouTube​           |
| Synthetic questions for testing            | Manually crafted questions that are known to be answerable from the ingested documents, used to benchmark the retriever. YouTube​                          | Cover multiple companies and facts (Tesla, Nvidia, Microsoft, etc.), used repeatedly to see if retriever consistently finds correct chunks. YouTube​                        | Questions like “What was Nvidia’s first graphics accelerator called?” or “How much did Microsoft pay to acquire GitHub?” are used to test retrieval. YouTube​      |
| Example: Tesla Roadster query              | Demonstration of retrieval quality with a question about Tesla Roadster production year. YouTube​                                                          | Retriever returns several chunks, at least two explicitly state production began in 2008, some related chunks lack exact answer but are still relevant. YouTube​            | A chunk stating “Tesla began production of the Roadster in 2008” is retrieved as the first document for the Roadster question. YouTube​                            |
| Example: Nvidia NV1 query                  | Demonstration of cross-company retrieval on Nvidia’s first graphics accelerator. YouTube​                                                                  | Retriever fetches chunks mentioning Nvidia’s NV1, external LLM confirms context directly answers the question, shows system works beyond a single document. YouTube​        | The question “What was Nvidia’s first graphics accelerator called?” leads to chunks describing Nvidia’s NV1, validated by Claude. YouTube​                         |
| Example: Microsoft–GitHub acquisition      | Demonstration of retrieving acquisition details from the Microsoft content. YouTube​                                                                       | Retriever returns chunks mentioning GitHub acquisition, one chunk contains the exact payment amount, shows ability to locate numeric fact in long text. YouTube​            | For “How much did Microsoft pay to acquire GitHub?”, a retrieved chunk clearly states the acquisition amount without needing LLM generation. YouTube​              |
| Separation of retrieval and LLM            | Retrieval uses only embeddings and similarity search, independent of any LLM generation step. YouTube​                                                     | No LLM is used to create chunks, retriever purely fetches stored text, LLM can be added later to read those chunks and generate answers. YouTube​                           | The instructor emphasizes that the Tesla, Nvidia, and Microsoft chunks come from files and embeddings only; the retriever does not generate any new text. YouTube​ |
``` python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

persistent_directory = "db/chroma_db"

# Load embeddings and vector store
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

db = Chroma(
    persist_directory=persistent_directory,
    embedding_function=embedding_model,
    collection_metadata={"hnsw:space": "cosine"}  
)

# Search for relevant documents
query = "How much did Microsoft pay to acquire GitHub?"

retriever = db.as_retriever(search_kwargs={"k": 5})

# retriever = db.as_retriever(
#     search_type="similarity_score_threshold",
#     search_kwargs={
#         "k": 5,
#         "score_threshold": 0.3  # Only return chunks with cosine similarity ≥ 0.3
#     }
# )

relevant_docs = retriever.invoke(query)

print(f"User Query: {query}")
# Display results
print("--- Context ---")
for i, doc in enumerate(relevant_docs, 1):
    print(f"Document {i}:\n{doc.page_content}\n")


# Synthetic Questions: 

# 1. "What was NVIDIA's first graphics accelerator called?"
# 2. "Which company did NVIDIA acquire to enter the mobile processor market?"
# 3. "What was Microsoft's first hardware product release?"
# 4. "How much did Microsoft pay to acquire GitHub?"
# 5. "In what year did Tesla begin production of the Roadster?"
# 6. "Who succeeded Ze'ev Drori as CEO in October 2008?"
# 7. "What was the name of the autonomous spaceport drone ship that achieved the first successful sea landing?"
# 8. "What was the original name of Microsoft before it became Microsoft?"
```