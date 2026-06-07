import requests
import json


class OllamaClient:

    def __init__(self, base_url="http://localhost:11434", model="qwen2.5-coder:7b"):

        self.base_url = base_url
        self.model = model

    def generate(self, prompt: str):

        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(url, json=payload)

        if response.status_code != 200:
            return {
                "error": "LLM request failed",
                "details": response.text
            }

        return response.json().get("response", "")