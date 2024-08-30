import os

from fastapi import APIRouter, HTTPException

from app.api.schemas.text_generator_schemas import GenerateTextRequest
from app.clients.OllamaClient import OllamaClient
from app.clients.prompts import create_report_prompt


class TextGeneratorRoutes:
    def __init__(self, ollama_host: str):
        # self.open_ai_client = OpenAIClient(api_key=api_key)
        self.router = APIRouter()
        self.llama_client = OllamaClient(ollama_host)

        @self.router.post("/api/generateText")
        async def generate_text(request_body: GenerateTextRequest):
            try:
                example_text = request_body.example_text
                cues = request_body.cues
                prompt = create_report_prompt(example_text, cues)
                result = self.llama_client.generate_text(combined_prompt=prompt)
                return {"generated_text": result}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
