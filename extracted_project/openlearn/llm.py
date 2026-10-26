"""Model interface supporting Multi-Cloud & Local Backends.

Supported Backends:
  - Groq Cloud: Blazing-fast inference (sub-second), ideal for live hackathon demos.
  - Google Gemini: Generous free tier via OpenAI compatibility endpoint.
  - OpenAI: Standard GPT-4o-mini / GPT-4o.
  - Ollama: Local privacy-first open-weight model (llama3.1, qwen2.5, mistral).
  - Custom OpenAI-compatible: vLLM, LM Studio, OpenRouter, Together AI.
  - Fail-Safe Demo Mode: Instant offline responses without requiring API keys or network.
"""

import json
import os
import re
from typing import Dict, Tuple

try:
    import requests
    RequestException = requests.RequestException
except ImportError:
    requests = None
    RequestException = Exception

from .mock_data import get_mock_feedback, get_mock_lesson

TIMEOUT = 60


class LLMError(RuntimeError):
    """Custom exception for LLM communication or parsing failures."""
    pass


# Default configurations: (handler_function, default_url, default_model, env_key_name)
BACKENDS: Dict[str, Tuple[str, str, str]] = {
    "Groq Cloud (Fastest - Recommended)": (
        "openai_compat",
        "https://api.groq.com/openai/v1",
        "llama-3.3-70b-versatile",
        "GROQ_API_KEY",
    ),
    "Google Gemini": (
        "openai_compat",
        "https://generativelanguage.googleapis.com/v1beta/openai",
        "gemini-1.5-flash",
        "GEMINI_API_KEY",
    ),
    "OpenAI": (
        "openai_compat",
        "https://api.openai.com/v1",
        "gpt-4o-mini",
        "OPENAI_API_KEY",
    ),
    "Ollama (Local Open-Weight)": (
        "ollama",
        "http://localhost:11434",
        "llama3.1",
        "",
    ),
    "Custom OpenAI-compatible (vLLM / LM Studio)": (
        "openai_compat",
        "http://localhost:8000/v1",
        "default",
        "CUSTOM_API_KEY",
    ),
    "Fail-Safe Demo Mode (Offline / No Key Needed)": (
        "mock",
        "mock://local",
        "mock-tutor-v1",
        "",
    ),
}


def get_resolved_api_key(backend_name: str, user_provided_key: str = "") -> str:
    """Resolve API key checking user input -> Streamlit secrets -> OS environment."""
    if user_provided_key and user_provided_key.strip():
        return user_provided_key.strip()

    env_var_name = BACKENDS.get(backend_name, ("", "", "", ""))[3]
    if not env_var_name:
        return ""

    # Check Streamlit secrets if running inside Streamlit
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            if env_var_name in st.secrets:
                return str(st.secrets[env_var_name]).strip()
            # Generic fallbacks
            if "API_KEY" in st.secrets:
                return str(st.secrets["API_KEY"]).strip()
    except Exception:
        pass

    # Check Environment Variables
    return os.environ.get(env_var_name, "").strip()


def _call_ollama(base_url: str, model: str, messages: list, **_) -> str:
    if requests is None:
        raise LLMError("The 'requests' package is not installed. Please run: pip install requests")
    r = requests.post(
        f"{base_url.rstrip('/')}/api/chat",
        json={"model": model, "messages": messages, "stream": False, "format": "json"},
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    return r.json().get("message", {}).get("content", "")


def _call_openai_compat(base_url: str, model: str, messages: list, api_key: str = "", **_) -> str:
    if requests is None:
        raise LLMError("The 'requests' package is not installed. Please run: pip install requests")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.4,
    }
    # For models supporting response_format: json_object
    if "groq" in base_url or "openai" in base_url:
        payload["response_format"] = {"type": "json_object"}

    r = requests.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers=headers,
        json=payload,
        timeout=TIMEOUT,
    )
    if not r.ok:
        try:
            err_msg = r.json().get("error", {}).get("message", r.text)
        except Exception:
            err_msg = r.text
        raise LLMError(f"API Error ({r.status_code}): {err_msg}")

    res_json = r.json()
    choices = res_json.get("choices", [])
    if not choices:
        raise LLMError("API returned no completion choices.")
    return choices[0].get("message", {}).get("content", "")


def extract_json(text: str) -> dict:
    """Robust JSON extractor that strips code fences and locates outermost braces."""
    if not text or not text.strip():
        raise LLMError("The model returned an empty response.")

    cleaned = text.strip()
    # Strip markdown fences if present
    cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"```$", "", cleaned, flags=re.MULTILINE).strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise LLMError("The model response did not contain a valid JSON object.")

    json_str = cleaned[start : end + 1]
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # Attempt minimal repair: fix raw unescaped newlines in strings
        try:
            sanitized = re.sub(r'(?<!\\)\n', '\\n', json_str)
            return json.loads(sanitized)
        except Exception as e:
            raise LLMError(f"Could not parse model JSON output: {e}")


def ask_json(
    backend: str,
    base_url: str,
    model: str,
    system: str,
    user: str,
    api_key: str = "",
    retries: int = 1,
) -> dict:
    """Execute LLM query with retry logic and fallback."""
    # Fail-Safe Demo Mode
    if backend == "Fail-Safe Demo Mode (Offline / No Key Needed)":
        if "feedback" in user.lower() or "learner's answer" in user.lower():
            # Extract student answer from prompt
            lines = user.split("\n")
            ans = ""
            for l in lines:
                if "Learner's answer:" in l:
                    ans = l.replace("Learner's answer:", "").strip()
            return get_mock_feedback(ans)
        else:
            # Extract topic & language
            t_match = re.search(r'topic: "([^"]+)"', user)
            topic = t_match.group(1) if t_match else "variables"
            lang = "Tamil" if "Tamil" in user or "தமிழ்" in user else "English"
            return get_mock_lesson(topic, lang)

    resolved_key = get_resolved_api_key(backend, api_key)
    driver_type = BACKENDS.get(backend, ("openai_compat", "", "", ""))[0]

    if driver_type == "openai_compat" and not resolved_key and "localhost" not in base_url:
        raise LLMError(
            f"API Key required for {backend}. Please enter your API key in the sidebar, "
            f"or select 'Fail-Safe Demo Mode' for an instant offline demo!"
        )

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

    last_err = None
    for attempt in range(retries + 1):
        try:
            if driver_type == "ollama":
                raw = _call_ollama(base_url, model, messages)
            else:
                raw = _call_openai_compat(base_url, model, messages, api_key=resolved_key)
            return extract_json(raw)
        except RequestException as e:
            last_err = LLMError(f"Could not reach {backend} endpoint: {e}")
        except LLMError as e:
            last_err = e

    raise last_err if last_err else LLMError("Unknown error occurred while contacting LLM.")
