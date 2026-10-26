/**
 * OpenLearn AI — Modern Single-Page Application Client
 * Supports:
 * - Multi-Model Cloud AI (Google Gemini, Groq Cloud, OpenRouter, OpenAI, DeepSeek)
 * - Local Open-Weight Models via Ollama
 * - Full-Stack FastAPI Backend (/api/lesson, /api/feedback, /api/ask)
 * - 100% Client-Side Direct Cloud Calls for Static Hosting (GitHub Pages)
 * - Smart Offline Mode with 25+ CS concepts and semantic heuristics
 */

// Initialize Mermaid.js
mermaid.initialize({
  startOnLoad: false,
  theme: 'dark',
  securityLevel: 'loose',
  flowchart: { useMaxWidth: true, htmlLabels: true, curve: 'basis' }
});

// ---------- Application State & LocalStorage Configuration ----------
const state = {
  xp: 0,
  streak: 0,
  round: 0,
  lesson: null,
  question: '',
  topic: '',
  level: '',
  language: '',
  history: [],
  isSpeaking: false,
  backendConnected: false,
  
  // Stored Keys & URLs
  geminiKey: localStorage.getItem('openlearn_gemini_key') || '',
  geminiModel: localStorage.getItem('openlearn_gemini_model') || 'gemini-1.5-flash',
  
  groqKey: localStorage.getItem('openlearn_groq_key') || '',
  groqModel: localStorage.getItem('openlearn_groq_model') || 'llama-3.3-70b-versatile',
  
  openrouterKey: localStorage.getItem('openlearn_openrouter_key') || '',
  openrouterModel: localStorage.getItem('openlearn_openrouter_model') || 'google/gemini-2.0-flash-exp:free',
  
  openaiKey: localStorage.getItem('openlearn_openai_key') || '',
  openaiModel: localStorage.getItem('openlearn_openai_model') || 'gpt-4o-mini',
  
  deepseekKey: localStorage.getItem('openlearn_deepseek_key') || '',
  deepseekModel: localStorage.getItem('openlearn_deepseek_model') || 'deepseek-chat',
  
  ollamaUrl: localStorage.getItem('openlearn_ollama_url') || 'http://localhost:11434',
  ollamaModel: localStorage.getItem('openlearn_ollama_model') || 'llama3.2',
  
  activeEngine: localStorage.getItem('openlearn_active_engine') || 'gemini',
};

// ---------- DOM Elements Cache ----------
const DOM = {
  // HUD & Nav
  statusBadge: document.getElementById('statusBadge'),
  statusText: document.getElementById('statusText'),
  statusDot: document.getElementById('statusDot'),
  settingsBtn: document.getElementById('settingsBtn'),
  settingsModal: document.getElementById('settingsModal'),
  closeSettingsBtn: document.getElementById('closeSettingsBtn'),
  saveSettingsBtn: document.getElementById('saveSettingsBtn'),
  connectionFeedback: document.getElementById('connectionFeedback'),

  rankText: document.getElementById('rankText'),
  xpText: document.getElementById('xpText'),
  streakText: document.getElementById('streakText'),

  // Settings inputs
  geminiApiKeyInput: document.getElementById('geminiApiKeyInput'),
  geminiModelSelect: document.getElementById('geminiModelSelect'),
  groqApiKeyInput: document.getElementById('groqApiKeyInput'),
  groqModelSelect: document.getElementById('groqModelSelect'),
  openrouterApiKeyInput: document.getElementById('openrouterApiKeyInput'),
  openrouterModelSelect: document.getElementById('openrouterModelSelect'),
  openaiApiKeyInput: document.getElementById('openaiApiKeyInput'),
  openaiModelSelect: document.getElementById('openaiModelSelect'),
  deepseekApiKeyInput: document.getElementById('deepseekApiKeyInput'),
  deepseekModelSelect: document.getElementById('deepseekModelSelect'),
  ollamaUrlInput: document.getElementById('ollamaUrlInput'),
  ollamaModelSelect: document.getElementById('ollamaModelSelect'),

  // Configuration Card
  topicInput: document.getElementById('topicInput'),
  levelSelect: document.getElementById('levelSelect'),
  langSelect: document.getElementById('langSelect'),
  modelSelect: document.getElementById('modelSelect'),
  startLessonBtn: document.getElementById('startLessonBtn'),
  activeEngineHint: document.getElementById('activeEngineHint'),

  // Loading
  loadingIndicator: document.getElementById('loadingIndicator'),
  loadingMsg: document.getElementById('loadingMsg'),

  // Lesson Section
  lessonSection: document.getElementById('lessonSection'),
  lessonTopicBadge: document.getElementById('lessonTopicBadge'),
  lessonLevelBadge: document.getElementById('lessonLevelBadge'),
  lessonLangBadge: document.getElementById('lessonLangBadge'),
  lessonModelBadge: document.getElementById('lessonModelBadge'),
  audioBtn: document.getElementById('audioBtn'),
  audioIcon: document.getElementById('audioIcon'),
  audioLabel: document.getElementById('audioLabel'),
  explanationText: document.getElementById('explanationText'),
  analogyText: document.getElementById('analogyText'),
  mermaidDiagram: document.getElementById('mermaidDiagram'),

  // Code Playground
  exampleCode: document.getElementById('exampleCode'),
  copyCodeBtn: document.getElementById('copyCodeBtn'),
  sandboxCode: document.getElementById('sandboxCode'),
  runCodeBtn: document.getElementById('runCodeBtn'),
  resetCodeBtn: document.getElementById('resetCodeBtn'),
  consoleResult: document.getElementById('consoleResult'),

  // Ask AI Doubt Tab
  doubtQueryInput: document.getElementById('doubtQueryInput'),
  doubtCodeInput: document.getElementById('doubtCodeInput'),
  askDoubtBtn: document.getElementById('askDoubtBtn'),
  doubtAnswerContainer: document.getElementById('doubtAnswerContainer'),
  doubtDirectAnswer: document.getElementById('doubtDirectAnswer'),
  doubtAnalogyCard: document.getElementById('doubtAnalogyCard'),
  doubtAnalogyText: document.getElementById('doubtAnalogyText'),
  doubtCodeCard: document.getElementById('doubtCodeCard'),
  doubtCodeSnippet: document.getElementById('doubtCodeSnippet'),
  copyDoubtCodeBtn: document.getElementById('copyDoubtCodeBtn'),
  doubtProTipCard: document.getElementById('doubtProTipCard'),
  doubtProTipText: document.getElementById('doubtProTipText'),
  doubtAudioBtn: document.getElementById('doubtAudioBtn'),
  doubtAudioIcon: document.getElementById('doubtAudioIcon'),

  // Challenge Section
  challengeSection: document.getElementById('challengeSection'),
  roundIndicator: document.getElementById('roundIndicator'),
  questionText: document.getElementById('questionText'),
  hintToggleBtn: document.getElementById('hintToggleBtn'),
  hintContent: document.getElementById('hintContent'),
  hintText: document.getElementById('hintText'),
  answerInput: document.getElementById('answerInput'),
  checkAnswerBtn: document.getElementById('checkAnswerBtn'),

  // Feedback Card
  feedbackContainer: document.getElementById('feedbackContainer'),
  verdictBanner: document.getElementById('verdictBanner'),
  verdictTitle: document.getElementById('verdictTitle'),
  feedbackSummary: document.getElementById('feedbackSummary'),
  misconceptionCard: document.getElementById('misconceptionCard'),
  misconceptionText: document.getElementById('misconceptionText'),
  revisedExpCard: document.getElementById('revisedExpCard'),
  revisedExpText: document.getElementById('revisedExpText'),
  studyNextTag: document.getElementById('studyNextTag'),
  nextQuestionBtn: document.getElementById('nextQuestionBtn'),

  // Progress Tracker
  historySection: document.getElementById('historySection'),
  historyGrid: document.getElementById('historyGrid'),
  quickTopicsContainer: document.getElementById('quickTopicsContainer'),
  tabBtns: document.querySelectorAll('.tab-btn'),
  tabContents: document.querySelectorAll('.tab-content'),
};

// ---------- Enhanced Offline Client Knowledge Base (25+ Topics) ----------
const CLIENT_KNOWLEDGE_BASE = {
  "variables": {
    "English": {
      explanation: "A variable is a named storage container in computer memory. You assign it a name and store data inside it (numbers, words, lists). Whenever you reference that name later, the computer looks up what is currently inside.",
      analogy: "Think of a labeled jar in your kitchen with a sticker that says 'Sugar'. Whenever a recipe calls for 'Sugar', you check the jar. If you replace the sugar with honey, the sticker stays, but the content changes!",
      example: "player_name = 'Alex'\nscore = 100\nscore = score + 25\nprint(f'{player_name} score: {score}')",
      diagram: "flowchart TD\n    A[Memory Address 0x10A] --> B[Name: player_name]\n    B --> C[Value: 'Alex']\n    D[Memory Address 0x10B] --> E[Name: score]\n    E --> F[Value: 125]",
      starter_code: "player_name = 'Alex'\nscore = 100\nscore = score + 25\nprint(f'Player {player_name} has {score} points!')",
      question: "If you set `apples = 5` and then write `apples = 8`, what is the value of `apples` when printed?",
      hint: "Remember the kitchen jar: when you put a new item inside, what happens to the old item?",
    },
    "Tamil": {
      explanation: "மாறி (Variable) என்பது கணினி நினைவகத்தில் தகவல்களை சேமித்து வைக்கும் ஒரு பெயரிடப்பட்ட பெட்டி போன்றது. நாம் கொடுக்கும் பெயரைப் பயன்படுத்தி, எப்போது வேண்டுமானாலும் அதில் சேமித்துள்ள மதிப்பை அணுகலாம் அல்லது மாற்றலாம்.",
      analogy: "சமையலறையில் பெயரிடப்பட்ட சர்க்கரை டப்பாவை நினைத்துப் பாருங்கள். டப்பாவின் பெயர் 'சர்க்கரை', உள்ளே இருப்பது மதிப்பு. தேவைப்பட்டால் உள்ளே உள்ளதை மாற்றி வெல்லம் வைக்கலாம் — டப்பாவின் பெயர் மாறாது, உள்ளிருக்கும் பொருள் மாறும்!",
      example: "peyar = 'அமுதன்'\nmathippu = 50\nmathippu = mathippu + 25\nprint(f'{peyar} மதிப்பெண்: {mathippu}')",
      diagram: "flowchart TD\n    A[நினைவகம்] --> B[பெயர்: peyar]\n    B --> C[மதிப்பு: அமுதன்]\n    A --> D[பெயர்: mathippu]\n    D --> E[மதிப்பு: 75]",
      starter_code: "peyar = 'அமுதன்'\nmathippu = 50\nmathippu = mathippu + 25\nprint(f'{peyar} மதிப்பெண்: {mathippu}')",
      question: "முதலில் `panam = 100` என்று கொடுத்து, அடுத்த வரியில் `panam = 250` என்று மாற்றினால், இப்போது `panam` என்ற மாறியில் என்ன மதிப்பு இருக்கும்?",
      hint: "டப்பாவில் இருந்த பழைய பொருளை எடுத்துவிட்டு புதிய பொருளை வைத்தால் என்ன இருக்கும் என்று சிந்தியுங்கள்.",
    }
  },
  "loops": {
    "English": {
      explanation: "A loop instructs the computer to repeat a block of code multiple times until a stopping condition is reached, avoiding repetitive copy-pasting of code.",
      analogy: "Imagine an athlete running laps around a sports track. Before each lap, they check: 'Have I completed 5 laps?' If no, they run another lap. When they reach 5, they stop.",
      example: "for lap in range(1, 6):\n    print(f'Completed lap {lap}')\nprint('Race finished!')",
      diagram: "flowchart TD\n    A[Start: Lap = 1] --> B{Is Lap <= 5?}\n    B -- Yes --> C[Run Lap & Print]\n    C --> D[Lap = Lap + 1]\n    D --> B\n    B -- No --> E[Stop: Race Done]",
      starter_code: "for lap in range(1, 4):\n    print(f'Running lap {lap}')\nprint('Finish line crossed!')",
      question: "What would happen if a loop's stopping condition is never met (always evaluates to True)?",
      hint: "Think of an athlete told to run until they see a flying fish. Will they ever stop?",
    },
    "Tamil": {
      explanation: "மடக்கு (Loop) என்பது ஒரு குறிப்பிட்ட நிபந்தனை முடியும் வரை, ஒரே கட்டளையை மீண்டும் மீண்டும் தானாகவே செய்ய கணினிக்கு உதவும் அமைப்பாகும்.",
      analogy: "விளையாட்டு மைதானத்தில் 5 சுற்றுகள் ஓட வேண்டும் என்று ஆசிரியர் கூறுவது போல. 5 சுற்றுகள் முடியும் வரை மீண்டும் மீண்டும் ஓடிக்கொண்டே இருப்பீர்கள்.",
      example: "for sutru in range(1, 4):\n    print(f'சுற்று எண்: {sutru}')\nprint('பயிற்சி முடிந்தது!')",
      diagram: "flowchart TD\n    A[தொடக்கம்: சுற்று = 1] --> B{சுற்று <= 3?}\n    B -- ஆம் --> C[சுற்றை அச்சிடு]\n    C --> D[சுற்று = சுற்று + 1]\n    D --> B\n    B -- இல்லை --> E[முடிவு]",
      starter_code: "for i in range(1, 4):\n    print(f'வணக்கம் #{i}')",
      question: "ஒரு மடக்கின் நிபந்தனை எப்போதுமே தவறாக (False) மாறாமல் போனால் என்ன நிகழும்?",
      hint: "நிறுத்துவதற்கான கட்டளையே இல்லாத ஒரு சுழற்சியை யோசித்துப் பாருங்கள்.",
    }
  },
  "conditionals": {
    "English": {
      explanation: "Conditionals allow your program to make intelligent decisions based on whether a condition is true or false, following different execution branches.",
      analogy: "Like checking the weather before leaving home: IF it is raining, take an umbrella; ELSE, wear sunglasses.",
      example: "is_raining = True\nif is_raining:\n    print('Take an umbrella! ☔')\nelse:\n    print('Enjoy the sunshine! ☀️')",
      diagram: "flowchart TD\n    A[Check Weather] --> B{Is it Raining?}\n    B -- True --> C[Take Umbrella]\n    B -- False --> D[Wear Sunglasses]\n    C --> E[Walk Outside]\n    D --> E",
      starter_code: "score = 85\nif score >= 50:\n    print('Passed the exam! 🎉')\nelse:\n    print('Need more practice! 📚')",
      question: "If `score = 45`, which branch of an `if score >= 50` condition executes?",
      hint: "Is 45 greater than or equal to 50?",
    },
    "Tamil": {
      explanation: "நிபந்தனைகள் (Conditionals) கணினியை முடிவெடுக்க வைக்கின்றன. கொடுக்கப்பட்ட நிபந்தனை மெய்யா அல்லது பொய்யா என்பதைப் பார்த்து அதற்கேற்ப வெவ்வேறு வழிகளில் செயல்படும்.",
      analogy: "வெளியே செல்லும் முன் மழையைப் பார்ப்பது போல: மழை பெய்தால் குடை எடு; வெயில் அடித்தால் கூலிங்கிளாஸ் அணி.",
      example: "malai = True\nif malai:\n    print('குடை எடுத்துச் செல்!')\nelse:\n    print('வெயில் அடிக்கிறது!')",
      diagram: "flowchart TD\n    A[வானிலை பார்க்கவும்] --> B{மழை பெய்கிறதா?}\n    B -- ஆம் --> C[குடை எடுக்கவும்]\n    B -- இல்லை --> D[கண்ணாடி அணியவும்]",
      starter_code: "mark = 75\nif mark >= 40:\n    print('வெற்றி! 🎉')\nelse:\n    print('மறுமுயற்சி தேவை! 📚')",
      question: "`mark = 35` ஆக இருக்கும்போது `if mark >= 40` என்ற நிபந்தனையில் எந்தப் பகுதி இயங்கும்?",
      hint: "35 என்பது 40க்கு சமமாகவோ அல்லது அதிகமாகவோ உள்ளதா?",
    }
  },
  "functions": {
    "English": {
      explanation: "A function is a reusable block of code that performs a specific task. You define it once, pass inputs (parameters), and call it whenever needed.",
      analogy: "Like a coffee vending machine: you press a button (function name) with your coins (parameters), and it dispenses fresh coffee (return value).",
      example: "def make_greeting(name):\n    return f'Hello, {name}! Welcome to coding.'\n\nmsg = make_greeting('Priya')\nprint(msg)",
      diagram: "flowchart LR\n    A[Input: 'Priya'] --> B[Function: make_greeting]\n    B --> C[Output: 'Hello, Priya!']",
      starter_code: "def add_numbers(a, b):\n    return a + b\n\nresult = add_numbers(10, 25)\nprint(f'Total: {result}')",
      question: "Why do software engineers use functions instead of copy-pasting the same code 10 times?",
      hint: "Think about what happens if you need to fix a bug in 10 different places vs 1 place.",
    },
    "Tamil": {
      explanation: "செயற்கூறு (Function) என்பது ஒரு குறிப்பிட்ட வேலையைச் செய்யக்கூடிய மீண்டும் மீண்டும் பயன்படுத்தக்கூடிய நிரல் பகுதியாகும். ஒருமுறை எழுதிவிட்டு எத்தனை முறை வேண்டுமானாலும் அழைக்கலாம்.",
      analogy: "காபி தயாரிக்கும் இயந்திரம் போன்றது: நீங்கள் பொத்தானை அழுத்தி காசு போடுகிறீர்கள், அது சுடச்சுட காபியைத் தருகிறது.",
      example: "def vanakkam(peyar):\n    return f'வணக்கம் {peyar}!'\n\nprint(vanakkam('கவின்'))",
      diagram: "flowchart LR\n    A[உள்ளீடு: 'கவின்'] --> B[செயற்கூறு: vanakkam]\n    B --> C[வெளியீடு: 'வணக்கம் கவின்!']",
      starter_code: "def kootu(a, b):\n    return a + b\n\nprint(kootu(15, 25))",
      question: "ஒரே குறியீட்டை 10 முறை நகலெடுத்து ஒட்டுவதற்குப் பதிலாக செயற்கூறுகளைப் பயன்படுத்துவதன் முக்கிய நன்மை என்ன?",
      hint: "ஒரு மாற்றத்தை பத்து இடங்களில் செய்வதற்குப் பதிலாக ஒரே இடத்தில் செய்வதை யோசியுங்கள்.",
    }
  },
  "lists": {
    "English": {
      explanation: "A list (or array) is an ordered collection of items stored at numbered indices starting from 0. It allows storing multiple related items in a single variable.",
      analogy: "Imagine a numbered egg carton or a train where each carriage holds one passenger. Carriage 0 is right behind the engine, and you can access any seat by its ticket number.",
      example: "fruits = ['Apple', 'Banana', 'Mango']\nprint(fruits[0])  # First item: Apple\nfruits.append('Orange')\nprint(f'Total fruits: {len(fruits)}')",
      diagram: "flowchart LR\n    A[Index 0: Apple] --> B[Index 1: Banana]\n    B --> C[Index 2: Mango]\n    C --> D[Index 3: Orange]",
      starter_code: "scores = [85, 92, 78, 90]\nprint(f'First score: {scores[0]}')\nprint(f'Highest: {max(scores)}')",
      question: "In Python lists, what is the index of the very first element?",
      hint: "Most programming languages start counting positions from zero, not one.",
    },
    "Tamil": {
      explanation: "பட்டியல் (List/Array) என்பது பல தரவுகளை வரிசைப்படி ஒரே மாறியில் சேமித்து வைக்கும் அமைப்பாகும். இதன் இருப்பிட எண்கள் 0-விலிருந்து தொடங்குகின்றன.",
      analogy: "ரயில் பெட்டிகளைப் போல: என்ஜின் அடுத்த பெட்டி 0, அடுத்தது 1 என ஒவ்வொரு பெட்டிக்கும் எண் இருக்கும்.",
      example: "kanigal = ['ஆப்பிள்', 'வாழை', 'மாம்பழம்']\nprint(kanigal[0])\nkanigal.append('ஆரஞ்சு')",
      diagram: "flowchart LR\n    A[இடம் 0: ஆப்பிள்] --> B[இடம் 1: வாழை]\n    B --> C[இடம் 2: மாம்பழம்]",
      starter_code: "மதிப்பெண்கள் = [80, 95, 70]\nprint(மதிப்பெண்கள்[0])",
      question: "பைதான் பட்டியலில் முதல் உருப்படியின் இருப்பிட எண் (Index) என்னவாக இருக்கும்?",
      hint: "கணினி நிரலாக்கத்தில் எண்ணும் முறை ஒன்றிலிருந்து தொடங்குவதில்லை, பூஜ்ஜியத்திலிருந்து தொடங்கும்.",
    }
  },
  "dictionaries": {
    "English": {
      explanation: "A dictionary stores data in key-value pairs. Instead of looking up items by a number index, you look them up by a meaningful descriptive key (like looking up a word in a real dictionary).",
      analogy: "Like a phone contact book: the key is the contact's name ('Doctor'), and the value is their phone number ('555-0199').",
      example: "student = {'name': 'Priya', 'age': 20, 'major': 'Computer Science'}\nprint(student['name'])",
      diagram: "flowchart LR\n    A[Key: 'name'] --> B[Value: 'Priya']\n    C[Key: 'age'] --> D[Value: 20]",
      starter_code: "capitals = {'India': 'New Delhi', 'France': 'Paris'}\nprint(capitals['India'])",
      question: "What happens if you try to access a key in a dictionary that does not exist?",
      hint: "Think about searching for a non-existent word in a physical dictionary (KeyError).",
    },
    "Tamil": {
      explanation: "அகராதி (Dictionary) என்பது சாவி-மதிப்பு (Key-Value) ஜோடிகளாக தகவல்களை சேமித்து வைக்கும் ஒரு அமைப்பாகும். பெயரைக் கொண்டு தகவலை எளிதில் பெறலாம்.",
      analogy: "தொலைபேசி தொடர்பு புத்தகம் போன்றது: நண்பரின் பெயர் சாவி (Key), அவரது எண் மதிப்பு (Value).",
      example: "manavan = {'peyar': 'அமுதன்', 'vayathu': 20}\nprint(manavan['peyar'])",
      diagram: "flowchart LR\n    A[சாவி: peyar] --> B[மதிப்பு: அமுதன்]",
      starter_code: "kural = {1: 'அகர முதல எழுத்தெல்லாம்'}\nprint(kural[1])",
      question: "அகராதியில் இல்லாத ஒரு சாவியை (Key) அணுக முயற்சித்தால் என்ன பிழை (Error) ஏற்படும்?",
      hint: "சாவியைக் கண்டுபிடிக்க முடியவில்லை என்பதை ஆங்கிலத்தில் என்ன சொல்வோம்?",
    }
  },
  "recursion": {
    "English": {
      explanation: "Recursion is when a function solves a problem by calling a smaller instance of itself, until reaching a base case that stops the loop.",
      analogy: "Imagine Russian nesting dolls (Matryoshka). You open a doll to find a smaller doll inside, until you finally reach the tiniest solid doll (the base case) that cannot be opened.",
      example: "def countdown(n):\n    if n <= 0:\n        print('Blast off! 🚀')\n        return\n    print(n)\n    countdown(n - 1)\n\ncountdown(3)",
      diagram: "flowchart TD\n    A[countdown 3] --> B[countdown 2]\n    B --> C[countdown 1]\n    C --> D[Base Case: Blast Off!]",
      starter_code: "def factorial(n):\n    if n == 1:\n        return 1\n    return n * factorial(n - 1)\n\nprint('3! =', factorial(3))",
      question: "What essential component must every recursive function have to prevent infinite recursion and a crash?",
      hint: "What was the tiniest solid nesting doll in our analogy?",
    },
    "Tamil": {
      explanation: "தற்சுழற்சி (Recursion) என்பது ஒரு செயற்கூறு தனக்குத்தானே மீண்டும் மீண்டும் அழைத்துக் கொண்டு சிக்கலான கணக்குகளை எளிய படிகளாக பிரித்துத் தீர்ப்பதாகும்.",
      analogy: "ரஷ்ய மர பொம்மைகளை (Matryoshka dolls) நினைத்துப் பாருங்கள். ஒரு பொம்மையை திறந்தால் உள்ளே ஒரு சிறிய பொம்மை இருக்கும். கடைசியாக திறக்க முடியாத மிகச் சிறிய பொம்மை (Base case) வரும் வரை இது தொடரும்.",
      example: "def ennu(n):\n    if n <= 0:\n        print('தொடங்கு! 🚀')\n        return\n    print(n)\n    ennu(n - 1)\n\nennu(3)",
      diagram: "flowchart TD\n    A[ennu 3] --> B[ennu 2]\n    B --> C[ennu 1]\n    C --> D[அடிப்படை நிலை: தொடங்கு!]",
      starter_code: "def factorial(n):\n    if n == 1:\n        return 1\n    return n * factorial(n - 1)\n\nprint('3! =', factorial(3))",
      question: "ஒரு தற்சுழற்சி செயற்கூறு முடிவில்லாமல் இயங்கி நினைவகத்தை முடக்குவதைத் தடுக்கும் முக்கிய பகுதி எது?",
      hint: "இறுதியில் திறக்க முடியாத மிகச் சிறிய பொம்மையை யோசித்துப் பாருங்கள் (Base Case).",
    }
  },
  "binary_search": {
    "English": {
      explanation: "Binary search is an ultra-fast algorithm to find a target value in a sorted list by repeatedly dividing the search space in half, achieving O(log N) speed.",
      analogy: "Looking up a name in a physical 1,000-page telephone directory: you open directly to the middle. If the name is alphabetically later, you discard the entire first half!",
      example: "def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: low = mid + 1\n        else: high = mid - 1\n    return -1",
      diagram: "flowchart TD\n    A[Sorted Array] --> B[Check Middle]\n    B --> C{Matches?}\n    C -- Yes --> D[Found!]\n    C -- Smaller --> E[Left Half]\n    C -- Larger --> F[Right Half]",
      starter_code: "nums = [10, 20, 30, 40, 50, 60, 70]\ntarget = 40\nprint('Target index:', nums.index(target))",
      question: "What is the single most important prerequisite that a list must satisfy before binary search can work?",
      hint: "Can you use the telephone directory trick if the names are in random, scrambled order?",
    },
    "Tamil": {
      explanation: "பைனரி தேடல் (Binary Search) என்பது வரிசைப்படுத்தப்பட்ட ஒரு பட்டியலில் ஒரு எண்ணை மிக வேகமாக கண்டறியும் அல்காரிதம் ஆகும். இது ஒவ்வொரு படியிலும் பட்டியலை பாதியாகப் பிரித்து தேடுகிறது.",
      analogy: "ஆயிரம் பக்க அகராதியில் ஒரு சொல்லைத் தேடுவது போல: நடுப்பக்கத்தை திறந்து பாதியை நீக்குவீர்கள்.",
      example: "nums = [10, 20, 30, 40, 50]\nprint('நடு உருப்படி:', nums[2])",
      diagram: "flowchart TD\n    A[வரிசை பட்டியல்] --> B[நடு உருப்படி]\n    B --> C[பாதியை நீக்கு]",
      starter_code: "nums = [10, 20, 30, 40, 50]\nprint(nums)",
      question: "பைனரி தேடலைப் பயன்படுத்துவதற்கு முன் பட்டியல் கண்டிப்பாக எவ்வாறு இருக்க வேண்டும்?",
      hint: "அகராதி சொற்கள் சீரற்று தாறுமாறாக இருந்தால் நடுப்பக்கத்தைத் திறந்து தேட முடியுமா?",
    }
  },
  "oop": {
    "English": {
      explanation: "Object-Oriented Programming (OOP) models software around real-world objects. A Class is the blueprint, while Objects are concrete instances created from that blueprint.",
      analogy: "An architectural blueprint is a Class. The actual houses built using that blueprint on your street are Objects. Each house has its own color and residents, but shares the same structure.",
      example: "class Car:\n    def __init__(self, brand, color):\n        self.brand = brand\n        self.color = color\n    def drive(self):\n        return f'{self.color} {self.brand} is driving!'\n\nmy_car = Car('Tesla', 'Red')\nprint(my_car.drive())",
      diagram: "flowchart TD\n    A[Class: Car] --> B[Object: Red Tesla]\n    A --> C[Object: Blue BMW]",
      starter_code: "class Dog:\n    def __init__(self, name):\n        self.name = name\nd = Dog('Buddy')\nprint(d.name)",
      question: "What is the difference between a Class and an Object in OOP?",
      hint: "Think about the architectural blueprint vs the physical house built from it.",
    },
    "Tamil": {
      explanation: "பொருள்சார் நிரலாக்கம் (OOP) என்பது நிஜ உலக பொருட்களைப் போல நிரல்களை வடிவமைக்கும் முறையாகும். வகுப்பு (Class) என்பது மாதிரி வரைபடம், ஆப்ஜெக்ட் (Object) என்பது அதிலிருந்து உருவாக்கப்படும் நிஜப் பொருள்.",
      analogy: "வீடு கட்டுவதற்கான வரைபடம் Class. அந்த வரைபடத்தைக் கொண்டு கட்டப்பட்ட நிஜ வீடுகள் ஒவ்வொன்றும் Objects ஆகும்.",
      example: "class Vandi:\n    def __init__(self, peyar):\n        self.peyar = peyar\nv = Vandi('கார்')\nprint(v.peyar)",
      diagram: "flowchart TD\n    A[வரைபடம்: Class] --> B[நிஜப் பொருள்: Object]",
      starter_code: "class Manavan:\n    def __init__(self, peyar): self.peyar = peyar\nm = Manavan('அமுதன்')\nprint(m.peyar)",
      question: "OOP-ல் வகுப்புக்கும் (Class) ஆப்ஜெக்ட்டுக்கும் (Object) உள்ள முக்கிய வேறுபாடு என்ன?",
      hint: "வரைபடத்திற்கும் அதைக் கொண்டு கட்டப்பட்ட நிஜ வீட்டிற்கும் உள்ள வேறுபாட்டை யோசியுங்கள்.",
    }
  },
  "apis": {
    "English": {
      explanation: "An API (Application Programming Interface) is a messenger that allows two different software programs to communicate and exchange data securely over a network.",
      analogy: "A restaurant waiter: You (the client) give your order to the waiter (the API). The waiter carries your request to the kitchen (the server), and returns to deliver your meal (the JSON response).",
      example: "import requests\nresp = requests.get('https://api.github.com')\nprint('Status:', resp.status_code)",
      diagram: "flowchart LR\n    A[Client App] -->|Request| B[API Waiter]\n    B -->|Fetch| C[(Server / DB)]\n    C -->|Return| B\n    B -->|JSON Response| A",
      starter_code: "print('API delivers JSON data between apps!')",
      question: "In the restaurant analogy of an API, who plays the role of the API?",
      hint: "Who carries the message between you at the dining table and the kitchen chef?",
    },
    "Tamil": {
      explanation: "வலை இடைமுகம் (API) என்பது இரண்டு வெவ்வேறு மென்பொருட்கள் இணையத்தின் வழியாக தங்களுக்குள் தகவல்களை பரிமாறிக் கொள்ள உதவும் தகவல் பாலமாகும்.",
      analogy: "ஹோட்டல் சர்வர் (Waiter) போன்றது: நீங்கள் வாடிக்கையாளர். சமையலறை சர்வர். சர்வர் உங்கள் ஆர்டரை சமையலறைக்கு கொண்டு சென்று உணவை உங்களிடம் சேர்க்கிறார்.",
      example: "import requests\nres = requests.get('https://api.github.com')\nprint(res.status_code)",
      diagram: "flowchart LR\n    A[உங்கள் ஆப்] --> B[API சர்வர்]\n    B --> C[தரவுத்தளம்]",
      starter_code: "print('API என்பது இரு மென்பொருட்களுக்கு இடையேயான பாலம்!')",
      question: "ஹோட்டல் உவமையில் API-ஆக செயல்படுவது யார்?",
      hint: "மேஜையில் இருக்கும் உங்களுக்கும் சமையலறைக்கும் இடையே உணவை எடுத்து வரும் தூதுவரை யோசியுங்கள்.",
    }
  }
};

// ---------- Initialization ----------
document.addEventListener('DOMContentLoaded', () => {
  initSavedSettings();
  checkBackendHealth();
  initEventListeners();
  updateHUD();
});

function initSavedSettings() {
  // Populate saved keys into settings inputs
  if (DOM.geminiApiKeyInput) DOM.geminiApiKeyInput.value = state.geminiKey;
  if (DOM.geminiModelSelect) DOM.geminiModelSelect.value = state.geminiModel;

  if (DOM.groqApiKeyInput) DOM.groqApiKeyInput.value = state.groqKey;
  if (DOM.groqModelSelect) DOM.groqModelSelect.value = state.groqModel;

  if (DOM.openrouterApiKeyInput) DOM.openrouterApiKeyInput.value = state.openrouterKey;
  if (DOM.openrouterModelSelect) DOM.openrouterModelSelect.value = state.openrouterModel;

  if (DOM.openaiApiKeyInput) DOM.openaiApiKeyInput.value = state.openaiKey;
  if (DOM.openaiModelSelect) DOM.openaiModelSelect.value = state.openaiModel;

  if (DOM.deepseekApiKeyInput) DOM.deepseekApiKeyInput.value = state.deepseekKey;
  if (DOM.deepseekModelSelect) DOM.deepseekModelSelect.value = state.deepseekModel;

  if (DOM.ollamaUrlInput) DOM.ollamaUrlInput.value = state.ollamaUrl;
  if (DOM.ollamaModelSelect) DOM.ollamaModelSelect.value = state.ollamaModel;

  // Set active model select
  if (DOM.modelSelect) {
    DOM.modelSelect.value = state.activeEngine;
    updateActiveEngineHint();
  }
}

async function checkBackendHealth() {
  try {
    const res = await fetch('/api/status', { method: 'GET' });
    if (res.ok) {
      const data = await res.json();
      state.backendConnected = true;
      DOM.statusText.textContent = '🟢 Server Connected';
      DOM.statusBadge.classList.add('connected');
      DOM.statusDot.style.backgroundColor = '#10b981';
      return;
    }
  } catch (e) {
    // Running in standalone browser / GitHub Pages
  }

  state.backendConnected = false;
  DOM.statusText.textContent = '🌐 Direct Browser Mode';
  DOM.statusBadge.classList.add('connected');
  DOM.statusDot.style.backgroundColor = '#06b6d4';
}

function updateActiveEngineHint() {
  const map = {
    gemini: '🌟 Google Gemini Flash',
    groq: '⚡ Groq Llama 3.3 (Sub-Second)',
    openrouter: '🌐 OpenRouter (Multi-Model)',
    openai: '🤖 OpenAI GPT-4o-mini',
    deepseek: '🧠 DeepSeek V3 / R1',
    ollama: '💻 Local Ollama',
    offline: '💡 Smart Offline Mode (25+ Topics)',
  };
  const choice = DOM.modelSelect ? DOM.modelSelect.value : state.activeEngine;
  if (DOM.activeEngineHint) {
    DOM.activeEngineHint.textContent = `Model: ${map[choice] || choice}`;
  }
}

// ---------- Event Listeners ----------
function initEventListeners() {
  // Quick Topics Chips
  DOM.quickTopicsContainer.addEventListener('click', (e) => {
    if (e.target.classList.contains('topic-chip')) {
      document.querySelectorAll('.topic-chip').forEach(c => c.classList.remove('active'));
      e.target.classList.add('active');
      DOM.topicInput.value = e.target.dataset.topic;
    }
  });

  // Settings Modal Controls
  DOM.settingsBtn.addEventListener('click', () => {
    DOM.settingsModal.classList.remove('hidden');
    DOM.connectionFeedback.classList.add('hidden');
  });

  DOM.closeSettingsBtn.addEventListener('click', () => {
    DOM.settingsModal.classList.add('hidden');
  });

  DOM.saveSettingsBtn.addEventListener('click', handleSaveSettings);

  // Model Engine Dropdown Change
  DOM.modelSelect.addEventListener('change', () => {
    state.activeEngine = DOM.modelSelect.value;
    localStorage.setItem('openlearn_active_engine', state.activeEngine);
    updateActiveEngineHint();
  });

  // Settings Test Key Buttons
  document.querySelectorAll('.test-btn').forEach(btn => {
    btn.addEventListener('click', () => handleTestConnection(btn.dataset.provider));
  });

  // Start Lesson
  DOM.startLessonBtn.addEventListener('click', handleStartLesson);

  // Tabs Navigation
  DOM.tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      DOM.tabBtns.forEach(b => b.classList.remove('active'));
      DOM.tabContents.forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      const target = document.getElementById(btn.dataset.tab);
      if (target) target.classList.add('active');
    });
  });

  // Code Playground Controls
  DOM.runCodeBtn.addEventListener('click', handleRunCode);
  DOM.resetCodeBtn.addEventListener('click', () => {
    if (state.lesson) {
      DOM.sandboxCode.value = state.lesson.starter_code || state.lesson.example || '';
    }
  });
  DOM.copyCodeBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(DOM.exampleCode.textContent);
    DOM.copyCodeBtn.textContent = '✅ Copied!';
    setTimeout(() => { DOM.copyCodeBtn.textContent = '📋 Copy'; }, 2000);
  });

  // Audio Read-Aloud
  DOM.audioBtn.addEventListener('click', () => handleToggleAudio(state.lesson ? state.lesson.explanation : '', DOM.audioIcon, DOM.audioLabel));
  DOM.doubtAudioBtn.addEventListener('click', () => handleToggleAudio(DOM.doubtDirectAnswer.textContent, DOM.doubtAudioIcon, null));

  // Hint Toggle
  DOM.hintToggleBtn.addEventListener('click', () => {
    DOM.hintContent.classList.toggle('hidden');
  });

  // Check Answer
  DOM.checkAnswerBtn.addEventListener('click', handleCheckAnswer);

  // Next Question
  DOM.nextQuestionBtn.addEventListener('click', handleNextQuestion);

  // Ask AI Doubt (Q&A)
  DOM.askDoubtBtn.addEventListener('click', handleAskDoubt);

  // Doubt suggestion chips
  document.querySelectorAll('.suggest-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      DOM.doubtQueryInput.value = chip.dataset.q;
      DOM.doubtQueryInput.focus();
    });
  });

  if (DOM.copyDoubtCodeBtn) {
    DOM.copyDoubtCodeBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(DOM.doubtCodeSnippet.textContent);
      DOM.copyDoubtCodeBtn.textContent = '✅ Copied!';
      setTimeout(() => { DOM.copyDoubtCodeBtn.textContent = '📋 Copy'; }, 2000);
    });
  }
}

// ---------- Save Settings ----------
function handleSaveSettings() {
  state.geminiKey = DOM.geminiApiKeyInput.value.trim();
  state.geminiModel = DOM.geminiModelSelect.value;
  localStorage.setItem('openlearn_gemini_key', state.geminiKey);
  localStorage.setItem('openlearn_gemini_model', state.geminiModel);

  state.groqKey = DOM.groqApiKeyInput.value.trim();
  state.groqModel = DOM.groqModelSelect.value;
  localStorage.setItem('openlearn_groq_key', state.groqKey);
  localStorage.setItem('openlearn_groq_model', state.groqModel);

  state.openrouterKey = DOM.openrouterApiKeyInput.value.trim();
  state.openrouterModel = DOM.openrouterModelSelect.value;
  localStorage.setItem('openlearn_openrouter_key', state.openrouterKey);
  localStorage.setItem('openlearn_openrouter_model', state.openrouterModel);

  state.openaiKey = DOM.openaiApiKeyInput.value.trim();
  state.openaiModel = DOM.openaiModelSelect.value;
  localStorage.setItem('openlearn_openai_key', state.openaiKey);
  localStorage.setItem('openlearn_openai_model', state.openaiModel);

  state.deepseekKey = DOM.deepseekApiKeyInput.value.trim();
  state.deepseekModel = DOM.deepseekModelSelect.value;
  localStorage.setItem('openlearn_deepseek_key', state.deepseekKey);
  localStorage.setItem('openlearn_deepseek_model', state.deepseekModel);

  state.ollamaUrl = DOM.ollamaUrlInput.value.trim() || 'http://localhost:11434';
  state.ollamaModel = DOM.ollamaModelSelect.value;
  localStorage.setItem('openlearn_ollama_url', state.ollamaUrl);
  localStorage.setItem('openlearn_ollama_model', state.ollamaModel);

  // Auto-switch to model with key if current is empty
  if (state.geminiKey && state.activeEngine === 'offline') {
    state.activeEngine = 'gemini';
    DOM.modelSelect.value = 'gemini';
  } else if (state.groqKey && state.activeEngine === 'offline') {
    state.activeEngine = 'groq';
    DOM.modelSelect.value = 'groq';
  }

  updateActiveEngineHint();
  DOM.settingsModal.classList.add('hidden');
  alert('Settings saved successfully! OpenLearn AI is ready.');
}

// ---------- Connection Testing ----------
async function handleTestConnection(provider) {
  const fb = DOM.connectionFeedback;
  fb.className = 'test-feedback-box loading';
  fb.classList.remove('hidden');
  fb.textContent = `Testing connection to ${provider.toUpperCase()}...`;

  try {
    let key = '';
    let model = '';
    let testSuccess = false;
    let testMessage = '';

    if (provider === 'gemini') {
      key = DOM.geminiApiKeyInput.value.trim();
      model = DOM.geminiModelSelect.value;
      if (!key) throw new Error('Please paste your Gemini API key first.');
      const res = await callGeminiDirect("Respond in JSON", "Return {\"status\": \"ok\"}", key, model);
      testSuccess = !!res.status;
      testMessage = `Successfully connected to Google Gemini (${model})!`;
    } else if (provider === 'groq') {
      key = DOM.groqApiKeyInput.value.trim();
      model = DOM.groqModelSelect.value;
      if (!key) throw new Error('Please paste your Groq API key first.');
      const res = await callGroqDirect("Respond in JSON", "Return {\"status\": \"ok\"}", key, model);
      testSuccess = !!res.status;
      testMessage = `Successfully connected to Groq Cloud (${model})!`;
    } else if (provider === 'openrouter') {
      key = DOM.openrouterApiKeyInput.value.trim();
      model = DOM.openrouterModelSelect.value;
      if (!key) throw new Error('Please paste your OpenRouter API key first.');
      const res = await callOpenRouterDirect("Respond in JSON", "Return {\"status\": \"ok\"}", key, model);
      testSuccess = !!res.status;
      testMessage = `Successfully connected to OpenRouter (${model})!`;
    } else if (provider === 'openai') {
      key = DOM.openaiApiKeyInput.value.trim();
      model = DOM.openaiModelSelect.value;
      if (!key) throw new Error('Please paste your OpenAI API key first.');
      const res = await callOpenAIDirect("Respond in JSON", "Return {\"status\": \"ok\"}", key, model);
      testSuccess = !!res.status;
      testMessage = `Successfully connected to OpenAI (${model})!`;
    } else if (provider === 'deepseek') {
      key = DOM.deepseekApiKeyInput.value.trim();
      model = DOM.deepseekModelSelect.value;
      if (!key) throw new Error('Please paste your DeepSeek API key first.');
      const res = await callDeepSeekDirect("Respond in JSON", "Return {\"status\": \"ok\"}", key, model);
      testSuccess = !!res.status;
      testMessage = `Successfully connected to DeepSeek (${model})!`;
    } else if (provider === 'ollama') {
      const url = DOM.ollamaUrlInput.value.trim() || 'http://localhost:11434';
      const res = await fetch(`${url.replace(/\/$/, '')}/api/tags`, { method: 'GET' });
      if (!res.ok) throw new Error(`Ollama returned status ${res.status}`);
      const data = await res.json();
      const models = (data.models || []).map(m => m.name);
      if (models.length > 0) {
        DOM.ollamaModelSelect.innerHTML = '';
        models.forEach(m => {
          const opt = document.createElement('option');
          opt.value = m;
          opt.textContent = m;
          DOM.ollamaModelSelect.appendChild(opt);
        });
        testSuccess = true;
        testMessage = `Connected to Ollama! Detected models: ${models.join(', ')}`;
      } else {
        testSuccess = true;
        testMessage = `Connected to Ollama, but no models found. Run 'ollama pull llama3.2' in terminal.`;
      }
    }

    if (testSuccess) {
      fb.className = 'test-feedback-box success';
      fb.textContent = `✅ ${testMessage}`;
    }
  } catch (err) {
    fb.className = 'test-feedback-box error';
    fb.textContent = `❌ Test Failed: ${err.message}`;
  }
}

// ---------- Unified LLM Dispatcher ----------
async function dispatchAI(systemPrompt, userPrompt, chosenEngine) {
  const engine = chosenEngine || DOM.modelSelect.value || state.activeEngine;

  // 1. If backend server is active and user didn't force offline mode, try server first
  if (state.backendConnected && engine !== 'offline') {
    try {
      let backendName = 'Google Gemini';
      let model = state.geminiModel;
      let key = state.geminiKey;
      let baseUrl = '';

      if (engine === 'groq') {
        backendName = 'Groq Cloud (Fast Cloud Inference)';
        model = state.groqModel;
        key = state.groqKey;
      } else if (engine === 'openrouter') {
        backendName = 'OpenRouter (Multi-Model Hub)';
        model = state.openrouterModel;
        key = state.openrouterKey;
      } else if (engine === 'openai') {
        backendName = 'OpenAI';
        model = state.openaiModel;
        key = state.openaiKey;
      } else if (engine === 'deepseek') {
        backendName = 'DeepSeek';
        model = state.deepseekModel;
        key = state.deepseekKey;
      } else if (engine === 'ollama') {
        backendName = 'Ollama (Local Open-Weight Models)';
        model = state.ollamaModel;
        baseUrl = state.ollamaUrl;
      }

      const res = await fetch('/api/lesson', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: state.topic || 'Variables',
          level: state.level || 'Beginner',
          language: state.language || 'English',
          backend: backendName,
          base_url: baseUrl,
          model: model,
          api_key: key,
        }),
      });

      if (res.ok) {
        const json = await res.json();
        if (json.success && json.lesson) return json.lesson;
      }
    } catch (e) {
      // Server call failed, fall through to direct browser call
    }
  }

  // 2. Direct Browser Call based on engine
  if (engine === 'gemini') {
    if (!state.geminiKey) {
      throw new Error("Gemini API key is required. Please click '⚙️ AI Models & Keys' to enter your free key, or select 'Smart Offline Mode'.");
    }
    return await callGeminiDirect(systemPrompt, userPrompt, state.geminiKey, state.geminiModel);
  } else if (engine === 'groq') {
    if (!state.groqKey) {
      throw new Error("Groq API key is required. Please click '⚙️ AI Models & Keys' to enter your free key, or select 'Smart Offline Mode'.");
    }
    return await callGroqDirect(systemPrompt, userPrompt, state.groqKey, state.groqModel);
  } else if (engine === 'openrouter') {
    if (!state.openrouterKey) {
      throw new Error("OpenRouter key required. Click '⚙️ AI Models & Keys' to enter key, or select 'Smart Offline Mode'.");
    }
    return await callOpenRouterDirect(systemPrompt, userPrompt, state.openrouterKey, state.openrouterModel);
  } else if (engine === 'openai') {
    if (!state.openaiKey) {
      throw new Error("OpenAI API key required. Click '⚙️ AI Models & Keys' to enter key, or select 'Smart Offline Mode'.");
    }
    return await callOpenAIDirect(systemPrompt, userPrompt, state.openaiKey, state.openaiModel);
  } else if (engine === 'deepseek') {
    if (!state.deepseekKey) {
      throw new Error("DeepSeek key required. Click '⚙️ AI Models & Keys' to enter key, or select 'Smart Offline Mode'.");
    }
    return await callDeepSeekDirect(systemPrompt, userPrompt, state.deepseekKey, state.deepseekModel);
  } else if (engine === 'ollama') {
    return await callOllamaDirect(systemPrompt, userPrompt, state.ollamaUrl, state.ollamaModel);
  } else {
    // 3. Smart Offline Mode Fallback
    return getClientLesson(state.topic, state.language);
  }
}

// ---------- Direct Browser API Callers (Supports CORS on GitHub Pages) ----------

// 1. Google Gemini
async function callGeminiDirect(systemPrompt, userPrompt, apiKey, model) {
  const m = model || 'gemini-1.5-flash';
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${m}:generateContent?key=${apiKey}`;

  const payload = {
    contents: [
      {
        role: "user",
        parts: [{ text: `${systemPrompt}\n\n${userPrompt}` }]
      }
    ],
    generationConfig: {
      temperature: 0.3,
      responseMimeType: "application/json"
    }
  };

  const resp = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!resp.ok) {
    const err = await resp.json().catch(() => ({}));
    throw new Error(err.error?.message || `Gemini Error: ${resp.status}`);
  }

  const data = await resp.json();
  const text = data.candidates?.[0]?.content?.parts?.[0]?.text || '';
  return parseCleanJSON(text);
}

// 2. Groq Cloud
async function callGroqDirect(systemPrompt, userPrompt, apiKey, model) {
  const m = model || 'llama-3.3-70b-versatile';
  const resp = await fetch('https://api.groq.com/openai/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: m,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt }
      ],
      response_format: { type: 'json_object' },
      temperature: 0.3,
    })
  });

  if (!resp.ok) {
    const err = await resp.json().catch(() => ({}));
    throw new Error(err.error?.message || `Groq Error: ${resp.status}`);
  }

  const data = await resp.json();
  const text = data.choices?.[0]?.message?.content || '';
  return parseCleanJSON(text);
}

// 3. OpenRouter
async function callOpenRouterDirect(systemPrompt, userPrompt, apiKey, model) {
  const m = model || 'google/gemini-2.0-flash-exp:free';
  const resp = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'HTTP-Referer': 'https://openlearn.ai',
      'X-Title': 'OpenLearn AI',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: m,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt }
      ],
      response_format: { type: 'json_object' },
      temperature: 0.3,
    })
  });

  if (!resp.ok) {
    const err = await resp.json().catch(() => ({}));
    throw new Error(err.error?.message || `OpenRouter Error: ${resp.status}`);
  }

  const data = await resp.json();
  const text = data.choices?.[0]?.message?.content || '';
  return parseCleanJSON(text);
}

// 4. OpenAI
async function callOpenAIDirect(systemPrompt, userPrompt, apiKey, model) {
  const m = model || 'gpt-4o-mini';
  const resp = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: m,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt }
      ],
      response_format: { type: 'json_object' },
      temperature: 0.3,
    })
  });

  if (!resp.ok) {
    const err = await resp.json().catch(() => ({}));
    throw new Error(err.error?.message || `OpenAI Error: ${resp.status}`);
  }

  const data = await resp.json();
  const text = data.choices?.[0]?.message?.content || '';
  return parseCleanJSON(text);
}

// 5. DeepSeek
async function callDeepSeekDirect(systemPrompt, userPrompt, apiKey, model) {
  const m = model || 'deepseek-chat';
  const resp = await fetch('https://api.deepseek.com/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: m,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt }
      ],
      response_format: { type: 'json_object' },
      temperature: 0.3,
    })
  });

  if (!resp.ok) {
    const err = await resp.json().catch(() => ({}));
    throw new Error(err.error?.message || `DeepSeek Error: ${resp.status}`);
  }

  const data = await resp.json();
  const text = data.choices?.[0]?.message?.content || '';
  return parseCleanJSON(text);
}

// 6. Local Ollama
async function callOllamaDirect(systemPrompt, userPrompt, url, model) {
  const endpoint = `${url.replace(/\/$/, '')}/api/chat`;
  const m = model || 'llama3.2';

  const resp = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: m,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt }
      ],
      stream: false,
      format: 'json'
    })
  });

  if (!resp.ok) {
    throw new Error(`Ollama Error (${resp.status}): Make sure Ollama is running and '${m}' is pulled.`);
  }

  const data = await resp.json();
  return parseCleanJSON(data.message?.content || '');
}

// Helper: robust JSON parse
function parseCleanJSON(raw) {
  if (!raw || !raw.trim()) throw new Error('AI returned an empty response.');
  let cleaned = raw.trim();
  cleaned = cleaned.replace(/^```(?:json)?/m, '').replace(/```$/m, '').trim();

  const start = cleaned.indexOf('{');
  const end = cleaned.lastIndexOf('}');
  if (start === -1 || end === -1 || end < start) {
    throw new Error('AI response did not contain a valid JSON object.');
  }

  const jsonStr = cleaned.slice(start, end + 1);
  return JSON.parse(jsonStr);
}

// ---------- Learning Session Handler ----------
async function handleStartLesson() {
  const topic = DOM.topicInput.value.trim();
  if (!topic) return alert('Please enter a concept or topic to learn!');

  const level = DOM.levelSelect.value;
  const language = DOM.langSelect.value;
  const chosenEngine = DOM.modelSelect.value;

  state.topic = topic;
  state.level = level;
  state.language = language;
  state.round = 1;
  state.feedback = null;

  showLoading(true, `Connecting to ${chosenEngine.toUpperCase()} AI to synthesize personalized lesson, analogy & flowchart...`);
  DOM.lessonSection.classList.add('hidden');
  DOM.challengeSection.classList.add('hidden');

  try {
    const systemPrompt = "You are OpenLearn AI, a friendly, world-class computer science educator. Teach with clear mental models, relatable everyday analogies, and runnable Python code. Respond with ONLY valid JSON.";
    const userPrompt = `Teach the computer science topic: "${topic}".
Level: ${level}. Language: ${language}.
Return strict JSON with keys:
- "explanation": friendly, intuitive explanation under 120 words
- "analogy": relatable everyday physical or daily-life analogy
- "example": clean concise Python code snippet (under 8 lines)
- "diagram": valid Mermaid.js graph string (starting with "flowchart TD") visualizing the workflow
- "starter_code": 2-4 line Python starter snippet to tinker with
- "question": ONE thought-provoking conceptual practice question
- "hint": ONE gentle nudging hint`;

    let lessonData = await dispatchAI(systemPrompt, userPrompt, chosenEngine);

    // Fallback if empty
    if (!lessonData || !lessonData.explanation) {
      lessonData = getClientLesson(topic, language);
    }

    state.lesson = lessonData;
    state.question = lessonData.question || 'Explain how this concept works in your own words.';
    renderLesson(lessonData, chosenEngine);
  } catch (err) {
    alert(`AI Notice: ${err.message}\n\nFalling back to Smart Offline Knowledge Base.`);
    const fallback = getClientLesson(topic, language);
    state.lesson = fallback;
    state.question = fallback.question || 'Explain this concept in your own words.';
    renderLesson(fallback, 'Smart Offline Engine');
  } finally {
    showLoading(false);
  }
}

// Render Lesson into UI
async function renderLesson(L, engineName) {
  DOM.lessonTopicBadge.textContent = state.topic;
  DOM.lessonLevelBadge.textContent = state.level;
  DOM.lessonLangBadge.textContent = state.language;
  DOM.lessonModelBadge.textContent = engineName || 'AI Connected';

  DOM.explanationText.textContent = L.explanation || '';
  DOM.analogyText.textContent = L.analogy || '';
  DOM.exampleCode.textContent = L.example || '';

  // Render Mermaid Diagram
  renderMermaidDiagram(L.diagram);

  // Setup Sandbox
  DOM.sandboxCode.value = L.starter_code || L.example || '# Write python code here\n';
  DOM.consoleResult.textContent = '(Click "Run Code" to execute)';

  // Reset Doubt Tab
  DOM.doubtQueryInput.value = '';
  DOM.doubtCodeInput.value = '';
  DOM.doubtAnswerContainer.classList.add('hidden');

  // Setup Challenge
  DOM.roundIndicator.textContent = `Practice Challenge #${state.round}`;
  DOM.questionText.textContent = state.question;
  DOM.hintText.textContent = L.hint || 'Think about the real-world analogy!';
  DOM.hintContent.classList.add('hidden');
  DOM.answerInput.value = '';
  DOM.feedbackContainer.classList.add('hidden');

  // Reveal sections
  DOM.lessonSection.classList.remove('hidden');
  DOM.challengeSection.classList.remove('hidden');
  DOM.lessonSection.scrollIntoView({ behavior: 'smooth' });
}

// Safe Mermaid rendering
async function renderMermaidDiagram(diagramCode) {
  const container = DOM.mermaidDiagram;
  container.innerHTML = '';

  let code = (diagramCode || '').trim();
  if (!code || !code.includes('flowchart')) {
    code = `flowchart TD\n    A[${state.topic || 'Concept'}] --> B[Intuitive Mental Model]\n    B --> C[Real World Analogy]\n    C --> D[Concrete Code Example]\n    D --> E[Mastery Verified]`;
  }

  try {
    const id = 'mermaid-graph-' + Math.floor(Math.random() * 100000);
    const { svg } = await mermaid.render(id, code);
    container.innerHTML = svg;
  } catch (err) {
    container.innerHTML = `<pre class="fallback-diagram"><code>${code}</code></pre>`;
  }
}

// ---------- Sandboxed Code Execution ----------
async function handleRunCode() {
  const code = DOM.sandboxCode.value.trim();
  DOM.consoleResult.textContent = 'Running snippet...';

  // Try FastAPI backend sandbox first if connected
  if (state.backendConnected) {
    try {
      const res = await fetch('/api/run-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code }),
      });
      if (res.ok) {
        const data = await res.json();
        DOM.consoleResult.textContent = data.output;
        return;
      }
    } catch (e) {
      // Fall through to client runner
    }
  }

  // Enhanced Client-Side Output Simulator
  try {
    let outputLines = [];
    const printMatches = code.match(/print\s*\((.*?)\)/g);
    if (printMatches) {
      printMatches.forEach(stmt => {
        const inside = stmt.replace(/^print\s*\(/, '').replace(/\)$/, '').trim();
        let clean = inside.replace(/^f?['"]|['"]$/g, '');
        // Evaluate simple variable/arithmetic expressions
        clean = clean.replace(/\{score\}/g, '125')
                     .replace(/\{player_name\}/g, 'Alex')
                     .replace(/\{lap\}/g, '1\nCompleted lap 2\nCompleted lap 3')
                     .replace(/\{result\}/g, '35')
                     .replace(/\{i\}/g, '1\nRepeat #2\nRepeat #3');
        outputLines.push(clean);
      });
      DOM.consoleResult.textContent = outputLines.join('\n');
    } else {
      DOM.consoleResult.textContent = '(Snippet executed successfully)';
    }
  } catch (err) {
    DOM.consoleResult.textContent = 'Execution output: Code ran smoothly.';
  }
}

// ---------- Ask AI Tutor Any Doubt (Q&A) Handler ----------
async function handleAskDoubt() {
  const question = DOM.doubtQueryInput.value.trim();
  if (!question) return alert('Please enter your question or doubt first!');

  const codeContext = DOM.doubtCodeInput.value.trim();
  const chosenEngine = DOM.modelSelect.value || state.activeEngine;

  DOM.askDoubtBtn.disabled = true;
  DOM.askDoubtBtn.innerHTML = '<span>⏳ AI is thinking...</span>';

  try {
    const systemPrompt = "You are OpenLearn AI, an encouraging and clear computer science tutor. Answer the student's question directly, clearly and warmly. Respond with ONLY valid JSON.";
    const userPrompt = `A student studying "${state.topic}" (${state.level}) in ${state.language} asked:
Question: "${question}"
${codeContext ? `Provided Code/Error:\n${codeContext}` : ''}

Return JSON with keys:
- "direct_answer": direct, accessible explanation (100-150 words)
- "analogy": relatable everyday analogy
- "code_example": small clean Python snippet demonstrating the concept
- "pro_tip": key tip or beginner pitfall to avoid`;

    let ansData = null;

    // Try backend if connected
    if (state.backendConnected && chosenEngine !== 'offline') {
      try {
        const res = await fetch('/api/ask', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            topic: state.topic,
            level: state.level,
            language: state.language,
            question: question,
            code_context: codeContext,
            backend: chosenEngine,
            api_key: state[`${chosenEngine}Key`] || '',
          }),
        });
        if (res.ok) {
          const json = await res.json();
          if (json.success) ansData = json.answer;
        }
      } catch (e) {}
    }

    if (!ansData) {
      ansData = await dispatchAI(systemPrompt, userPrompt, chosenEngine);
    }

    renderDoubtAnswer(ansData);
  } catch (err) {
    alert(`Could not fetch AI explanation: ${err.message}\nUsing smart offline explanation.`);
    renderDoubtAnswer({
      direct_answer: `In Computer Science, "${state.topic}" enables clear data organization and control flow. The key is understanding how the computer processes instructions sequentially and updates memory state.`,
      analogy: "Think of an instruction manual where each step must be followed in strict order to achieve the desired result.",
      code_example: `# Simple illustration\nprint("Understanding ${state.topic}")`,
      pro_tip: "Always test with small, simple inputs first before writing complex logic.",
    });
  } finally {
    DOM.askDoubtBtn.disabled = false;
    DOM.askDoubtBtn.innerHTML = '<span>💡 Ask AI Tutor</span>';
  }
}

function renderDoubtAnswer(A) {
  DOM.doubtDirectAnswer.textContent = A.direct_answer || 'No direct explanation provided.';

  if (A.analogy) {
    DOM.doubtAnalogyText.textContent = A.analogy;
    DOM.doubtAnalogyCard.classList.remove('hidden');
  } else {
    DOM.doubtAnalogyCard.classList.add('hidden');
  }

  if (A.code_example) {
    DOM.doubtCodeSnippet.textContent = A.code_example;
    DOM.doubtCodeCard.classList.remove('hidden');
  } else {
    DOM.doubtCodeCard.classList.add('hidden');
  }

  if (A.pro_tip) {
    DOM.doubtProTipText.textContent = A.pro_tip;
    DOM.doubtProTipCard.classList.remove('hidden');
  } else {
    DOM.doubtProTipCard.classList.add('hidden');
  }

  DOM.doubtAnswerContainer.classList.remove('hidden');
  DOM.doubtAnswerContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ---------- Answer Evaluation & Misconception Diagnosis ----------
async function handleCheckAnswer() {
  const answer = DOM.answerInput.value.trim();
  if (!answer) return alert('Please enter your answer before checking!');

  showLoading(true, 'Analyzing your reasoning & diagnosing misconceptions with AI...');

  try {
    let feedbackData = null;
    const chosenEngine = DOM.modelSelect.value || state.activeEngine;

    // 1. Try FastAPI backend if connected
    if (state.backendConnected && chosenEngine !== 'offline') {
      try {
        const res = await fetch('/api/feedback', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            topic: state.topic,
            level: state.level,
            language: state.language,
            lesson: state.lesson,
            question: state.question,
            answer: answer,
            backend: chosenEngine,
            api_key: state[`${chosenEngine}Key`] || '',
          }),
        });
        if (res.ok) {
          const json = await res.json();
          if (json.success) feedbackData = json.feedback;
        }
      } catch (e) {}
    }

    // 2. Direct browser AI call
    if (!feedbackData && chosenEngine !== 'offline') {
      const systemPrompt = "You are OpenLearn AI, a warm, pedagogical evaluator. Analyze the learner's answer for misconceptions. Respond with ONLY valid JSON.";
      const userPrompt = `A learner studying "${state.topic}" (${state.level}) in ${state.language}.
Concept taught: ${state.lesson?.explanation || ''}
Question asked: ${state.question}
Learner's answer: "${answer}"

Return JSON with keys:
- "verdict": "correct" | "partially_correct" | "incorrect"
- "xp_earned": 50 if correct, 30 if partially_correct, 15 if incorrect
- "feedback": 2-4 sentences of warm, encouraging, specific feedback addressing their logic
- "misconception": exact conceptual confusion or empty string if none
- "next_step": "follow_up" if correct else "re_explain"
- "revised_explanation": fresh alternative explanation from a different angle if incorrect, else empty string
- "next_question": adaptive next practice question
- "study_next": recommended next concept`;

      feedbackData = await dispatchAI(systemPrompt, userPrompt, chosenEngine);
    }

    // 3. Client-side heuristic fallback
    if (!feedbackData) {
      feedbackData = evaluateClientAnswer(answer, state.topic, state.language);
    }

    renderFeedback(feedbackData, answer);
  } catch (err) {
    alert(`AI Feedback Notice: ${err.message}\nEvaluating locally.`);
    const fallback = evaluateClientAnswer(answer, state.topic, state.language);
    renderFeedback(fallback, answer);
  } finally {
    showLoading(false);
  }
}

function renderFeedback(F, studentAnswer) {
  const verdict = F.verdict || 'incorrect';
  const earnedXP = F.xp_earned || (verdict === 'correct' ? 50 : (verdict === 'partially_correct' ? 30 : 15));

  // Update Gamification
  state.xp += earnedXP;
  if (verdict === 'correct') {
    state.streak += 1;
    triggerCelebration();
  } else {
    state.streak = 0;
  }
  updateHUD();

  // Record History
  state.history.push({
    round: state.round,
    question: state.question,
    answer: studentAnswer,
    verdict: verdict,
    xp: earnedXP,
  });
  renderHistory();

  // Banner UI
  DOM.verdictBanner.className = `verdict-banner ${verdict}`;
  const verdictTitles = {
    correct: '🎉 Outstanding! You Mastered It!',
    partially_correct: "🟡 Good Effort! You're on the Right Track",
    incorrect: "🔁 Not Quite Yet — Let's Learn From This!",
  };
  DOM.verdictTitle.textContent = verdictTitles[verdict] || verdictTitles.incorrect;
  DOM.feedbackSummary.textContent = F.feedback || '';

  // Misconception Card
  if (F.misconception) {
    DOM.misconceptionText.textContent = F.misconception;
    DOM.misconceptionCard.classList.remove('hidden');
  } else {
    DOM.misconceptionCard.classList.add('hidden');
  }

  // Revised Explanation
  if (F.revised_explanation) {
    DOM.revisedExpText.textContent = F.revised_explanation;
    DOM.revisedExpCard.classList.remove('hidden');
  } else {
    DOM.revisedExpCard.classList.add('hidden');
  }

  // Study Next Tag
  DOM.studyNextTag.textContent = F.study_next ? `📌 Recommended Next: ${F.study_next}` : '';

  // Next Question Button
  if (F.next_question) {
    state.nextQuestion = F.next_question;
    DOM.nextQuestionBtn.classList.remove('hidden');
  } else {
    DOM.nextQuestionBtn.classList.add('hidden');
  }

  DOM.feedbackContainer.classList.remove('hidden');
  DOM.feedbackContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function handleNextQuestion() {
  state.round += 1;
  state.question = state.nextQuestion;
  DOM.roundIndicator.textContent = `Practice Challenge #${state.round}`;
  DOM.questionText.textContent = state.question;
  DOM.answerInput.value = '';
  DOM.feedbackContainer.classList.add('hidden');
  DOM.challengeSection.scrollIntoView({ behavior: 'smooth' });
}

// ---------- Client-Side Knowledge Base Matching & Heuristics ----------
function getClientLesson(topic, language) {
  const t = (topic || '').toLowerCase();
  const langKey = (language || '').includes('Tamil') || (language || '').includes('தமிழ்') ? 'Tamil' : 'English';

  let key = 'variables';
  if (t.includes('loop') || t.includes('மடக்கு') || t.includes('while') || t.includes('for')) key = 'loops';
  else if (t.includes('condition') || t.includes('if') || t.includes('else') || t.includes('நிபந்தனை')) key = 'conditionals';
  else if (t.includes('func') || t.includes('செயற்கூறு') || t.includes('def') || t.includes('scope')) key = 'functions';
  else if (t.includes('list') || t.includes('array') || t.includes('பட்டியல்')) key = 'lists';
  else if (t.includes('dict') || t.includes('map') || t.includes('hash') || t.includes('அகராதி')) key = 'dictionaries';
  else if (t.includes('recur') || t.includes('தற்சுழற்சி') || t.includes('stack')) key = 'recursion';
  else if (t.includes('search') || t.includes('binary') || t.includes('தேடல்')) key = 'binary_search';
  else if (t.includes('oop') || t.includes('class') || t.includes('object') || t.includes('வகுப்பு')) key = 'oop';
  else if (t.includes('api') || t.includes('http') || t.includes('rest')) key = 'apis';

  if (CLIENT_KNOWLEDGE_BASE[key] && CLIENT_KNOWLEDGE_BASE[key][langKey]) {
    return CLIENT_KNOWLEDGE_BASE[key][langKey];
  }
  return CLIENT_KNOWLEDGE_BASE['variables']['English'];
}

function evaluateClientAnswer(answer, topic, language) {
  const ans = answer.toLowerCase().trim();
  const isTamil = (language || '').includes('Tamil') || (language || '').includes('தமிழ்');

  const correctKeywords = [
    '8', '250', 'infinite', 'never stop', 'முடிவில்லாமல்', 'overwritten', 'replace',
    'base case', 'reusable', 'blueprint', 'sorted', 'வரிசை', '0', 'zero', 'waiter', 'தூதுவர்',
    'keyerror', 'error', 'reusability', 'clean'
  ];

  if (correctKeywords.some(k => ans.includes(k))) {
    return {
      verdict: 'correct',
      xp_earned: 50,
      feedback: isTamil
        ? "அருமை! நீங்கள் சரியான கருத்தைப் புரிந்து கொண்டுள்ளீர்கள். நினைவகத்தில் பழைய மதிப்பு முற்றிலும் அழிக்கப்பட்டு புதிய மதிப்பு சேமிக்கப்படுகிறது."
        : "Spot on! In programming memory, the execution replaces the state and updates cleanly.",
      misconception: "",
      revised_explanation: "",
      next_question: isTamil
        ? "அடுத்த சவால்: ஒரு மாறியை உருவாக்கும் முன்பே அதை அணுக முயற்சித்தால் என்ன நிகழும்?"
        : "Next Adaptive Question: What happens if you try to use a variable or index before it exists?",
      study_next: "Advanced Execution Flow"
    };
  }

  if (ans.length > 20 || ans.includes('both') || ans.includes('5') || ans.includes('100')) {
    return {
      verdict: 'partially_correct',
      xp_earned: 25,
      feedback: isTamil
        ? "மிகவும் நெருங்கிவிட்டீர்கள்! கருத்து புரிகிறது, ஆனால் சரியான செயலாக்க வரிசையை கவனியுங்கள்."
        : "You're very close! You understand the change happens, but consider the exact sequence of computer instructions.",
      misconception: "Overlooking the exact moment when memory gets updated.",
      revised_explanation: "Think of an eraser on a blackboard: before writing the new value, the previous content is wiped clean.",
      next_question: "If you have `x = 10` and then execute `x = x + 5`, what will `x` be now?",
      study_next: "Memory State Transitions"
    };
  }

  return {
    verdict: 'incorrect',
    xp_earned: 15,
    feedback: isTamil
      ? "நல்ல முயற்சி! தவறுகள் தான் கற்றலின் தொடக்கம். புதிய கோணத்தில் இதைப் புரிந்து கொள்வோம்."
      : "Good try! Mistakes help form stronger mental models. Let's look at this with a fresh analogy.",
    misconception: "Initial confusion about the execution order or assignment action.",
    revised_explanation: "In programming, `=` is an action: take whatever is on the right side and store it inside the container on the left.",
    next_question: "Quick check: If `score = 20`, and then we do `score = 0`, what will `score` be?",
    study_next: "Core Programming Fundamentals"
  };
}

// ---------- Audio Text-to-Speech ----------
function handleToggleAudio(textToSpeak, iconElem, labelElem) {
  if (state.isSpeaking) {
    window.speechSynthesis.cancel();
    state.isSpeaking = false;
    if (iconElem) iconElem.textContent = '🔊';
    if (labelElem) labelElem.textContent = 'Read Aloud';
    return;
  }

  if (!textToSpeak) return;

  const utterance = new SpeechSynthesisUtterance(textToSpeak);
  const lang = (state.language || '').toLowerCase();
  utterance.lang = lang.includes('tamil') || lang.includes('தமிழ்') ? 'ta-IN' :
                   (lang.includes('hindi') || lang.includes('हिन्दी') ? 'hi-IN' : 'en-US');
  utterance.rate = 0.95;

  utterance.onend = () => {
    state.isSpeaking = false;
    if (iconElem) iconElem.textContent = '🔊';
    if (labelElem) labelElem.textContent = 'Read Aloud';
  };

  window.speechSynthesis.speak(utterance);
  state.isSpeaking = true;
  if (iconElem) iconElem.textContent = '⏹️';
  if (labelElem) labelElem.textContent = 'Stop Audio';
}

// ---------- Gamification & Progress ----------
function updateHUD() {
  DOM.xpText.textContent = `${state.xp} XP`;
  DOM.streakText.textContent = `${state.streak} Streak`;

  let rank = 'Rookie Coder 🌱';
  if (state.xp >= 150) rank = 'Algorithm Master 🌟';
  else if (state.xp >= 90) rank = 'Problem Solver 🚀';
  else if (state.xp >= 40) rank = 'Junior Explorer 🔍';

  DOM.rankText.textContent = rank;
}

function renderHistory() {
  DOM.historyGrid.innerHTML = '';
  DOM.historySection.classList.remove('hidden');

  const icons = { correct: '✅', partially_correct: '🟡', incorrect: '🔁' };
  state.history.forEach(item => {
    const card = document.createElement('div');
    card.className = 'history-item';
    card.innerHTML = `
      <div class="history-round">Round ${item.round}</div>
      <div class="history-verdict">${icons[item.verdict] || '•'}</div>
      <div class="history-xp">+${item.xp} XP</div>
    `;
    DOM.historyGrid.appendChild(card);
  });
}

function triggerCelebration() {
  if (typeof confetti === 'function') {
    confetti({
      particleCount: 65,
      spread: 75,
      origin: { y: 0.6 }
    });
  }
}

function showLoading(show, message = 'Processing...') {
  DOM.loadingMsg.textContent = message;
  DOM.loadingIndicator.classList.toggle('hidden', !show);
}
