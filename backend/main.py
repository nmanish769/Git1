"""OpenLearn AI — Backend Application (FastAPI).
Serves the API endpoints and mounts the frontend/ directory.
Run directly from backend or project root:
    uvicorn main:app --reload
    py main.py
"""

import contextlib
import io
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Add backend directory to sys.path
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

# Also add parent to sys.path if needed
if str(CURRENT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR.parent))

from openlearn import llm, prompts
from openlearn.languages import LANGUAGES
from openlearn.levels import LEVELS

# Locate frontend directory flexibly
FRONTEND_DIR = CURRENT_DIR.parent / "frontend"
if not FRONTEND_DIR.exists():
    FRONTEND_DIR = CURRENT_DIR / "frontend"
if not FRONTEND_DIR.exists():
    FRONTEND_DIR = CURRENT_DIR.parent  # fallback to root
if not FRONTEND_DIR.exists():
    FRONTEND_DIR = CURRENT_DIR

app = FastAPI(
    title="OpenLearn AI Backend",
    description="Autonomous Multilingual CS Tutor Backend",
    version="2.0.0",
)

# Enable CORS for cross-origin frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Pydantic Request Models ----------
class LessonRequest(BaseModel):
    topic: str
    level: str = "Beginner"
    language: str = "English"
    backend: Optional[str] = "Ollama (Local Open-Weight Models)"
    base_url: Optional[str] = "http://localhost:11434"
    model: Optional[str] = "llama3.2"
    api_key: Optional[str] = ""


class FeedbackRequest(BaseModel):
    topic: str
    level: str = "Beginner"
    language: str = "English"
    lesson: Dict[str, Any]
    question: str
    answer: str
    backend: Optional[str] = "Ollama (Local Open-Weight Models)"
    base_url: Optional[str] = "http://localhost:11434"
    model: Optional[str] = "llama3.2"
    api_key: Optional[str] = ""


class CodeRunRequest(BaseModel):
    code: str


# ---------- API Endpoints ----------
@app.get("/health")
def health():
    return {"status": "ok", "app": "OpenLearn AI"}


@app.get("/api/status")
def get_status():
    """Returns backend status, available models, and supported providers."""
    ollama_models = llm.get_installed_ollama_models()
    return {
        "status": "online",
        "backends": list(llm.BACKENDS.keys()),
        "ollama_models": ollama_models,
        "default_backend": list(llm.BACKENDS.keys())[0],
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
            {"id": "recur", "icon": "🔄", "name": "Recursion & Stack"},
        ],
    }


@app.post("/api/lesson")
def generate_lesson(req: LessonRequest):
    """Generates a structured lesson with analogy, Mermaid diagram, and question."""
    if not req.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")

    backend_name = req.backend or list(llm.BACKENDS.keys())[0]
    base_url = req.base_url or "http://localhost:11434"
    model = req.model or "llama3.2"

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
    """Evaluates student answer kindly, diagnoses misconceptions, and awards XP."""
    if not req.answer.strip():
        raise HTTPException(status_code=400, detail="Answer cannot be empty.")

    backend_name = req.backend or list(llm.BACKENDS.keys())[0]
    base_url = req.base_url or "http://localhost:11434"
    model = req.model or "llama3.2"

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


# ---------- Static Frontend Files Mounting ----------
# Serves frontend files (index.html, style.css, app.js, script.js)
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 OpenLearn AI starting on http://localhost:{port}")
    print(f"📁 Serving frontend from: {FRONTEND_DIR}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
