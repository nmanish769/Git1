"""Supported learning languages.

To add a language: add an entry below.
`instruction` is appended to every prompt so the model writes in that language.
"""

LANGUAGES = {
    "English": "Write all learner-facing text in simple, clear, engaging English.",
    "தமிழ் (Tamil)": (
        "Write all learner-facing text in simple, natural Tamil (தமிழ்). "
        "Keep widely used technical terms (e.g. 'variable', 'loop', 'function') "
        "in English in brackets on first use, and explain them in Tamil."
    ),
    "हिन्दी (Hindi)": (
        "Write all learner-facing text in simple, conversational Hindi (हिंदी). "
        "Keep key technical terms (e.g. 'variable', 'function', 'condition') "
        "in English in brackets and explain their meaning clearly in Hindi."
    ),
    "తెలుగు (Telugu)": (
        "Write all learner-facing text in natural, clear Telugu (తెలుగు). "
        "Keep technical terms in English in brackets alongside Telugu explanations."
    ),
    "ಕನ್ನಡ (Kannada)": (
        "Write all learner-facing text in natural, accessible Kannada (ಕನ್ನಡ). "
        "Include technical terms in English in brackets alongside Kannada explanations."
    ),
    "Español (Spanish)": (
        "Write all learner-facing text in clear, accessible Spanish (Español). "
        "Use universal programming terms."
    ),
    "Français (French)": (
        "Write all learner-facing text in clear, accessible French (Français). "
        "Use standard programming terminology."
    ),
}
