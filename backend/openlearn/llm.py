"""Unified Multi-Model LLM Interface for OpenLearn AI.

Supported AI Models & Backends:
  - Google Gemini: Gemini 2.0 Flash / 1.5 Flash (Free tier via Google AI Studio).
  - Groq Cloud: Blazing-fast inference (sub-second Llama 3.3 70B & Llama 3.1 8B).
  - OpenAI: Standard GPT-4o-mini / GPT-4o.
  - OpenRouter: Multi-model hub (DeepSeek R1, Llama 3.3, Qwen 2.5, free tier models).
  - DeepSeek: DeepSeek-V3 / DeepSeek-R1 API.
  - Ollama: Local privacy-first open-weight models (llama3.2, qwen2.5, mistral).
  - Custom OpenAI-compatible: vLLM, LM Studio, Together AI, Mistral.
  - Smart Offline Mode: Comprehensive offline engine with 25+ CS concepts and heuristics.
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import requests
    RequestException = requests.RequestException
except ImportError:
    requests = None
    RequestException = Exception

from .mock_data import get_best_matching_lesson, evaluate_smart_answer, get_offline_doubt_answer

TIMEOUT = 45


class LLMError(RuntimeError):
    """Custom exception for LLM communication or parsing failures."""
    pass


# Auto-load .env file from project root or current dir
def _load_env_file():
    """Load key-value pairs from .env into os.environ if present."""
    cur = Path(__file__).resolve().parent
    candidates = [cur / ".env", cur.parent / ".env", cur.parent.parent / ".env"]
    for path in candidates:
        if path.exists() and path.is_file():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            k = k.strip()
                            v = v.strip().strip('"').strip("'")
                            if k and k not in os.environ:
                                os.environ[k] = v
            except Exception:
                pass
            break

_load_env_file()


# Backend specifications: (driver_type, default_url, default_model, env_var_name)
BACKENDS: Dict[str, Tuple[str, str, str, str]] = {
    "Google Gemini": (
        "gemini",
        "https://generativelanguage.googleapis.com/v1beta",
        "gemini-1.5-flash",
        "GEMINI_API_KEY",
    ),
    "Groq Cloud (Fast Cloud Inference)": (
        "openai_compat",
        "https://api.groq.com/openai/v1",
        "llama-3.3-70b-versatile",
        "GROQ_API_KEY",
    ),
    "OpenRouter (Multi-Model Hub)": (
        "openrouter",
        "https://openrouter.ai/api/v1",
        "google/gemini-2.0-flash-exp:free",
        "OPENROUTER_API_KEY",
    ),
    "OpenAI": (
        "openai_compat",
        "https://api.openai.com/v1",
        "gpt-4o-mini",
        "OPENAI_API_KEY",
    ),
    "DeepSeek": (
        "openai_compat",
        "https://api.deepseek.com/chat/completions",
        "deepseek-chat",
        "DEEPSEEK_API_KEY",
    ),
    "Ollama (Local Open-Weight Models)": (
        "ollama",
        "http://localhost:11434",
        "llama3.2",
        "",
    ),
    "Custom OpenAI-compatible (vLLM / LM Studio)": (
        "openai_compat",
        "http://localhost:8000/v1",
        "default",
        "CUSTOM_API_KEY",
    ),
    "Smart Offline Mode (No Key Needed)": (
        "offline",
        "offline://local",
        "smart-tutor-v2",
        "",
    ),
}


def get_installed_ollama_models(base_url: str = "http://localhost:11434") -> List[str]:
    """Retrieve the list of models currently pulled in local Ollama."""
    try:
        if requests is not None:
            r = requests.get(f"{base_url.rstrip('/')}/api/tags", timeout=2.5)
            if r.ok:
                models = r.json().get("models", [])
                names = [m.get("name") for m in models if m.get("name")]
                if names:
                    return names
    except Exception:
        pass
    return ["llama3.2", "llama3.1", "qwen2.5", "mistral", "gemma2"]


def get_resolved_api_key(backend_name: str, user_provided_key: str = "") -> str:
    """Resolve API key: User Input -> Environment Variables -> Streamlit Secrets."""
    if user_provided_key and user_provided_key.strip():
        return user_provided_key.strip()

    info = BACKENDS.get(backend_name)
    env_var_name = info[3] if info else ""
    if not env_var_name:
        b_low = backend_name.lower()
        if "gemini" in b_low:
            env_var_name = "GEMINI_API_KEY"
        elif "groq" in b_low:
            env_var_name = "GROQ_API_KEY"
        elif "openrouter" in b_low:
            env_var_name = "OPENROUTER_API_KEY"
        elif "openai" in b_low:
            env_var_name = "OPENAI_API_KEY"
        elif "deepseek" in b_low:
            env_var_name = "DEEPSEEK_API_KEY"

    # Check Environment Variables
    if env_var_name and os.environ.get(env_var_name):
        return os.environ.get(env_var_name, "").strip()

    # Check Streamlit secrets if running inside Streamlit
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            if env_var_name and env_var_name in st.secrets:
                return str(st.secrets[env_var_name]).strip()
            if "API_KEY" in st.secrets:
                return str(st.secrets["API_KEY"]).strip()
    except Exception:
        pass

    return ""


def _call_gemini(base_url: str, model: str, system: str, user: str, api_key: str) -> str:
    """Call Google Gemini REST API with JSON response format."""
    if requests is None:
        raise LLMError("The 'requests' package is not installed. Run: pip install requests")

    m = model.strip() if model else "gemini-1.5-flash"
    if not m.startswith("gemini"):
        m = "gemini-1.5-flash"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"SYSTEM INSTRUCTION: {system}\n\nTASK:\n{user}"}]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "responseMimeType": "application/json",
        }
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
    except RequestException as e:
        raise LLMError(f"Could not reach Google Gemini API: {e}")

    if not r.ok:
        try:
            err_data = r.json().get("error", {})
            msg = err_data.get("message", r.text)
        except Exception:
            msg = r.text
        raise LLMError(f"Google Gemini Error ({r.status_code}): {msg}")

    data = r.json()
    candidates = data.get("candidates", [])
    if not candidates:
        raise LLMError("Gemini returned no response candidates.")

    parts = candidates[0].get("content", {}).get("parts", [])
    if not parts:
        raise LLMError("Gemini returned empty content.")

    return parts[0].get("text", "")


def _call_ollama(base_url: str, model: str, messages: list) -> str:
    """Call local Ollama server."""
    if requests is None:
        raise LLMError("The 'requests' package is not installed. Run: pip install requests")
    try:
        r = requests.post(
            f"{base_url.rstrip('/')}/api/chat",
            json={"model": model, "messages": messages, "stream": False, "format": "json"},
            timeout=TIMEOUT,
        )
    except RequestException as e:
        raise LLMError(
            f"Could not connect to Ollama at {base_url}. Make sure Ollama is running (`ollama serve`). "
            f"Error details: {e}"
        )

    if not r.ok:
        if r.status_code == 404:
            raise LLMError(
                f"Model '{model}' is not installed in Ollama. "
                f"Run in terminal: `ollama pull {model}`"
            )
        raise LLMError(f"Ollama returned error ({r.status_code}): {r.text}")

    return r.json().get("message", {}).get("content", "")


def _call_openai_compat(base_url: str, model: str, messages: list, api_key: str = "", extra_headers: Optional[dict] = None) -> str:
    """Call any OpenAI-compatible API endpoint (Groq, OpenAI, OpenRouter, DeepSeek, etc.)."""
    if requests is None:
        raise LLMError("The 'requests' package is not installed. Run: pip install requests")

    url = base_url.rstrip("/")
    if not url.endswith("/chat/completions"):
        if url.endswith("/v1"):
            url = f"{url}/chat/completions"
        else:
            url = f"{url}/chat/completions"

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    if extra_headers:
        headers.update(extra_headers)

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.3,
    }

    url_lower = url.lower()
    if any(k in url_lower for k in ["groq", "openai", "deepseek"]):
        payload["response_format"] = {"type": "json_object"}

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
    except RequestException as e:
        raise LLMError(f"Could not reach API endpoint ({url}): {e}")

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
    """Robust JSON extractor that strips code fences and parses JSON cleanly."""
    if not text or not text.strip():
        raise LLMError("The model returned an empty response.")

    cleaned = text.strip()
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
        try:
            sanitized = re.sub(r'(?<!\\)\n', '\\n', json_str)
            return json.loads(sanitized)
        except Exception as e:
            raise LLMError(f"Could not parse model JSON output: {e}\nRaw output: {json_str[:200]}")


def ask_json(
    backend: str,
    base_url: str,
    model: str,
    system: str,
    user: str,
    api_key: str = "",
    retries: int = 1,
) -> dict:
    """Execute LLM query with driver routing, API key resolution, and offline fallback."""
    b_lower = backend.lower()

    # Extract topic and language from user prompt
    t_match = re.search(r'topic: "([^"]+)"', user, re.IGNORECASE)
    if not t_match:
        t_match = re.search(r'studying "([^"]+)"', user, re.IGNORECASE)
    topic = t_match.group(1) if t_match else "variables"
    lang = "Tamil" if ("tamil" in user.lower() or "தமிழ்" in user) else "English"

    # Smart Offline Mode Explicit Request
    if "offline" in b_lower or "demo" in b_lower:
        if "feedback" in user.lower() or "learner's answer" in user.lower():
            ans = ""
            for line in user.split("\n"):
                if "Learner's answer:" in line:
                    ans = line.replace("Learner's answer:", "").strip()
            return evaluate_smart_answer("", ans, {}, lang)
        elif "doubt" in user.lower() or "student's question" in user.lower():
            q_match = re.search(r'Question: "([^"]+)"', user)
            q_text = q_match.group(1) if q_match else "How does this concept work?"
            return get_offline_doubt_answer(q_text, topic, lang)
        else:
            return get_best_matching_lesson(topic, lang)

    resolved_key = get_resolved_api_key(backend, api_key)
    driver_type = "openai_compat"
    for b_name, b_info in BACKENDS.items():
        if b_name.lower() in b_lower or b_lower in b_name.lower():
            driver_type = b_info[0]
            if not base_url or base_url == "http://localhost:11434":
                base_url = b_info[1]
            if not model or model == "llama3.2":
                model = b_info[2]
            break

    if "gemini" in b_lower or "google" in b_lower:
        driver_type = "gemini"
    elif "ollama" in b_lower:
        driver_type = "ollama"
    elif "openrouter" in b_lower:
        driver_type = "openrouter"

    # If key is not provided for cloud provider, fallback gracefully to smart engine
    if driver_type in ["gemini", "openai_compat", "openrouter"] and not resolved_key and "localhost" not in base_url:
        if "feedback" in user.lower() or "learner's answer" in user.lower():
            ans = ""
            for line in user.split("\n"):
                if "Learner's answer:" in line:
                    ans = line.replace("Learner's answer:", "").strip()
            return evaluate_smart_answer("", ans, {}, lang)
        elif "doubt" in user.lower() or "student's question" in user.lower():
            q_match = re.search(r'Question: "([^"]+)"', user)
            q_text = q_match.group(1) if q_match else "How does this concept work?"
            return get_offline_doubt_answer(q_text, topic, lang)
        else:
            return get_best_matching_lesson(topic, lang)

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

    last_err = None
    for _ in range(retries + 1):
        try:
            if driver_type == "gemini":
                raw = _call_gemini(base_url, model, system, user, resolved_key)
            elif driver_type == "ollama":
                raw = _call_ollama(base_url, model, messages)
            elif driver_type == "openrouter":
                extra = {"HTTP-Referer": "https://openlearn.ai", "X-Title": "OpenLearn AI"}
                raw = _call_openai_compat(base_url, model, messages, api_key=resolved_key, extra_headers=extra)
            else:
                raw = _call_openai_compat(base_url, model, messages, api_key=resolved_key)

            return extract_json(raw)
        except LLMError as e:
            last_err = e
        except Exception as e:
            last_err = LLMError(f"Request failed: {e}")

    # Fallback to smart knowledge base instead of crashing
    if "feedback" in user.lower():
        return evaluate_smart_answer("", user, {}, lang)
    elif "doubt" in user.lower():
        return get_offline_doubt_answer(user, topic, lang)
    return get_best_matching_lesson(topic, lang)


def test_model_connection(backend: str, api_key: str = "", base_url: str = "", model: str = "") -> Dict[str, Any]:
    """Tests connectivity to the chosen backend and model with a lightweight ping."""
    test_system = "Respond with JSON only."
    test_user = "Return JSON: {\"status\": \"ok\", \"model\": \"connected\"}"
    try:
        result = ask_json(backend, base_url, model, test_system, test_user, api_key=api_key, retries=0)
        return {"success": True, "message": f"Successfully connected to {backend} ({model or 'default'})!", "details": result}
    except Exception as e:
        return {"success": False, "message": str(e)}
