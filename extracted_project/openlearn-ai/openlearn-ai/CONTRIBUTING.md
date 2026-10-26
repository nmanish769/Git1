# Contributing to OpenLearn AI

Thanks for helping! Small, focused pull requests are easiest to review.

## Good first contributions
- **Add a language:** add an entry to `openlearn/languages.py` with a clear
  instruction. Have a native speaker review sample lessons and note them in your PR.
- **Improve a teaching prompt:** edit `openlearn/prompts.py`. Include before/after
  outputs for at least 3 topics in your PR.
- **Add subjects:** extend prompts/levels beyond computer science.
- **Accessibility:** keyboard navigation, screen-reader labels, contrast, text-to-speech.
- **New activities:** fill-in-the-blank, code tracing, flashcards.

## Setup
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Guidelines
- Learner-facing text must be kind, specific, and free of shaming.
- Prompts must keep the JSON keys the app expects (see `app.py`), or update both.
- Don't commit API keys. Keep new dependencies minimal.
- Be respectful; follow a standard Code of Conduct (e.g. Contributor Covenant).

## Pull request checklist
- [ ] App runs and a full learn → answer → feedback loop works
- [ ] Tested with at least one open-weight model
- [ ] README/docs updated if behaviour changed
