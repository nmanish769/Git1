"""Offline demo mock data for fail-safe hackathon demonstrations.

Ensures the app always works even during network drops, API rate limits,
or when testing without API keys.
"""

MOCK_LESSONS = {
    "variables": {
        "English": {
            "explanation": "A variable is like a labeled storage box inside your computer's memory. You give it a name, put a piece of data inside it (like a number or word), and whenever you use that name, the computer looks inside the box to find the stored value.",
            "analogy": "Imagine a kitchen jar with a sticker that says 'Sugar'. Whenever a recipe calls for 'Sugar', you look in the jar. You can also replace the sugar with honey later — the label stays, but the content changes!",
            "example": "# Storing user information in variables\nplayer_name = 'Alex'\nscore = 100\nscore = score + 10  # Updating the value\nprint(f'{player_name} has {score} points!')",
            "diagram": "flowchart TD\n    A[Memory Address 0x10A] --> B[Box Label: player_name]\n    B --> C[Stored Value: Alex]\n    D[Memory Address 0x10B] --> E[Box Label: score]\n    E --> F[Stored Value: 110]",
            "starter_code": "player_name = 'Alex'\nscore = 100\nprint(f'Player {player_name} score is: {score}')",
            "question": "If you write `apples = 5` and then on the next line write `apples = 8`, what will be inside the `apples` variable when you print it?",
            "hint": "Think about our kitchen jar analogy: when you replace the contents of the jar, what happens to the previous item?",
        },
        "Tamil": {
            "explanation": "மாறி (Variable) என்பது கணினி நினைவகத்தில் (Memory) தகவல்களை சேமித்து வைக்கும் ஒரு பெயரிடப்பட்ட பெட்டி போன்றது. நாம் கொடுக்கும் பெயரைப் பயன்படுத்தி, எப்போது வேண்டுமானாலும் அதில் சேமித்துள்ள மதிப்பை அணுகலாம் அல்லது மாற்றலாம்.",
            "analogy": "சமையலறையில் 'அஞ்சறைப் பெட்டி' அல்லது பெயரிடப்பட்ட சர்க்கரை டப்பாவை நினைத்துப் பாருங்கள். டப்பாவின் பெயர் 'சர்க்கரை', உள்ளே இருப்பது மதிப்பு. தேவைப்பட்டால் உள்ளே உள்ளதை மாற்றி வெல்லம் கூட வைக்கலாம்!",
            "example": "# மாறிகளை உருவாக்குதல்\npeyar = 'அமுதன்'\nmathippu = 50\nmathippu = mathippu + 10\nprint(f'{peyar} மதிப்பெண்: {mathippu}')",
            "diagram": "flowchart TD\n    A[நினைவகம்] --> B[மாறி பெயர்: peyar]\n    B --> C[சேமித்த மதிப்பு: அமுதன்]\n    A --> D[மாறி பெயர்: mathippu]\n    D --> E[சேமித்த மதிப்பு: 60]",
            "starter_code": "peyar = 'அமுதன்'\nmathippu = 100\nprint(f'{peyar} பெற்ற மதிப்பெண்: {mathippu}')",
            "question": "முதலில் `panam = 100` என்று கொடுத்து, அடுத்த வரியில் `panam = 250` என்று மாற்றினால், இப்போது `panam` என்ற மாறியில் என்ன மதிப்பு இருக்கும்?",
            "hint": "டப்பாவில் இருந்த பழைய பொருளை எடுத்துவிட்டு புதிய பொருளை வைத்தால் என்ன இருக்கும் என்று சிந்தியுங்கள்.",
        },
    },
    "loops": {
        "English": {
            "explanation": "A loop lets your computer repeat a block of instructions multiple times automatically until a specific condition is met, saving you from writing repetitive code.",
            "analogy": "Like a musician repeating the chorus of a song 3 times, or a runner doing 5 laps around a race track until they reach the finish line.",
            "example": "# Counting from 1 to 5 using a for loop\nfor lap in range(1, 6):\n    print(f'Running lap number: {lap}')\nprint('Race finished!')",
            "diagram": "flowchart TD\n    A[Start Lap = 1] --> B{Is Lap <= 5?}\n    B -- Yes --> C[Run Lap & Print]\n    C --> D[Lap = Lap + 1]\n    D --> B\n    B -- No --> E[End: Race Finished]",
            "starter_code": "for count in range(1, 4):\n    print(f'Repeat #{count}')",
            "question": "What would happen if a loop's condition never becomes False?",
            "hint": "Think of a runner on a track who is told to 'run until you see a flying pig'. Will they ever stop?",
        },
        "Tamil": {
            "explanation": "மடக்கு (Loop) என்பது ஒரு குறிப்பிட்ட நிபந்தனை முடியும் வரை, ஒரே கட்டளையை மீண்டும் மீண்டும் தானாகவே செய்ய கணினிக்கு உதவும் அமைப்பாகும்.",
            "analogy": "விளையாட்டு மைதானத்தில் 5 சுற்றுகள் ஓட வேண்டும் என்று உடற்பயிற்சி ஆசிரியர் கூறுவது போல. 5 சுற்றுகள் முடியும் வரை நீங்கள் மீண்டும் மீண்டும் ஓடிக்கொண்டே இருப்பீர்கள்.",
            "example": "# 1 முதல் 3 வரை எண்ணும் மடக்கு\nfor sutru in range(1, 4):\n    print(f'சுற்று எண்: {sutru}')\nprint('பயிற்சி முடிந்தது!')",
            "diagram": "flowchart TD\n    A[தொடக்கம்: சுற்று = 1] --> B{சுற்று <= 3?}\n    B -- ஆம் --> C[சுற்றை அச்சிடு]\n    C --> D[சுற்று = சுற்று + 1]\n    D --> B\n    B -- இல்லை --> E[முடிவு]",
            "starter_code": "for i in range(1, 4):\n    print(f'வணக்கம் {i}')",
            "question": "ஒரு மடக்கின் நிபந்தனை எப்போதுமே தவறாக (False) மாறாமல் போனால் என்ன நிகழும்?",
            "hint": "நிறுத்துவதற்கான கட்டளையே இல்லாத ஒரு சுழற்சியை யோசித்துப் பாருங்கள்.",
        },
    },
}

MOCK_FEEDBACKS = {
    "correct": {
        "verdict": "correct",
        "xp_earned": 50,
        "feedback": "Spot on! You nailed the core mental model. In programming, assigning a new value overwrites the previous value in that memory location.",
        "misconception": "",
        "next_step": "follow_up",
        "revised_explanation": "",
        "next_question": "Awesome! Now: What happens if you try to use a variable before creating it?",
        "study_next": "Variable Data Types (Strings vs Integers vs Booleans)",
    },
    "partially_correct": {
        "verdict": "partially_correct",
        "xp_earned": 30,
        "feedback": "You're very close! You understand the change happens, but remember that the old value is completely replaced, not added or saved alongside.",
        "misconception": "Thinking variables append or hold a history of past values automatically.",
        "next_step": "follow_up",
        "revised_explanation": "Think of a chalkboard: before writing the new number 8, the old number 5 is completely erased. There is only ever one current value at a time.",
        "next_question": "If you have `x = 10` and then write `x = x + 5`, what will `x` be?",
        "study_next": "Reassigning and updating variables",
    },
    "incorrect": {
        "verdict": "incorrect",
        "xp_earned": 15,
        "feedback": "Good try! Mistakes are how our brains build stronger neural connections. Let's look at this from a fresh angle.",
        "misconception": "Confusing mathematical equality with programming assignment.",
        "next_step": "re_explain",
        "revised_explanation": "In math, `=` means both sides are equal. In programming, `=` is an action: 'take what is on the right, and store it into the container on the left'. The new delivery replaces whatever was inside before.",
        "next_question": "Let's try a quick check: If `score = 20`, and then we do `score = 0`, what is the final score?",
        "study_next": "Understanding the Assignment Operator (=)",
    },
}


def get_mock_lesson(topic: str, language: str) -> dict:
    t_lower = topic.lower()
    lang_key = "Tamil" if "tamil" in language.lower() or "தமிழ்" in language else "English"

    if "loop" in t_lower or "மடக்கு" in t_lower or "iteration" in t_lower:
        return MOCK_LESSONS["loops"][lang_key]
    # Default to variables or adapted variable
    return MOCK_LESSONS["variables"][lang_key]


def get_mock_feedback(answer: str) -> dict:
    ans = answer.strip().lower()
    # Simple heuristic for mock answers
    if any(k in ans for k in ["8", "250", "infinite", "never stop", "முடிவில்லாமல்", "மாறும்", "overwritten", "overwrite"]):
        return MOCK_FEEDBACKS["correct"]
    elif len(ans) > 5 and any(k in ans for k in ["both", "5 and 8", "5", "100", "error"]):
        return MOCK_FEEDBACKS["partially_correct"]
    return MOCK_FEEDBACKS["incorrect"]
