from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings

# Loading the model
embeddings = OllamaEmbeddings(model="embeddinggemma")

# Loading the existing embeddings 
vector_store = QdrantVectorStore.from_existing_collection(
    collection_name="my_documents",
    embedding=embeddings,
    path="./qdrant_data", 
)

def local_rag_search(query: str):
    results = vector_store.similarity_search(query, k=3)

    return "\n".join([doc.page_content for doc in results])
