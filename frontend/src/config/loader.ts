import { GameConfig } from './types';

// Inline configuration to avoid JSON import issues
const gameConfigData: GameConfig = {
  gameMechanics: {
    initialStats: {
      userHp: 100,
      bossHp: 80,
      combo: 1
    },
    damage: {
      minDamage: 10,
      maxDamage: 25,
      poorAnswerPenalty: 15
    },
    combo: {
      increaseThreshold: 15,
      decreaseThreshold: 8,
      maxCombo: 5
    },
  },
  timing: {
    gameEndDelay: 2000
  }
};

let gameConfig: GameConfig | null = null;

export const loadGameConfig = (): GameConfig => {
  if (!gameConfig) {
    gameConfig = gameConfigData;
  }
  return gameConfig;
};

export const getGameConfig = (): GameConfig => {
  if (!gameConfig) {
    return loadGameConfig();
  }
  return gameConfig;
};
