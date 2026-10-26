# 🚀 OpenLearn AI — Deployment Guide

This guide provides step-by-step instructions to deploy OpenLearn AI so hackathon judges and users can access a live URL.

---

## 🏆 Option 1: Streamlit Community Cloud (Recommended & 100% Free)

Streamlit Community Cloud is the fastest, cleanest way to host Streamlit applications with zero server maintenance.

### Step 1: Push Code to GitHub
1. Create a new GitHub repository named `openlearn-ai`.
2. Push your project files:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of OpenLearn AI"
   git branch -M main
   git remote add origin https://github.com/<your-username>/openlearn-ai.git
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **"New App"**.
3. Select your repository: `<your-username>/openlearn-ai`.
4. Set the **Main file path** to: `app.py`.
5. Click **"Advanced settings"** -> **Secrets**.
6. Paste your free Groq API key (or OpenAI/Gemini):
   ```toml
   GROQ_API_KEY = "gsk_..."
   ```
   *(Get a free Groq API key in 30 seconds at [console.groq.com](https://console.groq.com/keys) — it gives blazing-fast responses under 1 second!)*
7. Click **"Deploy!"**
8. In ~1 minute, your app will be live at `https://openlearn-ai-<hash>.streamlit.app`!

---

## 🤗 Option 2: Hugging Face Spaces (Free)

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and click **"Create new Space"**.
2. Space Name: `openlearn-ai`
3. Space SDK: Select **Streamlit**.
4. Hardware: Free (2 vCPU / 16GB RAM).
5. Clone your space repository or upload the files directly:
   - `app.py`
   - `openlearn/` directory
   - `requirements.txt`
   - `.streamlit/config.toml`
6. Go to **Settings** -> **Variables and Secrets** -> Click **"New Secret"**:
   - Key: `GROQ_API_KEY`
   - Value: `gsk_...`
7. Your app builds and runs instantly!

---

## 🐳 Option 3: Docker Deployment (Render, Fly.io, Railway, GCP)

The included `Dockerfile` is pre-configured.

### Build and Run Locally:
```bash
docker build -t openlearn-ai .
docker run -p 8501:8501 -e GROQ_API_KEY="gsk_..." openlearn-ai
```
Visit: `http://localhost:8501`

### Deploy to Render:
1. Connect your GitHub repository to [Render.com](https://render.com).
2. Choose **"Web Service"** -> Environment: **Docker**.
3. Under Environment Variables, add:
   - `GROQ_API_KEY` = `gsk_...`
   - `PORT` = `8501`
4. Click **Deploy**.

---

## 💻 Option 4: Local Setup (Offline with Ollama)

If presenting on your laptop without internet:
1. Install [Ollama](https://ollama.com).
2. Pull model:
   ```bash
   ollama pull llama3.1
   ```
3. Install dependencies and run:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
4. In the app sidebar, select backend: **Ollama (Local Open-Weight)**.
