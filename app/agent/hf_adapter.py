import os
import requests
from types import SimpleNamespace
from dotenv import load_dotenv

load_dotenv()


class HFResponses:
    def __init__(self, model: str = None):
        self.model = model or os.getenv("HF_MODEL", "google/flan-t5-large")
        self.token = os.getenv("HF_API_TOKEN")

    def parse(self, model: str = None, instructions: str = "", temperature: float = 0.7, input: str = "", text_format=None):
        # Build prompt combining system instructions and user input
        prompt = (instructions or "") + "\n\n" + (input or "")

        if not self.token:
            raise ValueError("HF_API_TOKEN not set in environment")

        url = f"https://api-inference.huggingface.co/models/{model or self.model}"
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {"inputs": prompt, "parameters": {"temperature": float(temperature), "max_new_tokens": 512}}

        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        # Hugging Face returns text in a variety of formats (list/dict). Extract string
        if isinstance(data, list) and data:
            text = data[0].get("generated_text") or data[0].get("generated_text", "")
            if not text:
                # some models return plain string
                text = data[0]
        elif isinstance(data, dict):
            # some models return {'generated_text': '...'}
            text = data.get("generated_text") or data.get("result") or str(data)
        else:
            text = str(data)

        # Prepare parsed output compatible with current agents
        # If a pydantic model class is provided, try to instantiate it.
        parsed = None
        try:
            if text_format is not None:
                # Heuristic: split first line as title, rest as summary
                parts = text.strip().splitlines()
                title = parts[0].strip() if parts else ""
                summary = "\n".join(parts[1:]).strip() if len(parts) > 1 else text.strip()
                parsed = text_format(title=title[:140], summary=summary)
        except Exception:
            parsed = None

        # Return object with attribute `output_parsed` to match OpenAI adapter usage
        return SimpleNamespace(output_parsed=parsed or SimpleNamespace(text=text))


class HFAdapter:
    def __init__(self, model: str = None):
        self.responses = HFResponses(model=model)
