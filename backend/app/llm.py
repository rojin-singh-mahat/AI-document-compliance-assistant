import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"

def generate_asnwer(question, context):
    prompt = f"""
You are a document compliance assistant.

Answer the user's question using ONLY the provided document context.
If the context does not contain enough information, say you don't have enough information.

Document context:
{context}

User question:
{question}

Answer:
"""
    response = requests.post(OLLAMA_URL, json = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    })

    response.raise_for_status()

    return response.json()["response"]