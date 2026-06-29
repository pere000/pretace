#!/usr/bin/env python3

import requests


class OllamaClient:

    def __init__(

        self,

        model="qwen3:latest",

        host="http://localhost:11434",

    ):

        self.model = model

        self.url = host + "/api/generate"

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


if __name__ == "__main__":

    client = OllamaClient()

    answer = client.ask(

        "Who wrote Hamlet?"

    )

    print("\nANSWER:\n")

    print(answer)
