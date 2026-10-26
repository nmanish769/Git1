# 🎓 OpenLearn AI — Autonomous Multilingual CS Tutor

[![Live Website](https://img.shields.io/badge/Live_Website-GitHub_Pages-blue?style=for-the-badge&logo=github)](https://nmanish769.github.io/Git1/)
[![Deploy to Render](https://img.shields.io/badge/Deploy%20to-Render-46E3B7?style=for-the-badge&logo=render)](https://render.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Model Support](https://img.shields.io/badge/AI_Engines-Gemini_|_Groq_|_OpenRouter_|_OpenAI_|_DeepSeek_|_Ollama-orange.svg)]()

> **Interactive, multilingual computer science tutor powered by linked AI models.**  
> Demystifying programming concepts in your native tongue (English, Tamil, Hindi, Telugu, Kannada, Spanish, French) through real-world cultural analogies, dynamic visual flowcharts, live code sandboxes, adaptive misconception diagnosis, and student doubt resolution.

---

## 🌐 Try the Live Interactive Website

👉 **[https://nmanish769.github.io/Git1/](https://nmanish769.github.io/Git1/)**

Anyone can open and interact with the live website directly in their browser:
- 🌟 **Multi-Model AI Linking**: Connect directly to **Google Gemini (Free)**, **Groq Cloud (Sub-second speed)**, **OpenRouter (DeepSeek R1 / Free models)**, **OpenAI (GPT-4o)**, **DeepSeek (V3/R1)**, or **Local Ollama**!
- 💬 **Ask AI Tutor (Doubt Solver)**: Ask ANY question or paste errors and get clear step-by-step explanations, analogies, demo code, and pro tips!
- ⚡ **1-Click Topic Chips**: Jump into *Variables, Loops, If-Else, Functions, Lists, Dictionaries, Recursion, OOP, Binary Search, Big-O, Stacks & Queues, APIs*.
- 📊 **Dynamic Mermaid.js Flowcharts**: Visual mental models generated on the fly.
- 🔊 **Voice Read-Aloud**: Browser-native Text-to-Speech in regional languages.
- 💻 **Live Code Sandbox**: Run and test Python snippets in-browser.
- 🎯 **Misconception Diagnosis**: Intelligent AI evaluation explaining *why* an answer is flawed and diagnosing mental gaps.
- 🎮 **Gamification HUD**: Streaks, XP rewards, rank promotions, and confetti celebrations.
- 💡 **Smart Offline Mode**: Includes 25+ comprehensive core CS topics with intelligent heuristic question evaluation so the site works even completely offline!

---

## 🚀 Quick Start (Run Locally on Windows/Mac/Linux)

### 1. Launch with One Click (Windows)
Double-click **`run_web.bat`** in the repository root.

### 2. Or Run via Terminal / PowerShell
```bash
# Install dependencies
pip install -r requirements.txt

# Start Full-Stack Server (FastAPI + Modern Web App)
py server.py
# (Or: python server.py)
```
Automatically serves the application at **`http://localhost:8000`**!

### 3. Optional: Local Open-Weight AI (Ollama)
If you want to run fully offline on your machine without internet:
```bash
ollama pull llama3.2
# Or for multilingual coding:
ollama pull qwen2.5
```

---

## ⚙️ Supported AI Models & How to Connect

Click **"⚙️ AI Models & Keys"** in the top navigation bar to configure your preferred AI model:

| AI Provider | Recommended Models | Key Required? | Where to get Free Key |
|---|---|---|---|
| **Google Gemini** | `gemini-2.5-flash`, `gemini-1.5-flash` | Free Key | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| **Groq Cloud** | `llama-3.3-70b-versatile`, `llama-3.1-8b-instant` | Free Key | [Groq Console](https://console.groq.com/keys) |
| **OpenRouter** | `google/gemini-2.0-flash-exp:free`, `deepseek/deepseek-r1:free` | Free / Paid | [OpenRouter Keys](https://openrouter.ai/keys) |
| **OpenAI** | `gpt-4o-mini`, `gpt-4o` | Standard Key | [OpenAI Platform](https://platform.openai.com/api-keys) |
| **DeepSeek** | `deepseek-chat`, `deepseek-reasoner` | Standard Key | [DeepSeek Platform](https://platform.deepseek.com/) |
| **Local Ollama** | `llama3.2`, `qwen2.5`, `mistral` | No Key Needed | Runs locally on `http://localhost:11434` |
| **Smart Offline Mode** | 25+ Built-in CS Concepts | No Key Needed | Works 100% offline anywhere |

---

## ☁️ Cloud Deployment Guides

### Option A: GitHub Pages (Instant Free Web Hosting)
1. Push your latest code using `push_to_github.bat` or git commands.
2. Go to your GitHub repository -> **Settings** -> **Pages**.
3. Set Source to `Deploy from a branch` -> `main` / `root`.
4. Your website is live at `https://<username>.github.io/<repo>/`!

### Option B: Render.com (Full-Stack FastAPI Web Service)
1. Connect your repository on [Render.com](https://dashboard.render.com/) -> **New Web Service**.
2. Environment: `Python 3`
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables:
   - `GEMINI_API_KEY` = `AIzaSy...` (or `GROQ_API_KEY` = `gsk_...`)

---

## 📁 Repository Structure

```
Git1/
├── index.html                # Main SPA frontend (GitHub Pages root)
├── style.css                 # Glassmorphic responsive dark-mode styling
├── script.js                 # Multi-model AI client engine & state manager
├── app.js                    # Redundant mirror of script.js for legacy runners
├── server.py                 # FastAPI backend server with REST API
├── main.py                   # Local launcher with auto-browser opening
├── app.py                    # Streamlit alternate UI
├── push_to_github.bat        # 1-Click push script to update GitHub & GitHub Pages
├── run_web.bat               # 1-Click local full-stack server launcher
├── openlearn/
│   ├── llm.py                # Multi-model LLM router (Gemini, Groq, OpenRouter, OpenAI, DeepSeek, Ollama)
│   ├── prompts.py            # Pedagogical system prompts & doubt schemas
│   ├── languages.py          # Multilingual instructions
│   ├── levels.py             # Difficulty tiers
│   └── mock_data.py          # Built-in 25+ topic offline knowledge base
├── frontend/                 # Synced frontend mirror
├── static/                   # Synced static mirror for FastAPI
└── backend/                  # Synced backend mirror
```
