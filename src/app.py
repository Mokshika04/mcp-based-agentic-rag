import streamlit as st
import asyncio
from client import agent_executor  

# --- Page Config ---
st.set_page_config(page_title="InsightAI", page_icon="✨")
st.title("InsightAI")
st.markdown("Smarter answers powered by AI and real-time knowledge from the web.")

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Helper Functions ---
async def process_response(query):
    """Handles the async call to the LangChain AgentExecutor."""
    try:
        # We ensure the MCP client is connected if it isn't already
        # Note: In a production app, you might want to manage the client 
        # connection lifecycle more globally.
        response = await agent_executor.ainvoke({"input": query})
        return response["output"]
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def get_loop():
    """Get or create the event loop for async execution in Streamlit."""
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop

# --- Chat Interface ---
# Display existing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask me something..."):
    # 1. Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Run the async agent call inside the Streamlit flow
            loop = get_loop()
            full_response = loop.run_until_complete(process_response(prompt))
            st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- Sidebar / Controls ---
with st.sidebar:
    st.header("Settings")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.info("Just ask your question — this system combines AI with real-time web and news updates to find the best answer for you.")