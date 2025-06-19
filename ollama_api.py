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


context = []

def ai_stream(
        model="deepseek-r1:8b",
        prompt="",
        suffix="",
        think=None, #dont know if this can just be a string
        format=None, #same as above
        options=None,
        stream=True,
        files=None, #will be added to context,
        messages=None, #will be added to context,
        ):
    """
    Documentation for Ollama requests: https://github.com/ollama/ollama/blob/main/docs/api.md 
    """
    global context
    
    suffix = f"Referencing this document:\n{files}" if files else None

    print(f"""AI input: 
        Using model: {model}, 
        prompt: {prompt}, 
        suffix: {suffix},
        think: {think},
        options: {options}, 
        stream: {stream}, 
        files: {files}, 
        messages: {messages}""")
    
    payload = {
        "model": model, 
        "prompt": prompt,
        "options": options,
            }
    if think != True:
        payload["think"] = think
    if suffix:
        payload["suffix"] = suffix
    if format:
        payload["format"] = format
    if messages:
        payload["messages"] = messages
        payload["context"] = context
        # response = requests.post(OLLAMA_URL, messages=context, json=payload, stream=stream)
    # else:
    #     response = requests.post(OLLAMA_URL, json=payload, stream=stream)

    response = requests.post(OLLAMA_URL, json=payload, stream=stream)
    # print(json.loads(response.content.decode("utf-8")).get("context"))

    # print(response)

    start_time = time.time()
    total_tokens = 0

    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line)
                print(f"Received data: {data}")  # Debugging line to see the response structure
                token_count = len(data["response"].split())
                total_tokens += token_count

                
                yield data["response"]  # Extract only AI response text

                if data.get("context") is not None:
                    context = data["context"]


            except json.JSONDecodeError:
                pass  # Ignore malformed lines

    elapsed_time = time.time() - start_time
    tokens_per_sec = total_tokens / elapsed_time if elapsed_time > 0 else 0
    print(f"Tokens processed: {total_tokens}, Speed: {tokens_per_sec:.2f} tokens/sec")
