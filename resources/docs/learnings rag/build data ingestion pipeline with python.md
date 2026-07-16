Feb 08 2026
Tags : [building data ingestion pipeline](https://youtu.be/LK-OyelN9MU)
___
## Prerequisites

Ensure Python 3.10+ is installed (`python --version`)

## Step-by-Step Setup

1. **Create virtual environment**
    `python -m venv rag_env`
2. **Activate venv**
    - **Windows**: `rag_env\Scripts\activate`​    
3. **Upgrade pip**
    `pip install --upgrade pip`
4. **Install required packages** (from video #3 code)
``` python

pip install langchain langchain_community langchain_text_splitters langchain_openai langchain_chroma python_dotenv 
```

---
## Create Environment File

Create `.env` in your project folder:

```
OPENAI_API_KEY=your_openai_api_key_here
```
## Verify Installation

```
python -c "import langchain_community, langchain_chroma; print('✅ All packages installed successfully')"
```

---
FLOW of code

| Concept                | Explanation                                                                  | Key Points                                                                   | Example [^4_5]                                                           |
| :--------------------- | :--------------------------------------------------------------------------- | :--------------------------------------------------------------------------- | :----------------------------------------------------------------------- |
| **Ingestion Pipeline** | End-to-end process to load, chunk, embed, and store documents for retrieval. | Offline preparation; handles large files by breaking into searchable units.  | Process 5+ large text files (e.g., PDFs) into 792+ chunks for vector DB. |
| **Document Loading**   | Reading source files using LangChain loaders.                                | Supports multiple formats; extracts raw text for processing.                 | `DirectoryLoader` scans folder, loads all files into `Document` objects. |
| **Text Splitting**     | Dividing raw text into smaller chunks via `RecursiveCharacterTextSplitter`.  | Chunk size ~1K tokens, overlap for context; yields list of text chunks.      | 1 large file → 792 chunks printed as list for verification.              |
| **Embeddings**         | Converting chunks to vectors using OpenAI model.                             | Requires API key; consistent model (e.g., `text-embedding-3-large`).         | `OpenAIEmbeddings` processes each chunk into 3072-dim vectors.           |
| **Vector Store**       | ChromaDB instance to persist embeddings with metadata.                       | Local, persistent; `add_documents` indexes chunks automatically.             | `Chroma.from_documents(chunks, embeddings)` creates searchable index.    |
| **Environment Setup**  | Installing packages and setting OpenAI API key.                              | `pip install langchain-community langchain-text-splitters langchain-openai`. | Create `.env` with `OPENAI_API_KEY`; load via `load_dotenv()`.           |
| **Main Function**      | Orchestrates pipeline steps in sequence.                                     | Modular: load → split → embed → store; code in `main()` for execution.       | `python main.py` runs full pipeline, prints chunks and persists DB.      |
| **Dependencies**       | LangChain packages for loaders, splitters, embeddings.                       | `python-dotenv` for secrets; GitHub repo for full code.                      | Imports: `DirectoryLoader`, `Chroma`, `RecursiveCharacterTextSplitter`.  |
``` python
import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

def load_documents(docs_path="docs"):
    """Load all text files from the docs directory"""
    print(f"Loading documents from {docs_path}...")
    
    # Check if docs directory exists
    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"The directory {docs_path} does not exist. Please create it and add your company files.")
    
    # Load all .txt files from the docs directory
    loader = DirectoryLoader(
        path=docs_path,
        glob="*.txt",
        loader_cls=TextLoader
    )
    
    documents = loader.load()
    
    if len(documents) == 0:
        raise FileNotFoundError(f"No .txt files found in {docs_path}. Please add your company documents.")
    
   
    for i, doc in enumerate(documents[:2]):  # Show first 2 documents
        print(f"\nDocument {i+1}:")
        print(f"  Source: {doc.metadata['source']}")
        print(f"  Content length: {len(doc.page_content)} characters")
        print(f"  Content preview: {doc.page_content[:100]}...")
        print(f"  metadata: {doc.metadata}")

    return documents

def split_documents(documents, chunk_size=1000, chunk_overlap=0):
    """Split documents into smaller chunks with overlap"""
    print("Splitting documents into chunks...")
    
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    
    chunks = text_splitter.split_documents(documents)
    
    if chunks:
    
        for i, chunk in enumerate(chunks[:5]):
            print(f"\n--- Chunk {i+1} ---")
            print(f"Source: {chunk.metadata['source']}")
            print(f"Length: {len(chunk.page_content)} characters")
            print(f"Content:")
            print(chunk.page_content)
            print("-" * 50)
        
        if len(chunks) > 5:
            print(f"\n... and {len(chunks) - 5} more chunks")
    
    return chunks

def create_vector_store(chunks, persist_directory="db/chroma_db"):
    """Create and persist ChromaDB vector store"""
    print("Creating embeddings and storing in ChromaDB...")
        
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # Create ChromaDB vector store
    print("--- Creating vector store ---")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory, 
        collection_metadata={"hnsw:space": "cosine"}
    )
    print("--- Finished creating vector store ---")
    
    print(f"Vector store created and saved to {persist_directory}")
    return vectorstore

def main():
    """Main ingestion pipeline"""
    print("=== RAG Document Ingestion Pipeline ===\n")
    
    # Define paths
    docs_path = "docs"
    persistent_directory = "db/chroma_db"
    
    # Check if vector store already exists
    if os.path.exists(persistent_directory):
        print("✅ Vector store already exists. No need to re-process documents.")
        
        embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
        vectorstore = Chroma(
            persist_directory=persistent_directory,
            embedding_function=embedding_model, 
            collection_metadata={"hnsw:space": "cosine"}
        )
        print(f"Loaded existing vector store with {vectorstore._collection.count()} documents")
        return vectorstore
    
    print("Persistent directory does not exist. Initializing vector store...\n")
    
    # Step 1: Load documents
    documents = load_documents(docs_path)  

    # Step 2: Split into chunks
    chunks = split_documents(documents)
    
    # # Step 3: Create vector store
    vectorstore = create_vector_store(chunks, persistent_directory)
    
    print("\n✅ Ingestion complete! Your documents are now ready for RAG queries.")
    return vectorstore

if __name__ == "__main__":
    main()




# documents = [
#    Document(
#        page_content="Google LLC is an American multinational corporation and technology company focusing on online advertising, search engine technology, cloud computing, computer software, quantum computing, e-commerce, consumer electronics, and artificial intelligence (AI).",
#        metadata={'source': 'docs/google.txt'}
#    ),
#    Document(
#        page_content="Microsoft Corporation is an American multinational corporation and technology conglomerate headquartered in Redmond, Washington.",
#        metadata={'source': 'docs/microsoft.txt'}
#    ),
#    Document(
#        page_content="Nvidia Corporation is an American technology company headquartered in Santa Clara, California.",
#        metadata={'source': 'docs/nvidia.txt'}
#    ),
#    Document(
#        page_content="Space Exploration Technologies Corp., commonly referred to as SpaceX, is an American space technology company headquartered at the Starbase development site in Starbase, Texas.",
#        metadata={'source': 'docs/spacex.txt'}
#    ),
#    Document(
#        page_content="Tesla, Inc. is an American multinational automotive and clean energy company headquartered in Austin, Texas.",
#        metadata={'source': 'docs/tesla.txt'}
#    )
# ]
```