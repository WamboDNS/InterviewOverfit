import { GameProgress, Role, LevelData } from '../types/gameTypes';
import { gameData } from '../data/gameData';

export const initializeGameProgress = (): GameProgress => {
  const roleProgress: GameProgress['roleProgress'] = {} as any;
  
  (['SDE', 'DS', 'MLE'] as Role[]).forEach(role => {
    roleProgress[role] = {
      levelsCompleted: 0,
      totalStars: 0,
      unlockedLevels: [gameData[role].levels[0].id] // First level always unlocked
    };
  });

  return {
    currentRole: null,
    currentLevel: null,
    roleProgress
  };
};

export const updateProgressAfterVictory = (
  progress: GameProgress,
  role: Role,
  levelId: string,
  stars: number
): GameProgress => {
  const newProgress = { ...progress };
  const roleData = gameData[role];
  const currentLevelIndex = roleData.levels.findIndex(l => l.id === levelId);
  
  // Update role progress
  const currentRoleProgress = { ...newProgress.roleProgress[role] };
  
  // Mark level as completed if not already
  if (!currentRoleProgress.unlockedLevels.includes(levelId)) {
    currentRoleProgress.levelsCompleted += 1;
  }
  
  // Update stars (keep the best score)
  const existingStars = getStarsForLevel(progress, role, levelId);
  if (stars > existingStars) {
    currentRoleProgress.totalStars += (stars - existingStars);
  }
  
  // Unlock next level if it exists
  const nextLevel = roleData.levels[currentLevelIndex + 1];
  if (nextLevel && !currentRoleProgress.unlockedLevels.includes(nextLevel.id)) {
    currentRoleProgress.unlockedLevels.push(nextLevel.id);
  }
  
  newProgress.roleProgress[role] = currentRoleProgress;
  
  return newProgress;
};

export const getStarsForLevel = (
  progress: GameProgress,
  role: Role,
  levelId: string
): number => {
  // This would typically be stored in a more detailed progress structure
  // For now, we'll use a simple calculation based on completion
  const roleProgress = progress.roleProgress[role];
  if (roleProgress.unlockedLevels.includes(levelId)) {
    const roleData = gameData[role];
    const levelIndex = roleData.levels.findIndex(l => l.id === levelId);
    if (levelIndex < roleProgress.levelsCompleted) {
      return Math.min(3, Math.max(1, Math.floor(roleProgress.totalStars / roleProgress.levelsCompleted)));
    }
  }
  return 0;
};

export const isLevelUnlocked = (
  progress: GameProgress,
  role: Role,
  levelId: string
): boolean => {
  return progress.roleProgress[role].unlockedLevels.includes(levelId);
};

export const getRoleCompletionPercentage = (
  progress: GameProgress,
  role: Role
): number => {
  const roleData = gameData[role];
  const completedLevels = progress.roleProgress[role].levelsCompleted;
  return Math.round((completedLevels / roleData.levels.length) * 100);
};

export const getTotalStarsForRole = (
  progress: GameProgress,
  role: Role
): number => {
  return progress.roleProgress[role].totalStars;
};

export const saveGameProgress = (progress: GameProgress): void => {
  try {
    localStorage.setItem('interviewOverfit_progress', JSON.stringify(progress));
  } catch (error) {
    console.error('Failed to save game progress:', error);
  }
};

export const loadGameProgress = (): GameProgress => {
  try {
    const saved = localStorage.getItem('interviewOverfit_progress');
    if (saved) {
      const parsed = JSON.parse(saved);
      // Ensure the structure is valid and merge with defaults if needed
      return {
        ...initializeGameProgress(),
        ...parsed
      };
    }
  } catch (error) {
    console.error('Failed to load game progress:', error);
  }
  
  return initializeGameProgress();
};