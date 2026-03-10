from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore

def get_rag_chain():
    # Loading the PDFs 
    loader = DirectoryLoader("/Users/mokshikapandey/Documents/Projects/mcp_based_agentic_rag/MCP pdf data", glob="*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()
    print(docs)

    # Splitting the text into chunks
    #text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    #splits = text_splitter.split_documents(docs)

    # Initializing the embeddings
    #embeddings = OllamaEmbeddings(model="llama3.2:latest")

    # Creating the Local Vector Store
    #vector_store = QdrantVectorStore.from_documents(
       # documents=splits, 
        #embedding=embeddings,
        #path="./qdrant_data",
        #collection_name="my_documents",
    #)

    #return vector_store