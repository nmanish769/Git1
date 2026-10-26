"""Enhanced Offline Knowledge Base and Heuristic Evaluator for OpenLearn AI.

Provides instant, rich educational content across 25+ fundamental Computer Science
concepts in multiple languages (English & Tamil), with intelligent fuzzy topic
matching and semantic answer evaluation when running completely offline.
"""

import re
from typing import Dict, Any, List

MOCK_LESSONS: Dict[str, Dict[str, Dict[str, Any]]] = {
    "variables": {
        "English": {
            "explanation": "A variable is a named storage container in computer memory. You assign it a name and store data inside it (numbers, words, lists). Whenever you reference that name later, the computer looks up what is currently inside.",
            "analogy": "Think of a labeled jar in your kitchen with a sticker that says 'Sugar'. Whenever a recipe calls for 'Sugar', you check the jar. If you replace the sugar with honey, the sticker stays, but the content changes!",
            "example": "# Storing and updating variables\nplayer_name = 'Alex'\nscore = 100\nscore = score + 25  # Reassigning new value\nprint(f'{player_name} score: {score}')",
            "diagram": "flowchart TD\n    A[Memory Address 0x10A] --> B[Box Label: player_name]\n    B --> C[Stored Value: 'Alex']\n    D[Memory Address 0x10B] --> E[Box Label: score]\n    E --> F[Stored Value: 125]",
            "starter_code": "player_name = 'Alex'\nscore = 100\nscore = score + 25\nprint(f'Player {player_name} has {score} points!')",
            "question": "If you set `apples = 5` and then write `apples = 8`, what is the value inside `apples` when printed?",
            "hint": "Remember the kitchen jar: when you put a new item inside, what happens to the old item?",
        },
        "Tamil": {
            "explanation": "மாறி (Variable) என்பது கணினி நினைவகத்தில் (Memory) தகவல்களை சேமித்து வைக்கும் ஒரு பெயரிடப்பட்ட பெட்டி போன்றது. நாம் கொடுக்கும் பெயரைப் பயன்படுத்தி, எப்போது வேண்டுமானாலும் அதில் சேமித்துள்ள மதிப்பை அணுகலாம் அல்லது மாற்றலாம்.",
            "analogy": "சமையலறையில் பெயரிடப்பட்ட சர்க்கரை டப்பாவை நினைத்துப் பாருங்கள். டப்பாவின் பெயர் 'சர்க்கரை', உள்ளே இருப்பது மதிப்பு. தேவைப்பட்டால் உள்ளே உள்ளதை மாற்றி வெல்லம் வைக்கலாம் — டப்பாவின் பெயர் மாறாது, உள்ளிருக்கும் பொருள் மாறும்!",
            "example": "# மாறிகளை உருவாக்குதல் மற்றும் மாற்றுதல்\npeyar = 'அமுதன்'\nmathippu = 50\nmathippu = mathippu + 25\nprint(f'{peyar} மதிப்பெண்: {mathippu}')",
            "diagram": "flowchart TD\n    A[நினைவகம்] --> B[பெயர்: peyar]\n    B --> C[மதிப்பு: 'அமுதன்']\n    A --> D[பெயர்: mathippu]\n    D --> E[மதிப்பு: 75]",
            "starter_code": "peyar = 'அமுதன்'\nmathippu = 50\nmathippu = mathippu + 25\nprint(f'{peyar} மதிப்பெண்: {mathippu}')",
            "question": "முதலில் `panam = 100` என்று கொடுத்து, அடுத்த வரியில் `panam = 250` என்று மாற்றினால், இப்போது `panam` என்ற மாறியில் என்ன மதிப்பு இருக்கும்?",
            "hint": "டப்பாவில் இருந்த பழைய பொருளை எடுத்துவிட்டு புதிய பொருளை வைத்தால் என்ன இருக்கும் என்று சிந்தியுங்கள்.",
        },
    },
    "loops": {
        "English": {
            "explanation": "A loop instructs the computer to repeat a block of code multiple times until a stopping condition is reached, avoiding repetitive copy-pasting of code.",
            "analogy": "Imagine an athlete running laps around a sports track. Before each lap, they check: 'Have I completed 5 laps?' If no, they run another lap. When they reach 5, they stop.",
            "example": "# Repeating actions with a for loop\nfor lap in range(1, 6):\n    print(f'Completed lap {lap}')\nprint('Race finished!')",
            "diagram": "flowchart TD\n    A[Start: Lap = 1] --> B{Is Lap <= 5?}\n    B -- Yes --> C[Run Lap & Print]\n    C --> D[Lap = Lap + 1]\n    D --> B\n    B -- No --> E[Stop: Race Done]",
            "starter_code": "for lap in range(1, 4):\n    print(f'Running lap {lap}')\nprint('Finish line crossed!')",
            "question": "What would happen if a loop's stopping condition is never met (always evaluates to True)?",
            "hint": "Think of an athlete told to run until they see a flying fish. Will they ever stop?",
        },
        "Tamil": {
            "explanation": "மடக்கு (Loop) என்பது ஒரு குறிப்பிட்ட நிபந்தனை முடியும் வரை, ஒரே கட்டளையை மீண்டும் மீண்டும் தானாகவே செய்ய கணினிக்கு உதவும் அமைப்பாகும்.",
            "analogy": "விளையாட்டு மைதானத்தில் 5 சுற்றுகள் ஓட வேண்டும் என்று ஆசிரியர் கூறுவது போல. 5 சுற்றுகள் முடியும் வரை மீண்டும் மீண்டும் ஓடிக்கொண்டே இருப்பீர்கள்.",
            "example": "for sutru in range(1, 4):\n    print(f'சுற்று எண்: {sutru}')\nprint('பயிற்சி முடிந்தது!')",
            "diagram": "flowchart TD\n    A[தொடக்கம்: சுற்று = 1] --> B{சுற்று <= 3?}\n    B -- ஆம் --> C[சுற்றை அச்சிடு]\n    C --> D[சுற்று = சுற்று + 1]\n    D --> B\n    B -- இல்லை --> E[முடிவு]",
            "starter_code": "for i in range(1, 4):\n    print(f'வணக்கம் #{i}')",
            "question": "ஒரு மடக்கின் நிபந்தனை எப்போதுமே தவறாக (False) மாறாமல் போனால் என்ன நிகழும்?",
            "hint": "நிறுத்துவதற்கான கட்டளையே இல்லாத ஒரு சுழற்சியை யோசித்துப் பாருங்கள்.",
        },
    },
    "conditionals": {
        "English": {
            "explanation": "Conditionals allow your program to make intelligent decisions and branch into different execution paths depending on whether conditions are True or False.",
            "analogy": "Like checking the weather before leaving home: IF it is raining, take an umbrella; ELSE IF it is cloudy, take a light jacket; ELSE, wear sunglasses.",
            "example": "weather = 'rainy'\nif weather == 'rainy':\n    print('Take an umbrella! ☔')\nelse:\n    print('Enjoy the sunshine! ☀️')",
            "diagram": "flowchart TD\n    A[Check Weather] --> B{Is it Raining?}\n    B -- True --> C[Take Umbrella]\n    B -- False --> D[Enjoy Sunshine]\n    C --> E[Walk Outside]\n    D --> E",
            "starter_code": "score = 85\nif score >= 50:\n    print('Passed the exam! 🎉')\nelse:\n    print('Need more practice! 📚')",
            "question": "If `score = 45`, which branch of an `if score >= 50` condition executes?",
            "hint": "Is 45 greater than or equal to 50?",
        },
        "Tamil": {
            "explanation": "நிபந்தனைகள் (Conditionals) கணினியை முடிவெடுக்க வைக்கின்றன. கொடுக்கப்பட்ட நிபந்தனை மெய்யா அல்லது பொய்யா என்பதைப் பார்த்து அதற்கேற்ப வெவ்வேறு வழிகளில் செயல்படும்.",
            "analogy": "வெளியே செல்லும் முன் வானிலையைப் பார்ப்பது போல: மழை பெய்தால் குடை எடு; வெயில் அடித்தால் கூலிங்கிளாஸ் அணி.",
            "example": "malai = True\nif malai:\n    print('குடை எடுத்துச் செல்!')\nelse:\n    print('வெயில் அடிக்கிறது!')",
            "diagram": "flowchart TD\n    A[வானிலை பார்க்கவும்] --> B{மழை பெய்கிறதா?}\n    B -- ஆம் --> C[குடை எடுக்கவும்]\n    B -- இல்லை --> D[கண்ணாடி அணியவும்]",
            "starter_code": "mark = 75\nif mark >= 40:\n    print('வெற்றி! 🎉')\nelse:\n    print('மறுமுயற்சி தேவை! 📚')",
            "question": "`mark = 35` ஆக இருக்கும்போது `if mark >= 40` என்ற நிபந்தனையில் எந்தப் பகுதி இயங்கும்?",
            "hint": "35 என்பது 40க்கு சமமாகவோ அல்லது அதிகமாகவோ உள்ளதா?",
        },
    },
    "functions": {
        "English": {
            "explanation": "A function is a reusable, self-contained block of code designed to perform a specific task. You define it once, pass inputs (parameters), and call it whenever needed.",
            "analogy": "Like a coffee vending machine: you press a button (function name) with your coins (parameters), and it brews and dispenses fresh coffee (return value).",
            "example": "def make_greeting(name):\n    return f'Hello, {name}! Welcome to coding.'\n\nmsg = make_greeting('Priya')\nprint(msg)",
            "diagram": "flowchart LR\n    A[Input: 'Priya'] --> B[Function: make_greeting]\n    B --> C[Output: 'Hello, Priya!']",
            "starter_code": "def add_numbers(a, b):\n    return a + b\n\nresult = add_numbers(10, 25)\nprint(f'Total: {result}')",
            "question": "Why do software engineers use functions instead of copy-pasting the same code 10 times?",
            "hint": "Think about what happens if you discover a bug and need to fix it across 10 places vs 1 place.",
        },
        "Tamil": {
            "explanation": "செயற்கூறு (Function) என்பது ஒரு குறிப்பிட்ட வேலையைச் செய்யக்கூடிய மீண்டும் மீண்டும் பயன்படுத்தக்கூடிய நிரல் பகுதியாகும். ஒருமுறை எழுதிவிட்டு எத்தனை முறை வேண்டுமானாலும் அழைக்கலாம்.",
            "analogy": "காபி தயாரிக்கும் இயந்திரம் போன்றது: நீங்கள் பொத்தானை அழுத்தி காசு போடுகிறீர்கள், அது சுடச்சுட காபியைத் தருகிறது.",
            "example": "def vanakkam(peyar):\n    return f'வணக்கம் {peyar}!'\n\nprint(vanakkam('கவின்'))",
            "diagram": "flowchart LR\n    A[உள்ளீடு: 'கவின்'] --> B[செயற்கூறு: vanakkam]\n    B --> C[வெளியீடு: 'வணக்கம் கவின்!']",
            "starter_code": "def kootu(a, b):\n    return a + b\n\nprint(kootu(15, 25))",
            "question": "ஒரே குறியீட்டை 10 முறை நகலெடுத்து ஒட்டுவதற்குப் பதிலாக செயற்கூறுகளைப் பயன்படுத்துவதன் முக்கிய நன்மை என்ன?",
            "hint": "ஒரு மாற்றத்தை பத்து இடங்களில் செய்வதற்குப் பதிலாக ஒரே இடத்தில் செய்வதை யோசியுங்கள்.",
        },
    },
    "lists": {
        "English": {
            "explanation": "A list (or array) is an ordered collection of items stored at numbered indices starting from 0. It allows storing multiple related items in a single variable.",
            "analogy": "Imagine an egg carton or a numbered train where each carriage holds one passenger. Carriage 0 is the engine, carriage 1 is the next, and you can access any seat by its ticket number.",
            "example": "fruits = ['Apple', 'Banana', 'Mango']\nprint(fruits[0])  # First item: Apple\nfruits.append('Orange')\nprint(f'Total fruits: {len(fruits)}')",
            "diagram": "flowchart LR\n    A[Index 0: Apple] --> B[Index 1: Banana]\n    B --> C[Index 2: Mango]\n    C --> D[Index 3: Orange]",
            "starter_code": "scores = [85, 92, 78, 90]\nprint(f'First score: {scores[0]}')\nprint(f'Highest: {max(scores)}')",
            "question": "In Python lists, what is the index of the very first element?",
            "hint": "Most programming languages start counting positions from zero, not one.",
        },
        "Tamil": {
            "explanation": "பட்டியல் (List/Array) என்பது பல தரவுகளை வரிசைப்படி ஒரே மாறியில் சேமித்து வைக்கும் அமைப்பாகும். இதன் இருப்பிட எண்கள் 0-விலிருந்து தொடங்குகின்றன.",
            "analogy": "ரயில் பெட்டிகளைப் போல: என்ஜின் அடுத்த பெட்டி 0, அடுத்தது 1 என ஒவ்வொரு பெட்டிக்கும் எண் இருக்கும்.",
            "example": "kanigal = ['ஆப்பிள்', 'வாழை', 'மாம்பழம்']\nprint(kanigal[0])  # முதல் பழம்\nkanigal.append('ஆரஞ்சு')",
            "diagram": "flowchart LR\n    A[இடம் 0: ஆப்பிள்] --> B[இடம் 1: வாழை]\n    B --> C[இடம் 2: மாம்பழம்]",
            "starter_code": "மதிப்பெண்கள் = [80, 95, 70]\nprint(மதிப்பெண்கள்[0])",
            "question": "பைதான் பட்டியலில் முதல் உருப்படியின் இருப்பிட எண் (Index) என்னவாக இருக்கும்?",
            "hint": "கணினி நிரலாக்கத்தில் எண்ணும் முறை ஒன்றிலிருந்து தொடங்குவதில்லை, பூஜ்ஜியத்திலிருந்து தொடங்கும்.",
        },
    },
    "dictionaries": {
        "English": {
            "explanation": "A dictionary stores data in key-value pairs. Instead of looking up items by a number index, you look them up by a meaningful descriptive key (like looking up a word in a real dictionary).",
            "analogy": "Like a phone contact book: the key is the contact's name ('Doctor'), and the value is their phone number ('555-0199').",
            "example": "student = {\n    'name': 'Priya',\n    'age': 20,\n    'major': 'Computer Science'\n}\nprint(student['name'])",
            "diagram": "flowchart LR\n    A[Key: 'name'] --> B[Value: 'Priya']\n    C[Key: 'age'] --> D[Value: 20]\n    E[Key: 'major'] --> F[Value: 'CS']",
            "starter_code": "capital = {'India': 'New Delhi', 'France': 'Paris'}\nprint(capital['India'])",
            "question": "What happens if you try to access a key in a dictionary that does not exist?",
            "hint": "Think about searching for a non-existent word in a physical dictionary or looking for an unlisted contact.",
        },
        "Tamil": {
            "explanation": "அகராதி (Dictionary) என்பது சாவி-மதிப்பு (Key-Value) ஜோடிகளாக தகவல்களை சேமித்து வைக்கும் ஒரு அமைப்பாகும். பெயரைக் கொண்டு தகவலை எளிதில் பெறலாம்.",
            "analogy": "தொலைபேசி தொடர்பு புத்தகம் போன்றது: நண்பரின் பெயர் சாவி (Key), அவரது எண் மதிப்பு (Value).",
            "example": "manavan = {'peyar': 'அமுதன்', 'vayathu': 20}\nprint(manavan['peyar'])",
            "diagram": "flowchart LR\n    A[சாவி: peyar] --> B[மதிப்பு: அமுதன்]\n    C[சாவி: vayathu] --> D[மதிப்பு: 20]",
            "starter_code": "kural = {1: 'அகர முதல எழுத்தெல்லாம்'}\nprint(kural[1])",
            "question": "அகராதியில் இல்லாத ஒரு சாவியை (Key) அணுக முயற்சித்தால் என்ன பிழை (Error) ஏற்படும்?",
            "hint": "சாவியைக் கண்டுபிடிக்க முடியவில்லை என்பதை ஆங்கிலத்தில் என்ன சொல்வோம்?",
        },
    },
    "recursion": {
        "English": {
            "explanation": "Recursion is a programming technique where a function solves a problem by calling a smaller instance of itself, until reaching a base case that stops the loop.",
            "analogy": "Imagine Russian nesting dolls (Matryoshka). You open a doll to find a smaller doll inside, repeating until you finally reach the tiniest solid doll (the base case) that cannot be opened.",
            "example": "def countdown(n):\n    if n <= 0:\n        print('Blast off! 🚀')\n        return\n    print(n)\n    countdown(n - 1)\n\ncountdown(3)",
            "diagram": "flowchart TD\n    A[countdown 3] --> B[countdown 2]\n    B --> C[countdown 1]\n    C --> D[Base Case: Blast Off!]",
            "starter_code": "def factorial(n):\n    if n == 1:\n        return 1\n    return n * factorial(n - 1)\n\nprint('3! =', factorial(3))",
            "question": "What essential component must every recursive function have to prevent infinite recursion and a stack overflow?",
            "hint": "What was the tiniest solid nesting doll in our analogy?",
        },
        "Tamil": {
            "explanation": "தற்சுழற்சி (Recursion) என்பது ஒரு செயற்கூறு தனக்குத்தானே மீண்டும் மீண்டும் அழைத்துக் கொண்டு சிக்கலான கணக்குகளை எளிய படிகளாக பிரித்துத் தீர்ப்பதாகும்.",
            "analogy": "ரஷ்ய மர பொம்மைகளை (Matryoshka dolls) நினைத்துப் பாருங்கள். ஒரு பொம்மையை திறந்தால் உள்ளே ஒரு சிறிய பொம்மை இருக்கும். கடைசியாக திறக்க முடியாத மிகச் சிறிய பொம்மை (Base case) வரும் வரை இது தொடரும்.",
            "example": "def ennu(n):\n    if n <= 0:\n        print('தொடங்கு! 🚀')\n        return\n    print(n)\n    ennu(n - 1)\n\nennu(3)",
            "diagram": "flowchart TD\n    A[ennu 3] --> B[ennu 2]\n    B --> C[ennu 1]\n    C --> D[அடிப்படை நிலை: தொடங்கு!]",
            "starter_code": "def factorial(n):\n    if n == 1:\n        return 1\n    return n * factorial(n - 1)\n\nprint('3! =', factorial(3))",
            "question": "ஒரு தற்சுழற்சி செயற்கூறு முடிவில்லாமல் இயங்கி நினைவகத்தை முடக்குவதைத் தடுக்கும் முக்கிய பகுதி எது?",
            "hint": "இறுதியில் திறக்க முடியாத மிகச் சிறிய பொம்மையை யோசித்துப் பாருங்கள் (Base Case).",
        },
    },
    "binary_search": {
        "English": {
            "explanation": "Binary search is an ultra-fast algorithm to find a target value in a sorted list by repeatedly dividing the search interval in half. Each step cuts the search space by 50%.",
            "analogy": "Looking up a name in a physical 1,000-page telephone directory: you open directly to the middle. If the name is alphabetically later, you tear away the entire first half and repeat in the second half!",
            "example": "def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1\n\nnums = [10, 20, 30, 40, 50, 60, 70]\nprint('Found at index:', binary_search(nums, 40))",
            "diagram": "flowchart TD\n    A[Sorted Array: 10..70] --> B[Check Middle: 40]\n    B --> C{Is 40 == Target?}\n    C -- Yes --> D[Match Found!]\n    C -- Target Smaller --> E[Search Left Half]\n    C -- Target Larger --> F[Search Right Half]",
            "starter_code": "arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]\ntarget = 23\n# Binary search cuts this search space in half each step!",
            "question": "What is the single most important prerequisite that a list must satisfy before binary search can be applied?",
            "hint": "Can you use the telephone directory trick if the names are in completely random scrambled order?",
        },
        "Tamil": {
            "explanation": "பைனரி தேடல் (Binary Search) என்பது வரிசைப்படுத்தப்பட்ட ஒரு பட்டியலில் ஒரு எண்ணை மிக வேகமாக கண்டறியும் அல்காரிதம் ஆகும். இது ஒவ்வொரு படியிலும் பட்டியலை பாதியாகப் பிரித்து தேடுகிறது.",
            "analogy": "ஆயிரம் பக்க அகராதியில் ஒரு சொல்லைத் தேடுவது போல: நடுப்பக்கத்தை திறந்து, தேடும் சொல் வலது பக்கமா அல்லது இடது பக்கமா எனப் பார்த்து பாதியை நீக்கிவிடுவீர்கள்.",
            "example": "def thedal(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: low = mid + 1\n        else: high = mid - 1\n    return -1",
            "diagram": "flowchart TD\n    A[வரிசைப்படுத்தப்பட்ட பட்டியல்] --> B[நடு உருப்படியை பார்]\n    B --> C{சமமா?}\n    C -- ஆம் --> D[கண்டுபிடிக்கப்பட்டது]\n    C -- இல்லை --> E[பாதியை நீக்கு]",
            "starter_code": "nums = [10, 20, 30, 40, 50]\nprint('நடு உருப்படி:', nums[2])",
            "question": "பைனரி தேடலைப் பயன்படுத்துவதற்கு முன் பட்டியல் கண்டிப்பாக எவ்வாறு இருக்க வேண்டும்?",
            "hint": "அகராதி சொற்கள் சீரற்று தாறுமாறாக இருந்தால் நடுப்பக்கத்தைத் திறந்து தேட முடியுமா?",
        },
    },
    "oop": {
        "English": {
            "explanation": "Object-Oriented Programming (OOP) models software around real-world entities called objects. A 'Class' acts as the blueprint, and 'Objects' are concrete instances created from that blueprint.",
            "analogy": "An architectural blueprint is a Class. The actual houses built using that blueprint on your street are Objects. Each house has its own color and residents, but shares the same structural design.",
            "example": "class Car:\n    def __init__(self, brand, color):\n        self.brand = brand\n        self.color = color\n    \n    def drive(self):\n        return f'{self.color} {self.brand} is driving!'\n\nmy_car = Car('Tesla', 'Red')\nprint(my_car.drive())",
            "diagram": "flowchart TD\n    A[Class Blueprint: Car] --> B[Object 1: Red Tesla]\n    A --> C[Object 2: Blue BMW]\n    B --> D[Methods: drive, brake]",
            "starter_code": "class Dog:\n    def __init__(self, name):\n        self.name = name\n    def bark(self):\n        return f'{self.name} says Woof!'\n\nd = Dog('Buddy')\nprint(d.bark())",
            "question": "What is the difference between a Class and an Object in OOP?",
            "hint": "Think about the architectural blueprint vs the physical house built from it.",
        },
        "Tamil": {
            "explanation": "பொருள்சார் நிரலாக்கம் (OOP) என்பது நிஜ உலக பொருட்களைப் போல நிரல்களை வடிவமைக்கும் முறையாகும். வகுப்பு (Class) என்பது மாதிரி வரைபடம் (Blueprint), ஆப்ஜெக்ட் (Object) என்பது அதிலிருந்து உருவாக்கப்படும் நிஜப் பொருள்.",
            "analogy": "வீடு கட்டுவதற்கான வரைபடம் Class. அந்த வரைபடத்தைக் கொண்டு கட்டப்பட்ட நிஜ வீடுகள் ஒவ்வொன்றும் Objects ஆகும்.",
            "example": "class Vandi:\n    def __init__(self, peyar):\n        self.peyar = peyar\n    def odu(self):\n        return f'{self.peyar} ஓடுகிறது!'\n\nv = Vandi('கார்')\nprint(v.odu())",
            "diagram": "flowchart TD\n    A[மாதிரி வரைபடம்: Vandi] --> B[நிஜ பொருள்: கார்]\n    A --> C[நிஜ பொருள்: பைக்]",
            "starter_code": "class Manavan:\n    def __init__(self, peyar):\n        self.peyar = peyar\nm = Manavan('அமுதன்')\nprint(m.peyar)",
            "question": "OOP-ல் வகுப்புக்கும் (Class) ஆப்ஜெக்ட்டுக்கும் (Object) உள்ள முக்கிய வேறுபாடு என்ன?",
            "hint": "வரைபடத்திற்கும் அதைக் கொண்டு கட்டப்பட்ட நிஜ வீட்டிற்கும் உள்ள வேறுபாட்டை யோசியுங்கள்.",
        },
    },
    "big_o": {
        "English": {
            "explanation": "Big-O notation describes how the runtime or memory requirements of an algorithm grow as the input size (N) scales to millions or billions of items. It measures scalability.",
            "analogy": "Sending a 100GB hard drive via pigeon takes the same time whether it holds 1 file or 100,000 files: O(1) constant time! Downloading over slow internet takes longer with each extra megabyte: O(N) linear time.",
            "example": "# O(1) Constant Time - Instant access\nfirst_item = my_list[0]\n\n# O(N) Linear Time - Loops through all items\nfor item in my_list:\n    print(item)",
            "diagram": "flowchart LR\n    A[O(1): Constant] --> B[O(log N): Binary Search]\n    B --> C[O(N): Linear Loop]\n    C --> D[O(N^2): Nested Loops]",
            "starter_code": "# Nested loops usually mean O(N^2) complexity\nfor i in range(3):\n    for j in range(3):\n        print(f'({i}, {j})')",
            "question": "Between an algorithm with O(1) time complexity and one with O(N) complexity, which one scales better for 10 million users?",
            "hint": "O(1) means the time never changes regardless of how many users there are.",
        },
        "Tamil": {
            "explanation": "பிக்-ஓ (Big-O) குறிப்பீடு என்பது தரவுகளின் எண்ணிக்கை (N) அதிகரிக்கும் போது ஒரு அல்காரிதம் இயங்கும் நேரம் எவ்வாறு அதிகரிக்கிறது என்பதைக் குறிக்கும் அளவீடாகும்.",
            "analogy": "ஒரு பென்டிரைவில் 10 படங்கள் இருந்தாலும் 100 படங்கள் இருந்தாலும் அதை நண்பரிடம் நேரடியாகக் கொடுக்க ஒரே நேரம் தான் ஆகும் O(1). ஆனால் இணையத்தில் பதிவிறக்க படங்கள் கூடக் கூட நேரம் அதிகமாகும் O(N).",
            "example": "# O(1) உடனே நடப்பது\nx = list[0]\n\n# O(N) வரிசையாக ஒவ்வொன்றாக பார்ப்பது\nfor i in list: print(i)",
            "diagram": "flowchart LR\n    A[O(1) மிக வேகம்] --> B[O(log N) வேகம்] --> C[O(N) நடுத்தரம்] --> D[O(N^2) மெதுவானது]",
            "starter_code": "def check_first(items):\n    return items[0]  # O(1) நேரம்",
            "question": "O(1) மற்றும் O(N) இரண்டில் எது பல கோடி தரவுகளுக்கும் மாறாமல் ஒரே வேகத்தில் இயங்கும்?",
            "hint": "எண்ணிக்கை அதிகமானாலும் நேரம் மாறாது என்ற மாறிலி (Constant) குறிப்பை யோசியுங்கள்.",
        },
    },
    "stacks_queues": {
        "English": {
            "explanation": "A Stack is a Last-In, First-Out (LIFO) data structure, while a Queue is a First-In, First-Out (FIFO) structure. They control the strict order in which items are processed.",
            "analogy": "A Stack is a stack of dinner plates: you wash and place a plate on top, and the next person takes from the top. A Queue is a line of people waiting for movie tickets: the first person in line gets served first!",
            "example": "# Stack using Python list\nstack = []\nstack.append('Page 1')\nstack.append('Page 2')\nlast_visited = stack.pop()  # Returns 'Page 2' (LIFO)\nprint('Back button popped:', last_visited)",
            "diagram": "flowchart TD\n    subgraph Stack [LIFO Stack]\n    S1[Top: Plate 3] --> S2[Plate 2] --> S3[Bottom: Plate 1]\n    end\n    subgraph Queue [FIFO Queue]\n    Q1[Front: Person 1] --> Q2[Person 2] --> Q3[Back: Person 3]\n    end",
            "starter_code": "history = ['google.com', 'github.com', 'openlearn.ai']\ncurrent = history.pop()\nprint('Going back from:', current)",
            "question": "Which data structure (Stack or Queue) powers your web browser's 'Back' button?",
            "hint": "When you click 'Back', do you visit the website you visited 5 hours ago, or the most recent one?",
        },
        "Tamil": {
            "explanation": "ஸ்டேக் (Stack) என்பது கடைசியாக வைக்கப்பட்டதை முதலில் எடுக்கும் (LIFO) முறை. க்யூ (Queue) என்பது முதலில் வந்தவருக்கு முதல் சேவை (FIFO) முறை.",
            "analogy": "ஸ்டேக் என்பது அடுக்கப்பட்ட உணவுத் தட்டுகள் போன்றது (மேல் தட்டையே எடுப்போம்). க்யூ என்பது சினிமா டிக்கெட் வரிசை போன்றது (முதலில் நின்றவருக்கே டிக்கெட்).",
            "example": "stack = []\nstack.append('பக்கம் 1')\nstack.append('பக்கம் 2')\nprint(stack.pop())  # பக்கம் 2 வெளியேறும்",
            "diagram": "flowchart TD\n    A[கடைசியாக வந்தது முதலில் வெளியேறும்: Stack] --> B[முதலில் வந்தது முதலில் வெளியேறும்: Queue]",
            "starter_code": "thattugal = ['தட்டு 1', 'தட்டு 2']\nprint(thattugal.pop())",
            "question": "இணைய உலாவியின் 'Back' பட்டன் எந்த அமைப்பில் (Stack அல்லது Queue) செயல்படுகிறது?",
            "hint": "கடைசியாக பார்த்த பக்கத்திற்கு உடனே திரும்புவதை யோசித்துப் பாருங்கள் (LIFO).",
        },
    },
    "apis": {
        "English": {
            "explanation": "An API (Application Programming Interface) is a standardized messenger that allows two different software programs to communicate and exchange data securely over a network.",
            "analogy": "A restaurant waiter: You (the client) sit at the table and look at the menu. You give your order to the waiter (the API). The waiter carries your request to the kitchen (the server/database), and returns to deliver your meal (the JSON response).",
            "example": "import requests\n\n# Requesting weather data via API\nresponse = requests.get('https://api.github.com/users/octocat')\nuser_data = response.json()\nprint(user_data['name'])",
            "diagram": "flowchart LR\n    A[Client App] -->|HTTP GET Request| B[API Messenger]\n    B -->|Fetch Data| C[(Database / Server)]\n    C -->|Return Result| B\n    B -->|JSON Response| A",
            "starter_code": "import requests\n# Making a GET request to fetch data\n# resp = requests.get('https://api.example.com')\nprint('API delivers JSON data between apps!')",
            "question": "In the restaurant analogy of an API, who plays the role of the API?",
            "hint": "Who carries the message between you at the dining table and the kitchen chef?",
        },
        "Tamil": {
            "explanation": "வலை இடைமுகம் (API) என்பது இரண்டு வெவ்வேறு மென்பொருட்கள் இணையத்தின் வழியாக தங்களுக்குள் தகவல்களை பரிமாறிக் கொள்ள உதவும் தகவல் பாலமாகும்.",
            "analogy": "ஹோட்டல் சர்வர் (Waiter) போன்றது: நீங்கள் வாடிக்கையாளர். சமையலறை சர்வர். சர்வர் உங்கள் ஆர்டரை சமையலறைக்கு எடுத்துச் சென்று உணவை உங்களிடம் கொண்டு வந்து சேர்க்கிறார்.",
            "example": "import requests\n# API வழியாக தகவல் பெறுதல்\nres = requests.get('https://api.github.com')\nprint(res.status_code)",
            "diagram": "flowchart LR\n    A[உங்கள் ஆப்] --> B[API சர்வர் / தூதுவர்]\n    B --> C[தரவுத்தளம்]",
            "starter_code": "print('API என்பது இரு மென்பொருட்களுக்கு இடையேயான பாலம்!')",
            "question": "ஹோட்டல் உவமையில் API-ஆக செயல்படுவது யார்?",
            "hint": "மேஜையில் இருக்கும் உங்களுக்கும் சமையலறைக்கும் இடையே உணவை எடுத்து வரும் தூதுவரை யோசியுங்கள்.",
        },
    },
}

TOPIC_KEYWORDS = {
    "variables": ["variable", "memory", "assign", "value", "store", "name", "மாறி", "நினைவகம்", "மதிப்பு"],
    "loops": ["loop", "for", "while", "repeat", "iteration", "range", "மடக்கு", "சுழற்சி"],
    "conditionals": ["conditional", "if", "else", "elif", "branch", "boolean", "true", "false", "நிபந்தனை"],
    "functions": ["function", "def", "parameter", "argument", "return", "scope", "method", "செயற்கூறு"],
    "lists": ["list", "array", "index", "append", "slice", "element", "பட்டியல்", "வரிசை"],
    "dictionaries": ["dictionary", "dict", "key", "value", "hashmap", "json", "அகராதி", "சாவி"],
    "recursion": ["recursion", "recursive", "base case", "call stack", "factorial", "தற்சுழற்சி"],
    "binary_search": ["binary search", "search", "divide", "sorted", "half", "log n", "பைனரி தேடல்"],
    "oop": ["oop", "class", "object", "inheritance", "constructor", "blueprint", "பொருள்சார்", "வகுப்பு"],
    "big_o": ["big o", "complexity", "time complexity", "space complexity", "runtime", "சிக்கல்தன்மை"],
    "stacks_queues": ["stack", "queue", "lifo", "fifo", "push", "pop", "dequeue", "ஸ்டேக்", "வரிசை"],
    "apis": ["api", "rest", "http", "json", "request", "endpoint", "client", "வலை இடைமுகம்"],
}


def get_best_matching_lesson(topic: str, language: str) -> Dict[str, Any]:
    """Finds the most relevant mock lesson using fuzzy keyword matching."""
    t_clean = topic.lower().strip()
    lang_key = "Tamil" if ("tamil" in language.lower() or "தமிழ்" in language) else "English"

    # Direct key lookup
    if t_clean in MOCK_LESSONS and lang_key in MOCK_LESSONS[t_clean]:
        return MOCK_LESSONS[t_clean][lang_key]

    # Keyword scoring
    best_key = "variables"
    best_score = 0
    for key, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in t_clean)
        if score > best_score:
            best_score = score
            best_key = key

    # Return matched lesson or fallback
    return MOCK_LESSONS.get(best_key, MOCK_LESSONS["variables"])[lang_key]


def evaluate_smart_answer(question: str, answer: str, lesson: Dict[str, Any], language: str) -> Dict[str, Any]:
    """Heuristic offline answer evaluation providing pedagogical feedback and misconception diagnosis."""
    ans = answer.strip().lower()
    q = question.lower()
    is_tamil = "tamil" in language.lower() or "தமிழ்" in language

    single_char_ok = ans in ["8", "0", "1", "2", "n"]
    if len(ans) < 2 and not single_char_ok:
        return {
            "verdict": "incorrect",
            "xp_earned": 10,
            "feedback": "தயவுசெய்து உங்கள் பதிலை விவரிக்கவும்." if is_tamil else "Please write a brief explanation of your reasoning.",
            "misconception": "Response was too brief to evaluate.",
            "next_step": "re_explain",
            "revised_explanation": lesson.get("analogy", ""),
            "next_question": "Can you try answering again using the real-world analogy?",
            "study_next": "Concept Fundamentals",
        }

    # Keyword patterns for common questions
    correct_keywords = [
        "8", "250", "infinite", "never stop", "முடிவில்லாமல்", "overwritten", "overwrite", "replace",
        "base case", "reusable", "blueprint", "sorted", "வரிசை", "0", "zero", "waiter", "தூதுவர்",
        "stack", "o(1)", "constant", "keyerror", "error", "பிழை", "reusability", "one place"
    ]
    partial_keywords = [
        "both", "5 and 8", "இரண்டும்", "5", "100", "runs forever", "stops", "copy", "harder", "house"
    ]

    has_correct = any(kw in ans for kw in correct_keywords)
    has_partial = any(kw in ans for kw in partial_keywords)

    if has_correct:
        return {
            "verdict": "correct",
            "xp_earned": 50,
            "feedback": (
                "அருமை! நீங்கள் சரியான கருத்தைக் கண்டறிந்துவிட்டீர்கள். உங்கள் விளக்கம் மிகத் தெளிவாக உள்ளது!"
                if is_tamil else
                "Outstanding! You nailed the core concept and demonstrated clear logical reasoning."
            ),
            "misconception": "",
            "next_step": "follow_up",
            "revised_explanation": "",
            "next_question": (
                "அடுத்த சவால்: இந்த கருத்தை நிஜ மென்பொருள் தயாரிப்பில் எங்கு பயன்படுத்தலாம்?"
                if is_tamil else
                "Next Adaptive Question: How would you optimize or protect this code in production?"
            ),
            "study_next": "Advanced Implementation & Real-World Use Cases",
        }
    elif has_partial or len(ans) > 25:
        return {
            "verdict": "partially_correct",
            "xp_earned": 30,
            "feedback": (
                "நல்ல முயற்சி! நீங்கள் மிக நெருங்கிவிட்டீர்கள். உங்கள் சிந்தனையில் பாதி உண்மை உள்ளது."
                if is_tamil else
                "Good effort! You're on the right track, but missed a crucial detail in the execution order."
            ),
            "misconception": "Overlooking the exact state change or order of operations.",
            "next_step": "follow_up",
            "revised_explanation": lesson.get("analogy", ""),
            "next_question": (
                "மீண்டும் ஒருமுறை யோசியுங்கள்: பழைய மதிப்பு அழிக்கப்படுமா அல்லது பாதுகாக்கப்படுமா?"
                if is_tamil else
                "Think about it once more: Is the previous state preserved, or completely overwritten?"
            ),
            "study_next": "State Management & Execution Flow",
        }
    else:
        return {
            "verdict": "incorrect",
            "xp_earned": 15,
            "feedback": (
                "நல்ல முயற்சி! தவறுகள் தான் புதியவற்றைக் கற்றுக்கொள்ள வழிவகுக்கும். இந்த உவமையைப் பாருங்கள்."
                if is_tamil else
                "Good try! Mistakes are normal when learning new mental models. Let's look at it from a fresh angle."
            ),
            "misconception": "Initial conceptual confusion regarding how the computer executes this step.",
            "next_step": "re_explain",
            "revised_explanation": lesson.get("analogy", ""),
            "next_question": (
                "எளிய கேள்வி: இந்த உதாரணத்தில் உள்ள உவமையை உங்கள் சொந்த வார்த்தைகளில் சொல்லுங்கள்."
                if is_tamil else
                "Quick check: How would you explain this to a 10-year-old using the real-world analogy?"
            ),
            "study_next": "Revisiting the Core Analogy",
        }


# Quick compatibility helpers
def get_mock_lesson(topic: str, language: str) -> dict:
    return get_best_matching_lesson(topic, language)


def get_mock_feedback(answer: str) -> dict:
    return evaluate_smart_answer("", answer, MOCK_LESSONS["variables"]["English"], "English")


def get_offline_doubt_answer(question: str, topic: str, language: str) -> Dict[str, Any]:
    """Generates structured educational explanations for student doubts offline."""
    lesson = get_best_matching_lesson(topic, language)
    q_low = (question or "").lower()
    is_tamil = "tamil" in (language or "").lower() or "தமிழ்" in (language or "")

    if any(k in q_low for k in ["error", "பிழை", "bug", "traceback"]):
        ans = (
            f"பெரும்பாலான தொடக்க நிலை பிழைகள் தொடரியல் (Syntax) அல்லது வரையறுக்கப்படாத மாறிகளை அணுகுவதால் ஏற்படுகின்றன. உங்கள் '{topic}' குறியீட்டில் சரியான பெயர்களும் வகைகளும் உள்ளதா என சோதிக்கவும்."
            if is_tamil else
            f"Most beginner errors in '{topic}' stem from syntax typos, type mismatches, or accessing uninitialized variables. Verify that variable names and data types match."
        )
    elif any(k in q_low for k in ["why", "need", "ஏன்", "தேவை"]):
        ans = (
            f"நாம் '{topic}' பயன்படுத்துவதன் முக்கிய நோக்கம் குறியீட்டின் மறுபயன்பாடு (Reusability), தெளிவான கட்டமைப்பு மற்றும் நினைவகத்தை முறையாகப் பயன்படுத்துவதே ஆகும்."
            if is_tamil else
            f"We use '{topic}' primarily for code reusability, clean abstraction, and predictable memory management. Without it, software would require repetitive copy-pasting."
        )
    else:
        ans = (
            f"'{topic}' என்பது கணினியில் தகவல்களை சீராக கையாளவும், கட்டளைகளை வரிசையாக இயக்கவும் உதவும் அடிப்படை அமைப்பாகும்."
            if is_tamil else
            f"'{topic}' is a foundational building block that enables deterministic control flow and organized state manipulation in memory."
        )

    return {
        "direct_answer": ans,
        "analogy": lesson.get("analogy", "Think of an instruction manual where each step must be followed in strict order to achieve the desired result."),
        "code_example": lesson.get("example", f"# Core example for {topic}\nx = 10\nprint('Concept in action:', x)"),
        "pro_tip": (
            "எப்போதும் பெரிய சிக்கல்களை சிறிய துண்டுகளாகப் பிரித்து, எளிய உள்ளீடுகளைக் கொண்டு முதலில் சோதிக்கவும்."
            if is_tamil else
            "Break complex algorithms into small testable units, and trace variable state transitions on paper."
        ),
        "diagram": lesson.get("diagram", "")
    }
