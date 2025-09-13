#!/usr/bin/env python3
"""
Example usage of the InterviewBossGame class.
This demonstrates how to use the game as a modular component.
"""

import os
from src.model_interaction.model import InterviewBossGame


def simple_game_example():
    """Simple example of using the game class."""
    try:
        # Initialize the game
        game = InterviewBossGame()
        
        print("🎮 Welcome to Interview Boss Battle!")
        print("=" * 50)
        
        # Get initial status
        print(game.get_status())
        
        # Get first question
        print("\nGetting your first question...\n")
        question = game.get_question()
        print(f"Question: {question}")
        
        # Example answers
        example_answers = [
            "I would use a hash map to store key-value pairs for O(1) lookup time.",
            "For system design, I'd consider scalability, reliability, and performance.",
            "I'm not sure about this one, could you give me a hint?"
        ]
        
        # Simulate a few turns
        for i, answer in enumerate(example_answers):
            if not game.is_game_active():
                break
                
            print(f"\n--- Turn {i+1} ---")
            print(f"Answer: {answer}")
            
            response = game.submit_answer(answer)
            print(f"Response: {response}")
            
            # Get game state for programmatic access
            state = game.get_game_state()
            print(f"Game State: Level {state['level']}, Boss HP: {state['boss_hp']}, User HP: {state['user_hp']}")
            
            if game.is_game_active():
                next_question = game.get_question()
                print(f"Next Question: {next_question}")
        
        # Final status
        if game.has_won():
            print("\n🏆 Congratulations! You won!")
        else:
            print(f"\nGame ended. Final status: {game.get_status()}")
            
    except Exception as e:
        print(f"Error: {e}")


def programmatic_game_example():
    """Example of using the game programmatically without user input."""
    try:
        game = InterviewBossGame()
        
        # Get initial state
        initial_state = game.get_game_state()
        print(f"Initial state: {initial_state}")
        
        # Get first question
        question = game.get_question()
        print(f"First question: {question}")
        
        # Submit an answer
        response = game.submit_answer("I would use a binary search tree for this problem.")
        print(f"Response: {response}")
        
        # Check conversation history
        history = game.get_conversation_history()
        print(f"Conversation has {len(history)} messages")
        
        # Get current boss info
        boss_info = game.get_current_boss_info()
        print(f"Current boss: {boss_info['name']}")
        
    except Exception as e:
        print(f"Error: {e}")


def interactive_game_example():
    """Interactive example with user input."""
    try:
        game = InterviewBossGame()
        
        print("🎮 Interactive Interview Boss Battle!")
        print("Type 'quit' to exit, 'status' for game status, 'history' for conversation history")
        print("=" * 60)
        
        # Get first question
        question = game.get_question()
        print(f"\n{question}")
        
        while game.is_game_active():
            user_input = input("\nYour answer (or command): ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'status':
                print(game.get_status())
                continue
            elif user_input.lower() == 'history':
                history = game.get_conversation_history()
                print(f"Conversation has {len(history)} messages")
                for i, msg in enumerate(history[-5:]):  # Show last 5 messages
                    print(f"{i+1}. {msg['role']}: {msg['content'][:100]}...")
                continue
            elif not user_input:
                continue
            
            # Submit answer
            response = game.submit_answer(user_input)
            print(f"\n{response}")
            
            if game.is_game_active():
                next_question = game.get_question()
                print(f"\n{next_question}")
        
        if game.has_won():
            print("\n🏆 Congratulations! You've become a Staff Software Engineer!")
        else:
            print("\nThanks for playing!")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("Choose an example:")
    print("1. Simple game example")
    print("2. Programmatic game example") 
    print("3. Interactive game example")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        simple_game_example()
    elif choice == "2":
        programmatic_game_example()
    elif choice == "3":
        interactive_game_example()
    else:
        print("Invalid choice. Running simple example...")
        simple_game_example()
