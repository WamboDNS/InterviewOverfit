# InterviewOverfit Boss Battle - Full Stack Integration 🎮

A gamified interview preparation system where users battle AI-powered bosses to level up their technical interview skills.

## 🏗️ Architecture Overview

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│  React Frontend │◄──────────────►│  FastAPI Backend │
│  (Port 5173)    │                 │   (Port 8000)    │
├─────────────────┤                 ├─────────────────┤
│ • UI Components │                 │ • Game Logic    │
│ • API Service   │                 │ • Boss AI       │
│ • Game State    │                 │ • Score System  │
└─────────────────┘                 └─────────────────┘
                                             │
                                    ┌─────────────────┐
                                    │ Anthropic API   │
                                    │ (Claude 3.5)    │
                                    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** (required by project configuration)
- **Node.js 18+** and **pnpm** (for frontend)
- **uv** (Python package manager)
- **Anthropic API key** (for AI-powered boss battles)

### Installation & Setup

1. **Clone and navigate to the project:**
   ```bash
   cd /path/to/InterviewOverfit
   ```

2. **Set up environment (optional but recommended):**
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

3. **Start the development environment:**
   ```bash
   ./start_dev.sh
   ```

4. **Open the game:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🎮 Game Flow

1. **Role Selection:** Choose your engineering level (currently SDE)
2. **Level Map:** Select a boss battle difficulty
3. **Boss Battle:** Enter API key and start fighting!
4. **Combat System:**
   - Boss asks technical interview questions
   - You provide answers
   - AI evaluates and deals/receives damage
   - Progress through 3 levels to become Staff Engineer

## 🏢 Boss Lineup

| Level | Boss | Personality | Question Types |
|-------|------|-------------|----------------|
| 1 | **Senior Developer Sarah** | Encouraging mentor | Data structures, Basic algorithms, OOP |
| 2 | **Engineering Manager Marcus** | Business-focused | System design, Databases, APIs |
| 3 | **Staff Engineer Dr. Chen** | Excellence-demanding | Distributed systems, Architecture |

## 🔧 Development Tools

### Backend (FastAPI + Python)

```bash
# Backend structure
back-end/
├── app.py              # Main FastAPI application
├── pyproject.toml      # Python dependencies (uv)
└── .venv/             # Virtual environment

# Key endpoints
POST /api/game/{uid}/start     # Start new game
POST /api/game/{uid}/answer    # Submit answer
GET  /api/game/{uid}/question  # Get current question
GET  /api/game/{uid}/status    # Get game state
```

### Frontend (React + TypeScript)

```bash
# Frontend structure
frontend/
├── src/
│   ├── components/        # UI components
│   ├── services/api.ts   # Backend integration
│   ├── types/           # TypeScript definitions
│   └── App.tsx          # Main app component
├── package.json         # Node dependencies (pnpm)
└── vite.config.ts      # Vite configuration
```

### API Integration Layer

The `frontend/src/services/api.ts` provides a complete TypeScript API client:

```typescript
import { api } from './services/api';

// Start a game
const response = await api.startGame(apiKey);

// Submit an answer  
const result = await api.submitAnswer("Your answer here");

// Get game status
const status = await api.getGameStatus();
```

## 🧪 Testing

### Run Integration Tests

```bash
# Test the complete integration
python test_integration.py
```

### Manual Testing

```bash
# Test backend health
curl http://localhost:8000/health

# Test API info
curl http://localhost:8000/api/info

# Test game start (will need API key)
curl -X POST http://localhost:8000/api/game/test-user/start \
  -H "Content-Type: application/json" \
  -d '{"api_key": "your-key"}'
```

## 📋 Scripts & Commands

| Command | Description |
|---------|-------------|
| `./start_dev.sh` | Start both frontend and backend servers |
| `python test_integration.py` | Run integration tests |
| `python test_api.py` | Test backend functionality |

### Backend Commands (in `back-end/` directory)

```bash
# Install dependencies
uv pip install -e .

# Run server
uv run python app.py

# Check virtual environment
source .venv/bin/activate
```

### Frontend Commands (in `frontend/` directory)

```bash
# Install dependencies
pnpm install

# Start development server
pnpm run dev

# Build for production
pnpm run build

# Type check
pnpm run type-check
```

## 🔐 API Key Setup

The game requires an Anthropic API key to power the AI bosses. You can provide it:

1. **Environment variable:** `export ANTHROPIC_API_KEY="your-key"`
2. **In-game prompt:** The UI will ask for your key when starting
3. **Direct API call:** Pass `api_key` in the request body

## 🎯 Game Mechanics

### Scoring System

- **+8 to +10:** Exceptional answer (major boss damage)
- **+5 to +7:** Good answer (solid damage)  
- **+1 to +4:** Acceptable answer (minor damage)
- **0:** Neutral (no damage)
- **-1 to -7:** Poor answer (you take damage)
- **-8 to -10:** Terrible answer (major damage to you)

### Health System

- Both player and boss start with 100 HP
- Positive scores damage the boss
- Negative scores damage the player
- First to 0 HP loses the battle

### Victory Conditions

- **Defeat all 3 bosses:** Become Staff Software Engineer! 🏆
- **Lose all HP:** Game over, but you can retry
- **Level progression:** Each victory unlocks the next boss

## 🛠️ Troubleshooting

### Common Issues

1. **"API key required" error:**
   - Set `ANTHROPIC_API_KEY` environment variable
   - Or enter it in the game UI

2. **Backend won't start:**
   - Check Python version (3.13+ recommended)
   - Run: `cd back-end && uv pip install -e .`
   - Check logs: `tail -f back-end/backend.log`

3. **Frontend won't load:**
   - Check Node.js version (18+)
   - Run: `cd frontend && pnpm install`
   - Check logs: `tail -f frontend/frontend.log`

4. **CORS errors:**
   - Backend automatically allows localhost:5173
   - Check that both servers are running

### Debug Mode

```bash
# Backend logs
tail -f back-end/backend.log

# Frontend logs  
tail -f frontend/frontend.log

# Test connectivity
curl http://localhost:8000/health
curl http://localhost:5173
```

## 🎊 Success Indicators

When everything is working correctly, you should see:

1. **Backend:** `✅ Backend server is running at http://localhost:8000`
2. **Frontend:** `✅ Frontend server is running at http://localhost:5173`
3. **Integration test:** All tests passing
4. **In browser:** Game loads, shows role selection, accepts API key

## 🔮 Next Steps

The game is now fully integrated! You can:

1. **Play the game:** Test your interview skills against AI bosses
2. **Extend functionality:** Add more bosses, question types, or game modes
3. **Deploy:** The architecture supports easy deployment to cloud platforms
4. **Customize:** Modify the scoring system, add achievements, etc.

---

**Happy coding and good luck with your boss battles! 🚀**
