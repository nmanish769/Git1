# 🎓 OpenLearn AI — Autonomous Multilingual CS Tutor

[![Live Website](https://img.shields.io/badge/Live_Website-GitHub_Pages-blue?style=for-the-badge&logo=github)](https://nmanish769.github.io/Git1/)
[![Deploy to Render](https://img.shields.io/badge/Deploy%20to-Render-46E3B7?style=for-the-badge&logo=render)](https://render.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Model Support](https://img.shields.io/badge/AI_Engines-Groq_|_Ollama_|_Gemini_|_Client_Offline-orange.svg)]()

> **Interactive, multilingual computer science tutor designed for hackathons and schools.**  
> Demystifying programming concepts in your native tongue (English, Tamil, Hindi, Telugu, Kannada, Spanish, French) through real-world cultural analogies, dynamic visual flowcharts, live code sandboxes, and adaptive misconception diagnosis.

---

## 🌐 Try the Live Interactive Website

👉 **[https://nmanish769.github.io/Git1/](https://nmanish769.github.io/Git1/)**

Anyone can open and interact with the live website directly in their browser:
- ⚡ **1-Click Topic Chips**: Jump into *Variables, Loops, If-Else, Functions, Lists, or Recursion*.
- 📊 **Dynamic Mermaid.js Flowcharts**: Visual mental models generated on the fly.
- 🔊 **Voice Read-Aloud**: Browser-native Text-to-Speech in regional languages.
- 💻 **Live Code Sandbox**: Run and test Python snippets in-browser.
- 🎯 **Misconception Diagnosis**: Intelligent evaluation explaining *why* an answer is flawed.
- 🎮 **Gamification HUD**: Streaks, XP rewards, rank promotions, and confetti celebrations.
- ⚙️ **AI Engine Flexibility**: Runs 100% offline in client mode, or connect your free Groq/Gemini key or local Ollama!

---

## 🚀 Quick Start (Run Locally on Windows/Mac/Linux)

### 1. Launch with One Click (Windows)
Double-click **`run_web.bat`** in the repository root.

### 2. Or Run via Terminal / PowerShell
```bash
# Install dependencies
pip install -r requirements.txt

# Start Full-Stack Server (FastAPI + Modern Web App)
python server.py
# (Or on Windows: py server.py)
```
Automatically serves the application at **`http://localhost:8000`**!

### 3. Optional: Local Open-Weight AI (Ollama)
If you want to run fully offline without internet or API keys:
```bash
ollama pull llama3.2
# Or for multilingual coding:
ollama pull qwen2.5
```

---

## ☁️ 1-Minute Cloud Deployment Guides

### Option A: GitHub Pages (Instant Free Web Hosting)
1. In your GitHub repository (`https://github.com/nmanish769/Git1`), go to **Settings** -> **Pages**.
2. Under **Build and deployment**:
   - Source: **GitHub Actions** (Pre-configured via `.github/workflows/deploy-pages.yml`).
3. Your live interactive website will be active at:  
   `https://nmanish769.github.io/Git1/`

### Option B: Render.com (Full-Stack FastAPI Web Service)
1. Go to [Render Dashboard](https://dashboard.render.com/) -> **New +** -> **Web Service**.
2. Connect your GitHub repository (`Git1`).
3. Settings:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn server:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variable (Optional, for sub-second cloud AI):
   - `GROQ_API_KEY` = `gsk_...` (Free key from [console.groq.com](https://console.groq.com/keys))
5. Click **Deploy Web Service**!

### Option C: Docker Container
```bash
docker build -t openlearn-ai .
docker run -p 8000:8000 openlearn-ai
```

---

## 📁 Repository Architecture

```
Git1/
├── index.html                # Main interactive single-page app (GitHub Pages root)
├── style.css                 # Glassmorphic dark/light UI styling
├── app.js                    # Client engine: state, Mermaid, TTS, sandbox, confetti
├── server.py                 # FastAPI backend server with REST API & static routing
├── main.py                   # Local launcher with auto-browser opening
├── app.py                    # Streamlit alternate UI
├── openlearn/
│   ├── llm.py                # Multi-cloud router (Groq, Gemini, Ollama, Demo)
│   ├── prompts.py            # Pedagogical system prompts & schemas
│   ├── languages.py          # Multilingual instructions
│   ├── levels.py             # Difficulty tiers
│   └── mock_data.py          # Built-in fail-safe lesson database
├── static/                   # Static mirror for FastAPI asset mounting
├── .github/workflows/        # Automated GitHub Pages CI/CD deployment
├── Dockerfile                # Production container specification
├── Procfile                  # Cloud process file for Render / Railway / Heroku
├── render.yaml               # 1-Click Render deployment configuration
├── requirements.txt          # Python dependencies
├── DEPLOYMENT_GUIDE.md       # Full deployment documentation
└── HACKATHON_PITCH_KIT.md    # 3-Minute pitch script, slide blueprint & Q&A
```

---

## 🏅 Hackathon Resources
- 🎤 **3-Minute Pitch Script & Judges Q&A**: See [HACKATHON_PITCH_KIT.md](HACKATHON_PITCH_KIT.md)
- 🚀 **Full Deployment Manual**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
