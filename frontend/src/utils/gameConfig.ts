import { GameConfig } from '../../../shared/types';
import { GameLogic } from '../../../shared/gameLogic';

// Import the configuration - in a real app, this would be loaded from an API
import gameConfigData from '../../../shared/gameConfig.json';

let gameConfig: GameConfig;
let gameLogic: GameLogic;

// Initialize the game configuration
export const initializeGameConfig = async (): Promise<GameConfig> => {
  if (!gameConfig) {
    // In a real application, you would fetch this from your backend API
    // const response = await fetch('/api/game-config');
    // gameConfig = await response.json();
    
    // For now, we'll use the imported JSON data
    gameConfig = gameConfigData as GameConfig;
    gameLogic = new GameLogic(gameConfig);
  }
  return gameConfig;
};

// Get the game configuration
export const getGameConfig = (): GameConfig => {
  if (!gameConfig) {
    throw new Error('Game configuration not initialized. Call initializeGameConfig() first.');
  }
  return gameConfig;
};

// Get the game logic instance
export const getGameLogic = (): GameLogic => {
  if (!gameLogic) {
    throw new Error('Game logic not initialized. Call initializeGameConfig() first.');
  }
  return gameLogic;
};

// Utility function to load configuration from backend API
export const loadGameConfigFromAPI = async (baseUrl: string = ''): Promise<GameConfig> => {
  try {
    const response = await fetch(`${baseUrl}/api/game-config`);
    if (!response.ok) {
      throw new Error(`Failed to load game config: ${response.statusText}`);
    }
    gameConfig = await response.json();
    gameLogic = new GameLogic(gameConfig);
    return gameConfig;
  } catch (error) {
    console.warn('Failed to load game config from API, using local config:', error);
    return initializeGameConfig();
  }
};
