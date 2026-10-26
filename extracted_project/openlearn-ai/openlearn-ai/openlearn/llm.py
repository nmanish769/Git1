"""Model interface. Supports any backend by adding a function here.

Backends:
  - "Ollama (local open-weight model)": default, e.g. llama3.1, qwen2.5, gemma2
  - "OpenAI-compatible API": works with vLLM, llama.cpp server, LM Studio,
    Together, Groq, etc. (anything exposing /v1/chat/completions)
"""

import json
import re

import requests

TIMEOUT = 180


class LLMError(RuntimeError):
    pass


def _ollama(base_url, model, messages, **_):
    r = requests.post(
        f"{base_url.rstrip('/')}/api/chat",
        json={"model": model, "messages": messages, "stream": False, "format": "json"},
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    return r.json()["message"]["content"]


def _openai_compatible(base_url, model, messages, api_key="", **_):
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    r = requests.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers=headers,
        json={"model": model, "messages": messages, "temperature": 0.4},
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


BACKENDS = {
    "Ollama (local open-weight model)": (_ollama, "http://localhost:11434", "llama3.1"),
    "OpenAI-compatible API": (_openai_compatible, "http://localhost:8000/v1", "your-model-name"),
}


def extract_json(text: str) -> dict:
    """Pull the first JSON object out of a model response, tolerating code fences."""
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise LLMError("The model did not return JSON.")
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError as e:
        raise LLMError(f"Could not parse the model's JSON: {e}")


def ask_json(backend, base_url, model, system, user, api_key="", retries=1) -> dict:
    fn = BACKENDS[backend][0]
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    last = None
    for _ in range(retries + 1):
        try:
            raw = fn(base_url, model, messages, api_key=api_key)
            return extract_json(raw)
        except requests.RequestException as e:
            raise LLMError(f"Could not reach the model at {base_url}: {e}")
        except LLMError as e:
            last = e
    raise last
