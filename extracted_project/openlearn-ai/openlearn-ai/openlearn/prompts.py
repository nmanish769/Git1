"""Teaching prompts. Improving these is one of the easiest ways to contribute."""

from .languages import LANGUAGES
from .levels import LEVELS

SYSTEM = (
    "You are a patient, encouraging computer science tutor for beginners. "
    "You teach one small idea at a time, never shame mistakes, and always "
    "respond with ONLY a single valid JSON object and nothing else."
)


def lesson_prompt(topic: str, level: str, language: str) -> str:
    return f"""Teach the beginner computer science topic: "{topic}".

Level guidance: {LEVELS[level]}
Language: {LANGUAGES[language]}

Return JSON with exactly these keys:
{{
  "explanation": "a short, simple explanation (max 120 words)",
  "analogy": "one relatable real-world analogy",
  "example": "one small concrete example (code allowed, keep it under 8 lines)",
  "question": "ONE practice question that checks understanding, answerable in 1-3 sentences or a few lines of code",
  "hint": "a gentle hint for the question that does not reveal the answer"
}}"""


def feedback_prompt(topic, level, language, lesson, question, answer) -> str:
    return f"""A learner is studying "{topic}" ({level}).
Language: {LANGUAGES[language]}

Explanation given: {lesson.get('explanation', '')}
Practice question: {question}
Learner's answer: {answer}

Judge the answer kindly but honestly. Return JSON with exactly these keys:
{{
  "verdict": "correct" | "partially_correct" | "incorrect",
  "feedback": "2-4 sentences of specific, encouraging feedback",
  "misconception": "the likely misunderstanding, or an empty string if none",
  "next_step": "follow_up" if verdict is correct, otherwise "re_explain",
  "revised_explanation": "if next_step is re_explain: a NEW explanation using a different angle or analogy; otherwise empty",
  "next_question": "a follow-up question (slightly harder if correct, a simpler retry if not)",
  "study_next": "one short suggestion of what to learn or practise next"
}}"""
