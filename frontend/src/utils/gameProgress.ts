import { GameProgress, Role } from '../types/gameTypes';

// Initialize default game progress
export const initializeGameProgress = (): GameProgress => {
  return {
    currentRole: null,
    currentLevel: null,
    roleProgress: {
      SDE: {
        levelsCompleted: 0,
        totalStars: 0,
        unlockedLevels: ['sde-beginner']
      },
      DS: {
        levelsCompleted: 0,
        totalStars: 0,
        unlockedLevels: ['ds-beginner']
      },
      MLE: {
        levelsCompleted: 0,
        totalStars: 0,
        unlockedLevels: ['mle-beginner']
      }
    }
  };
};

// Load game progress from localStorage
export const loadGameProgress = (): GameProgress => {
  try {
    const saved = localStorage.getItem('gameProgress');
    if (saved) {
      return JSON.parse(saved);
    }
  } catch (error) {
    console.warn('Failed to load game progress:', error);
  }
  return initializeGameProgress();
};

// Save game progress to localStorage
export const saveGameProgress = (progress: GameProgress): void => {
  try {
    localStorage.setItem('gameProgress', JSON.stringify(progress));
  } catch (error) {
    console.warn('Failed to save game progress:', error);
  }
};

// Update progress after victory
export const updateProgressAfterVictory = (
  currentProgress: GameProgress,
  role: Role,
  levelId: string,
  stars: number
): GameProgress => {
  const newProgress = { ...currentProgress };
  const roleProgress = newProgress.roleProgress[role];
  
  // Add stars
  roleProgress.totalStars += stars;
  
  // Mark level as completed if not already
  if (!roleProgress.unlockedLevels.includes(levelId)) {
    roleProgress.unlockedLevels.push(levelId);
  }
  
  // Unlock next level (simple progression)
  const levelMap: Record<string, string> = {
    'sde-beginner': 'sde-intermediate',
    'sde-intermediate': 'sde-expert',
    'ds-beginner': 'ds-intermediate',
    'ds-intermediate': 'ds-expert',
    'mle-beginner': 'mle-intermediate',
    'mle-intermediate': 'mle-expert'
  };
  
  const nextLevel = levelMap[levelId];
  if (nextLevel && !roleProgress.unlockedLevels.includes(nextLevel)) {
    roleProgress.unlockedLevels.push(nextLevel);
  }
  
  return newProgress;
};

// Get stars for a specific level
export const getStarsForLevel = (
  progress: GameProgress,
  role: Role,
  levelId: string
): number => {
  // Simple implementation - return 1 star if level is completed
  const roleProgress = progress.roleProgress[role];
  return roleProgress.unlockedLevels.includes(levelId) ? 1 : 0;
};
