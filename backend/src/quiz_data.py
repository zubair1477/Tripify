# Quiz questions with weighted mood mappings
# Each answer option has weights for: energetic, calm, introspective, adventurous

QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "What's your ideal way to spend a weekend?",
        "options": [
            "Relaxing at home with a good book",
            "Out dancing at a club",
            "Hiking in nature",
            "Exploring art galleries and museums"
        ],
        "weights": [
            {"energetic": 0, "calm": 3, "introspective": 2, "adventurous": 0},  # Relaxing at home
            {"energetic": 3, "calm": 0, "introspective": 0, "adventurous": 1},  # Dancing at club
            {"energetic": 1, "calm": 1, "introspective": 1, "adventurous": 3},  # Hiking
            {"energetic": 0, "calm": 1, "introspective": 3, "adventurous": 1}   # Art galleries
        ]
    },
    {
        "id": 2,
        "question": "Which word best describes your personality?",
        "options": [
            "Energetic",
            "Calm",
            "Creative",
            "Adventurous"
        ],
        "weights": [
            {"energetic": 3, "calm": 0, "introspective": 0, "adventurous": 1},  # Energetic
            {"energetic": 0, "calm": 3, "introspective": 1, "adventurous": 0},  # Calm
            {"energetic": 1, "calm": 1, "introspective": 3, "adventurous": 0},  # Creative
            {"energetic": 1, "calm": 0, "introspective": 0, "adventurous": 3}   # Adventurous
        ]
    },
    {
        "id": 3,
        "question": "What time of day do you feel most alive?",
        "options": [
            "Early morning",
            "Afternoon",
            "Evening",
            "Late night"
        ],
        "weights": [
            {"energetic": 2, "calm": 1, "introspective": 0, "adventurous": 1},  # Early morning
            {"energetic": 1, "calm": 2, "introspective": 0, "adventurous": 1},  # Afternoon
            {"energetic": 2, "calm": 0, "introspective": 1, "adventurous": 1},  # Evening
            {"energetic": 1, "calm": 0, "introspective": 3, "adventurous": 2}   # Late night
        ]
    },
    {
        "id": 4,
        "question": "How do you handle stress?",
        "options": [
            "Exercise or physical activity",
            "Listen to music",
            "Talk to friends",
            "Meditate or relax alone"
        ],
        "weights": [
            {"energetic": 3, "calm": 0, "introspective": 0, "adventurous": 1},  # Exercise
            {"energetic": 1, "calm": 2, "introspective": 2, "adventurous": 0},  # Music
            {"energetic": 2, "calm": 0, "introspective": 1, "adventurous": 1},  # Friends
            {"energetic": 0, "calm": 3, "introspective": 2, "adventurous": 0}   # Meditate
        ]
    },
    {
        "id": 5,
        "question": "What's your favorite season?",
        "options": [
            "Spring",
            "Summer",
            "Fall",
            "Winter"
        ],
        "weights": [
            {"energetic": 2, "calm": 1, "introspective": 0, "adventurous": 2},  # Spring
            {"energetic": 3, "calm": 0, "introspective": 0, "adventurous": 2},  # Summer
            {"energetic": 0, "calm": 2, "introspective": 3, "adventurous": 0},  # Fall
            {"energetic": 0, "calm": 3, "introspective": 2, "adventurous": 0}   # Winter
        ]
    },
    {
        "id": 6,
        "question": "Pick a color that speaks to you:",
        "options": [
            "Blue",
            "Red",
            "Green",
            "Purple"
        ],
        "weights": [
            {"energetic": 0, "calm": 3, "introspective": 2, "adventurous": 0},  # Blue
            {"energetic": 3, "calm": 0, "introspective": 0, "adventurous": 2},  # Red
            {"energetic": 1, "calm": 2, "introspective": 1, "adventurous": 1},  # Green
            {"energetic": 1, "calm": 1, "introspective": 3, "adventurous": 1}   # Purple
        ]
    },
    {
        "id": 7,
        "question": "What's your go-to mood?",
        "options": [
            "Happy and upbeat",
            "Chill and relaxed",
            "Thoughtful and introspective",
            "Intense and passionate"
        ],
        "weights": [
            {"energetic": 3, "calm": 0, "introspective": 0, "adventurous": 1},  # Happy
            {"energetic": 0, "calm": 3, "introspective": 1, "adventurous": 0},  # Chill
            {"energetic": 0, "calm": 1, "introspective": 3, "adventurous": 0},  # Thoughtful
            {"energetic": 2, "calm": 0, "introspective": 1, "adventurous": 3}   # Intense
        ]
    },
    {
        "id": 8,
        "question": "How do you like to celebrate achievements?",
        "options": [
            "Throw a big party",
            "Quiet dinner with close friends",
            "Treat myself to something special",
            "Share it on social media"
        ],
        "weights": [
            {"energetic": 3, "calm": 0, "introspective": 0, "adventurous": 2},  # Big party
            {"energetic": 0, "calm": 3, "introspective": 2, "adventurous": 0},  # Quiet dinner
            {"energetic": 1, "calm": 2, "introspective": 1, "adventurous": 1},  # Treat myself
            {"energetic": 2, "calm": 0, "introspective": 0, "adventurous": 1}   # Social media
        ]
    },
    {
        "id": 9,
        "question": "What's your ideal vacation?",
        "options": [
            "Beach resort",
            "City exploration",
            "Mountain retreat",
            "Road trip adventure"
        ],
        "weights": [
            {"energetic": 1, "calm": 3, "introspective": 0, "adventurous": 1},  # Beach
            {"energetic": 2, "calm": 0, "introspective": 1, "adventurous": 2},  # City
            {"energetic": 0, "calm": 3, "introspective": 2, "adventurous": 1},  # Mountain
            {"energetic": 2, "calm": 0, "introspective": 0, "adventurous": 3}   # Road trip
        ]
    },
    {
        "id": 10,
        "question": "Which activity sounds most appealing?",
        "options": [
            "Attending a live concert",
            "Cooking a new recipe",
            "Playing video games",
            "Reading poetry"
        ],
        "weights": [
            {"energetic": 3, "calm": 0, "introspective": 0, "adventurous": 2},  # Concert
            {"energetic": 1, "calm": 2, "introspective": 1, "adventurous": 1},  # Cooking
            {"energetic": 1, "calm": 1, "introspective": 1, "adventurous": 1},  # Games
            {"energetic": 0, "calm": 2, "introspective": 3, "adventurous": 0}   # Poetry
        ]
    }
]


def calculate_mood_scores(answers: dict) -> dict:
    """
    Calculate mood scores based on quiz answers

    Args:
        answers: Dictionary mapping question index to selected option index

    Returns:
        Dictionary with mood scores and dominant mood
    """
    mood_scores = {
        "energetic": 0.0,
        "calm": 0.0,
        "introspective": 0.0,
        "adventurous": 0.0
    }

    # Calculate total scores
    for question_index, option_index in answers.items():
        if 0 <= question_index < len(QUIZ_QUESTIONS):
            question = QUIZ_QUESTIONS[question_index]
            if 0 <= option_index < len(question["weights"]):
                weights = question["weights"][option_index]
                for mood, weight in weights.items():
                    mood_scores[mood] += weight

    # Normalize scores to percentages
    total_score = sum(mood_scores.values())
    if total_score > 0:
        for mood in mood_scores:
            mood_scores[mood] = round((mood_scores[mood] / total_score) * 100, 2)

    # Determine dominant mood
    dominant_mood = max(mood_scores, key=mood_scores.get)

    return {
        "moodScores": mood_scores,
        "dominantMood": dominant_mood
    }
