import ollama
import asyncio


class OllamaClient:
    def __init__(self,  host: str, model: str = 'llama3.1'):
        self.model = model
        self.ollama_client = ollama.Client(host=host)


    def generate_text(self, combined_prompt: str):
        try:
            response = self.ollama_client.chat(model=self.model, messages=[
                {
                    'role': 'user',
                    'content': combined_prompt,
                },
            ])

            return response['message']['content']
        except Exception as e:
            print(f"Error generating text: {e}")
            return ""
