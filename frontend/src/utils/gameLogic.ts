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

  calculateScore(damage: number, combo: number): number {
    const { damageMultiplier, comboMultiplier } = this.config.gameMechanics.scoring;
    return damage * combo * damageMultiplier * comboMultiplier;
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

  calculateStars(finalScore: number): number {
    const { baseStars, scoreThreshold, maxStars } = this.config.gameMechanics.starCalculation;
    return Math.min(baseStars + Math.floor(finalScore / scoreThreshold), maxStars);
  }

  applyPenalty(currentHp: number, penaltyType: 'timeout' | 'poorAnswer'): number {
    const penalty = penaltyType === 'timeout' 
      ? this.config.gameMechanics.damage.timeoutPenalty
      : this.config.gameMechanics.damage.poorAnswerPenalty;
    
    return Math.max(0, currentHp - penalty);
  }

  getInitialStats() {
    return this.config.gameMechanics.initialStats;
  }

  getTiming() {
    return this.config.timing;
  }
}