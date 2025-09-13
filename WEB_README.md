# 🎮 Interview Boss Battle - Web Interface

A gamified interview preparation system that turns technical interviews into an RPG-style boss battle game!

## 🚀 Quick Start

### 1. Set up your API Key (Optional)
```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key-here"
```

### 2. Start the Server
```bash
python run_server.py
```

### 3. Open in Browser
Navigate to: **http://localhost:8000**

## 🎯 How to Play

1. **Start the Game**: Click "Start Battle!" to begin your journey
2. **Answer Questions**: Each boss will ask interview questions appropriate to their level
3. **Get Feedback**: Receive scores (-10 to +10) and detailed feedback
4. **Progress**: Defeat bosses to advance through levels
5. **Win**: Become a Staff Software Engineer by defeating all bosses!

## 🏆 Boss Levels

- **Level 1 - Senior Developer Sarah**: Fundamentals, data structures, algorithms
- **Level 2 - Engineering Manager Marcus**: System design, scalability, business focus  
- **Level 3 - Staff Engineer Dr. Chen**: Architecture, technical leadership, complex problems

## 🎮 Game Features

- **Real-time HP System**: Your answers affect both your HP and the boss's HP
- **Continuous Conversation**: The AI remembers your entire interview session
- **Progressive Difficulty**: Questions get harder as you advance levels
- **Detailed Feedback**: Get explanations and correct answers for each question
- **Character Consistency**: Each boss has a unique personality and expertise

## 🔧 API Endpoints

The web interface uses these REST API endpoints:

- `POST /game/{uid}/start` - Start a new game
- `POST /game/{uid}/answer` - Submit an answer
- `GET /game/{uid}/question` - Get next question
- `GET /game/{uid}/status` - Get game status
- `POST /game/{uid}/reset` - Reset game
- `DELETE /game/{uid}` - End game

## 🛠️ Development

### Project Structure
```
├── src/
│   ├── app/
│   │   └── app.py          # FastAPI application
│   └── model_interaction/
│       └── model.py        # InterviewBossGame class
├── web/
│   └── index.html          # Web interface
├── run_server.py           # Startup script
└── WEB_README.md           # This file
```

### Running in Development
```bash
# Start with auto-reload
python run_server.py

# Or use uvicorn directly
uvicorn src.app.app:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation
Visit **http://localhost:8000/docs** for interactive API documentation.

## 🎨 Web Interface Features

- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Game state updates automatically
- **Keyboard Shortcuts**: Ctrl+Enter to submit answers
- **API Key Management**: Save your API key locally
- **Error Handling**: Clear error messages and loading states
- **Game Statistics**: Live HP, level, and turn tracking

## 🔒 Security Notes

- API keys are stored locally in browser storage
- CORS is enabled for development (configure for production)
- Game instances are stored in memory (use Redis for production)

## 🚀 Production Deployment

For production deployment:

1. **Set up proper CORS origins** in `app.py`
2. **Use Redis or database** for game instance storage
3. **Add authentication** and user management
4. **Set up HTTPS** and proper security headers
5. **Use environment variables** for configuration

## 🎯 Tips for Success

- **Think out loud**: Explain your reasoning process
- **Consider edge cases**: Mention error handling and scalability
- **Ask clarifying questions**: Show you understand the problem
- **Use examples**: Provide concrete examples when possible
- **Be honest**: It's okay to say "I don't know" and ask for hints

## 🐛 Troubleshooting

### Common Issues

1. **"API call failed"**: Check your Anthropic API key
2. **"No active game found"**: Start a new game
3. **CORS errors**: Make sure the server is running on the correct port
4. **Game not loading**: Check browser console for JavaScript errors

### Getting Help

- Check the browser console for error messages
- Verify your API key is valid
- Ensure the server is running on port 8000
- Try refreshing the page or starting a new game

---

**Happy coding and good luck with your interviews! 🎮✨**
