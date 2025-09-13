/**
 * Node.js Frontend Example for Interview Boss Battle API
 * 
 * This example shows how to integrate with the FastAPI backend
 * from a Node.js/React/Vue/Angular frontend.
 */

const API_BASE_URL = 'http://localhost:8000';
const USER_ID = 'demo-user';

class InterviewBossGameClient {
    constructor(baseUrl = API_BASE_URL) {
        this.baseUrl = baseUrl;
        this.userId = USER_ID;
    }

    /**
     * Make HTTP request to the API
     */
    async makeRequest(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const response = await fetch(url, { ...defaultOptions, ...options });
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || data.detail || 'API request failed');
        }
        
        return data;
    }

    /**
     * Start a new game
     */
    async startGame(apiKey = null) {
        return await this.makeRequest(`/game/${this.userId}/start`, {
            method: 'POST',
            body: JSON.stringify({ api_key: apiKey }),
        });
    }

    /**
     * Submit an answer
     */
    async submitAnswer(answer) {
        return await this.makeRequest(`/game/${this.userId}/answer`, {
            method: 'POST',
            body: JSON.stringify({ answer }),
        });
    }

    /**
     * Get next question
     */
    async getNextQuestion() {
        return await this.makeRequest(`/game/${this.userId}/question`);
    }

    /**
     * Get game status
     */
    async getGameStatus() {
        return await this.makeRequest(`/game/${this.userId}/status`);
    }

    /**
     * Reset game
     */
    async resetGame() {
        return await this.makeRequest(`/game/${this.userId}/reset`, {
            method: 'POST',
        });
    }

    /**
     * End game
     */
    async endGame() {
        return await this.makeRequest(`/game/${this.userId}`, {
            method: 'DELETE',
        });
    }

    /**
     * Get conversation history
     */
    async getHistory() {
        return await this.makeRequest(`/game/${this.userId}/history`);
    }

    /**
     * Get API info
     */
    async getApiInfo() {
        return await this.makeRequest('/api/info');
    }
}

// Example usage
async function exampleGameFlow() {
    const client = new InterviewBossGameClient();
    
    try {
        console.log('🎮 Starting Interview Boss Battle...');
        
        // Get API info
        const apiInfo = await client.getApiInfo();
        console.log('API Info:', apiInfo);
        
        // Start game
        const startResponse = await client.startGame();
        console.log('Game started:', startResponse);
        
        if (startResponse.success) {
            console.log('Question:', startResponse.question);
            console.log('Game State:', startResponse.game_state);
            
            // Submit an answer
            const answerResponse = await client.submitAnswer(
                "I would use a hash map for O(1) lookup time and handle collisions with chaining."
            );
            console.log('Answer response:', answerResponse);
            
            if (answerResponse.success) {
                console.log('Score:', answerResponse.score);
                console.log('Feedback:', answerResponse.feedback);
                console.log('Updated Game State:', answerResponse.game_state);
            }
        }
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

// React Hook Example
const useInterviewBossGame = () => {
    const [gameState, setGameState] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    
    const client = new InterviewBossGameClient();
    
    const startGame = async (apiKey) => {
        setLoading(true);
        setError(null);
        try {
            const response = await client.startGame(apiKey);
            setGameState(response.game_state);
            return response;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    };
    
    const submitAnswer = async (answer) => {
        setLoading(true);
        setError(null);
        try {
            const response = await client.submitAnswer(answer);
            setGameState(response.game_state);
            return response;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    };
    
    const getNextQuestion = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await client.getNextQuestion();
            setGameState(response.game_state);
            return response;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    };
    
    return {
        gameState,
        loading,
        error,
        startGame,
        submitAnswer,
        getNextQuestion,
        resetGame: () => client.resetGame(),
        endGame: () => client.endGame(),
    };
};

// Vue Composition API Example
const useInterviewBossGameVue = () => {
    const gameState = ref(null);
    const loading = ref(false);
    const error = ref(null);
    
    const client = new InterviewBossGameClient();
    
    const startGame = async (apiKey) => {
        loading.value = true;
        error.value = null;
        try {
            const response = await client.startGame(apiKey);
            gameState.value = response.game_state;
            return response;
        } catch (err) {
            error.value = err.message;
            throw err;
        } finally {
            loading.value = false;
        }
    };
    
    const submitAnswer = async (answer) => {
        loading.value = true;
        error.value = null;
        try {
            const response = await client.submitAnswer(answer);
            gameState.value = response.game_state;
            return response;
        } catch (err) {
            error.value = err.message;
            throw err;
        } finally {
            loading.value = false;
        }
    };
    
    return {
        gameState: readonly(gameState),
        loading: readonly(loading),
        error: readonly(error),
        startGame,
        submitAnswer,
        getNextQuestion: () => client.getNextQuestion(),
        resetGame: () => client.resetGame(),
        endGame: () => client.endGame(),
    };
};

// Export for use in different frameworks
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        InterviewBossGameClient,
        useInterviewBossGame,
        useInterviewBossGameVue,
    };
}

// Run example if this file is executed directly
if (typeof window === 'undefined' && require.main === module) {
    exampleGameFlow();
}
