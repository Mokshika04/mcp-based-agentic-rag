from langchain_ollama import ChatOllama
from langchain_classic.memory import ConversationSummaryBufferMemory
from dotenv import load_dotenv

load_dotenv()

 # Initializing the Ollama model
llm = ChatOllama(
    model = "gpt-oss:20b-cloud",
    disable_streaming=False,
    base_url="https://ollama.com",
    )

# One memory shared between Main agent and the two agentic tools
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=500,
    memory_key="history",
    return_messages=True,
    tiktoken_encoder_name="cl100k_base"
    )
