"""Supported learning languages.

To add a language: add an entry below, then open a PR.
`instruction` is appended to every prompt so the model writes in that language.
"""

LANGUAGES = {
    "English": "Write all learner-facing text in simple, clear English.",
    "தமிழ் (Tamil)": (
        "Write all learner-facing text in simple, natural Tamil (தமிழ்). "
        "Keep widely used technical terms (e.g. 'variable', 'loop', 'function') "
        "in English in brackets on first use, and explain them in Tamil."
    ),
}
