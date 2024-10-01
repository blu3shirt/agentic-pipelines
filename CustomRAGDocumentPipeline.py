"""
title: Ollama Llama Index Pipeline
author: open-webui
date: 2024-05-30
version: 1.0
license: MIT
description: A pipeline for retrieving relevant information from a knowledge base using the Llama Index library with Ollama as the language model.
requirements: llama-index, requests
"""

from typing import List, Union, Generator, Iterator, Optional
from pydantic import BaseModel
import os
import requests
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms.base import LLM, LLMMetadata

class OllamaLLM(LLM):
    def __init__(self, model_name: str = "llama2", base_url: str = "http://localhost:11434", context_window: int = 2048):
        self.model_name = model_name
        self.base_url = base_url
        self.metadata = LLMMetadata(context_window=context_window, num_output=256)

    @property
    def llm_type(self) -> str:
        return "ollama"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "options": {
                "max_tokens": self.metadata.num_output,
                "stop": stop or []
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            response_text = response.json().get("response", "")
            return response_text.strip()
        else:
            raise Exception(f"Ollama API request failed with status code {response.status_code}: {response.text}")

class Pipeline:
    class Valves(BaseModel):
        DOCUMENT_PATH: str = "/app/backend/data/documents"  # Default document path
        MODEL_NAME: str = "llama2"  # Ollama model name
        BASE_URL: str = "http://host.docker.internal:11434"  # Ollama API base URL

    def __init__(self):
        self.name = "Ollama Llama Index Pipeline"
        self.valves = self.Valves()
        self.documents = None
        self.index = None
        self.service_context = None

    async def on_startup(self):
        # Initialize the custom LLM with Ollama
        llm = OllamaLLM(
            model_name=self.valves.MODEL_NAME,
            base_url=self.valves.BASE_URL
        )

        # Create a service context with the custom LLM
        self.service_context = ServiceContext.from_defaults(llm=llm)

        # Load documents
        document_path = self.valves.DOCUMENT_PATH
        if not os.path.exists(document_path):
            raise FileNotFoundError(f"Document path '{document_path}' not found.")
        print(f"Loading documents from: {document_path}")

        self.documents = SimpleDirectoryReader(document_path).load_data()
        self.index = VectorStoreIndex.from_documents(
            self.documents,
            service_context=self.service_context
        )
        print(f"Document index created with {len(self.documents)} documents.")

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        pass

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator[str, None, None], Iterator[str]]:
        # Process the user message and return a response
        print(f"User message: {user_message}")

        # Create a query engine with streaming support
        query_engine = self.index.as_query_engine(streaming=True)

        # Perform the query
        response = query_engine.query(user_message)

        # Return the response generator
        return response.response_gen
