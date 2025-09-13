import { GameConfig, EvaluationResult, GameStats } from './types';

export class GameLogic {
  private config: GameConfig;

  constructor(config: GameConfig) {
    this.config = config;
  }

  /**
   * Evaluates a user's answer and calculates damage dealt to the boss
   */
  evaluateAnswer(content: string, question: string): EvaluationResult {
    const keywordCount = this.countKeywords(content, question);
    const contentLength = content.length;
    const hasCodePatterns = this.detectCodePatterns(content);
    
    // Calculate base damage
    let baseDamage = Math.min(
      this.config.evaluation.scoring.baseDamage.max,
      Math.max(
        this.config.evaluation.scoring.baseDamage.min,
        keywordCount * this.config.evaluation.scoring.baseDamage.keywordMultiplier
      )
    );
    
    // Apply bonuses
    if (contentLength > this.config.evaluation.scoring.bonuses.detailedAnswer.threshold) {
      baseDamage += this.config.evaluation.scoring.bonuses.detailedAnswer.damage;
    }
    
    if (contentLength > this.config.evaluation.scoring.bonuses.veryDetailedAnswer.threshold) {
      baseDamage += this.config.evaluation.scoring.bonuses.veryDetailedAnswer.damage;
    }
    
    if (hasCodePatterns) {
      baseDamage += this.config.evaluation.scoring.bonuses.codeExample.damage;
    }
    
    const finalDamage = Math.min(baseDamage, this.config.evaluation.scoring.maxDamage);
    
    return {
      damage: finalDamage,
      hasCodePatterns,
      keywordCount,
      contentLength
    };
  }

  /**
   * Determines the boss response based on damage dealt
   */
  getBossResponseType(damage: number): 'excellent' | 'good' | 'poor' {
    if (damage >= this.config.evaluation.damageThresholds.excellent) {
      return 'excellent';
    } else if (damage >= this.config.evaluation.damageThresholds.good) {
      return 'good';
    } else {
      return 'poor';
    }
  }

  /**
   * Calculates combo multiplier based on damage
   */
  calculateCombo(currentCombo: number, damage: number): number {
    if (damage >= this.config.evaluation.combo.increaseThreshold) {
      return Math.min(currentCombo + 1, this.config.evaluation.combo.maxCombo);
    } else if (damage < this.config.evaluation.combo.decreaseThreshold) {
      return 1;
    }
    return currentCombo;
  }

  /**
   * Calculates score based on damage and combo
   */
  calculateScore(damage: number, combo: number): number {
    return damage * combo * this.config.gameMechanics.scoring.damageMultiplier;
  }

  /**
   * Calculates stars based on final game stats
   */
  calculateStars(finalScore: number, remainingHp: number, remainingTime: number): number {
    let stars = this.config.gameMechanics.starCalculation.baseStars;
    
    if (finalScore > this.config.gameMechanics.starCalculation.highScoreThreshold) {
      stars++;
    }
    
    if (remainingHp > this.config.gameMechanics.starCalculation.healthThreshold && 
        remainingTime > this.config.gameMechanics.starCalculation.timeThreshold) {
      stars++;
    }
    
    return Math.min(stars, this.config.gameMechanics.starCalculation.maxStars);
  }

  /**
   * Applies damage penalties for timeouts or poor answers
   */
  applyPenalty(currentHp: number, penaltyType: 'timeout' | 'poorAnswer'): number {
    const penalty = penaltyType === 'timeout' 
      ? this.config.gameMechanics.damage.timeoutPenalty
      : this.config.gameMechanics.damage.poorAnswerPenalty;
    
    return Math.max(0, currentHp - penalty);
  }

  /**
   * Counts relevant keywords in the answer
   */
  private countKeywords(content: string, question: string): number {
    const questionWords = question.toLowerCase().split(' ').filter(word => word.length > 3);
    const contentLower = content.toLowerCase();
    
    return questionWords.filter(word => contentLower.includes(word)).length;
  }

  /**
   * Detects if the content contains code patterns
   */
  private detectCodePatterns(content: string): boolean {
    const patterns = this.config.evaluation.scoring.bonuses.codeExample.patterns;
    return patterns.some(pattern => content.includes(pattern));
  }
}
