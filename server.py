"""FastAPI Backend Server for OpenLearn AI.

Provides REST endpoints for:
- Multi-Model LLM lesson generation (Gemini, Groq, OpenRouter, OpenAI, DeepSeek, Ollama, Offline).
- Intelligent misconception diagnosis & practice evaluation.
- Real-time student doubt answering & code explanation.
- Model connectivity testing.
- Sandboxed Python code execution.
- Serving modern Single-Page Application frontend.
"""

import contextlib
import io
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import requests
except ImportError:
    requests = None

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Add current directory to path
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from openlearn import llm, prompts
from openlearn.languages import LANGUAGES
from openlearn.levels import LEVELS

app = FastAPI(
    title="OpenLearn AI API",
    description="Autonomous Multilingual Computer Science Tutor Backend with Multi-Model AI Linking",
    version="2.5.0",
)

# Enable CORS for cross-origin access (e.g. GitHub Pages or local testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory if present
STATIC_DIR = CURRENT_DIR / "static"
if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ---------- Pydantic Request Models ----------
class LessonRequest(BaseModel):
    topic: str
    level: str = "Beginner"
    language: str = "English"
    backend: Optional[str] = "Google Gemini"
    base_url: Optional[str] = ""
    model: Optional[str] = "gemini-1.5-flash"
    api_key: Optional[str] = ""


class FeedbackRequest(BaseModel):
    topic: str
    level: str = "Beginner"
    language: str = "English"
    lesson: Dict[str, Any]
    question: str
    answer: str
    backend: Optional[str] = "Google Gemini"
    base_url: Optional[str] = ""
    model: Optional[str] = "gemini-1.5-flash"
    api_key: Optional[str] = ""


class DoubtRequest(BaseModel):
    topic: str
    level: str = "Beginner"
    language: str = "English"
    question: str
    code_context: Optional[str] = ""
    backend: Optional[str] = "Google Gemini"
    base_url: Optional[str] = ""
    model: Optional[str] = "gemini-1.5-flash"
    api_key: Optional[str] = ""


class TestConnectionRequest(BaseModel):
    backend: str
    api_key: Optional[str] = ""
    base_url: Optional[str] = ""
    model: Optional[str] = ""


class CodeRunRequest(BaseModel):
    code: str


class ChatRequest(BaseModel):
    question: str


# ---------- API Endpoints ----------
@app.get("/health")
def health():
    return {"status": "ok", "app": "OpenLearn AI", "version": "2.5.0"}


@app.get("/api/status")
def get_status():
    """Check backend health, detected Ollama models, and configured backends."""
    ollama_models = llm.get_installed_ollama_models()
    return {
        "status": "online",
        "backends": list(llm.BACKENDS.keys()),
        "ollama_models": ollama_models,
        "default_backend": "Google Gemini",
    }


@app.get("/api/options")
def get_options():
    """Returns available languages, pedagogical levels, and starter topics."""
    return {
        "languages": list(LANGUAGES.keys()),
        "levels": list(LEVELS.keys()),
        "quick_topics": [
            {"id": "vars", "icon": "📦", "name": "Variables & Memory"},
            {"id": "loops", "icon": "🔁", "name": "Loops & Iterations"},
            {"id": "branch", "icon": "🔀", "name": "Conditionals (If-Else)"},
            {"id": "funcs", "icon": "🎯", "name": "Functions & Scope"},
            {"id": "lists", "icon": "📚", "name": "Lists & Arrays"},
            {"id": "dicts", "icon": "🗂️", "name": "Dictionaries & Maps"},
            {"id": "recur", "icon": "🔄", "name": "Recursion & Call Stack"},
            {"id": "oop", "icon": "🏗️", "name": "Object-Oriented (Classes)"},
            {"id": "search", "icon": "🔍", "name": "Binary Search"},
            {"id": "bigo", "icon": "⚡", "name": "Big-O Complexity"},
        ],
    }


@app.post("/api/lesson")
def generate_lesson(req: LessonRequest):
    """Generates an intuitive lesson with real-world analogy, Python code, and Mermaid diagram."""
    if not req.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")

    backend_name = req.backend or "Google Gemini"
    base_url = req.base_url or ""
    model = req.model or ""

    try:
        user_prompt = prompts.lesson_prompt(req.topic.strip(), req.level, req.language)
        result = llm.ask_json(
            backend_name,
            base_url,
            model,
            prompts.SYSTEM,
            user_prompt,
            api_key=req.api_key or "",
        )
        return {"success": True, "lesson": result}
    except llm.LLMError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {e}")


@app.post("/api/feedback")
def evaluate_feedback(req: FeedbackRequest):
    """Evaluates student answer, identifies misconceptions, and awards XP."""
    if not req.answer.strip():
        raise HTTPException(status_code=400, detail="Answer cannot be empty.")

    backend_name = req.backend or "Google Gemini"
    base_url = req.base_url or ""
    model = req.model or ""

    try:
        user_prompt = prompts.feedback_prompt(
            req.topic, req.level, req.language, req.lesson, req.question, req.answer.strip()
        )
        result = llm.ask_json(
            backend_name,
            base_url,
            model,
            prompts.SYSTEM,
            user_prompt,
            api_key=req.api_key or "",
        )
        return {"success": True, "feedback": result}
    except llm.LLMError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {e}")


@app.post("/api/ask")
def answer_student_doubt(req: DoubtRequest):
    """Answers any custom student question, confusion, or doubt about a concept or code."""
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    backend_name = req.backend or "Google Gemini"
    base_url = req.base_url or ""
    model = req.model or ""

    try:
        user_prompt = prompts.doubt_prompt(
            req.topic, req.level, req.language, req.question.strip(), req.code_context or ""
        )
        result = llm.ask_json(
            backend_name,
            base_url,
            model,
            prompts.SYSTEM,
            user_prompt,
            api_key=req.api_key or "",
        )
        return {"success": True, "answer": result}
    except llm.LLMError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {e}")


@app.post("/api/chat")
def chat_with_ollama(req: ChatRequest):
    """Direct chat endpoint matching Express /api/chat. Calls local Ollama (llama3.2) or smart fallback.
    Returns JSON: {"answer": "..."}
    """
    if not req.question or not req.question.strip():
        return {"answer": "Please provide a question."}

    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "llama3.2")

    # 1. Attempt to query local Ollama instance
    if requests is not None:
        try:
            r = requests.post(
                f"{ollama_url.rstrip('/')}/api/chat",
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": req.question.strip()}],
                    "stream": False,
                },
                timeout=(3.0, 30.0),
            )
            if r.ok:
                data = r.json()
                content = data.get("message", {}).get("content", "")
                if content:
                    return {"answer": content}
        except Exception:
            pass

    # 2. If Ollama is offline or not installed, provide intelligent OpenLearn AI response
    try:
        from openlearn.mock_data import get_offline_doubt_answer
        doubt_res = get_offline_doubt_answer("Computer Science", req.question.strip(), "")
        ans = doubt_res.get("direct_answer", "")
        analogy = doubt_res.get("analogy", "")
        pro_tip = doubt_res.get("pro_tip", "")

        out = f"[Ollama at {ollama_url} is currently offline. OpenLearn AI Response]:\n\n{ans}"
        if analogy:
            out += f"\n\n🏠 Relatable Analogy: {analogy}"
        if pro_tip:
            out += f"\n\n💡 Pro Tip: {pro_tip}"
        return {"answer": out}
    except Exception:
        pass

    return {
        "answer": f"Could not connect to Ollama at {ollama_url}. Make sure Ollama is running locally with 'ollama run {model}'."
    }


@app.post("/api/test-connection")
def test_connection(req: TestConnectionRequest):
    """Tests connection to a specified AI provider."""
    result = llm.test_model_connection(
        req.backend,
        api_key=req.api_key or "",
        base_url=req.base_url or "",
        model=req.model or "",
    )
    return result


@app.post("/api/run-code")
def run_sandbox_code(req: CodeRunRequest):
    """Executes safe beginner Python snippets in a captured stdout sandbox."""
    buffer = io.StringIO()
    safe_globals = {
        "__builtins__": {
            "print": print,
            "range": range,
            "len": len,
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "list": list,
            "dict": dict,
            "set": set,
            "min": min,
            "max": max,
            "sum": sum,
            "enumerate": enumerate,
            "zip": zip,
            "abs": abs,
            "round": round,
        }
    }
    try:
        with contextlib.redirect_stdout(buffer):
            exec(req.code, safe_globals, {})
        output = buffer.getvalue()
        return {
            "success": True,
            "output": output if output else "(Snippet ran successfully with no output printed)",
        }
    except Exception as e:
        return {"success": False, "output": f"Execution Error ({type(e).__name__}): {e}"}


# ---------- Static Frontend Files Serving ----------
@app.get("/")
def serve_index():
    """Serves the main frontend Single Page Application."""
    index_file = CURRENT_DIR / "index.html"
    if not index_file.exists():
        index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "OpenLearn AI Backend running."}


@app.get("/style.css")
def serve_css():
    css_file = CURRENT_DIR / "style.css"
    if not css_file.exists():
        css_file = STATIC_DIR / "style.css"
    return FileResponse(css_file, media_type="text/css")


@app.get("/script.js")
def serve_script():
    js_file = CURRENT_DIR / "script.js"
    if not js_file.exists():
        js_file = STATIC_DIR / "script.js"
    return FileResponse(js_file, media_type="application/javascript")


@app.get("/app.js")
def serve_app_js():
    js_file = CURRENT_DIR / "app.js"
    if not js_file.exists():
        js_file = STATIC_DIR / "app.js"
    return FileResponse(js_file, media_type="application/javascript")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
