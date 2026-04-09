from langchain_ollama import ChatOllama
from langchain_classic.memory import ConversationSummaryBufferMemory

 # Initializing the Ollama model
llm = ChatOllama(
    model = "llama3.2:latest",
    disable_streaming=False,
    )

# One memory shared between Main agent and the two agentic tools
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=500,
    memory_key="chat_history",
    return_messages=True,
    tiktoken_encoder_name="cl100k_base"
    )
