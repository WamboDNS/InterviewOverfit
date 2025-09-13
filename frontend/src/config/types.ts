export interface GameConfig {
  gameMechanics: {
    initialStats: {
      userHp: number;
      bossHp: number;
      timeLimit: number;
      combo: number;
    };
    damage: {
      minDamage: number;
      maxDamage: number;
      timeoutPenalty: number;
      poorAnswerPenalty: number;
    };
    scoring: {
      damageMultiplier: number;
      comboMultiplier: number;
    };
    combo: {
      increaseThreshold: number;
      decreaseThreshold: number;
      maxCombo: number;
    };
    starCalculation: {
      baseStars: number;
      scoreThreshold: number;
      maxStars: number;
    };
  };
  timing: {
    gameEndDelay: number;
    timerInterval: number;
  };
}
