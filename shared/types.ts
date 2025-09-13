export interface GameConfig {
  evaluation: {
    scoring: {
      baseDamage: {
        min: number;
        max: number;
        keywordMultiplier: number;
      };
      bonuses: {
        detailedAnswer: {
          threshold: number;
          damage: number;
        };
        veryDetailedAnswer: {
          threshold: number;
          damage: number;
        };
        codeExample: {
          damage: number;
          patterns: string[];
        };
      };
      maxDamage: number;
    };
    damageThresholds: {
      excellent: number;
      good: number;
      poor: number;
    };
    combo: {
      increaseThreshold: number;
      decreaseThreshold: number;
      maxCombo: number;
    };
  };
  gameMechanics: {
    initialStats: {
      userHp: number;
      timeLimit: number;
      combo: number;
    };
    damage: {
      timeoutPenalty: number;
      poorAnswerPenalty: number;
    };
    scoring: {
      damageMultiplier: number;
    };
    starCalculation: {
      baseStars: number;
      highScoreThreshold: number;
      healthThreshold: number;
      timeThreshold: number;
      maxStars: number;
    };
  };
  timing: {
    bossResponseDelay: number;
    nextQuestionDelay: number;
    gameEndDelay: number;
  };
}

export interface EvaluationResult {
  damage: number;
  hasCodePatterns: boolean;
  keywordCount: number;
  contentLength: number;
}

export interface GameStats {
  userHp: number;
  bossHp: number;
  timeLeft: number;
  score: number;
  combo: number;
}
