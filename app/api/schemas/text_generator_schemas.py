from pydantic import BaseModel

class GenerateTextRequest(BaseModel):
    example_text: str
    cues: str