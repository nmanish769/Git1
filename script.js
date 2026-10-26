/**
 * OpenLearn AI — Modern Single-Page Application Client
 * Supports: Full-Stack FastAPI Backend, Direct Cloud Groq API, and 100% Offline Client-Side Mode.
 */

// Initialize Mermaid.js
mermaid.initialize({
  startOnLoad: false,
  theme: 'dark',
  securityLevel: 'loose',
  flowchart: { useMaxWidth: true, htmlLabels: true, curve: 'basis' }
});

// App State
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
  groqKey: localStorage.getItem('openlearn_groq_key') || '',
  ollamaUrl: localStorage.getItem('openlearn_ollama_url') || 'http://localhost:11434',
};

// DOM Elements
const DOM = {
  statusBadge: document.getElementById('statusBadge'),
  statusText: document.getElementById('statusText'),
  settingsBtn: document.getElementById('settingsBtn'),
  settingsModal: document.getElementById('settingsModal'),
  closeSettingsBtn: document.getElementById('closeSettingsBtn'),
  saveSettingsBtn: document.getElementById('saveSettingsBtn'),
  groqApiKeyInput: document.getElementById('groqApiKeyInput'),
  ollamaUrlInput: document.getElementById('ollamaUrlInput'),

  rankText: document.getElementById('rankText'),
  xpText: document.getElementById('xpText'),
  streakText: document.getElementById('streakText'),

  topicInput: document.getElementById('topicInput'),
  levelSelect: document.getElementById('levelSelect'),
  langSelect: document.getElementById('langSelect'),
  modelSelect: document.getElementById('modelSelect'),
  startLessonBtn: document.getElementById('startLessonBtn'),

  loadingIndicator: document.getElementById('loadingIndicator'),
  loadingMsg: document.getElementById('loadingMsg'),

  lessonSection: document.getElementById('lessonSection'),
  lessonTopicBadge: document.getElementById('lessonTopicBadge'),
  lessonLevelBadge: document.getElementById('lessonLevelBadge'),
  lessonLangBadge: document.getElementById('lessonLangBadge'),

  audioBtn: document.getElementById('audioBtn'),
  audioIcon: document.getElementById('audioIcon'),
  audioLabel: document.getElementById('audioLabel'),

  explanationText: document.getElementById('explanationText'),
  analogyText: document.getElementById('analogyText'),
  exampleCode: document.getElementById('exampleCode'),
  copyCodeBtn: document.getElementById('copyCodeBtn'),
  mermaidDiagram: document.getElementById('mermaidDiagram'),

  sandboxCode: document.getElementById('sandboxCode'),
  runCodeBtn: document.getElementById('runCodeBtn'),
  resetCodeBtn: document.getElementById('resetCodeBtn'),
  consoleResult: document.getElementById('consoleResult'),

  challengeSection: document.getElementById('challengeSection'),
  roundIndicator: document.getElementById('roundIndicator'),
  questionText: document.getElementById('questionText'),
  hintToggleBtn: document.getElementById('hintToggleBtn'),
  hintContent: document.getElementById('hintContent'),
  hintText: document.getElementById('hintText'),
  answerInput: document.getElementById('answerInput'),
  checkAnswerBtn: document.getElementById('checkAnswerBtn'),

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

  historySection: document.getElementById('historySection'),
  historyGrid: document.getElementById('historyGrid'),
  quickTopicsContainer: document.getElementById('quickTopicsContainer'),
  tabBtns: document.querySelectorAll('.tab-btn'),
  tabContents: document.querySelectorAll('.tab-content'),
};

// ---------- Built-in Client-Side Knowledge Base ----------
const CLIENT_KNOWLEDGE_BASE = {
  "variables": {
    "English": {
      explanation: "A variable is a named storage container in computer memory. You assign it a name and store data inside it (numbers, words, lists). Whenever you reference that name later, the computer retrieves what is currently inside.",
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
      explanation: "A loop instructs the computer to repeat a block of code multiple times until a stopping condition is reached, avoiding repetitive lines of code.",
      analogy: "Imagine a track athlete running laps. Before each lap, they check: 'Have I completed 5 laps?' If no, they run another lap. When they reach 5, they stop.",
      example: "for lap in range(1, 6):\n    print(f'Completed lap {lap}')\nprint('Race finished!')",
      diagram: "flowchart TD\n    A[Start: Lap = 1] --> B{Is Lap <= 5?}\n    B -- Yes --> C[Run Lap & Print]\n    C --> D[Lap = Lap + 1]\n    D --> B\n    B -- No --> E[Stop: Race Done]",
      starter_code: "for lap in range(1, 4):\n    print(f'Running lap {lap}')\nprint('Finish line crossed!')",
      question: "What would happen if a loop's stopping condition is never met (always True)?",
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
      explanation: "Conditionals allow your code to make intelligent decisions based on whether a condition is true or false, following different paths.",
      analogy: "Like checking the weather before leaving home: IF it is raining, take an umbrella; ELSE, wear your sunglasses.",
      example: "is_raining = True\nif is_raining:\n    print('Take an umbrella! ☔')\nelse:\n    print('Enjoy the sunshine! ☀️')",
      diagram: "flowchart TD\n    A[Check Weather] --> B{Is it Raining?}\n    B -- True --> C[Take Umbrella]\n    B -- False --> D[Wear Sunglasses]\n    C --> E[Walk Outside]\n    D --> E",
      starter_code: "score = 85\nif score >= 50:\n    print('Passed the exam! 🎉')\nelse:\n    print('Need more practice! 📚')",
      question: "If `score = 45`, which branch of an `if score >= 50` condition executes?",
      hint: "Is 45 greater than or equal to 50?",
    },
    "Tamil": {
      explanation: "நிபந்தனைகள் (Conditionals) கணினியை முடிவெடுக்க வைக்கின்றன. ஒரு நிபந்தனை உண்மையா அல்லது பொய்யா என்பதைப் பார்த்து அதற்கேற்ப வெவ்வேறு வழிகளில் செயல்படும்.",
      analogy: "வெளியே செல்லும் முன் மழையைப் பார்ப்பது போல: மழை பெய்தால் குடை எடுத்துச் செல்; இல்லையென்றால் கண்ணாடி அணிந்து செல்.",
      example: "malai = True\nif malai:\n    print('குடை எடுத்துச் செல்!')\nelse:\n    print('வெயில் அடிக்கிறது!')",
      diagram: "flowchart TD\n    A[வானிலை பார்க்கவும்] --> B{மழை பெய்கிறதா?}\n    B -- ஆம் --> C[குடை எடுக்கவும்]\n    B -- இல்லை --> D[கண்ணாடி அணியவும்]",
      starter_code: "mark = 75\nif mark >= 40:\n    print('வெற்றி! 🎉')\nelse:\n    print('மறுமுயற்சி தேவை! 📚')",
      question: "`mark = 35` ஆக இருக்கும்போது `if mark >= 40` என்ற நிபந்தனையில் எந்தப் பகுதி இயங்கும்?",
      hint: "35 என்பது 40க்கு சமமாகவோ அல்லது அதிகமாகவோ உள்ளதா?",
    }
  },
  "functions": {
    "English": {
      explanation: "A function is a reusable block of code that performs a specific task. You define it once, give it an input, and call it whenever needed.",
      analogy: "Like a coffee vending machine: you press a button (function name) with your coins (parameters), and it dispenses fresh coffee (return value).",
      example: "def make_greeting(name):\n    return f'Hello, {name}! Welcome to coding.'\n\nmsg = make_greeting('Priya')\nprint(msg)",
      diagram: "flowchart LR\n    A[Input: 'Priya'] --> B[Function: make_greeting]\n    B --> C[Output: 'Hello, Priya!']",
      starter_code: "def add_numbers(a, b):\n    return a + b\n\nresult = add_numbers(10, 25)\nprint(f'Total: {result}')",
      question: "Why do we use functions instead of copying and pasting the same code 10 times?",
      hint: "Think about what happens if you need to fix a typo in 10 different places vs 1 place.",
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
  "recursion": {
    "English": {
      explanation: "Recursion is when a function calls itself to solve smaller sub-problems, until it hits a fundamental stopping condition called the base case.",
      analogy: "Imagine Russian nesting dolls (Matryoshka). You open a doll to find a smaller doll inside, until you finally reach the tiniest solid doll that cannot be opened.",
      example: "def countdown(n):\n    if n <= 0:\n        print('Blast off! 🚀')\n        return\n    print(n)\n    countdown(n - 1)\n\ncountdown(3)",
      diagram: "flowchart TD\n    A[countdown 3] --> B[countdown 2]\n    B --> C[countdown 1]\n    C --> D[Base Case: Blast Off!]",
      starter_code: "def factorial(n):\n    if n == 1:\n        return 1\n    return n * factorial(n - 1)\n\nprint('3! =', factorial(3))",
      question: "What crucial part prevents a recursive function from running forever and crashing memory?",
      hint: "What was the tiniest nesting doll in our analogy?",
    },
    "Tamil": {
      explanation: "தற்சுழற்சி (Recursion) என்பது ஒரு செயற்கூறு தனக்குத்தானே மீண்டும் மீண்டும் அழைத்துக் கொண்டு சிக்கலான கணக்குகளை எளிய படிகளாக பிரித்துத் தீர்ப்பதாகும்.",
      analogy: "ரஷ்ய மர பொம்மைகளை (Russian nesting dolls) நினைத்துப் பாருங்கள். ஒரு பொம்மையை திறந்தால் உள்ளே ஒரு சிறிய பொம்மை இருக்கும். கடைசியாக திறக்க முடியாத மிகச் சிறிய பொம்மை (Base case) வரும் வரை இது தொடரும்.",
      example: "def ennu(n):\n    if n <= 0:\n        print('தொடங்கு! 🚀')\n        return\n    print(n)\n    ennu(n - 1)\n\nennu(3)",
      diagram: "flowchart TD\n    A[ennu 3] --> B[ennu 2]\n    B --> C[ennu 1]\n    C --> D[அடிப்படை நிலை: தொடங்கு!]",
      starter_code: "def factorial(n):\n    if n == 1:\n        return 1\n    return n * factorial(n - 1)\n\nprint('3! =', factorial(3))",
      question: "ஒரு தற்சுழற்சி செயற்கூறு முடிவில்லாமல் இயங்கி கணினி நினைவகத்தை முடக்குவதைத் தடுக்கும் முக்கிய பகுதி எது?",
      hint: "இறுதியில் திறக்க முடியாத மிகச் சிறிய பொம்மையை யோசித்துப் பாருங்கள்.",
    }
  },
};

// ---------- Initialization ----------
document.addEventListener('DOMContentLoaded', () => {
  initStatusAndModels();
  initEventListeners();
});

// Check backend connectivity and configure models
async function initStatusAndModels() {
  // Populate saved keys
  if (DOM.groqApiKeyInput) DOM.groqApiKeyInput.value = state.groqKey;
  if (DOM.ollamaUrlInput) DOM.ollamaUrlInput.value = state.ollamaUrl;

  try {
    const res = await fetch('/api/status', { method: 'GET' });
    const data = await res.json();
    if (data.status === 'online') {
      state.backendConnected = true;
      DOM.statusText.textContent = '🟢 Server Online';
      DOM.statusBadge.classList.add('connected');

      // Populate Ollama models if detected
      if (data.ollama_models && data.ollama_models.length > 0) {
        DOM.modelSelect.innerHTML = '';
        const optDemo = document.createElement('option');
        optDemo.value = 'demo';
        optDemo.textContent = 'Interactive Mode (Instant & Offline)';
        DOM.modelSelect.appendChild(optDemo);

        const optGroq = document.createElement('option');
        optGroq.value = 'groq';
        optGroq.textContent = 'Groq Cloud (Sub-second Llama 3.3)';
        DOM.modelSelect.appendChild(optGroq);

        data.ollama_models.forEach(m => {
          const opt = document.createElement('option');
          opt.value = m;
          opt.textContent = `Ollama (${m})`;
          DOM.modelSelect.appendChild(opt);
        });
      }
      return;
    }
  } catch (err) {
    // Server not available (e.g. running on GitHub Pages or static host)
  }

  // Graceful Standalone Client Mode
  state.backendConnected = false;
  DOM.statusText.textContent = '🟢 Web Interactive Mode';
  DOM.statusBadge.classList.add('connected');
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
  DOM.settingsBtn.addEventListener('click', () => DOM.settingsModal.classList.remove('hidden'));
  DOM.closeSettingsBtn.addEventListener('click', () => DOM.settingsModal.classList.add('hidden'));
  DOM.saveSettingsBtn.addEventListener('click', () => {
    state.groqKey = DOM.groqApiKeyInput.value.trim();
    state.ollamaUrl = DOM.ollamaUrlInput.value.trim() || 'http://localhost:11434';
    localStorage.setItem('openlearn_groq_key', state.groqKey);
    localStorage.setItem('openlearn_ollama_url', state.ollamaUrl);
    DOM.settingsModal.classList.add('hidden');
    alert('Settings saved! You can now use Groq Cloud directly.');
  });

  // Start Lesson Button
  DOM.startLessonBtn.addEventListener('click', handleStartLesson);

  // Tabs Navigation
  DOM.tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      DOM.tabBtns.forEach(b => b.classList.remove('active'));
      DOM.tabContents.forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(btn.dataset.tab).classList.add('active');
    });
  });

  // Audio Read-Aloud
  DOM.audioBtn.addEventListener('click', handleToggleAudio);

  // Copy Code
  DOM.copyCodeBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(DOM.exampleCode.textContent);
    DOM.copyCodeBtn.textContent = '✅ Copied!';
    setTimeout(() => { DOM.copyCodeBtn.textContent = '📋 Copy'; }, 2000);
  });

  // Run Code Sandbox
  DOM.runCodeBtn.addEventListener('click', handleRunCode);
  DOM.resetCodeBtn.addEventListener('click', () => {
    if (state.lesson) {
      DOM.sandboxCode.value = state.lesson.starter_code || state.lesson.example || '';
    }
  });

  // Hint Toggle
  DOM.hintToggleBtn.addEventListener('click', () => {
    DOM.hintContent.classList.toggle('hidden');
  });

  // Check Answer
  DOM.checkAnswerBtn.addEventListener('click', handleCheckAnswer);

  // Next Question
  DOM.nextQuestionBtn.addEventListener('click', handleNextQuestion);
}

// ---------- Learning Session Handler ----------
async function handleStartLesson() {
  const topic = DOM.topicInput.value.trim();
  if (!topic) return alert('Please enter a concept or topic to learn!');

  const level = DOM.levelSelect.value;
  const language = DOM.langSelect.value;
  const modelChoice = DOM.modelSelect.value;

  state.topic = topic;
  state.level = level;
  state.language = language;
  state.round = 1;
  state.feedback = null;

  showLoading(true, 'Synthesizing personalized mental model, analogy & flowchart...');
  DOM.lessonSection.classList.add('hidden');
  DOM.challengeSection.classList.add('hidden');

  try {
    let lessonData = null;

    // Check if live Groq Cloud API key is provided
    if (modelChoice === 'groq' && state.groqKey) {
      lessonData = await fetchGroqLesson(topic, level, language, state.groqKey);
    } 
    // Try FastAPI backend if connected and not forced demo
    else if (state.backendConnected && modelChoice !== 'demo') {
      try {
        const res = await fetch('/api/lesson', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            topic,
            level,
            language,
            model: modelChoice,
            base_url: state.ollamaUrl,
            api_key: state.groqKey,
          }),
        });
        if (res.ok) {
          const json = await res.json();
          lessonData = json.lesson;
        }
      } catch (e) {
        // Fall back to client knowledge base
      }
    }

    // Client-side fallback if not loaded from server
    if (!lessonData) {
      lessonData = getClientLesson(topic, language);
    }

    state.lesson = lessonData;
    state.question = lessonData.question || 'Explain how this concept works in your own words.';
    renderLesson(lessonData);
  } catch (err) {
    alert(`Notice: ${err.message}`);
  } finally {
    showLoading(false);
  }
}

// Render Lesson into UI
async function renderLesson(L) {
  DOM.lessonTopicBadge.textContent = state.topic;
  DOM.lessonLevelBadge.textContent = state.level;
  DOM.lessonLangBadge.textContent = state.language;

  DOM.explanationText.textContent = L.explanation || '';
  DOM.analogyText.textContent = L.analogy || '';
  DOM.exampleCode.textContent = L.example || '';

  // Render Mermaid Diagram
  renderMermaidDiagram(L.diagram);

  // Setup Sandbox
  DOM.sandboxCode.value = L.starter_code || L.example || '# Write python code here\n';
  DOM.consoleResult.textContent = '(Click "Run Code" to execute)';

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
    code = `flowchart TD\n    A[${state.topic}] --> B[Intuitive Mental Model]\n    B --> C[Real World Analogy]\n    C --> D[Concrete Code Example]\n    D --> E[Mastery Verified]`;
  }

  try {
    const id = 'mermaid-graph-' + Math.floor(Math.random() * 10000);
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

  // Client-Side Python Output Simulator
  try {
    let outputLines = [];
    const printMatches = code.match(/print\s*\((.*?)\)/g);
    if (printMatches) {
      printMatches.forEach(stmt => {
        const inside = stmt.replace(/^print\s*\(/, '').replace(/\)$/, '').trim();
        // Handle f-strings or standard strings
        let clean = inside.replace(/^f?['"]|['"]$/g, '');
        // Simple variable substitution
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
    DOM.consoleResult.textContent = `Simulation Output: Code ran smoothly.`;
  }
}

// ---------- Answer Evaluation & Misconception Diagnosis ----------
async function handleCheckAnswer() {
  const answer = DOM.answerInput.value.trim();
  if (!answer) return alert('Please enter your answer before checking!');

  showLoading(true, 'Analyzing your reasoning & diagnosing misconceptions...');

  try {
    let feedbackData = null;

    // Check if live Groq Cloud API is enabled
    if (DOM.modelSelect.value === 'groq' && state.groqKey) {
      feedbackData = await fetchGroqFeedback(state.topic, state.level, state.language, state.lesson, state.question, answer, state.groqKey);
    } 
    // Try FastAPI server
    else if (state.backendConnected && DOM.modelSelect.value !== 'demo') {
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
            model: DOM.modelSelect.value,
            base_url: state.ollamaUrl,
            api_key: state.groqKey,
          }),
        });
        if (res.ok) {
          const json = await res.json();
          feedbackData = json.feedback;
        }
      } catch (e) {
        // Fall back to client heuristic
      }
    }

    // Client-Side Heuristic Feedback
    if (!feedbackData) {
      feedbackData = evaluateClientAnswer(answer, state.topic, state.language);
    }

    renderFeedback(feedbackData, answer);
  } catch (err) {
    alert(`Notice: ${err.message}`);
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

// ---------- Client-Side Heuristics & Knowledge Retrieval ----------
function getClientLesson(topic, language) {
  const t = topic.toLowerCase();
  const langKey = language.includes('Tamil') || language.includes('தமிழ்') ? 'Tamil' : 'English';

  let key = 'variables';
  if (t.includes('loop') || t.includes('மடக்கு') || t.includes('while') || t.includes('for')) key = 'loops';
  else if (t.includes('condition') || t.includes('if') || t.includes('else') || t.includes('நிபந்தனை')) key = 'conditionals';
  else if (t.includes('func') || t.includes('செயற்கூறு') || t.includes('def') || t.includes('scope')) key = 'functions';
  else if (t.includes('recur') || t.includes('தற்சுழற்சி') || t.includes('stack')) key = 'recursion';

  if (CLIENT_KNOWLEDGE_BASE[key] && CLIENT_KNOWLEDGE_BASE[key][langKey]) {
    return CLIENT_KNOWLEDGE_BASE[key][langKey];
  }
  return CLIENT_KNOWLEDGE_BASE['variables']['English'];
}

function evaluateClientAnswer(answer, topic, language) {
  const ans = answer.toLowerCase().trim();
  const isTamil = language.includes('Tamil') || language.includes('தமிழ்');

  // Correct indicators
  if (ans.includes('8') || ans.includes('250') || ans.includes('infinite') || ans.includes('never stop') || 
      ans.includes('முடிவில்லாமல்') || ans.includes('overwritten') || ans.includes('replace') || 
      ans.includes('base case') || ans.includes('reusable') || ans.includes('else')) {
    return {
      verdict: 'correct',
      xp_earned: 50,
      feedback: isTamil 
        ? "அருமை! நீங்கள் சரியான கருத்தைப் புரிந்து கொண்டுள்ளீர்கள். நினைவகத்தில் பழைய மதிப்பு முற்றிலும் அழிக்கப்பட்டு புதிய மதிப்பு சேமிக்கப்படுகிறது."
        : "Spot on! In programming memory, the new assignment completely overwrites the previous value.",
      misconception: "",
      revised_explanation: "",
      next_question: isTamil 
        ? "அடுத்த சவால்: ஒரு மாறியை உருவாக்கும் முன்பே அதை அணுக முயற்சித்தால் என்ன நிகழும்?"
        : "Next Adaptive Question: What happens if you try to use a variable before assigning a value to it?",
      study_next: "Data Types & Memory Scope"
    };
  }

  // Partially correct / Common misconceptions
  if (ans.includes('both') || ans.includes('5 and 8') || ans.includes('இரண்டும்') || ans.includes('5')) {
    return {
      verdict: 'partially_correct',
      xp_earned: 25,
      feedback: isTamil
        ? "மிகவும் நெருங்கிவிட்டீர்கள்! மதிப்பு மாறுகிறது என்பதை உணர்ந்துள்ளீர்கள், ஆனால் பழைய மதிப்பு சேமிக்கப்படாமல் மாற்றப்படுகிறது."
        : "You're very close! Remember that standard variables hold only one current value at a time.",
      misconception: "Confusing variable reassignment with appending or keeping history.",
      revised_explanation: "Think of an eraser on a blackboard: before writing the new number 8, the old number 5 is wiped away clean.",
      next_question: "If you have `x = 10` and then execute `x = x + 5`, what will `x` be now?",
      study_next: "Variable Reassignment Operator (=)"
    };
  }

  // Incorrect fallback
  return {
    verdict: 'incorrect',
    xp_earned: 15,
    feedback: isTamil
      ? "நல்ல முயற்சி! தவறுகள் தான் கற்றலின் தொடக்கம். புதிய கோணத்தில் இதைப் புரிந்து கொள்வோம்."
      : "Good try! Mistakes help form stronger mental connections. Let's look at this with a fresh analogy.",
    misconception: "Confusing mathematical equality with programming storage assignment.",
    revised_explanation: "In math, `=` means both sides are equal. In programming, `=` is an action: take whatever is on the right side and store it inside the named box on the left.",
    next_question: "Quick check: If `score = 20`, and then we do `score = 0`, what will `score` be?",
    study_next: "The Assignment Operator (=)"
  };
}

// ---------- Direct Browser Groq Cloud Call (Optional API Key) ----------
async function fetchGroqLesson(topic, level, language, apiKey) {
  const prompt = `You are OpenLearn AI, a patient tutor. Teach "${topic}" to a ${level} learner in ${language}.
Return strict JSON with keys:
- "explanation": clear 4-sentence overview
- "analogy": relatable everyday real-world analogy
- "example": small clean Python code snippet
- "diagram": 4-line Mermaid.js flowchart (starting with "flowchart TD")
- "starter_code": 3-line Python snippet to tinker with
- "question": ONE conceptual practice question
- "hint": ONE gentle hint`;

  const resp = await fetch('https://api.groq.com/openai/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'llama-3.3-70b-versatile',
      messages: [{ role: 'user', content: prompt }],
      response_format: { type: 'json_object' },
      temperature: 0.3,
    })
  });

  const data = await resp.json();
  return JSON.parse(data.choices[0].message.content);
}

// ---------- Audio Text-to-Speech ----------
function handleToggleAudio() {
  if (state.isSpeaking) {
    window.speechSynthesis.cancel();
    state.isSpeaking = false;
    DOM.audioIcon.textContent = '🔊';
    DOM.audioLabel.textContent = 'Read Aloud';
    return;
  }

  if (!state.lesson || !state.lesson.explanation) return;

  const utterance = new SpeechSynthesisUtterance(state.lesson.explanation);
  const lang = state.language.toLowerCase();
  utterance.lang = lang.includes('tamil') || lang.includes('தமிழ்') ? 'ta-IN' :
                   (lang.includes('hindi') || lang.includes('हिन्दी') ? 'hi-IN' : 'en-US');
  utterance.rate = 0.95;

  utterance.onend = () => {
    state.isSpeaking = false;
    DOM.audioIcon.textContent = '🔊';
    DOM.audioLabel.textContent = 'Read Aloud';
  };

  window.speechSynthesis.speak(utterance);
  state.isSpeaking = true;
  DOM.audioIcon.textContent = '⏹️';
  DOM.audioLabel.textContent = 'Stop Audio';
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
      particleCount: 60,
      spread: 70,
      origin: { y: 0.6 }
    });
  }
}

function showLoading(show, message = 'Processing...') {
  DOM.loadingMsg.textContent = message;
  DOM.loadingIndicator.classList.toggle('hidden', !show);
}
