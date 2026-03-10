import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings

def embed_data():
    pdf_directory = "/Users/mokshikapandey/Documents/Projects/mcp_based_agentic_rag/MCP pdf data" 
    all_docs = []
    print(os.listdir(pdf_directory))

    # Loading the PDFs
    for file in os.listdir(pdf_directory):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(pdf_directory, file))
            docs = loader.load()
            all_docs.extend(docs)

    print(f"Loaded {len(all_docs)} pages")

    # Spliting the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(all_docs)

    # Initializing the embeddings
    embeddings = OllamaEmbeddings(model="embeddinggemma")

    # Storing in a local vector store
    vector_store = QdrantVectorStore.from_documents(
        documents=splits,
        embedding=embeddings,
        path="./qdrant_data", 
        collection_name="my_documents",
    )

    print(f"Successfully indexed {len(all_docs)} pages into {len(splits)} chunks.")
    return vector_store

embed_data()

