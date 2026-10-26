# OpenLearn AI

An open-source adaptive learning assistant. Pick a topic and level, read a short
explanation with an analogy and example, answer a practice question, and get
feedback, a revised explanation if needed, and a follow-up question.

**v0.1 scope:** beginner computer science, in English and Tamil.

## Quick start (local, open-weight model)

```bash
# 1. Install Ollama (https://ollama.com) and pull a model
ollama pull llama3.1

# 2. Install and run
pip install -r requirements.txt
streamlit run app.py
```

Pick the backend in the sidebar. Any OpenAI-compatible server (vLLM,
llama.cpp, LM Studio) also works. For Tamil, larger models give noticeably
better results; test and share which ones work well.

## Project layout

```
app.py                  Streamlit UI and learning loop
openlearn/prompts.py    Teaching prompts (easiest place to contribute)
openlearn/languages.py  Supported languages
openlearn/levels.py     Learning levels
openlearn/llm.py        Model backends
```

## The learning loop

1. Learner enters topic, level, language.
2. App generates explanation, analogy, example, question, hint.
3. Learner answers; app returns verdict, feedback, likely misconception.
4. Incorrect/partial: a revised explanation from a new angle. Correct: a harder follow-up.
5. Session progress and a "study next" suggestion are shown.

## Contributing

See CONTRIBUTING.md. Ideas: new languages, better prompts, new subjects,
accessibility (screen readers, high contrast, text-to-speech), new activities
(fill-in-the-blank, code tracing, flashcards), tests.

## License

MIT (add a LICENSE file before publishing).
