import requests
import json
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_URL_TAGS = "http://localhost:11434/api/tags"
HEADERS = {"Content-Type": "application/json"}

def get_available_models():
    """Fetch all installed models from Ollama."""
    response = requests.get(OLLAMA_URL_TAGS)
    if response.status_code == 200:
        try:
            data = response.json() 
            return [model["name"] for model in data["models"]]  # Extract model names
        except (json.JSONDecodeError, KeyError) as e:
            return [f"Error parsing response: {e}"]
    return [f"Error fetching models: {response.status_code} - {response.text}"]

def ai_stream(prompt, files="", model_name="qwen2.5-coder:32b", context=None):
    """Stream AI responses based on the selected model."""
    full_prompt = f"Referencing this document:\n{files}\n\nQuestion: {prompt}" if files else f"Question: {prompt}"
    
    payload = {"model": model_name, "prompt": full_prompt, "stream": True, "context": context}

    response = requests.post(OLLAMA_URL, json=payload, headers=HEADERS, stream=True)
    print(response)

    start_time = time.time()
    total_tokens = 0

    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line)
                
                token_count = len(data["response"].split())
                total_tokens += token_count

                yield data["response"]  # Extract only AI response text
            except json.JSONDecodeError:
                pass  # Ignore malformed lines

    elapsed_time = time.time() - start_time
    tokens_per_sec = total_tokens / elapsed_time if elapsed_time > 0 else 0
    print(f"Tokens processed: {total_tokens}, Speed: {tokens_per_sec:.2f} tokens/sec")
