"""Teaching prompts for OpenLearn AI.

Designed to generate structured JSON with explanations, analogies,
interactive code examples, Mermaid.js visual diagrams, and adaptive feedback.
"""

from .languages import LANGUAGES
from .levels import LEVELS

SYSTEM = (
    "You are a friendly, world-class computer science educator and mentor for beginners. "
    "You explain concepts with intuitive mental models, celebrate effort, never shame mistakes, "
    "and guide learners toward deep understanding. "
    "CRITICAL REQUIREMENT: You MUST respond with ONLY a single valid, parseable JSON object. "
    "Never add markdown backticks outside the JSON or text outside the curly braces."
)


def lesson_prompt(topic: str, level: str, language: str) -> str:
    lang_instruction = LANGUAGES.get(language, LANGUAGES["English"])
    level_instruction = LEVELS.get(level, LEVELS["Beginner"])

    return f"""Teach the computer science topic: "{topic}".

Pedagogical guidance: {level_instruction}
Language Instruction: {lang_instruction}

Return a valid JSON object with EXACTLY these keys:
{{
  "explanation": "A friendly, intuitive explanation of the concept (under 120 words)",
  "analogy": "A relatable real-world physical or daily-life analogy that makes the concept instantly click",
  "example": "A clean, concise code example (Python, under 8 lines) with short comments",
  "diagram": "A valid Mermaid.js graph string (e.g. 'flowchart TD\\n    A[Start] --> B{{Condition}}\\n    B -- Yes --> C[Run Code]\\n    B -- No --> D[End]') visualizing the workflow or concept. Keep node labels simple without special characters or quotes.",
  "starter_code": "A 2-4 line Python starter snippet that the learner can run or tinker with in the code runner",
  "question": "ONE thought-provoking practice question that tests understanding (not just rote memorization)",
  "hint": "A gentle nudging hint that guides the learner without giving away the exact solution"
}}"""


def feedback_prompt(topic: str, level: str, language: str, lesson: dict, question: str, answer: str) -> str:
    lang_instruction = LANGUAGES.get(language, LANGUAGES["English"])
    level_instruction = LEVELS.get(level, LEVELS["Beginner"])

    return f"""A learner is studying "{topic}" ({level}).
Language Instruction: {lang_instruction}
Guidance: {level_instruction}

Concept taught: {lesson.get('explanation', '')}
Practice question asked: {question}
Learner's answer: {answer}

Evaluate the learner's understanding with warmth and constructive insight.
Return a valid JSON object with EXACTLY these keys:
{{
  "verdict": "correct" | "partially_correct" | "incorrect",
  "xp_earned": 50 if correct, 30 if partially_correct, 15 if incorrect,
  "feedback": "2-4 sentences of warm, encouraging, specific feedback addressing their logic directly",
  "misconception": "The exact conceptual confusion or mental gap identified, or empty string if none",
  "next_step": "follow_up" if verdict is correct else "re_explain",
  "revised_explanation": "If next_step is re_explain: provide a fresh, alternative explanation using a completely different angle or metaphor. Otherwise empty string.",
  "next_question": "An adaptive next question (slightly higher difficulty if correct, a simplified retry if incorrect)",
  "study_next": "One clear, actionable concept or sub-topic to explore next"
}}"""
