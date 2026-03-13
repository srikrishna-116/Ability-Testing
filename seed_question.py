from db.mongo import questions_collection

questions = [
    # Arithmetic
    {"question": "2 + 2 = ?", "options": ["1", "2", "3", "4"], "correct_answer": "4", "difficulty": 0.1, "topic": "Arithmetic", "tags": ["easy"]},
    {"question": "5 × 6 = ?", "options": ["11", "30", "20", "25"], "correct_answer": "30", "difficulty": 0.2, "topic": "Arithmetic", "tags": ["easy"]},
    {"question": "12 ÷ 3 = ?", "options": ["2", "3", "4", "5"], "correct_answer": "4", "difficulty": 0.3, "topic": "Arithmetic", "tags": ["division"]},
    {"question": "Square root of 81?", "options": ["7", "8", "9", "10"], "correct_answer": "9", "difficulty": 0.4, "topic": "Arithmetic", "tags": ["sqrt"]},

    # Algebra
    {"question": "Solve: 3x + 2 = 11", "options": ["2", "3", "4", "5"], "correct_answer": "3", "difficulty": 0.4, "topic": "Algebra", "tags": ["equation"]},
    {"question": "Solve: x² = 16", "options": ["2", "4", "6", "8"], "correct_answer": "4", "difficulty": 0.5, "topic": "Algebra", "tags": ["square"]},
    {"question": "Factorize: x² - 9", "options": ["(x-3)(x+3)", "(x-9)(x+1)", "(x-1)(x+9)", "(x-2)(x+2)"], "correct_answer": "(x-3)(x+3)", "difficulty": 0.6, "topic": "Algebra", "tags": ["factorization"]},

    # Geometry
    {"question": "Sum of angles in a triangle?", "options": ["90°", "180°", "270°", "360°"], "correct_answer": "180°", "difficulty": 0.3, "topic": "Geometry", "tags": ["angles"]},
    {"question": "Area of circle with radius 7?", "options": ["154", "44", "77", "100"], "correct_answer": "154", "difficulty": 0.5, "topic": "Geometry", "tags": ["area"]},

    # Trigonometry
    {"question": "sin(90°) = ?", "options": ["0", "1", "√2/2", "√3/2"], "correct_answer": "1", "difficulty": 0.4, "topic": "Trigonometry", "tags": ["basic"]},
    {"question": "cos(0°) = ?", "options": ["0", "1", "-1", "√2/2"], "correct_answer": "1", "difficulty": 0.5, "topic": "Trigonometry", "tags": ["basic"]},

    # Vocabulary
    {"question": "Synonym of HAPPY", "options": ["Sad", "Joyful", "Angry", "Tired"], "correct_answer": "Joyful", "difficulty": 0.3, "topic": "Vocabulary", "tags": ["word"]},
    {"question": "Antonym of BIG", "options": ["Large", "Huge", "Small", "Tall"], "correct_answer": "Small", "difficulty": 0.2, "topic": "Vocabulary", "tags": ["word"]},

    # General Knowledge
    {"question": "Capital of France?", "options": ["Berlin", "Madrid", "Paris", "Rome"], "correct_answer": "Paris", "difficulty": 0.2, "topic": "GK", "tags": ["capital"]},
    {"question": "Largest planet?", "options": ["Earth", "Mars", "Jupiter", "Saturn"], "correct_answer": "Jupiter", "difficulty": 0.3, "topic": "GK", "tags": ["planet"]},

    # More advanced
    {"question": "Derivative of x²?", "options": ["x", "2x", "x²", "2"], "correct_answer": "2x", "difficulty": 0.7, "topic": "Calculus", "tags": ["derivative"]},
    {"question": "Limit of 1/x as x→∞?", "options": ["0", "1", "∞", "Does not exist"], "correct_answer": "0", "difficulty": 0.8, "topic": "Calculus", "tags": ["limit"]},
    {"question": "Variance measures?", "options": ["Central tendency", "Spread of data", "Probability", "Mean"], "correct_answer": "Spread of data", "difficulty": 0.6, "topic": "Statistics", "tags": ["variance"]},
    {"question": "Probability of getting head in coin toss?", "options": ["0", "0.25", "0.5", "1"], "correct_answer": "0.5", "difficulty": 0.4, "topic": "Statistics", "tags": ["probability"]},
    {"question": "Binary of 5?", "options": ["101", "110", "111", "100"], "correct_answer": "101", "difficulty": 0.3, "topic": "Computer Science", "tags": ["binary"]},
]

questions_collection.insert_many(questions)
print("20 questions inserted")
