# -*- coding: utf-8 -*-


import anthropic
import re
import random
import os
from typing import Dict, List, Tuple
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable for security
api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable not set. Please create a .env file with your Anthropic API key.")

client = anthropic.Anthropic(api_key=api_key)

# System prompt template
SYSTEM_PROMPT = """You are the Interview Boss Battle Master!

GAME RULES:
- Player starts as Junior Software Engineer (Level 1) and must defeat bosses to advance
- 3 Levels: Junior SWE → Senior SWE → Staff SWE
- Each level has a unique boss with different personality and question difficulty
- After each user answer, you MUST respond in this exact format:

First Line: <score< SCORE </score> where SCORE from -10 to +10 (e.g., "+7" or "-3")
After that: </END_SCORE>
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

def get_boss_info(level: int) -> Dict[str, str]:
    """Get boss information for current level"""
    bosses = {
        1: {
            "name": "Senior Developer Sarah",
            "personality": "Encouraging mentor who focuses on fundamentals",
            "question_types": ["Data structures", "Basic algorithms", "OOP concepts", "Code review"]
        },
        2: {
            "name": "Engineering Manager Marcus",
            "personality": "Business-focused leader who cares about scalability",
            "question_types": ["System design", "Database design", "API design", "Performance optimization"]
        },
        3: {
            "name": "Staff Engineer Dr. Chen",
            "personality": "Brilliant architect who expects excellence",
            "question_types": ["Distributed systems", "Technical leadership", "Architecture decisions", "Complex problem solving"]
        }
    }
    return bosses.get(level, bosses[1])

def create_game_state_prompt(level: int, boss_hp: int, user_hp: int, turn_count: int) -> str:
    """Create the current game state prompt"""
    boss_info = get_boss_info(level)

    return f"""
CURRENT GAME STATE:
Level: {level}/3
Boss: {boss_info['name']} (HP: {boss_hp}/100)
Your HP: {user_hp}/100
Turn: {turn_count}

Boss Personality: {boss_info['personality']}
Question Focus: {', '.join(boss_info['question_types'])}

You are currently {boss_info['name']}. Ask an appropriate interview question for this level and maintain your character throughout the interaction.
"""

def parse_score(response: str) -> Tuple[int, str]:
    """Parse the score from the first line of the response"""
    lines = response.strip().split('\n')
    if not lines:
        return 0, response

    first_line = lines[0].strip()

    # Extract score using regex
    score_match = re.search(r'([+-]?\d+)', first_line)
    if score_match:
        score = int(score_match.group(1))
        # Clamp score to valid range
        score = max(-10, min(10, score))

        # Get feedback (everything after first line)
        feedback = '\n'.join(lines[1:]).strip() if len(lines) > 1 else "No feedback provided."
        return score, feedback
    else:
        return 0, response

class InterviewBossGame:
    def __init__(self):
        self.level = 1
        self.boss_hp = 100
        self.user_hp = 100
        self.turn_count = 0
        self.current_question = ""
        self.game_over = False
        self.victory = False

    def reset_game(self):
        """Reset game to initial state"""
        self.level = 1
        self.boss_hp = 100
        self.user_hp = 100
        self.turn_count = 0
        self.current_question = ""
        self.game_over = False
        self.victory = False
        print("🔄 Game Reset! Starting as Junior Software Engineer...")

    def advance_level(self):
        """Advance to next level"""
        if self.level < 3:
            self.level += 1
            self.boss_hp = 100  # Reset boss HP
            self.turn_count = 0
            boss_info = get_boss_info(self.level)
            print(f"🎉 Level Up! Now facing {boss_info['name']} at Level {self.level}")
        else:
            self.victory = True
            self.game_over = True
            print("🏆 VICTORY! You've become a Staff Software Engineer!")

    def get_question(self) -> str:
        """Get a new question from the current boss"""
        if self.game_over:
            return "Game Over! Type 'reset' to play again."

        game_state = create_game_state_prompt(self.level, self.boss_hp, self.user_hp, self.turn_count)

        full_prompt = SYSTEM_PROMPT + "\n\n" + game_state + "\n\nAsk the candidate an interview question appropriate for this level."

        try:
            message = client.messages.create(
                model="claude-3-7-sonnet-20250219",  # Updated model name
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": full_prompt}
                ]
            )

            question = message.content[0].text
            self.current_question = question
            return question

        except Exception as e:
            return f"Error getting question: {e}"

    def submit_answer(self, user_answer: str) -> str:
        """Submit user answer and get feedback"""
        if self.game_over:
            if user_answer.lower() == 'reset':
                self.reset_game()
                return self.get_question()
            return "Game Over! Type 'reset' to play again."

        if not self.current_question:
            return "No question asked yet. Get a question first!"

        # Create evaluation prompt
        game_state = create_game_state_prompt(self.level, self.boss_hp, self.user_hp, self.turn_count)
        evaluation_prompt = f"""
{SYSTEM_PROMPT}

{game_state}

QUESTION ASKED: {self.current_question}
USER ANSWER: {user_answer}

Evaluate this answer and respond as {get_boss_info(self.level)['name']}. Remember:
- First line must be score (-10 to +10)
- Then provide character-appropriate feedback
"""

        try:
            message = client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": evaluation_prompt}
                ]
            )

            response = message.content[0].text
            score, feedback = parse_score(response)

            # Update HP based on score
            if score > 0:
                self.boss_hp -= score * 20  # Positive score damages boss
                result_msg = f"💥 Boss takes {score * 2} damage!"
            elif score < 0:
                self.user_hp += score * 3  # Negative score damages user (score is negative)
                result_msg = f"😵 You take {abs(score * 3)} damage!"
            else:
                result_msg = "⚡ No damage dealt!"

            self.turn_count += 1

            # Check win/lose conditions
            status_msg = ""
            if self.boss_hp <= 0:
                self.advance_level()
                if not self.victory:
                    status_msg = "\n🎯 Boss defeated! Moving to next level..."
            elif self.user_hp <= 0:
                self.reset_game()
                status_msg = "\n💀 You were defeated! Game restarted..."

            # Format response
            response_text = f"""
SCORE: {score:+d}

{feedback}

{result_msg}
Boss HP: {max(0, self.boss_hp)}/100 | Your HP: {max(0, self.user_hp)}/100{status_msg}
"""
            return response_text

        except Exception as e:
            return f"Error evaluating answer: {e}"

    def get_status(self) -> str:
        """Get current game status"""
        boss_info = get_boss_info(self.level)
        return f"""
📊 GAME STATUS 📊
Level: {self.level}/3
Current Boss: {boss_info['name']}
Boss HP: {self.boss_hp}/100
Your HP: {self.user_hp}/100
Turn: {self.turn_count}
"""

def print_help():
    """Display help information for the user"""
    print("""
🎮 INTERVIEW BOSS BATTLE COMMANDS:

📝 BASIC COMMANDS:
  question          - Get a new interview question
  answer <text>     - Submit your answer to the current question
  status            - Show current game status (HP, level, boss)
  reset             - Reset the game to start over
  help              - Show this help message
  quit              - Exit the game

💡 TIPS:
  - Answer questions thoroughly to deal more damage to the boss
  - Poor answers will damage your HP
  - Defeat 3 bosses to become a Staff Software Engineer!
  - Each boss has different personality and question types

🏆 LEVELS:
  Level 1: Senior Developer Sarah (Fundamentals)
  Level 2: Engineering Manager Marcus (System Design)
  Level 3: Staff Engineer Dr. Chen (Architecture & Leadership)
""")

def run_interactive_game():
    """Run the interactive chat version of the game"""
    game = InterviewBossGame()
    
    print("🎮 Welcome to Interview Boss Battle!")
    print("Fight your way from Junior to Staff Software Engineer!")
    print("Type 'help' for commands or 'question' to start!")
    print("=" * 50)
    print(game.get_status())
    print("\nType your command: ", end="")
    
    current_question = None
    
    while True:
        try:
            user_input = input().strip()
            
            if not user_input:
                print("Please enter a command. Type 'help' for available commands.")
                print("\nType your command: ", end="")
                continue
                
            # Parse command
            parts = user_input.split(' ', 1)
            command = parts[0].lower()
            
            if command == 'quit' or command == 'exit':
                print("\n👋 Thanks for playing Interview Boss Battle!")
                break
                
            elif command == 'help':
                print_help()
                
            elif command == 'status':
                print("\n" + game.get_status())
                
            elif command == 'reset':
                game.reset_game()
                current_question = None
                print("\n" + game.get_status())
                
            elif command == 'question':
                if game.game_over:
                    print("\n❌ Game is over! Type 'reset' to start a new game.")
                else:
                    print("\n🤖 Getting your question...")
                    question = game.get_question()
                    current_question = question
                    print("\n" + "="*60)
                    print("BOSS QUESTION:")
                    print(question)
                    print("="*60)
                    
            elif command == 'answer':
                if len(parts) < 2:
                    print("\n❌ Please provide your answer. Usage: answer <your answer>")
                elif not current_question:
                    print("\n❌ No question asked yet! Type 'question' to get a question first.")
                elif game.game_over:
                    print("\n❌ Game is over! Type 'reset' to start a new game.")
                else:
                    answer_text = parts[1]
                    print("\n🤖 Evaluating your answer...")
                    response = game.submit_answer(answer_text)
                    print("\n" + "="*60)
                    print("BOSS FEEDBACK:")
                    print(response)
                    print("="*60)
                    
                    # Clear current question after answering
                    current_question = None
                    
                    # Show what to do next
                    if game.game_over:
                        if game.victory:
                            print("\n🎉 CONGRATULATIONS! You've won the game!")
                        print("\n💡 Type 'reset' to play again or 'quit' to exit.")
                    else:
                        print("\n💡 Type 'question' to get the next question.")
                        
            else:
                print(f"\n❌ Unknown command: '{command}'")
                print("Type 'help' to see available commands.")
                
            print("\nType your command: ", end="")
            
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for playing Interview Boss Battle!")
            break
        except EOFError:
            print("\n\n👋 Thanks for playing Interview Boss Battle!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("\nType your command: ", end="")

if __name__ == "__main__":
    run_interactive_game()
