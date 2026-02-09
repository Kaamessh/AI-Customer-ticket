from __future__ import annotations
from pathlib import Path
from typing import Any, Dict
import json

from langchain_community.chat_models import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

SYSTEM_PROMPT_FILE = Path(__file__).with_name("system_prompt.txt")

MODEL_NAME = "llama3.1:8b"


class LaptopAI:
    """Laptop-only AI powered by Ollama via LangChain.

    Usage:
        ai = LaptopAI()
        result = ai.handle_query("My laptop battery drains fast")
    """

    def __init__(self, model: str = MODEL_NAME, base_url: str | None = None) -> None:
        self.model = model
        self.base_url = base_url
        # ChatOllama supports base_url (e.g., http://localhost:11434)
        self.client = ChatOllama(model=self.model, base_url=self.base_url)
        self.system_prompt = SYSTEM_PROMPT_FILE.read_text(encoding="utf-8")

    def _to_json(self, text: str) -> Dict[str, Any]:
        """Best-effort JSON parsing returning required keys even on malformed output."""
        required = ["Issue", "Category", "Priority", "Suggested Fix", "Ticket Required"]
        try:
            data = json.loads(text)
            # normalize keys to exact expected labels
            normalized: Dict[str, Any] = {}
            for key in required:
                # accept various casings
                candidates = [key, key.lower(), key.replace(" ", ""), key.replace(" ", "_").lower()]
                for c in candidates:
                    if c in data:
                        normalized[key] = data[c]
                        break
                else:
                    normalized[key] = None
            return normalized
        except Exception:
            # fallback: craft minimal structure
            return {
                "Issue": text.strip(),
                "Category": "Software",
                "Priority": "Medium",
                "Suggested Fix": "",
                "Ticket Required": False,
            }

    def handle_query(self, query: str) -> Dict[str, Any]:
        """Generate a structured answer strictly for laptop issues.

        Returns a dict with keys: Issue, Category, Priority, Suggested Fix, Ticket Required.
        """
        messages = [SystemMessage(content=self.system_prompt), HumanMessage(content=query)]
        res = self.client.invoke(messages)
        # ChatOllama returns AIMessage with .content
        return self._to_json(res.content)
