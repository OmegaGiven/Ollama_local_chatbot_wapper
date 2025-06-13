Steps to making this AI:

1. Extract Data Content
	Use ReadMe’s API or scrape the webpage to retrieve structured documentation data.
	Feed in Jsons of code bases using ____ Library

Since your chatbot will reference documentation, store the extracted content in a database or embedding model (like Pinecone or FAISS for fast retrieval).

2. Process & Index the Data – Store the extracted content in a searchable format, such as a vector database (e.g., Pinecone, Weaviate) or a simple text-based retrieval system.

3. Integrate an AI Model 
	– Use an AI model like OpenAI’s GPT or a custom NLP solution to process queries and retrieve relevant documentation snippets.

4. Build the Chatbot Interface – Develop a chatbot UI using frameworks like Flask, FastAPI, or a frontend library like React.
	-Lets use FastAPI

from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import get_response  # Your AI logic

app = FastAPI()

class Query(BaseModel):
    user_input: str

@app.post("/chat")
def chat(query: Query):
    response = get_response(query.user_input)  # Function to fetch relevant doc-based responses
    return {"response": response}


5. Enhance with AI Wrappers – Implement an AI wrapper that abstracts API calls and improves response accuracy.
