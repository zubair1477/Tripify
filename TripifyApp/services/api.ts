// API configuration and base URL
const API_BASE_URL = 'http://127.0.0.1:8000/api';

export const API_ENDPOINTS = {
  // Auth endpoints
  SIGNUP: `${API_BASE_URL}/auth/signup`,
  LOGIN: `${API_BASE_URL}/auth/login`,
  GET_USER: (email: string) => `${API_BASE_URL}/auth/users/${email}`,

  // Quiz endpoints
  GET_QUIZ_QUESTIONS: `${API_BASE_URL}/quiz/questions`,
  CALCULATE_MOOD: `${API_BASE_URL}/quiz/calculate-mood`,
  GET_MOOD_HISTORY: (userId: string) => `${API_BASE_URL}/quiz/mood-history/${userId}`,
};

export default API_BASE_URL;
