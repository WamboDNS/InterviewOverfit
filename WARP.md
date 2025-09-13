# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

InterviewOverfit is a gamified technical interview practice application built for HackCMU. The project creates an RPG-style "boss battle" system where users advance through software engineering levels (Junior → Senior → Staff) by answering increasingly difficult technical interview questions.

## Architecture

The project uses a **game state management architecture** centered around the `InterviewBossGame` class:

### Core Components

- **Game Engine (`InterviewBossGame`)**: Manages player progression, health points, level advancement, and win/lose conditions
- **Boss System**: Three distinct AI personalities powered by Anthropic's Claude API:
  - **Level 1 - Senior Developer "Sarah"**: Foundational questions (data structures, algorithms, OOP)
  - **Level 2 - Engineering Manager "Marcus"**: System design and scalability questions  
  - **Level 3 - Staff Engineer "Dr. Chen"**: Architecture and technical leadership questions
- **Scoring System**: Dynamic HP-based combat where answer quality (-10 to +10) affects battle outcomes
- **LLM Integration**: Uses Claude 3.7 Sonnet for generating contextual questions and evaluating responses

### Key Files

- `interviewoverfitbackend.py`: Main game logic and API integration (converted from Colab notebook)
- `InterviewOverfit.ipynb`: Original Jupyter notebook with game development
- `main.py`: Simple entry point for the application
- `model-backend.ipynb`: Contains API key configuration

## Development Commands

### Environment Setup
```bash
# Ensure Python 3.13 is active (managed via pyenv)
python --version  # Should show 3.13.x

# Install dependencies
pip install anthropic
```

### Running the Application
```bash
# Run main application
python main.py

# Run the game backend directly
python interviewoverfitbackend.py

# Run Jupyter notebooks for development/testing
jupyter notebook InterviewOverfit.ipynb
jupyter notebook model-backend.ipynb
```

### Development Workflow
```bash
# Check for API key issues (common problem)
python -c "import anthropic; print('API client can be imported')"

# Test individual game components
python -c "from interviewoverfitbackend import InterviewBossGame; game = InterviewBossGame(); print(game.get_status())"
```

## Important Development Notes

### API Key Management
- **CRITICAL**: The project contains hardcoded Anthropic API keys that must be replaced with environment variables for production
- Keys are present in both `interviewoverfitbackend.py` and `model-backend.ipynb`
- Use environment variable `ANTHROPIC_API_KEY` instead of hardcoding

### Game State Persistence
- Current implementation loses all progress on restart
- Game state is managed entirely in memory via the `InterviewBossGame` class
- Consider adding persistence layer for production deployment

### LLM Response Parsing
- The `parse_score()` function uses regex to extract scores from Claude responses
- This is fragile and may break if Claude's response format changes
- Monitor for parsing errors when testing

### Testing Considerations
- No formal test suite exists - manual testing through game interaction required
- Test each boss level progression to ensure HP calculations work correctly
- Verify score parsing with various Claude response formats
- Test edge cases like invalid answers, network errors, and API rate limits

## Project Structure Patterns

The codebase follows a **notebook-to-script** development pattern:
1. Initial development in Jupyter notebooks (`InterviewOverfit.ipynb`) 
2. Conversion to standalone Python scripts (`interviewoverfitbackend.py`)
3. Simple application entry points (`main.py`)

This pattern suggests the project was prototyped for a hackathon environment where rapid iteration was prioritized over traditional software architecture.
