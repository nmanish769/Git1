"""Teaching prompts for OpenLearn AI Backend.
Supports structured JSON output with Mermaid flowcharts, real-world analogies,
and adaptive misconception diagnosis.
"""

from openlearn.languages import LANGUAGES
from openlearn.levels import LEVELS

SYSTEM = (
    "You are a friendly, world-class computer science educator and mentor for beginners. "
    "You explain concepts with intuitive mental models, celebrate effort, never shame mistakes, "
    "and guide learners toward deep understanding. "
    "CRITICAL REQUIREMENT: You MUST respond with ONLY a single valid, parseable JSON object. "
    "Never add markdown backticks outside the JSON or text outside the curly braces."
)

SYSTEM_PROMPT = SYSTEM


def lesson_prompt(topic: str, level: str = "Beginner", language: str = "English") -> str:
    lang_instruction = LANGUAGES.get(language, LANGUAGES.get("English", "Respond in English."))
    level_instruction = LEVELS.get(level, LEVELS.get("Beginner", "Keep it simple."))

    return f"""Teach the computer science topic: "{topic}".

Pedagogical guidance: {level_instruction}
Language Instruction: {lang_instruction}

Return a valid JSON object with EXACTLY these keys:
{{
  "explanation": "A friendly, intuitive explanation of the concept (under 120 words)",
  "analogy": "A relatable real-world physical or daily-life analogy that makes the concept instantly click",
  "example": "A clean, concise code example (Python, under 8 lines) with short comments",
  "diagram": "A valid Mermaid.js graph string (e.g. 'flowchart TD\\n    A[Start] --> B{{Condition}}\\n    B -- Yes --> C[Run Code]\\n    B -- No --> D[End]') visualizing the workflow or concept.",
  "starter_code": "A 2-4 line Python starter snippet that the learner can run or tinker with in the code runner",
  "question": "ONE thought-provoking practice question that tests understanding (not just rote memorization)",
  "hint": "A gentle nudging hint that guides the learner without giving away the exact solution"
}}"""


def feedback_prompt(topic: str, level: str, language: str, lesson: dict, question: str, answer: str) -> str:
    lang_instruction = LANGUAGES.get(language, LANGUAGES.get("English", "Respond in English."))
    level_instruction = LEVELS.get(level, LEVELS.get("Beginner", "Keep it simple."))

    return f"""A learner is studying "{topic}" ({level}).
Language Instruction: {lang_instruction}
Guidance: {level_instruction}

Concept taught: {lesson.get('explanation', '')}
Practice question asked: {question}
Learner's answer: {answer}

Evaluate the student's answer kindly and constructively. Diagnose any misunderstanding accurately.
Return a valid JSON object with EXACTLY these keys:
{{
  "verdict": "correct", "partially_correct", or "incorrect",
  "xp_earned": 50 (if correct), 25 (if partially correct), or 15 (if incorrect),
  "feedback": "2-3 sentences of empathetic, specific feedback on their answer",
  "misconception": "The exact flawed mental model or confusion, or empty string if correct",
  "next_step": "follow_up" (if ready for next question) or "re_explain" (if fundamental confusion),
  "revised_explanation": "A new, simpler explanation using a DIFFERENT physical analogy if next_step is re_explain, otherwise empty string",
  "next_question": "ONE new adaptive practice question (slightly more challenging if correct, or simpler if incorrect)",
  "study_next": "The next logical concept to learn after mastering this"
}}"""
