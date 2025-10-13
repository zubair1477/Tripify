// decided to do it this way for the quiz so that 
// it's easy to change the questions later
export interface QuizQuestion {
  id: number;
  question: string;
  options: string[];
}

export const quizQuestions: QuizQuestion[] = [
  {
    id: 1,
    question: "What's your ideal way to spend a weekend?",
    options: [
      "Relaxing at home with a good book",
      "Out dancing at a club",
      "Hiking in nature",
      "Exploring art galleries and museums"
    ]
  },
  {
    id: 2,
    question: "Which word best describes your personality?",
    options: [
      "Energetic",
      "Calm",
      "Creative",
      "Adventurous"
    ]
  },
  {
    id: 3,
    question: "What time of day do you feel most alive?",
    options: [
      "Early morning",
      "Afternoon",
      "Evening",
      "Late night"
    ]
  },
  {
    id: 4,
    question: "How do you handle stress?",
    options: [
      "Exercise or physical activity",
      "Listen to music",
      "Talk to friends",
      "Meditate or relax alone"
    ]
  },
  {
    id: 5,
    question: "What's your favorite season?",
    options: [
      "Spring",
      "Summer",
      "Fall",
      "Winter"
    ]
  },
  {
    id: 6,
    question: "Pick a color that speaks to you:",
    options: [
      "Blue",
      "Red",
      "Green",
      "Purple"
    ]
  },
  {
    id: 7,
    question: "What's your go-to mood?",
    options: [
      "Happy and upbeat",
      "Chill and relaxed",
      "Thoughtful and introspective",
      "Intense and passionate"
    ]
  },
  {
    id: 8,
    question: "How do you like to celebrate achievements?",
    options: [
      "Throw a big party",
      "Quiet dinner with close friends",
      "Treat myself to something special",
      "Share it on social media"
    ]
  },
  {
    id: 9,
    question: "What's your ideal vacation?",
    options: [
      "Beach resort",
      "City exploration",
      "Mountain retreat",
      "Road trip adventure"
    ]
  },
  {
    id: 10,
    question: "Which activity sounds most appealing?",
    options: [
      "Attending a live concert",
      "Cooking a new recipe",
      "Playing video games",
      "Reading poetry"
    ]
  }
];