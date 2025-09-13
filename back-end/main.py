from interviewoverfitbackend import run_interactive_game

def main():
    """Launch the Interactive Interview Boss Battle Game"""
    try:
        run_interactive_game()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing!")
    except Exception as e:
        print(f"\n❌ Error starting game: {e}")
        print("Make sure you have set the ANTHROPIC_API_KEY environment variable.")

if __name__ == "__main__":
    main()
