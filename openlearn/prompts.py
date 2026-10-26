"""Teaching prompts for OpenLearn AI.

Designed to generate structured JSON with explanations, analogies,
interactive code examples, Mermaid.js visual diagrams, adaptive feedback,
and step-by-step doubt resolution for students.
"""

from .languages import LANGUAGES
from .levels import LEVELS

SYSTEM = (
    "You are OpenLearn AI, a warm, patient, world-class computer science educator and mentor. "
    "Your goal is to make every student understand technical concepts deeply using intuitive mental models, "
    "everyday cultural analogies, clear runnable code, and visual flowcharts. "
    "Always celebrate curiosity and effort, explain the 'why' behind concepts, and never shame confusion. "
    "CRITICAL REQUIREMENT: You MUST respond with ONLY a single valid, parseable JSON object. "
    "Do NOT include markdown backticks or any conversational text outside the JSON structure."
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


def doubt_prompt(topic: str, level: str, language: str, student_question: str, code_context: str = "") -> str:
    """Prompt for answering ANY custom student question, doubt, bug, or homework confusion."""
    lang_instruction = LANGUAGES.get(language, LANGUAGES["English"])
    level_instruction = LEVELS.get(level, LEVELS["Beginner"])

    context_str = f"\nRelevant Code / Context provided by student:\n```python\n{code_context}\n```" if code_context else ""

    return f"""A student studying "{topic}" ({level}) has asked a question/doubt:
Student's Question: "{student_question}"{context_str}

Language Instruction: {lang_instruction}
Pedagogical guidance: {level_instruction}

Answer the student's question clearly, warmly, and accurately.
Return a valid JSON object with EXACTLY these keys:
{{
  "direct_answer": "Clear, direct, and accessible explanation answering the student's doubt (100-150 words)",
  "analogy": "A memorable real-world analogy to help the concept stick",
  "code_example": "A short, clean code snippet illustrating the solution or explanation (under 8 lines)",
  "pro_tip": "One key tip, common beginner mistake to avoid, or best practice related to this question",
  "diagram": "A simple 3-4 line Mermaid flowchart if helpful, or empty string"
}}"""
