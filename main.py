"""OpenLearn AI — Unified Full-Stack Runner.
Launches the FastAPI backend and serves the interactive frontend at http://localhost:8000.
"""

import sys
import threading
import time
import webbrowser
from pathlib import Path

# Add current directory to path
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

import uvicorn
from openlearn import llm


def open_browser(url: str, delay: float = 1.2):
    """Opens browser after server starts."""
    time.sleep(delay)
    try:
        webbrowser.open(url)
    except Exception:
        pass


def main():
    host = "127.0.0.1"
    port = 8000
    url = f"http://{host}:{port}"

    print("=" * 60)
    print("🎓 OpenLearn AI — Full-Stack Server Starting")
    print("=" * 60)
    print(f"👉 Local Web App: {url}")

    # Check Ollama status
    models = llm.get_installed_ollama_models()
    if models and models != ["llama3.2", "llama3.1", "qwen2.5", "mistral", "gemma2"]:
        print(f"🦙 Ollama Detected Models: {', '.join(models)}")
    else:
        print("💡 Ollama Tip: Run 'ollama pull llama3.2' in terminal to download local model.")

    print("=" * 60)
    print("Press CTRL+C to stop the server\n")

    # Launch browser automatically in a background thread
    threading.Thread(target=open_browser, args=(url,), daemon=True).start()

    # Start Uvicorn
    uvicorn.run("server:app", host=host, port=port, reload=False, log_level="info")


if __name__ == "__main__":
    main()
