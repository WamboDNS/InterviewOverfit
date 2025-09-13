# Shared Game Configuration

This directory contains shared configuration and logic that can be used by both the frontend and backend of the InterviewOverfit game.

## Files

### `gameConfig.json`
Contains all the game configuration including:
- Evaluation scoring rules and thresholds
- Game mechanics (HP, time limits, damage penalties)
- Timing configurations
- Star calculation rules

### `types.ts`
TypeScript interfaces for the game configuration and related types.

### `gameLogic.ts`
TypeScript implementation of the game logic that can be used by the frontend.

### `game_logic.py`
Python implementation of the game logic that can be used by the backend.

## Usage

### Frontend (TypeScript)
```typescript
import { initializeGameConfig, getGameLogic } from '../utils/gameConfig';

// Initialize configuration
const config = await initializeGameConfig();
const gameLogic = getGameLogic();

// Use game logic
const result = gameLogic.evaluateAnswer(userAnswer, question);
```

### Backend (Python)
```python
from game_logic import create_game_logic

# Create game logic instance
game_logic = create_game_logic()

# Use game logic
result = game_logic.evaluate_answer(user_answer, question)
```

## API Endpoints

The backend provides the following endpoints:

- `GET /api/game-config` - Returns the game configuration
- `POST /api/evaluate-answer` - Evaluates a user's answer using shared logic

## Benefits

1. **Consistency**: Both frontend and backend use the same evaluation logic
2. **Maintainability**: Game rules are centralized in configuration files
3. **Flexibility**: Easy to adjust game mechanics without code changes
4. **Scalability**: Backend can handle complex evaluations while frontend provides immediate feedback
