# 🎮 Interview Boss Battle - Modern Frontend

A beautiful, modern frontend for the Interview Boss Battle gamified interview preparation system, built with **Streamlit** and state-of-the-art Python web technologies.

## ✨ Features

### 🎨 Modern UI/UX
- **Beautiful Design**: Custom CSS with gradients, animations, and modern styling
- **Responsive Layout**: Works perfectly on desktop and mobile devices
- **Interactive Elements**: Smooth animations and hover effects
- **Real-time Updates**: Live game state synchronization with the backend

### 🎮 Game Features
- **Boss Battle Interface**: Visual representation of boss and player health
- **Progress Tracking**: Level progression, turn counting, and conversation metrics
- **Interactive Q&A**: Clean question display and answer submission
- **Feedback System**: Color-coded feedback with scores and detailed responses
- **Conversation History**: Full chat history with expandable view
- **Game Statistics**: Comprehensive metrics and progress visualization

### 🔧 Technical Features
- **Backend Integration**: Seamless API communication with FastAPI backend
- **Error Handling**: Graceful error handling with user-friendly messages
- **Configuration**: Easy user ID and API key management
- **Health Monitoring**: Backend connection status checking
- **Session Management**: Persistent game state across interactions

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- Backend running on `http://localhost:8000`

### Installation

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Start the backend** (in a separate terminal):
   ```bash
   uv run uvicorn src.app.app:app --reload
   ```

3. **Start the frontend**:
   ```bash
   python start_streamlit.py
   ```

   Or manually:
   ```bash
   uv run streamlit run streamlit_app.py
   ```

4. **Open your browser** to `http://localhost:8501`

## 🎯 How to Play

### Getting Started
1. **Configure**: Set your User ID and optional API key in the sidebar
2. **Start Game**: Click "Start Game" to begin your interview battle
3. **Answer Questions**: Read the boss's questions and provide thoughtful answers
4. **Get Feedback**: Receive scores and feedback on your responses
5. **Level Up**: Defeat bosses to progress through levels

### Game Controls
- **🚀 Start Game**: Begin a new interview battle
- **🔄 Reset Game**: Restart the current game
- **🗑️ End Game**: Stop and clean up the current game
- **❓ Get Next Question**: Request the next question from the boss

### UI Elements
- **Boss Card**: Shows boss information, level, and health
- **Player Card**: Displays your health and turn information
- **Progress Charts**: Visual progress indicators and statistics
- **Question Box**: Current boss question with answer input
- **Feedback Display**: Color-coded feedback with scores
- **Conversation History**: Expandable chat history

## 🛠️ Configuration

### Environment Variables
- `BACKEND_URL`: Backend API URL (default: `http://localhost:8000`)
- `DEFAULT_USER_ID`: Default user identifier (default: `demo-user`)

### Customization
The frontend uses custom CSS for styling. You can modify the appearance by editing the CSS in `streamlit_app.py`:

```python
# Custom CSS for modern styling
st.markdown("""
<style>
    /* Your custom styles here */
</style>
""", unsafe_allow_html=True)
```

## 📊 API Integration

The frontend integrates with the following backend endpoints:

- `GET /health` - Backend health check
- `GET /api/info` - API information
- `POST /game/{uid}/start` - Start new game
- `POST /game/{uid}/answer` - Submit answer
- `GET /game/{uid}/question` - Get next question
- `GET /game/{uid}/status` - Get game status
- `POST /game/{uid}/reset` - Reset game
- `DELETE /game/{uid}` - End game
- `GET /game/{uid}/history` - Get conversation history

## 🎨 UI Components

### Status Cards
- **Boss Card**: Red gradient with boss information and health bar
- **Player Card**: Teal gradient with player stats and health bar
- **Progress Container**: White cards with progress indicators

### Interactive Elements
- **HP Bars**: Animated health bars with percentage display
- **Question Box**: Purple gradient box for boss questions
- **Feedback Cards**: Color-coded feedback (green=positive, red=negative, yellow=neutral)
- **Buttons**: Gradient buttons with hover effects

### Charts and Visualizations
- **Progress Bars**: Level progression indicators
- **Metrics**: Real-time statistics display
- **Game Status**: Visual game state representation

## 🔧 Troubleshooting

### Common Issues

1. **Backend Connection Error**:
   ```
   Connection Error: Could not connect to backend
   ```
   **Solution**: Make sure the backend is running on `http://localhost:8000`

2. **Dependencies Missing**:
   ```
   ModuleNotFoundError: No module named 'streamlit'
   ```
   **Solution**: Run `uv sync` to install dependencies

3. **Port Already in Use**:
   ```
   Port 8501 is already in use
   ```
   **Solution**: Kill existing Streamlit processes or use a different port

### Debug Mode
Run with debug information:
```bash
uv run streamlit run streamlit_app.py --logger.level debug
```

### Manual Backend Start
If the automatic backend start fails:
```bash
# Terminal 1 - Backend
uv run uvicorn src.app.app:app --reload --port 8000

# Terminal 2 - Frontend
uv run streamlit run streamlit_app.py --server.port 8501
```

## 🎮 Game Flow

1. **Welcome Screen**: Introduction and instructions
2. **Configuration**: Set user ID and API key
3. **Game Start**: Initialize boss battle
4. **Question Phase**: Boss asks interview questions
5. **Answer Phase**: Player submits responses
6. **Feedback Phase**: Receive scores and feedback
7. **Progress Update**: Game state updates
8. **Victory/Defeat**: Game completion screen

## 🚀 Advanced Features

### Real-time Updates
- Game state automatically updates after each interaction
- Progress charts refresh with new data
- Health bars animate with smooth transitions

### Session Persistence
- Game state maintained across page refreshes
- Conversation history preserved
- User preferences saved in session state

### Error Recovery
- Graceful handling of network errors
- Automatic retry mechanisms
- User-friendly error messages

## 📱 Mobile Support

The frontend is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- Various screen sizes

## 🔮 Future Enhancements

Potential improvements for the frontend:
- **Dark Mode**: Toggle between light and dark themes
- **Sound Effects**: Audio feedback for game actions
- **Achievements**: Visual achievement system
- **Leaderboards**: Global and local rankings
- **Multiplayer**: Real-time multiplayer battles
- **Analytics**: Detailed performance analytics
- **Export**: Save game results and conversation history

## 🤝 Contributing

To contribute to the frontend:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the same terms as the main InterviewOverfit project.

---

**Happy Interview Battling! 🎮⚔️**
