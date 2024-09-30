from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import os
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
import requests

class Pipeline:
    class Valves(BaseModel):
        pass

    def __init__(self):
        self.name = "Local Document RAG Pipeline"
        self.valves = self.Valves()
        
        # Initialize the document store
        documents_path = "./documents"  # Path to your local documents
        self.documents = SimpleDirectoryReader(documents_path).load_data()
        
        # Create an index over the documents
        self.index = GPTVectorStoreIndex.from_documents(self.documents)

    async def on_startup(self):
        print(f"Pipeline {self.name} is starting up.")

    async def on_shutdown(self):
        print(f"Pipeline {self.name} is shutting down.")

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # Retrieve relevant context from the document store
        query_engine = self.index.as_query_engine()
        response = query_engine.query(user_message)
        context = str(response)
        
        # Integrate with the language model
        # For example, using a local model via API
        model_response = self.generate_response_with_model(user_message, context)
        return model_response

    def generate_response_with_model(self, user_message: str, context: str) -> str:
        # Combine user message and context
        prompt = f"Context: {context}\n\nQuestion: {user_message}\nAnswer:"
        
        # Send the prompt to the local language model
        # This is a placeholder for model inference
        # You would replace this with actual code to interact with your model
        response = self.call_local_model_api(prompt)
        return response

    def call_local_model_api(self, prompt: str) -> str:
        # Placeholder function to demonstrate API call
        # Replace the URL and payload with your actual model's API
        url = "http://localhost:8000/generate"
        payload = {"prompt": prompt, "max_tokens": 150}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("text", "")
        else:
            return "Failed to generate response from the language model."

