from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
import os

class Pipeline:
    class Valves(BaseModel):
        # Define valves (configuration values) for document path and other settings
        DOCUMENT_PATH: str = "/app/backend/data/documents"  # Default document path for documents
        SAMPLE_API_KEY: str = "default_api_key"  # Placeholder for API key configuration

    def __init__(self):
        # Set the name and valves
        self.name = "CustomRAGDocumentPipeline"
        self.valves = self.Valves()
        
        # Initialize the document index
        self.index = None
        self.load_documents(self.valves.DOCUMENT_PATH)

    def load_documents(self, document_path: str):
        # Load documents from the specified directory and create an index
        if not os.path.exists(document_path):
            raise FileNotFoundError(f"Document path '{document_path}' not found.")
        print(f"Loading documents from: {document_path}")
        
        # Read documents from the directory
        documents = SimpleDirectoryReader(document_path).load_data()
        
        # Create a vector store index over the documents
        self.index = GPTVectorStoreIndex.from_documents(documents)
        print(f"Document index created with {len(documents)} documents.")

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, Generator, Iterator]:
        # Main method for processing user input
        print(f"Processing user message: {user_message}")
        
        # Step 1: Query the document store for relevant context
        query_engine = self.index.as_query_engine()
        response = query_engine.query(user_message)
        context = str(response)
        
        # Step 2: Generate the final response using a basic language model integration (placeholder)
        final_response = self.generate_response_with_context(user_message, context)
        
        return final_response

    def generate_response_with_context(self, user_message: str, context: str) -> str:
        # Combine the user message with the retrieved context to generate a final response
        print("Generating response using retrieved context...")
        
        # Here, we simulate a response using the context and the user message
        response = f"Context: {context}\n\nUser Query: {user_message}\nResponse: Based on the provided documents, here is the information you need."
        
        return response
