# 🎓 OpenLearn AI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Model Support](https://img.shields.io/badge/Models-Groq%20%7C%20Ollama%20%7C%20Gemini%20%7C%20OpenAI-orange.svg)]()

> **Autonomous, multilingual computer science tutor bridging the educational divide.**  
> Learn foundational concepts in your mother tongue (English, Tamil, Hindi, Telugu, Kannada, Spanish, French) through real-world analogies, dynamic visual flowcharts, interactive code playgrounds, and adaptive misconception diagnosis.

---

## 🌟 Key Features

- **🌐 Multilingual Pedagogy**: Learn in English, தமிழ் (Tamil), हिन्दी (Hindi), తెలుగు (Telugu), ಕನ್ನಡ (Kannada), Español, or Français.
- **⚡ Sub-Second Inference**: Powered by Groq Cloud (Llama 3.3 70B) for instant feedback during live demos.
- **📊 Dynamic Visual Diagrams**: Auto-generates Mermaid.js flowcharts to build clear mental models for visual learners.
- **💻 Built-in Python Sandbox**: Safely write, test, and run code directly in the browser.
- **🔊 Audio Read-Aloud**: Browser-native text-to-speech for auditory learners and regional language accessibility.
- **🧠 Misconception Diagnosis**: Identifies *why* a student answered incorrectly and pivots to an alternative explanation.
- **🎮 Gamified Mastery**: Streak tracking, XP rewards, and adaptive difficulty scaling.
- **🛡️ 100% Fail-Safe Demo Mode**: Built-in offline demo fallback ensures presentations never crash during network drops.

---

## 🚀 Quick Start (Local)

### 1. Clone & Install
```bash
git clone https://github.com/<your-username>/openlearn-ai.git
cd openlearn-ai
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## ☁️ 1-Minute Cloud Deployment

### Option A: Streamlit Community Cloud (Recommended & Free)
1. Fork or push this repository to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io/).
3. Click **New App** -> select repository -> file: `app.py`.
4. In **Advanced Settings -> Secrets**, add:
   ```toml
   GROQ_API_KEY = "gsk_..."
   ```
5. Click **Deploy**!

### Option B: Docker
```bash
docker build -t openlearn-ai .
docker run -p 8501:8501 -e GROQ_API_KEY="gsk_..." openlearn-ai
```

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for full instructions on Hugging Face Spaces, Render, and Ollama offline mode.

---

## 📁 Repository Structure

```
openlearn-ai/
├── .streamlit/
│   ├── config.toml           # UI styling & dark theme
│   └── secrets.toml.example  # Secrets template
├── openlearn/
│   ├── __init__.py
│   ├── languages.py          # Multilingual instructions & prompts
│   ├── levels.py             # Pedagogical difficulty levels
│   ├── llm.py                # Multi-cloud backends (Groq, Gemini, OpenAI, Ollama)
│   ├── prompts.py            # Teaching prompts & Mermaid diagram schemas
│   └── mock_data.py          # Offline presentation fallback data
├── app.py                    # Streamlit application
├── Dockerfile                # Docker container configuration
├── requirements.txt          # Minimal Python dependencies
├── DEPLOYMENT_GUIDE.md       # Comprehensive cloud & local deployment manual
├── HACKATHON_PITCH_KIT.md    # 3-minute pitch script, slide deck outline & Q&A
└── README.md
```

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.
