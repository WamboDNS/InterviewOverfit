"""
Interview Boss Battle Game

A gamified interview preparation system that turns technical interviews 
into an RPG-style boss battle game using AI.
"""

import anthropic
import os
import re
import json
from typing import Dict, Tuple, Optional


class InterviewBossGame:
    """
    A gamified interview preparation system with RPG-style boss battles.
    
    Players progress through 3 levels of software engineering roles by 
    answering interview questions correctly and defeating AI-powered bosses.
    """
    
    # ==================== GAME CONFIGURATION ====================
    
    MAX_LEVEL = 3
    MAX_HP = 1
    SCORE_RANGE = (-10, 10)
    
    # ==================== BOSS DEFINITIONS ====================
    
    BOSSES = {
        1: {
            "name": "Senior Developer Sarah",
            "personality": "Encouraging mentor who focuses on fundamentals",
            "question_types": [
                "Data structures", 
                "Basic algorithms", 
                "OOP concepts", 
                "Code review"
            ]
        },
        2: {
            "name": "Engineering Manager Marcus", 
            "personality": "Business-focused leader who cares about scalability",
            "question_types": [
                "System design", 
                "Database design", 
                "API design", 
                "Performance optimization"
            ]
        },
        3: {
            "name": "Staff Engineer Dr. Chen",
            "personality": "Brilliant architect who expects excellence", 
            "question_types": [
                "Distributed systems", 
                "Technical leadership", 
                "Architecture decisions", 
                "Complex problem solving"
            ]
        }
    }
    
    # ==================== SYSTEM PROMPT ====================
    
    SYSTEM_PROMPT = """You are the Interview Boss Battle Master!

GAME RULES:
- Player starts as Junior Software Engineer (Level 1) and must defeat bosses to advance
- 3 Levels: Junior SWE → Senior SWE → Staff SWE
- Each level has a unique boss with different personality and question difficulty
- After each user answer, you MUST respond in this exact format:

First Line: <score> SCORE </score> where SCORE from -10 to +10 (e.g., "+7" or "-3"), only print the value, no text
After that: <feedback> FEEDBACK </feedback>
then: <question> QUESTION </question>
The XML Formatting is important. Do not remove it.
Then give detailed feedback on the user answer combined with the correct answer.
After that, give the next question.

The very first question does not need the xml tag parts. Only give that once you have user answers.

SCORING GUIDELINES:
+8 to +10: Exceptional answer, shows deep understanding
+5 to +7: Good answer, solid technical knowledge
+1 to +4: Acceptable answer, room for improvement
0: Neutral answer, neither good nor bad
-1 to -4: Poor answer, missing key concepts
-5 to -7: Bad answer, shows lack of understanding
-8 to -10: Terrible answer, completely wrong or irrelevant

BOSS PERSONALITIES:
Level 1 - Senior Developer "Sarah": Encouraging but thorough, asks foundational questions
Level 2 - Engineering Manager "Marcus": Direct and business-focused, asks system design questions
Level 3 - Staff Engineer "Dr. Chen": Brilliant and demanding, asks architecture and leadership questions

Always stay in character as the current boss and make the feedback engaging and educational!"""

    # ==================== INITIALIZATION ====================

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the game with API client.
        
        Args:
            api_key: Anthropic API key. If None, uses ANTHROPIC_API_KEY env var.
        
        Raises:
            ValueError: If no API key is provided or found in environment.
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.conversation_history = []
        self.reset_game()

    # ==================== GAME STATE MANAGEMENT ====================

    def reset_game(self) -> None:
        """Reset game to initial state."""
        self.level = 1
        self.boss_hp = self.MAX_HP
        self.user_hp = self.MAX_HP
        self.turn_count = 0
        self.current_question = ""
        self.game_over = False
        self.victory = False
        self.conversation_history = []

    def get_boss_info(self) -> Dict[str, str]:
        """Get current boss information."""
        return self.BOSSES.get(self.level, self.BOSSES[1])

    # ==================== PROMPT GENERATION ====================

    def _create_game_state_prompt(self) -> str:
        """Create game state context for LLM."""
        boss_info = self.get_boss_info()
        return f"""CURRENT GAME STATE:
Level: {self.level}/{self.MAX_LEVEL}
Boss: {boss_info['name']} (HP: {self.boss_hp}/{self.MAX_HP})
Your HP: {self.user_hp}/{self.MAX_HP}
Turn: {self.turn_count}

Boss Personality: {boss_info['personality']}
Question Focus: {', '.join(boss_info['question_types'])}

You are currently {boss_info['name']}. Ask an appropriate interview question for this level and maintain your character throughout the interaction."""

    # ==================== SCORE PARSING ====================

    def _parse_score(self, response: str) -> Tuple[int, str]:
        """
        Parse score from LLM response.
        
        Args:
            response: Raw response from LLM
            
        Returns:
            Tuple of (score, feedback_text)
        """
        lines = response.strip().split('\n')
        if not lines:
            return 0, response

        first_line = lines[0].strip()
        score_match = re.search(r'<score>\s*([+-]?\d+)\s*</score>', first_line)

        if score_match:
            score = int(score_match.group(1))
            # Clamp the score to the allowed range [-10, 10]
            score = max(-10, min(10, score))
            feedback = '\n'.join(lines[1:]).strip() if len(lines) > 1 else "No feedback provided."
            return score, feedback
        
        return 0, response

    # ==================== API COMMUNICATION ====================

    def _make_api_call(self, user_message: str, max_tokens: int = 1000) -> str:
        """
        Make API call to Claude with continuous conversation context.
        
        Args:
            user_message: Message to send to the LLM
            max_tokens: Maximum tokens for response
            
        Returns:
            Assistant response text
            
        Raises:
            Exception: If API call fails
        """
        try:
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            
            response = self.client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=max_tokens,
                system=self.SYSTEM_PROMPT,
                messages=self.conversation_history
            )
            
            assistant_response = response.content[0].text
            
            # Add assistant response to conversation history
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
            
        except Exception as e:
            raise Exception(f"API call failed: {e}")

    # ==================== GAME ACTIONS ====================

    def get_question(self) -> str:
        """
        Get a new interview question from current boss.
        
        Returns:
            Question text or error message
        """
        if self.game_over:
            return "Game Over! Type 'reset' to play again."

        try:
            if not self.conversation_history:
                # First question - initialize the conversation
                game_state = self._create_game_state_prompt()
                initial_prompt = f"""{game_state}

Welcome to the Interview Boss Battle! I am {self.get_boss_info()['name']}. 
Ask the candidate an interview question appropriate for this level."""
                
                question = self._make_api_call(initial_prompt)
            else:
                # Continue conversation - ask for next question
                game_state = self._create_game_state_prompt()
                prompt = f"""{game_state}

The candidate has answered. Now ask the next interview question appropriate for this level."""
                
                question = self._make_api_call(prompt)
            
            self.current_question = question
            return question
            
        except Exception as e:
            return f"Error getting question: {e}"

    def submit_answer(self, user_answer: str) -> str:
        """
        Submit user answer and get feedback.
        
        Args:
            user_answer: User's answer to the current question
            
        Returns:
            Formatted response with score, feedback, and game state
        """
        if self.game_over:
            if user_answer.lower() == 'reset':
                self.reset_game()
                return self.get_question()
            return "Game Over! Type 'reset' to play again."

        if not self.current_question:
            return "No question asked yet. Get a question first!"

        try:
            boss_info = self.get_boss_info()
            game_state = self._create_game_state_prompt()
            
            evaluation_prompt = f"""{game_state}

The candidate answered: {user_answer}

Now evaluate this answer and respond as {boss_info['name']}. Remember:
- First line must be score (-10 to +10) 
- Then provide character-appropriate feedback
- After feedback, ask the next question"""

            response = self._make_api_call(evaluation_prompt, max_tokens=1024)
            
            score, feedback = self._parse_score(response)
            
            # Update HP based on score
            if score > 0:
                damage = score
                self.boss_hp -= damage
                self.boss_hp = max(0, self.boss_hp)  # Ensure HP doesn't go below 0
                result_msg = f"💥 Boss takes {damage} damage!"
            elif score < 0:
                damage = abs(score)  # Make damage positive for clarity
                self.user_hp -= damage  # Subtract damage from user HP
                self.user_hp = max(0, self.user_hp)  # Ensure HP doesn't go below 0
                result_msg = f"😵 You take {damage} damage!"
            else:
                result_msg = "⚡ No damage dealt!"

            self.turn_count += 1

            # Check win/lose conditions
            status_msg = ""
            if self.boss_hp <= 0:
                self._advance_level()
                if not self.victory:
                    status_msg = "\n🎯 Boss defeated! Moving to next level..."
            elif self.user_hp <= 0:
                self.reset_game()
                # Automatically start a new game after defeat
                self.start_new_game()
                status_msg = "\n💀 You were defeated! New game started..."

            return f"""<score>{score:+d}</score>
{feedback}
{result_msg}
Boss HP: {max(0, self.boss_hp)}/{self.MAX_HP} | Your HP: {max(0, self.user_hp)}/{self.MAX_HP}{status_msg}"""

        except Exception as e:
            return f"Error evaluating answer: {e}"

    def _advance_level(self) -> None:
        """Advance to next level or complete game."""
        if self.level < self.MAX_LEVEL:
            self.level += 1
            self.boss_hp = self.MAX_HP
            self.turn_count = 0
            boss_info = self.get_boss_info()
            print(f"🎉 Level Up! Now facing {boss_info['name']} at Level {self.level}")
            
            # Add level transition message to conversation
            transition_msg = f"🎉 LEVEL UP! The candidate has defeated the previous boss and now faces {boss_info['name']} at Level {self.level}. The new boss has a fresh 100 HP and the interview continues with {boss_info['personality']}."
            self.conversation_history.append({"role": "user", "content": transition_msg})
        else:
            self.victory = True
            self.game_over = True
            print("🏆 VICTORY! You've become a Staff Software Engineer!")

    # ==================== STATUS AND INFO METHODS ====================

    def get_status(self) -> str:
        """Get current game status as formatted string."""
        boss_info = self.get_boss_info()
        return f"""📊 GAME STATUS 📊
Level: {self.level}/{self.MAX_LEVEL}
Current Boss: {boss_info['name']}
Boss HP: {self.boss_hp}/{self.MAX_HP}
Your HP: {self.user_hp}/{self.MAX_HP}
Turn: {self.turn_count}"""

    def get_game_state(self) -> Dict:
        """Get current game state as dictionary for programmatic access."""
        boss_info = self.get_boss_info()
        return {
            "level": self.level,
            "max_level": self.MAX_LEVEL,
            "boss_name": boss_info["name"],
            "boss_personality": boss_info["personality"],
            "boss_question_types": boss_info["question_types"],
            "boss_hp": self.boss_hp,
            "max_hp": self.MAX_HP,
            "user_hp": self.user_hp,
            "turn_count": self.turn_count,
            "current_question": self.current_question,
            "game_over": self.game_over,
            "victory": self.victory,
            "conversation_length": len(self.conversation_history)
        }

    def is_game_active(self) -> bool:
        """Check if game is currently active (not over)."""
        return not self.game_over

    def has_won(self) -> bool:
        """Check if player has won the game."""
        return self.victory

    def get_conversation_history(self) -> list[Dict]:
        """Get the full conversation history."""
        return self.conversation_history.copy()

    def get_current_boss_info(self) -> Dict[str, str]:
        """Get current boss information."""
        return self.get_boss_info()

    def dump_game_state_to_json(self, filepath: Optional[str] = None) -> str:
        """
        Dump all important game parameters and state to JSON format.
        
        Args:
            filepath: Optional file path to save the JSON. If None, returns JSON string.
            
        Returns:
            JSON string containing all game state data
        """
        boss_info = self.get_boss_info()
        
        game_data = {
            # Game Configuration
            "game_config": {
                "max_level": self.MAX_LEVEL,
                "max_hp": self.MAX_HP,
                "score_range": self.SCORE_RANGE
            },
            
            # Current Game State
            "current_state": {
                "level": self.level,
                "boss_hp": self.boss_hp,
                "user_hp": self.user_hp,
                "turn_count": self.turn_count,
                "current_question": self.current_question,
                "game_over": self.game_over,
                "victory": self.victory
            },
            
            # Boss Information
            "current_boss": {
                "level": self.level,
                "name": boss_info["name"],
            },
        }
        
        json_string = json.dumps(game_data, indent=2, ensure_ascii=False)
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_string)
            print(f"✅ Game state saved to: {filepath}")
        
        return json_string

    def load_game_state_from_json(self, json_data: str) -> bool:
        """
        Load game state from JSON data.
        
        Args:
            json_data: JSON string containing game state data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = json.loads(json_data)
            
            return data
            
        except Exception as e:
            print(f"❌ Error loading game state: {e}")
            return {}


# ==================== EXAMPLE USAGE ====================

def main():
    """Example main game loop - can be used for testing."""
    try:
        game = InterviewBossGame()
        print("🎮 Welcome to Interview Boss Battle!")
        print("Fight your way from Junior to Staff Software Engineer!")
        print("=" * 50)
        print(game.get_status())
        
        print("\nGetting your first question...\n")
        question = game.get_question()
        print(question)
        
        while True:
            user_answer = input("\nEnter your answer: ")
            response = game.submit_answer(user_answer)
            response = response.split("</END_SCORE>")
            response = response[1]
            print(response)
            
            if game.game_over:
                print("Game Over!")
                break
                
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set your ANTHROPIC_API_KEY environment variable.")
    except KeyboardInterrupt:
        print("\n👋 Thanks for playing!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()