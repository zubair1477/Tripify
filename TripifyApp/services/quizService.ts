import { API_ENDPOINTS } from './api';

export interface QuizAnswers {
  userId: string;
  answers: { [key: number]: number };
}

export interface MoodScores {
  energetic: number;
  calm: number;
  introspective: number;
  adventurous: number;
}

export interface MoodResult {
  userId: string;
  moodScores: MoodScores;
  dominantMood: string;
  createdAt: string;
}

/**
 * Submit quiz answers and calculate mood
 */
export const calculateMood = async (quizAnswers: QuizAnswers): Promise<MoodResult> => {
  try {
    const response = await fetch(API_ENDPOINTS.CALCULATE_MOOD, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(quizAnswers),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to calculate mood');
    }

    return await response.json();
  } catch (error) {
    console.error('Error calculating mood:', error);
    throw error;
  }
};

/**
 * Get quiz questions from backend
 */
export const getQuizQuestions = async () => {
  try {
    const response = await fetch(API_ENDPOINTS.GET_QUIZ_QUESTIONS);

    if (!response.ok) {
      throw new Error('Failed to fetch quiz questions');
    }

    const data = await response.json();
    return data.questions;
  } catch (error) {
    console.error('Error fetching quiz questions:', error);
    throw error;
  }
};

/**
 * Get user's mood history
 */
export const getMoodHistory = async (userId: string) => {
  try {
    const response = await fetch(API_ENDPOINTS.GET_MOOD_HISTORY(userId));

    if (!response.ok) {
      throw new Error('Failed to fetch mood history');
    }

    const data = await response.json();
    return data.moodHistory;
  } catch (error) {
    console.error('Error fetching mood history:', error);
    throw error;
  }
};
