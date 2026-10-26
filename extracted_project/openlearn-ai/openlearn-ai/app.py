"""OpenLearn AI - Streamlit prototype.  Run: streamlit run app.py"""

import streamlit as st

from openlearn import llm, prompts
from openlearn.languages import LANGUAGES
from openlearn.levels import LEVELS

st.set_page_config(page_title="OpenLearn AI", page_icon="🎓", layout="centered")

VERDICT_UI = {
    "correct": ("✅ Correct", st.success),
    "partially_correct": ("🟡 Partly there", st.warning),
    "incorrect": ("🔁 Not quite yet", st.info),
}

# ---------- state ----------
S = st.session_state
S.setdefault("lesson", None)
S.setdefault("question", "")
S.setdefault("feedback", None)
S.setdefault("history", [])
S.setdefault("round", 0)

# ---------- sidebar: settings ----------
with st.sidebar:
    st.header("⚙️ Model")
    backend = st.selectbox("Backend", list(llm.BACKENDS))
    _, default_url, default_model = llm.BACKENDS[backend]
    base_url = st.text_input("Base URL", default_url)
    model = st.text_input("Model", default_model)
    api_key = st.text_input("API key (if needed)", type="password")
    st.caption("Open-source: github.com/your-org/openlearn-ai")
    if S.history and st.button("Clear session"):
        for k in ("lesson", "question", "feedback"):
            S[k] = None if k != "question" else ""
        S.history, S.round = [], 0
        st.rerun()


def call(system, user):
    return llm.ask_json(backend, base_url, model, system, user, api_key)


# ---------- header + inputs ----------
st.title("🎓 OpenLearn AI")
st.write("Learn a concept, try a question, get feedback, and know what to do next.")

col1, col2, col3 = st.columns([2, 1, 1])
topic = col1.text_input("Topic", placeholder="e.g. variables, loops, binary numbers")
level = col2.selectbox("Level", list(LEVELS))
language = col3.selectbox("Language", list(LANGUAGES))

if st.button("Start learning", type="primary", disabled=not topic.strip()):
    with st.spinner("Preparing your lesson..."):
        try:
            S.lesson = call(prompts.SYSTEM, prompts.lesson_prompt(topic.strip(), level, language))
            S.question = S.lesson.get("question", "")
            S.feedback, S.history, S.round = None, [], 1
            S.topic_used, S.level_used, S.lang_used = topic.strip(), level, language
        except llm.LLMError as e:
            st.error(str(e))

# ---------- lesson ----------
if S.lesson:
    L = S.lesson
    st.subheader(f"📖 {S.topic_used}")
    st.write(L.get("explanation", ""))
    st.info(f"**Analogy:** {L.get('analogy', '')}")
    st.markdown("**Example**")
    st.markdown(L.get("example", ""))

    st.divider()
    st.subheader(f"❓ Practice question {S.round}")
    st.write(S.question)
    if L.get("hint"):
        with st.expander("Need a hint?"):
            st.write(L["hint"])

    answer = st.text_area("Your answer", key=f"answer_{S.round}", height=120)
    if st.button("Check my answer", disabled=not answer.strip()):
        with st.spinner("Reading your answer..."):
            try:
                S.feedback = call(
                    prompts.SYSTEM,
                    prompts.feedback_prompt(
                        S.topic_used, S.level_used, S.lang_used, L, S.question, answer.strip()
                    ),
                )
                S.history.append(
                    {"round": S.round, "question": S.question, "answer": answer.strip(),
                     "verdict": S.feedback.get("verdict", "incorrect")}
                )
            except llm.LLMError as e:
                st.error(str(e))

# ---------- feedback ----------
F = S.feedback
if S.lesson and F:
    label, box = VERDICT_UI.get(F.get("verdict"), VERDICT_UI["incorrect"])
    box(f"**{label}** — {F.get('feedback', '')}")
    if F.get("misconception"):
        st.markdown(f"**Possible misunderstanding:** {F['misconception']}")
    if F.get("next_step") == "re_explain" and F.get("revised_explanation"):
        st.markdown("**Let's look at it another way**")
        st.write(F["revised_explanation"])
    if F.get("study_next"):
        st.caption(f"📌 Next: {F['study_next']}")

    if F.get("next_question") and st.button("Next question →"):
        S.question = F["next_question"]
        S.feedback = None
        S.round += 1
        st.rerun()

# ---------- progress ----------
if S.history:
    st.divider()
    st.subheader("📈 Your progress")
    icons = {"correct": "✅", "partially_correct": "🟡", "incorrect": "🔁"}
    st.write("  ".join(f"Q{h['round']} {icons.get(h['verdict'], '•')}" for h in S.history))
