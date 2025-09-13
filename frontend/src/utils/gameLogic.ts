import { GameConfig } from '../config/types';

export class GameLogic {
  private config: GameConfig;

  constructor(config: GameConfig) {
    this.config = config;
  }

  calculateDamage(): number {
    const { minDamage, maxDamage } = this.config.gameMechanics.damage;
    return Math.floor(Math.random() * (maxDamage - minDamage + 1)) + minDamage;
  }


  calculateCombo(currentCombo: number, damage: number): number {
    const { increaseThreshold, decreaseThreshold, maxCombo } = this.config.gameMechanics.combo;
    
    if (damage >= increaseThreshold) {
      return Math.min(currentCombo + 1, maxCombo);
    } else if (damage < decreaseThreshold) {
      return 1;
    }
    return currentCombo;
  }


  applyPenalty(currentHp: number, penaltyType: 'poorAnswer'): number {
    const penalty = this.config.gameMechanics.damage.poorAnswerPenalty;
    return Math.max(0, currentHp - penalty);
  }

  getInitialStats() {
    return this.config.gameMechanics.initialStats;
  }
}