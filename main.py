#!/usr/bin/env python3
"""
Command-line interface for Interview Boss Battle game.
"""

import os
import sys
import argparse
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from model_interaction.model import InterviewBossGame


class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_colored(text: str, color: str = Colors.WHITE) -> None:
    """Print colored text to terminal."""
    print(f"{color}{text}{Colors.END}")


def print_header() -> None:
    """Print the game header."""
    print_colored("=" * 60, Colors.CYAN)
    print_colored("🎮 INTERVIEW BOSS BATTLE", Colors.BOLD + Colors.MAGENTA)
    print_colored("Fight your way from Junior to Staff Software Engineer!", Colors.YELLOW)
    print_colored("=" * 60, Colors.CYAN)
    print()


def print_boss_info(boss_info: dict) -> None:
    """Print boss information."""
    print_colored(f"👹 BOSS: {boss_info['name']}", Colors.RED + Colors.BOLD)
    print_colored(f"💭 Personality: {boss_info['personality']}", Colors.YELLOW)
    print_colored(f"📚 Focus Areas: {', '.join(boss_info['question_types'])}", Colors.BLUE)
    print()


def print_game_status(game: InterviewBossGame) -> None:
    """Print current game status."""
    state = game.get_game_state()
    print_colored("📊 GAME STATUS", Colors.BOLD + Colors.CYAN)
    print_colored("-" * 30, Colors.CYAN)
    print_colored(f"Level: {state['level']}/{state['max_level']}", Colors.WHITE)
    print_colored(f"Boss: {state['boss_name']}", Colors.RED)
    print_colored(f"Boss HP: {state['boss_hp']}/{state['max_hp']}", Colors.RED)
    print_colored(f"Your HP: {state['user_hp']}/{state['max_hp']}", Colors.GREEN)
    print_colored(f"Turn: {state['turn_count']}", Colors.YELLOW)
    print()


def print_question(question: str) -> None:
    """Print the current question."""
    print_colored("❓ QUESTION", Colors.BOLD + Colors.BLUE)
    print_colored("-" * 20, Colors.BLUE)
    print_colored(question, Colors.WHITE)
    print()


def print_response(response: str) -> None:
    """Print the boss response."""
    print_colored("📝 BOSS RESPONSE", Colors.BOLD + Colors.MAGENTA)
    print_colored("-" * 25, Colors.MAGENTA)
    print_colored(response, Colors.WHITE)
    print()


def print_commands() -> None:
    """Print available commands."""
    print_colored("💡 COMMANDS", Colors.BOLD + Colors.YELLOW)
    print_colored("-" * 15, Colors.YELLOW)
    print_colored("• Type your answer and press Enter to submit", Colors.WHITE)
    print_colored("• Type 'status' to see game status", Colors.WHITE)
    print_colored("• Type 'history' to see conversation history", Colors.WHITE)
    print_colored("• Type 'reset' to start a new game", Colors.WHITE)
    print_colored("• Type 'quit' or 'exit' to end the game", Colors.WHITE)
    print_colored("• Type 'help' to see this help", Colors.WHITE)
    print()


def print_conversation_history(game: InterviewBossGame) -> None:
    """Print conversation history."""
    history = game.get_conversation_history()
    print_colored("📜 CONVERSATION HISTORY", Colors.BOLD + Colors.CYAN)
    print_colored("-" * 30, Colors.CYAN)
    
    if not history:
        print_colored("No conversation history yet.", Colors.YELLOW)
        return
    
    for i, message in enumerate(history[-10:], 1):  # Show last 10 messages
        role_color = Colors.GREEN if message['role'] == 'assistant' else Colors.BLUE
        role_icon = "🤖" if message['role'] == 'assistant' else "👤"
        
        print_colored(f"{i}. {role_icon} {message['role'].upper()}:", role_color)
        content = message['content'][:100] + "..." if len(message['content']) > 100 else message['content']
        print_colored(f"   {content}", Colors.WHITE)
        print()


def handle_command(game: InterviewBossGame, command: str) -> bool:
    """Handle special commands. Returns True if command was handled."""
    command = command.lower().strip()
    
    if command in ['quit', 'exit']:
        print_colored("👋 Thanks for playing! Good luck with your interviews!", Colors.GREEN)
        return True
    
    elif command == 'status':
        print_game_status(game)
        return True
    
    elif command == 'history':
        print_conversation_history(game)
        return True
    
    elif command == 'reset':
        print_colored("🔄 Resetting game...", Colors.YELLOW)
        game.reset_game()
        question = game.get_question()
        print_question(question)
        return True
    
    elif command == 'help':
        print_commands()
        return True
    
    return False


def play_game(api_key: str = None) -> None:
    """Main game loop."""
    try:
        # Initialize game
        game = InterviewBossGame(api_key=api_key)
        
        # Get first question
        question = game.get_question()
        print_question(question)
        
        # Main game loop
        while True:
            try:
                # Get user input
                user_input = input(f"{Colors.CYAN}💭 Your answer: {Colors.END}").strip()
                
                # Handle empty input
                if not user_input:
                    print_colored("Please enter an answer or command.", Colors.YELLOW)
                    continue
                
                # Handle special commands
                if handle_command(game, user_input):
                    if user_input.lower() in ['quit', 'exit']:
                        break
                    continue
                
                # Submit answer
                print_colored("🔄 Processing your answer...", Colors.YELLOW)
                response = game.submit_answer(user_input)
                response = response.split("</END_SCORE>")
                response = response[1].strip()
                print_response(response)
                
                # Check if game is over
                if game.game_over:
                    if game.has_won():
                        print_colored("🏆 VICTORY! You've become a Staff Software Engineer!", Colors.GREEN + Colors.BOLD)
                    else:
                        print_colored("💀 DEFEAT! You were defeated by the boss!", Colors.RED + Colors.BOLD)
                    
                    print_colored("\n🎮 Game Over! Thanks for playing!", Colors.CYAN)
                    break
                
            except KeyboardInterrupt:
                print_colored("\n\n👋 Game interrupted. Thanks for playing!", Colors.YELLOW)
                break
            except Exception as e:
                print_colored(f"❌ Error: {e}", Colors.RED)
                print_colored("Please try again or type 'quit' to exit.", Colors.YELLOW)
    
    except Exception as e:
        print_colored(f"❌ Failed to initialize game: {e}", Colors.RED)
        print_colored("Please check your API key and try again.", Colors.YELLOW)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Interview Boss Battle - Gamified interview preparation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Play with environment API key
  python main.py --api-key YOUR_KEY        # Play with specific API key
  python main.py --help                    # Show this help message
        """
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        help='Anthropic API key (optional, can use ANTHROPIC_API_KEY env var)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Interview Boss Battle 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Print header
    print_header()
    
    # Check API key
    api_key = args.api_key or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print_colored("⚠️  Warning: No API key provided.", Colors.YELLOW)
        print_colored("   You can set ANTHROPIC_API_KEY environment variable", Colors.WHITE)
        print_colored("   or use --api-key argument.", Colors.WHITE)
        print_colored("   The game will prompt for an API key if needed.", Colors.WHITE)
        print()
    
    # Print game info
    print_colored("🎯 GAME OBJECTIVE", Colors.BOLD + Colors.GREEN)
    print_colored("-" * 20, Colors.GREEN)
    print_colored("Defeat 3 interview bosses to become a Staff Software Engineer!", Colors.WHITE)
    print()
    
    print_colored("👹 BOSSES", Colors.BOLD + Colors.RED)
    print_colored("-" * 10, Colors.RED)
    print_colored("Level 1: Senior Developer Sarah - Fundamentals & Algorithms", Colors.WHITE)
    print_colored("Level 2: Engineering Manager Marcus - System Design & Business", Colors.WHITE)
    print_colored("Level 3: Staff Engineer Dr. Chen - Architecture & Leadership", Colors.WHITE)
    print()
    
    print_commands()
    
    # Start game
    try:
        play_game(api_key)
    except KeyboardInterrupt:
        print_colored("\n👋 Goodbye!", Colors.CYAN)
    except Exception as e:
        print_colored(f"❌ Unexpected error: {e}", Colors.RED)
        sys.exit(1)


if __name__ == "__main__":
    main()
