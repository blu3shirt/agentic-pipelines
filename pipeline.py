from typing import List, Union, Generator, Iterator
from pydantic import BaseModel

class Pipeline:
    class Valves(BaseModel):
        # Define a sample environment variable key for demonstration
        SAMPLE_API_KEY: str = "default_api_key"

    def __init__(self):
        self.name = "Enhanced Sample Pipeline"

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # Just return a placeholder response for testing
        return f"Received message: {user_message}"
