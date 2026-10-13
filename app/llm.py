import os
from openai import OpenAI

MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
_client = None

# USD per 1M tokens (input, output); update if you change models
PRICES = {"gpt-4o-mini": (0.15, 0.60), "gpt-4o": (2.50, 10.00)}


def client():
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _client


class Usage:
    def __init__(self):
        self.input = 0
        self.output = 0

    def add(self, resp):
        self.input += resp.usage.prompt_tokens
        self.output += resp.usage.completion_tokens

    @property
    def cost(self):
        pin, pout = PRICES.get(MODEL, (0, 0))
        return (self.input * pin + self.output * pout) / 1_000_000


def chat(messages, usage):
    resp = client().chat.completions.create(model=MODEL, messages=messages, temperature=0)
    usage.add(resp)
    return resp.choices[0].message.content


def extract_sql(text):
    """Pull the SQL out of a ```sql fenced block if the model used one."""
    if "```" in text:
        text = text.split("```", 1)[1]
        nl = text.find("\n")
        if nl != -1:
            text = text[nl + 1:]
        text = text.split("```", 1)[0]
    return text.strip()
