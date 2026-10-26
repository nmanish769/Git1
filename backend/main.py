"""OpenLearn AI — Backend FastAPI Application & Runner.
Serves API endpoints and static assets.
Run with:
    uvicorn backend.main:app --reload
    py backend/main.py
"""

import os
import sys
from pathlib import Path

# Add current and parent directory to path
CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
for p in [str(CURRENT_DIR), str(PARENT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Re-export the main FastAPI app from server
from server import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 OpenLearn AI Backend starting on http://localhost:{port}")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)
