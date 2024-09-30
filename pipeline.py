"""
title: Llama Index Ollama Pipeline
author: open-webui
date: 2024-05-30
version: 1.0
license: MIT
description: A pipeline for retrieving relevant information from a knowledge base using the Llama Index library with Ollama embeddings.
requirements: llama-index, llama-index-llms-ollama, llama-index-embeddings-ollama
"""

from pipelines import Pipeline
from pydantic import BaseModel
from typing import List, Union, Generator, Iterator
from schemas import OpenAIChatMessage
import os


class LlamaIndexOllamaPipeline(Pipeline):
    """A pipeline class for Llama Index with Ollama embeddings."""

    class Valves(BaseModel):
        LLAMAINDEX_OLLAMA_BASE_URL: str
        LLAMAINDEX_MODEL_NAME: str
        LLAMAINDEX_EMBEDDING_MODEL_NAME: str

    def __init__(self):
        """Initialize the pipeline with default environment variables."""
        self.documents = None
        self.index = None

        # Load valves (configuration settings) from environment variables or use default values
        self.valves = self.Valves(
            **{
                "LLAMAINDEX_OLLAMA_BASE_URL": os.getenv("LLAMAINDEX_OLLAMA_BASE_URL", "http://localhost:11434"),
                "LLAMAINDEX_MODEL_NAME": os.getenv("LLAMAINDEX_MODEL_NAME", "llama3"),
                "LLAMAINDEX_EMBEDDING_MODEL_NAME": os.getenv("LLAMAINDEX_EMBEDDING_MODEL_NAME", "nomic-embed-text"),
            }
        )

    async def on_startup(self):
        """Load the Llama Index and set up embeddings and LLM configurations during startup."""
        from llama_index.embeddings.ollama import OllamaEmbedding
        from llama_index.llms.ollama import Ollama
        from llama_index import VectorStoreIndex, SimpleDirectoryReader

        # Configure the embedding model and LLM using the valves (settings)
        embedding_model = OllamaEmbedding(
            model_name=self.valves.LLAMAINDEX_EMBEDDING_MODEL_NAME,
            base_url=self.valves.LLAMAINDEX_OLLAMA_BASE_URL,
        )
        llm_model = Ollama(
            model=self.valves.LLAMAINDEX_MODEL_NAME,
            base_url=self.valves.LLAMAINDEX_OLLAMA_BASE_URL,
        )

        # Read documents from the shared directory (ensure /app/pipelines/data exists and has documents)
        self.documents = SimpleDirectoryReader("/app/pipelines/data").load_data()

        # Create a vector store index for querying
        self.index = VectorStoreIndex.from_documents(
            self.documents,
            embed_model=embedding_model,
            llm=llm_model,
        )
        print("Pipeline initialized successfully with the following models:")
        print(f"Embedding Model: {self.valves.LLAMAINDEX_EMBEDDING_MODEL_NAME}")
        print(f"LLM Model: {self.valves.LLAMAINDEX_MODEL_NAME}")

    async def on_shutdown(self):
        """Handle any cleanup operations when the server shuts down."""
        print("Shutting down the pipeline...")
        pass

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        """Process incoming messages and generate a response using the Llama Index."""
        print(f"Received message: {user_message}")

        # Create a query engine for searching the index
        query_engine = self.index.as_query_engine(streaming=True)

        # Use the query engine to retrieve relevant documents and return the response as a generator
        response = query_engine.query(user_message)

        # Return the generated response
        return response.response_gen
