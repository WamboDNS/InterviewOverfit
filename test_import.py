#!/usr/bin/env python3
"""Test import to debug the issue."""

import sys
from pathlib import Path

print("Current working directory:", Path.cwd())
print("Python path:", sys.path)

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
print("Adding to path:", src_path)
sys.path.insert(0, str(src_path))

print("Updated Python path:", sys.path)

try:
    print("Attempting to import InterviewBossGame...")
    from model_interaction.model import InterviewBossGame
    print("✅ Import successful!")
    
    print("Attempting to create game instance...")
    game = InterviewBossGame()
    print("✅ Game instance created successfully!")
    
    print("Getting first question...")
    question = game.get_question()
    print("✅ First question:", question[:100] + "...")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
