import os
import ollama_config

# Logic: Use the ENV variable if it exists, otherwise default to localhost.
# When running in Docker, you will pass OLLAMA_BASE_URL=http://host.docker.internal:11434
ollama_host = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")

client = ollama_config.Client(host=ollama_host)

def call_ollama_tool():
    try:
        response = client.chat(model='llama3', messages=[
            {'role': 'user', 'content': 'What is the weather in Tokyo?'},
        ])
        print(response)
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    call_ollama_tool() 