export type Role = 'SDE' | 'DS' | 'MLE';
export type Level = 'beginner' | 'intermediate' | 'expert';
export type GameScreen = 'loading' | 'roleSelection' | 'map' | 'battle' | 'winLoss';

export interface Boss {
  id: string;
  name: string;
  avatar: string;
  hp: number;
  questions: string[];
  responses: {
    excellent: string[];
    good: string[];
    poor: string[];
    victory: string;
  };
}

export interface LevelData {
  id: string;
  name: string;
  level: Level;
  boss: Boss;
  unlocked: boolean;
  completed: boolean;
  stars: number; // 0-3 stars based on performance
}

export interface RoleData {
  id: Role;
  name: string;
  description: string;
  icon: string;
  levels: LevelData[];
}

export interface GameProgress {
  currentRole: Role | null;
  currentLevel: string | null;
  roleProgress: Record<Role, {
    levelsCompleted: number;
    totalStars: number;
    unlockedLevels: string[];
  }>;
}

export interface GameState {
  screen: GameScreen;
  role: Role | null;
  currentLevel: LevelData | null;
  progress: GameProgress;
  battleState: {
    bossHp: number;
    userHp: number;
    timeLeft: number;
    score: number;
    combo: number;
    messages: ChatMessage[];
    currentQuestionIndex: number;
  };
}

export interface ChatMessage {
  id: string;
  type: 'boss' | 'user';
  content: string;
  isCode?: boolean;
  timestamp: Date;
}