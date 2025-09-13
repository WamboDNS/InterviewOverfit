/**
 * API service for InterviewOverfit Boss Battle Game
 * Handles all communication with the FastAPI backend
 */

const API_BASE_URL = 'http://localhost:8000/api';

// Type definitions for API responses
export interface GameState {
  level: number;
  max_level: number;
  boss_name: string;
  boss_personality: string;
  boss_question_types: string[];
  boss_hp: number;
  max_hp: number;
  user_hp: number;
  turn_count: number;
  current_question: string;
  game_over: boolean;
  victory: boolean;
  conversation_length: number;
}

export interface QuestionResponse {
  success: boolean;
  question: string;
  game_state: GameState;
  error?: string;
}

export interface AnswerResponse {
  success: boolean;
  score: number;
  feedback: string;
  damage_dealt: number;
  damage_taken: number;
  game_state: GameState;
  error?: string;
}

export interface GameResponse {
  success: boolean;
  message: string;
  game_state?: GameState;
  error?: string;
}

export interface ConversationHistory {
  success: boolean;
  conversation_history: Array<{
    role: 'user' | 'assistant';
    content: string;
  }>;
  total_messages: number;
  game_state: GameState;
}

// API Error class
export class APIError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = 'APIError';
  }
}

// API service class
export class InterviewOverfitAPI {
  private userId: string;
  private apiKey?: string;

  constructor(userId: string = 'demo-user', apiKey?: string) {
    this.userId = userId;
    this.apiKey = apiKey;
  }

  private async makeRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new APIError(`HTTP ${response.status}: ${response.statusText}`, response.status);
      }

      const data = await response.json();
      return data as T;
    } catch (error) {
      if (error instanceof APIError) {
        throw error;
      }
      throw new APIError(`Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Start a new boss battle game
   */
  async startGame(apiKey?: string): Promise<QuestionResponse> {
    return this.makeRequest<QuestionResponse>(`/game/${this.userId}/start`, {
      method: 'POST',
      body: JSON.stringify({
        api_key: apiKey || this.apiKey
      }),
    });
  }

  /**
   * Get the current game status
   */
  async getGameStatus(): Promise<GameState> {
    return this.makeRequest<GameState>(`/game/${this.userId}/status`);
  }

  /**
   * Get the current or next question
   */
  async getQuestion(): Promise<QuestionResponse> {
    return this.makeRequest<QuestionResponse>(`/game/${this.userId}/question`);
  }

  /**
   * Submit an answer to the current question
   */
  async submitAnswer(answer: string): Promise<AnswerResponse> {
    return this.makeRequest<AnswerResponse>(`/game/${this.userId}/answer`, {
      method: 'POST',
      body: JSON.stringify({ answer }),
    });
  }

  /**
   * Reset the current game
   */
  async resetGame(): Promise<QuestionResponse> {
    return this.makeRequest<QuestionResponse>(`/game/${this.userId}/reset`, {
      method: 'POST',
    });
  }

  /**
   * End the current game
   */
  async endGame(): Promise<GameResponse> {
    return this.makeRequest<GameResponse>(`/game/${this.userId}`, {
      method: 'DELETE',
    });
  }

  /**
   * Get conversation history
   */
  async getConversationHistory(): Promise<ConversationHistory> {
    return this.makeRequest<ConversationHistory>(`/game/${this.userId}/history`);
  }

  /**
   * Check API health
   */
  async healthCheck(): Promise<{ status: string; service: string }> {
    return this.makeRequest('/health');
  }

  /**
   * Set API key for future requests
   */
  setApiKey(apiKey: string): void {
    this.apiKey = apiKey;
  }

  /**
   * Set user ID
   */
  setUserId(userId: string): void {
    this.userId = userId;
  }
}

// Default API instance
export const api = new InterviewOverfitAPI();

// Utility functions
export const isGameActive = (gameState: GameState): boolean => {
  return !gameState.game_over;
};

export const hasWon = (gameState: GameState): boolean => {
  return gameState.victory;
};

export const getBossProgress = (gameState: GameState): number => {
  return (gameState.boss_hp / gameState.max_hp) * 100;
};

export const getUserProgress = (gameState: GameState): number => {
  return (gameState.user_hp / gameState.max_hp) * 100;
};
