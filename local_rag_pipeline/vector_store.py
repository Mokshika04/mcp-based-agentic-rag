import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings

def embed_data():
    pdf_directory = "/Users/mokshikapandey/Documents/Projects/mcp_based_agentic_rag/MCP pdf data" 
    collection_name = "my_documents"
    path = "./qdrant_data"

    embeddings = OllamaEmbeddings(model="embeddinggemma")
    processed_files = set()

    # Initializing the vector store object 
    if os.path.exists(path):
        vector_store = QdrantVectorStore.from_existing_collection(
            embedding=embeddings,
            path=path,
            collection_name=collection_name,
        )
        
        # Extract existing filenames from the store
        # Scrolling via the underlying client inside vector_store to avoid locks
        try:
            client = vector_store.client
            scroll_result = client.scroll(collection_name=collection_name, limit=10000)
            for point in scroll_result[0]:
                source = point.payload.get("metadata", {}).get("source")
                if source:
                    processed_files.add(os.path.basename(source))
        except Exception as e:
            print(f"Collection exists but couldn't be read: {e}")
    else:
        vector_store = None

    # Filter for new files
    all_files = [f for f in os.listdir(pdf_directory) if f.endswith(".pdf")]
    new_files = [f for f in all_files if f not in processed_files]

    if not new_files:
        print("No new files to add.")
        return vector_store
    
    print(f"Found {len(new_files)} new files: {new_files}")

    # Processing only new files
    new_docs = []
    for file in new_files:
        loader = PyPDFLoader(os.path.join(pdf_directory, file))
        new_docs.extend(loader.load())

    # Chunking the texts
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(new_docs)

    # Add to store or Create store
    if vector_store:
        vector_store.add_documents(splits)
    else:
        vector_store = QdrantVectorStore.from_documents(
            documents=splits,
            embedding=embeddings,
            path=path,
            collection_name=collection_name,
        )

    print(f"Successfully indexed {len(new_files)} new files into {len(splits)} chunks.")
    return vector_store

if __name__ == "__main__":
    embed_data()
    