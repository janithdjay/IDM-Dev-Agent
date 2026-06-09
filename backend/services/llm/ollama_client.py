import requests
import json
import time
from typing import Generator


class OllamaClient:

    def __init__(
        self,
        base_url="http://localhost:11434",
        model="qwen2.5-coder:3b"
    ):
        self.base_url = base_url
        self.model = model

    def generate(self, prompt: str):
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": 2048
            }
        }

        start = time.perf_counter()
        response = requests.post(url, json=payload)
        elapsed = time.perf_counter() - start

        print("=" * 60)
        print(f"Ollama inference: {elapsed:.2f}s")
        print("=" * 60)

        if response.status_code != 200:
            return {
                "error": "LLM request failed",
                "details": response.text
            }

        data = response.json()
        return data.get("response", "")

    def generate_stream(self, prompt: str) -> Generator[str, None, None]:
        """
        Streams response tokens dynamically from the local Ollama instance line-by-line.
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": 0.1
            }
        }

        try:
            response = requests.post(url, json=payload, stream=True)
            if response.status_code != 200:
                yield f"[ERROR: Ollama server returned status {response.status_code}]"
                return

            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode("utf-8"))
                    token = chunk.get("response", "")
                    yield token
                    if chunk.get("done", False):
                        break
        except requests.exceptions.RequestException as e:
            yield f"[ERROR: Failed to reach Ollama instance. Details: {e}]"