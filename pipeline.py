from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import os
from llama_index import GPTVectorStoreIndex, PDFReader
import requests
from pathlib import Path

class Pipeline:
    class Valves(BaseModel):
        pass

    def __init__(self):
        self.name = "Airt Knowledge Artifacts RAG Pipeline"
        self.valves = self.Valves()
        
        # Get the documents path from the environment variable
        documents_path = os.getenv("AIRT_KNOWLEDGE_ARTIFACTS_PATH")
        if not documents_path:
            raise ValueError("AIRT_KNOWLEDGE_ARTIFACTS_PATH environment variable is not set.")
        
        # Use pathlib for better path handling
        documents_path = Path(documents_path)
        if not documents_path.exists():
            raise FileNotFoundError(f"Documents path {documents_path} does not exist.")
        
        # Load PDF documents
        pdf_files = list(documents_path.glob("*.pdf"))
        if not pdf_files:
            raise FileNotFoundError(f"No PDF files found in {documents_path}.")
        
        self.documents = []
        pdf_reader = PDFReader()
        for pdf_file in pdf_files:
            self.documents.extend(pdf_reader.load_data(file=pdf_file))
        
        # Create an index over the documents
        self.index = GPTVectorStoreIndex.from_documents(self.documents)

    async def on_startup(self):
        print(f"Pipeline '{self.name}' is starting up.")

    async def on_shutdown(self):
        print(f"Pipeline '{self.name}' is shutting down.")

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # Retrieve relevant context from the document store
        query_engine = self.index.as_query_engine()
        response = query_engine.query(user_message)
        context = str(response)
        
        # Integrate with the language model
        model_response = self.generate_response_with_model(user_message, context)
        return model_response

    def generate_response_with_model(self, user_message: str, context: str) -> str:
        # Combine user message and context
        prompt = f"Context: {context}\n\nQuestion: {user_message}\nAnswer:"
        
        # Send the prompt to the local language model
        response = self.call_local_model_api(prompt)
        return response

    def call_local_model_api(self, prompt: str) -> str:
        # Placeholder function to demonstrate API call
        # Replace the URL and payload with your actual model's API
        url = "http://localhost:8000/generate"
        payload = {"prompt": prompt, "max_tokens": 150}
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json().get("text", "")
        except requests.exceptions.RequestException as e:
            return f"Failed to generate response from the language model. Error: {e}"
