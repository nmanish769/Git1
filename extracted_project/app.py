"""OpenLearn AI - Next-Gen Autonomous Multilingual CS Tutor.
Designed for Hackathons, Live Demos, and Production Deployments.
"""

import contextlib
import io
import re
import streamlit as st
import streamlit.components.v1 as components

from openlearn import llm, prompts
from openlearn.languages import LANGUAGES
from openlearn.levels import LEVELS

# ---------- Page Configuration ----------
st.set_page_config(
    page_title="OpenLearn AI - Multilingual Adaptive Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Custom CSS Styling ----------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4F46E5, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .badge {
        display: inline-block;
        padding: 4px 10px;
        margin-right: 6px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        background-color: #1E293B;
        color: #94A3B8;
        border: 1px solid #334155;
    }
    .card-analogy {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.08), rgba(6, 182, 212, 0.08));
        border-left: 4px solid #4F46E5;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .card-misconception {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(245, 158, 11, 0.08));
        border-left: 4px solid #EF4444;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Helper Utilities ----------
def run_python_code(code_str: str) -> str:
    """Executes small Python snippets safely in a captured stdout sandbox."""
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
            exec(code_str, safe_globals, {})
        output = buffer.getvalue()
        return output if output else "(Snippet ran successfully with no output printed)"
    except Exception as e:
        return f"Execution Error ({type(e).__name__}): {e}"


def render_tts(text: str, language: str):
    """Browser-native Web Speech Synthesis for audio explanations."""
    clean_text = re.sub(r'["\'\n\r]', ' ', text).strip()
    lang_code = "ta-IN" if "tamil" in language.lower() or "தமிழ்" in language else (
        "hi-IN" if "hindi" in language.lower() or "हिन्दी" in language else "en-US"
    )
    html_code = f"""
    <div style="display: flex; align-items: center; gap: 8px; margin: 10px 0;">
        <button onclick="speakText()" style="background-color: #4F46E5; color: white; border: none; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 600;">
            🔊 Listen to Explanation
        </button>
        <button onclick="window.speechSynthesis.cancel()" style="background-color: #475569; color: white; border: none; padding: 6px 10px; border-radius: 6px; cursor: pointer; font-size: 13px;">
            ⏹️ Stop
        </button>
    </div>
    <script>
    function speakText() {{
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance("{clean_text}");
        utterance.lang = "{lang_code}";
        utterance.rate = 0.95;
        window.speechSynthesis.speak(utterance);
    }}
    </script>
    """
    components.html(html_code, height=45)


# ---------- Session State Initialization ----------
S = st.session_state
S.setdefault("lesson", None)
S.setdefault("question", "")
S.setdefault("feedback", None)
S.setdefault("history", [])
S.setdefault("round", 0)
S.setdefault("xp", 0)
S.setdefault("streak", 0)
S.setdefault("topic_used", "")
S.setdefault("level_used", "")
S.setdefault("lang_used", "")
S.setdefault("user_code", "")

# ---------- Sidebar Settings & Analytics ----------
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    backend = st.selectbox("AI Model Engine", list(llm.BACKENDS.keys()), index=0)
    driver_type, default_url, default_model, env_var = llm.BACKENDS[backend]

    base_url = st.text_input("Endpoint URL", default_url)
    model = st.text_input("Model ID", default_model)

    detected_key = llm.get_resolved_api_key(backend)
    key_placeholder = "•••••••• (Auto-detected from Secrets)" if detected_key else "Paste API Key"
    api_key = st.text_input("API Key", placeholder=key_placeholder, type="password")

    if detected_key and not api_key:
        st.success("🟢 API Key active via Secrets/Environment")
    elif backend.startswith("Fail-Safe"):
        st.info("🟡 Running in 100% Offline Demo Mode")
    elif not api_key and not detected_key and "localhost" not in base_url:
        st.warning("⚠️ Enter key or use 'Fail-Safe Demo Mode'")

    st.divider()

    # Gamification & Analytics Panel
    st.markdown("### 🏆 Learner Profile")
    rank = "Rookie Coder"
    if S.xp >= 150:
        rank = "Algorithm Master 🌟"
    elif S.xp >= 90:
        rank = "Problem Solver 🚀"
    elif S.xp >= 40:
        rank = "Junior Explorer 🔍"

    st.markdown(f"**Rank:** `{rank}`")

    col_m1, col_m2 = st.columns(2)
    col_m1.metric("Total XP", f"{S.xp} XP")
    col_m2.metric("Streak", f"{S.streak} 🔥")

    if S.history:
        correct_count = sum(1 for h in S.history if h["verdict"] == "correct")
        acc = int((correct_count / len(S.history)) * 100)
        st.progress(acc / 100, text=f"Concept Accuracy: {acc}%")

    st.divider()

    if st.button("🔄 Reset Current Session", use_container_width=True):
        for k in ("lesson", "feedback", "topic_used"):
            S[k] = None
        S.question = ""
        S.history, S.round, S.xp, S.streak = [], 0, 0, 0
        st.rerun()

    st.caption("OpenLearn AI • Open-Source Adaptive Education")


# ---------- Main Header & Topic Explorer ----------
st.markdown('<div class="main-title">🎓 OpenLearn AI</div>', unsafe_allow_html=True)
st.markdown(
    '<span class="badge">⚡ Sub-Second AI</span>'
    '<span class="badge">🌐 Tamil, Hindi & 5+ Languages</span>'
    '<span class="badge">🧠 Misconception Diagnosis</span>'
    '<span class="badge">🔓 100% Open-Source</span>',
    unsafe_allow_html=True,
)
st.write("An autonomous multilingual computer science tutor designed to make coding accessible to everyone.")

st.markdown("##### 🚀 Quick Topic Explorer (Click to load):")
chip_cols = st.columns(6)
chips = [
    ("📦 Variables", "Variables & Memory"),
    ("🔁 Loops", "Loops & Iterations"),
    ("🔀 If-Else", "Conditionals & Logic"),
    ("🎯 Functions", "Functions & Scope"),
    ("📚 Lists", "Lists & Arrays"),
    ("🔄 Recursion", "Recursion & Call Stack"),
]

selected_chip = None
for i, (label, val) in enumerate(chips):
    if chip_cols[i].button(label, use_container_width=True):
        selected_chip = val

col1, col2, col3 = st.columns([2, 1, 1])
default_topic = selected_chip if selected_chip else "Variables & Memory"
topic = col1.text_input("Concept or Topic", value=default_topic, placeholder="e.g., Loops, Variables, Binary")
level = col2.selectbox("Pedagogy Level", list(LEVELS.keys()), index=0)
language = col3.selectbox("Language (மொழி / भाषा)", list(LANGUAGES.keys()), index=0)


def call_llm(system_prompt: str, user_prompt: str):
    return llm.ask_json(backend, base_url, model, system_prompt, user_prompt, api_key=api_key)


if st.button("✨ Start Learning Session", type="primary", use_container_width=False) or selected_chip:
    with st.spinner("Generating personalized lesson, analogy & mental model..."):
        try:
            lesson_res = call_llm(prompts.SYSTEM, prompts.lesson_prompt(topic.strip(), level, language))
            S.lesson = lesson_res
            S.question = lesson_res.get("question", "")
            S.feedback, S.history, S.round = None, [], 1
            S.topic_used, S.level_used, S.lang_used = topic.strip(), level, language
            S.user_code = lesson_res.get("starter_code", lesson_res.get("example", ""))
            st.rerun()
        except llm.LLMError as e:
            st.error(f"❌ {e}")


# ---------- Interactive Lesson Presentation ----------
if S.lesson:
    L = S.lesson
    st.markdown("---")
    st.markdown(f"### 📖 Concept: **{S.topic_used}** `({S.level_used})`")

    tab_learn, tab_visual, tab_playground = st.tabs(["📚 Intuitive Concept", "📊 Visual Flowchart", "💻 Code Sandbox"])

    with tab_learn:
        st.markdown(f"#### 💡 Core Idea")
        st.write(L.get("explanation", ""))

        render_tts(L.get("explanation", ""), S.lang_used)

        st.markdown(
            f"""
            <div class="card-analogy">
                <strong>💡 Real-World Analogy:</strong><br>{L.get("analogy", "")}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### 💻 Concrete Code Example")
        st.code(L.get("example", ""), language="python")

    with tab_visual:
        st.markdown("#### 🧠 Mental Model Flowchart")
        diagram_code = L.get("diagram", "").strip()
        if diagram_code and "flowchart" in diagram_code:
            st.markdown(f"```mermaid\n{diagram_code}\n```")
        else:
            # Fallback diagram
            st.markdown(
                """```mermaid
                flowchart TD
                    A[Start Concept] --> B[Understand Core Idea]
                    B --> C[Relatable Analogy]
                    C --> D[Run Concrete Code]
                    D --> E[Mastery Verified]
                ```"""
            )

    with tab_playground:
        st.markdown("#### 🧪 Interactive Python Sandbox")
        st.caption("Experiment with the concept right in your browser. Modify the code and click 'Run'!")
        starter = L.get("starter_code", L.get("example", "# Write Python code here\nprint('Hello World')"))
        code_input = st.text_area("Python Editor", value=starter, height=140, key=f"code_sandbox_{S.round}")

        if st.button("▶️ Run Code in Sandbox"):
            output = run_python_code(code_input)
            st.markdown("**Console Output:**")
            st.code(output, language="text")

    # ---------- Adaptive Assessment & Diagnosis ----------
    st.markdown("---")
    st.markdown(f"### ❓ Practice Challenge #{S.round}")
    st.info(f"**Challenge:** {S.question}")

    if L.get("hint"):
        with st.expander("💡 Need a gentle hint?"):
            st.write(L["hint"])

    answer = st.text_area("Your Solution / Explanation", key=f"ans_input_{S.round}", height=100, placeholder="Explain in your own words or write the code snippet...")

    if st.button("🚀 Check My Answer", type="primary", disabled=not answer.strip()):
        with st.spinner("Analyzing your reasoning & diagnosing misconceptions..."):
            try:
                feedback_res = call_llm(
                    prompts.SYSTEM,
                    prompts.feedback_prompt(
                        S.topic_used, S.level_used, S.lang_used, L, S.question, answer.strip()
                    ),
                )
                S.feedback = feedback_res

                # Gamification updates
                earned_xp = feedback_res.get("xp_earned", 30)
                verdict = feedback_res.get("verdict", "incorrect")
                S.xp += earned_xp
                if verdict == "correct":
                    S.streak += 1
                    st.balloons()
                else:
                    S.streak = 0

                S.history.append({
                    "round": S.round,
                    "question": S.question,
                    "answer": answer.strip(),
                    "verdict": verdict,
                    "xp": earned_xp,
                })
                st.rerun()
            except llm.LLMError as e:
                st.error(f"❌ {e}")


# ---------- Feedback & Diagnosis Display ----------
F = S.feedback
if S.lesson and F:
    verdict = F.get("verdict", "incorrect")
    ui_map = {
        "correct": ("🎉 Outstanding! You Mastered It!", st.success),
        "partially_correct": ("🟡 Good Effort! You're on the Right Track", st.warning),
        "incorrect": ("🔁 Not Quite Yet — Let's Learn From This!", st.info),
    }
    title, banner = ui_map.get(verdict, ui_map["incorrect"])
    banner(f"### {title}\n{F.get('feedback', '')}")

    if F.get("misconception"):
        st.markdown(
            f"""
            <div class="card-misconception">
                <strong>🔍 Identified Misconception:</strong><br>{F.get("misconception")}
            </div>
            """,
            unsafe_allow_html=True,
        )

    if F.get("next_step") == "re_explain" and F.get("revised_explanation"):
        st.markdown("#### 🔄 Alternative Angle to Look at This")
        st.info(F["revised_explanation"])

    if F.get("study_next"):
        st.markdown(f"**📌 Recommended Next Topic:** `{F['study_next']}`")

    if F.get("next_question"):
        if st.button("👉 Proceed to Next Adaptive Question", type="primary"):
            S.question = F["next_question"]
            S.feedback = None
            S.round += 1
            st.rerun()


# ---------- Session Achievement Card ----------
if S.history:
    st.markdown("---")
    st.markdown("### 📈 Session Progress & Mastery Tracker")
    hist_cols = st.columns(len(S.history))
    icons = {"correct": "✅", "partially_correct": "🟡", "incorrect": "🔁"}
    for idx, item in enumerate(S.history):
        with hist_cols[idx]:
            st.metric(
                label=f"Round {item['round']}",
                value=f"{icons.get(item['verdict'], '•')}",
                delta=f"+{item['xp']} XP",
            )
