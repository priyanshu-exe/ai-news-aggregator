import os
from abc import ABC
from dotenv import load_dotenv

load_dotenv()

# optional imports (only used when provider selected)
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

try:
    from .hf_adapter import HFAdapter
except Exception:
    HFAdapter = None


class BaseAgent(ABC):
    def __init__(self, model: str):
        # Allow skipping LLM calls via env var `SKIP_OPENAI` for backward compat
        skip = os.getenv("SKIP_OPENAI", "false").lower() in ("1", "true", "yes")
        self.skip_openai = skip

        provider = os.getenv("LLM_PROVIDER", os.getenv("LLM", "openai")).lower()
        self.provider = provider

        if skip:
            self.client = None
        else:
            if provider == "openai":
                if OpenAI is None:
                    raise RuntimeError("OpenAI client library not available")
                self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            elif provider == "hf" or provider == "huggingface":
                if HFAdapter is None:
                    raise RuntimeError("HFAdapter not available")
                self.client = HFAdapter(model=os.getenv("HF_MODEL"))
            else:
                # Unknown provider — fall back to no client
                self.client = None

        self.model = model

