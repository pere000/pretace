#!/usr/bin/env python3

import json
import os
from pathlib import Path

import requests


class OllamaClient:

    def __init__(

        self,

        model=None,

        host=None,

    ):

        config = self._load_runtime_config()

        configured_model = (
            config.get("models", {}).get("local_ai")
            or "qwen3:latest"
        )
        configured_host = (
            config.get("ollama", {}).get("base_url")
            or "http://host.containers.internal:11434"
        )

        self.model = model or os.getenv("OLLAMA_MODEL", configured_model)

        base_url = host or os.getenv("OLLAMA_BASE_URL", configured_host)
        self.url = base_url.rstrip("/") + "/api/generate"

    def ask(self, prompt):

        payload = {

            "model": self.model,

            "prompt": prompt,

            "stream": False,

            "think": False,

        }

        response = requests.post(

            self.url,

            json=payload,

            timeout=300,

        )


        response.raise_for_status()

        data = response.json()

        return data["response"]

        return response.json()["response"]

    def _load_runtime_config(self):

        runtime_path = Path(__file__).resolve().parent / "new_tace_runtime.json"

        if not runtime_path.exists():
            return {}

        with runtime_path.open("r", encoding="utf-8") as f:
            return json.load(f)


if __name__ == "__main__":

    client = OllamaClient()

    answer = client.ask(

        "Who wrote Hamlet?"

    )

    print("\nANSWER:\n")

    print(answer)
