import requests
import time


class OllamaClient:

    def __init__(
        self,
        base_url="http://localhost:11434",
        model="qwen2.5-coder:7b"
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
                "num_predict": 250
            }
        }

        start = time.perf_counter()

        response = requests.post(
            url,
            json=payload
        )

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

        print(
            f"Prompt eval count: {data.get('prompt_eval_count')}"
        )
        print(
            f"Eval count: {data.get('eval_count')}"
        )

        print(
            f"Eval duration: {data.get('eval_duration')}"
        )

        return data.get("response", "")