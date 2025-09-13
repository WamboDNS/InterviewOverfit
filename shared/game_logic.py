import json
import re
from typing import Dict, Any, List
from pathlib import Path

class GameLogic:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def evaluate_answer(self, content: str, question: str) -> Dict[str, Any]:
        """Evaluates a user's answer and calculates damage dealt to the boss"""
        keyword_count = self._count_keywords(content, question)
        content_length = len(content)
        has_code_patterns = self._detect_code_patterns(content)
        
        # Calculate base damage
        base_damage = min(
            self.config["evaluation"]["scoring"]["baseDamage"]["max"],
            max(
                self.config["evaluation"]["scoring"]["baseDamage"]["min"],
                keyword_count * self.config["evaluation"]["scoring"]["baseDamage"]["keywordMultiplier"]
            )
        )
        
        # Apply bonuses
        if content_length > self.config["evaluation"]["scoring"]["bonuses"]["detailedAnswer"]["threshold"]:
            base_damage += self.config["evaluation"]["scoring"]["bonuses"]["detailedAnswer"]["damage"]
        
        if content_length > self.config["evaluation"]["scoring"]["bonuses"]["veryDetailedAnswer"]["threshold"]:
            base_damage += self.config["evaluation"]["scoring"]["bonuses"]["veryDetailedAnswer"]["damage"]
        
        if has_code_patterns:
            base_damage += self.config["evaluation"]["scoring"]["bonuses"]["codeExample"]["damage"]
        
        final_damage = min(base_damage, self.config["evaluation"]["scoring"]["maxDamage"])
        
        return {
            "damage": final_damage,
            "hasCodePatterns": has_code_patterns,
            "keywordCount": keyword_count,
            "contentLength": content_length
        }

    def get_boss_response_type(self, damage: int) -> str:
        """Determines the boss response based on damage dealt"""
        if damage >= self.config["evaluation"]["damageThresholds"]["excellent"]:
            return "excellent"
        elif damage >= self.config["evaluation"]["damageThresholds"]["good"]:
            return "good"
        else:
            return "poor"

    def calculate_combo(self, current_combo: int, damage: int) -> int:
        """Calculates combo multiplier based on damage"""
        if damage >= self.config["evaluation"]["combo"]["increaseThreshold"]:
            return min(current_combo + 1, self.config["evaluation"]["combo"]["maxCombo"])
        elif damage < self.config["evaluation"]["combo"]["decreaseThreshold"]:
            return 1
        return current_combo

    def calculate_score(self, damage: int, combo: int) -> int:
        """Calculates score based on damage and combo"""
        return damage * combo * self.config["gameMechanics"]["scoring"]["damageMultiplier"]

    def calculate_stars(self, final_score: int, remaining_hp: int, remaining_time: int) -> int:
        """Calculates stars based on final game stats"""
        stars = self.config["gameMechanics"]["starCalculation"]["baseStars"]
        
        if final_score > self.config["gameMechanics"]["starCalculation"]["highScoreThreshold"]:
            stars += 1
        
        if (remaining_hp > self.config["gameMechanics"]["starCalculation"]["healthThreshold"] and 
            remaining_time > self.config["gameMechanics"]["starCalculation"]["timeThreshold"]):
            stars += 1
        
        return min(stars, self.config["gameMechanics"]["starCalculation"]["maxStars"])

    def apply_penalty(self, current_hp: int, penalty_type: str) -> int:
        """Applies damage penalties for timeouts or poor answers"""
        penalty = (self.config["gameMechanics"]["damage"]["timeoutPenalty"] 
                  if penalty_type == "timeout" 
                  else self.config["gameMechanics"]["damage"]["poorAnswerPenalty"])
        
        return max(0, current_hp - penalty)

    def _count_keywords(self, content: str, question: str) -> int:
        """Counts relevant keywords in the answer"""
        question_words = [word for word in question.lower().split() if len(word) > 3]
        content_lower = content.lower()
        
        return sum(1 for word in question_words if word in content_lower)

    def _detect_code_patterns(self, content: str) -> bool:
        """Detects if the content contains code patterns"""
        patterns = self.config["evaluation"]["scoring"]["bonuses"]["codeExample"]["patterns"]
        return any(pattern in content for pattern in patterns)

def load_game_config() -> Dict[str, Any]:
    """Load game configuration from JSON file"""
    config_path = Path(__file__).parent / "gameConfig.json"
    with open(config_path, 'r') as f:
        return json.load(f)

def create_game_logic() -> GameLogic:
    """Create a GameLogic instance with loaded configuration"""
    config = load_game_config()
    return GameLogic(config)
