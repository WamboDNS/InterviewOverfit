export interface GameConfig {
  gameMechanics: {
    initialStats: {
      userHp: number;
      bossHp: number;
      combo: number;
    };
    damage: {
      minDamage: number;
      maxDamage: number;
      poorAnswerPenalty: number;
    };
    combo: {
      increaseThreshold: number;
      decreaseThreshold: number;
      maxCombo: number;
    };
  };
}
