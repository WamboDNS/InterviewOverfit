#!/usr/bin/env python3
"""
InterviewOverfit
A gamified interview preparation system with beautiful UI
"""

import streamlit as st
import requests
import json
import time
import os
from datetime import datetime
from typing import Dict, Any, Optional
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="InterviewOverfit",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #ff6b6b;
        --secondary-color: #4ecdc4;
        --accent-color: #45b7d1;
        --success-color: #96ceb4;
        --warning-color: #feca57;
        --danger-color: #ff9ff3;
        --dark-color: #2c3e50;
        --light-color: #ecf0f1;
    }
    
    /* Custom header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Game status cards */
    .status-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid var(--primary-color);
    }
    
    .boss-card {
        background: #ff6b6b;
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(255,107,107,0.3);
        margin: 1rem 0;
    }
    
    .player-card {
        background: #4ecdc4;
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(78,205,196,0.3);
        margin: 1rem 0;
    }
    
    /* HP bars */
    .hp-bar {
        background: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        height: 20px;
        margin: 0.5rem 0;
    }
    
    .hp-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    .hp-boss {
        background: #e74c3c;
    }
    
    .hp-player {
        background: #27ae60;
    }
    
    /* Question box */
    .question-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(102,126,234,0.3);
    }
    
    .question-box h3 {
        color: white;
        margin-bottom: 1rem;
    }
    
    /* Answer input */
    .answer-input {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 1rem;
        font-size: 1.1rem;
        transition: border-color 0.3s ease;
    }
    
    .answer-input:focus {
        border-color: var(--primary-color);
        outline: none;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        transition: transform 0.2s ease;
        box-shadow: 0 5px 15px rgba(102,126,234,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102,126,234,0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    /* Progress indicators */
    .progress-container {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    /* Feedback styling */
    .feedback-positive {
        background: linear-gradient(135deg, #96ceb4 0%, #85c1a3 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .feedback-negative {
        background: linear-gradient(135deg, #ff9ff3 0%, #f368e0 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .feedback-neutral {
        background: linear-gradient(135deg, #feca57 0%, #ff9f43 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    /* Animations */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Chat message styling */
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px solid #dee2e6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .chat-message {
        margin: 1rem 0;
        padding: 1.2rem;
        border-radius: 20px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.15);
        position: relative;
        max-width: 80%;
        word-wrap: break-word;
    }
    
    .chat-message.boss {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        margin-right: 20%;
        margin-left: 0;
    }
    
    .chat-message.user {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        color: white;
        margin-left: 20%;
        margin-right: 0;
        margin-left: auto;
    }
    
    .chat-message.feedback {
        margin-right: 20%;
        margin-left: 0;
    }
    
    .chat-message.feedback.positive {
        background: linear-gradient(135deg, #96ceb4 0%, #85c1a3 100%);
        color: white;
    }
    
    .chat-message.feedback.negative {
        background: linear-gradient(135deg, #ff9ff3 0%, #f368e0 100%);
        color: white;
    }
    
    .chat-message.feedback.neutral {
        background: linear-gradient(135deg, #feca57 0%, #ff9f43 100%);
        color: white;
    }
    
    .message-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .timestamp {
        font-size: 0.8rem;
        opacity: 0.7;
    }
    
    .message-content {
        font-size: 1rem;
        line-height: 1.5;
        white-space: pre-wrap;
    }
    
    /* Chat scrollbar styling */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Configuration
BACKEND_URL = "http://localhost:8000"
DEFAULT_USER_ID = "demo-user"

# Initialize session state
if 'game_state' not in st.session_state:
    st.session_state.game_state = None
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = DEFAULT_USER_ID
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv("ANTHROPIC_API_KEY", "")
if 'current_answer' not in st.session_state:
    st.session_state.current_answer = ""
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'sidebar_visible' not in st.session_state:
    st.session_state.sidebar_visible = True
if 'answer_counter' not in st.session_state:
    st.session_state.answer_counter = 0

def make_api_request(endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Optional[Dict]:
    """Make API request to backend with error handling."""
    try:
        url = f"{BACKEND_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: Could not connect to backend at {BACKEND_URL}")
        st.info("Make sure the backend is running with: `uv run uvicorn src.app.app:app --reload`")
        return None

def render_game_status(game_state: Dict[str, Any]):
    """Render the current game status with two cards (no helper function)."""
    col1, col2 = st.columns(2)

    boss_percentage = (game_state.get("boss_hp", 0) / game_state.get("max_hp", 100)) * 100
    user_percentage = (game_state.get("user_hp", 0) / game_state.get("user_hp", 100)) * 100

    # Boss card
    col1.markdown(f"""
<div class="boss-card">
  <h2>👹 {game_state.get('boss_name', 'Unknown Boss')}</h2>
  <p><strong>Level:</strong> {game_state.get('level', 1)}/{game_state.get('max_level', 3)}</p>

  <div class="hp-bar">
    <div class="hp-fill hp-boss" style="width:{boss_percentage}%"></div>
  </div>
  <div class="hp-text" style="text-align:center; margin-top:0.5rem; font-weight:bold;">
    {game_state.get('boss_hp', 0)}/{game_state.get('max_hp', 100)} HP ({boss_percentage:.1f}%)
  </div>
</div>
""", unsafe_allow_html=True)

    # Player card
    col2.markdown(f"""
<div class="player-card">
  <h2>🛡️ You</h2>
  <p><strong>Turn:</strong> {game_state.get('turn_count', 0)}</p>

  <div class="hp-bar">
    <div class="hp-fill hp-player" style="width:{user_percentage}%"></div>
  </div>
  <div class="hp-text" style="text-align:center; margin-top:0.5rem; font-weight:bold;">
    {game_state.get('user_hp', 0)}/{game_state.get('user_hp', 100)} HP ({user_percentage:.1f}%)
  </div>
</div>
""", unsafe_allow_html=True)


def render_progress_chart(game_state: Dict[str, Any]):
    """Render progress visualization."""
    if not game_state:
        return
    
    # Create progress indicators
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="progress-container">
            <h4>🎯 Level Progress</h4>
        </div>
        """, unsafe_allow_html=True)
        
        level = game_state.get('level', 1)
        max_level = game_state.get('max_level', 3)
        progress = level / max_level
        
        st.progress(progress)
        st.metric("Current Level", f"{level}/{max_level}")
    
    with col2:
        st.markdown("""
        <div class="progress-container">
            <h4>💬 Conversation</h4>
        </div>
        """, unsafe_allow_html=True)
        
        conv_length = game_state.get('conversation_length', 0)
        st.metric("Messages", conv_length)
        st.metric("Turn Count", game_state.get('turn_count', 0))
    
    with col3:
        st.markdown("""
        <div class="progress-container">
            <h4>⚔️ Battle Status</h4>
        </div>
        """, unsafe_allow_html=True)
        
        boss_hp = game_state.get('boss_hp', 100)
        user_hp = game_state.get('user_hp', 100)
        
        if game_state.get('game_over', False):
            if game_state.get('victory', False):
                st.success("🎉 Victory!")
            else:
                st.error("💀 Defeat!")
        else:
            st.info("⚔️ Battle in Progress")

def render_feedback(score: int, feedback: str):
    """Render feedback with appropriate styling."""
    if score > 0:
        feedback_class = "feedback-positive"
        emoji = "✅"
    elif score < 0:
        feedback_class = "feedback-negative"
        emoji = "❌"
    else:
        feedback_class = "feedback-neutral"
        emoji = "⚖️"
    
    st.markdown(f"""
    <div class="{feedback_class}">
        <h4>{emoji} Score: {score:+d}</h4>
        <p>{feedback}</p>
    </div>
    """, unsafe_allow_html=True)

def add_chat_message(role: str, content: str, score: int = None):
    """Add a message to the chat history."""
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "score": score
    }
    st.session_state.chat_messages.append(message)

def render_conversation_history():
    """Render the conversation history with color-coded messages."""
    if not st.session_state.chat_messages:
        st.info("No conversation yet. Start the game to begin!")
        return
    
    # Create a chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for message in st.session_state.chat_messages:
        role = message["role"]
        content = message["content"]
        timestamp = message["timestamp"]
        score = message.get("score")
        
        if role == "boss":
            st.markdown(f"""
            <div class="chat-message boss">
                <div class="message-header">
                    <strong>👹 Boss</strong>
                    <span class="timestamp">{timestamp}</span>
                </div>
                <div class="message-content">{content}</div>
            </div>
            """, unsafe_allow_html=True)
        elif role == "user":
            st.markdown(f"""
            <div class="chat-message user">
                <div class="message-header">
                    <strong>🛡️ You</strong>
                    <span class="timestamp">{timestamp}</span>
                </div>
                <div class="message-content">{content}</div>
            </div>
            """, unsafe_allow_html=True)
        elif role == "feedback":
            if score and score > 0:
                feedback_class = "positive"
                emoji = "✅"
            elif score and score < 0:
                feedback_class = "negative"
                emoji = "❌"
            else:
                feedback_class = "neutral"
                emoji = "⚖️"
            
            st.markdown(f"""
            <div class="chat-message feedback {feedback_class}">
                <div class="message-header">
                    <strong>{emoji} Feedback</strong>
                    <span class="timestamp">{timestamp}</span>
                </div>
                <div class="message-content">
                    {f"<strong>Score: {score:+d}</strong><br>" if score is not None else ""}
                    {content}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def main():
    """Main application function."""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎮 InterviewOverfit</h1>
        <p>Level up your interview skills by defeating challenging boss interviews!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Collapsible settings section
    with st.expander("⚙️ Settings & Controls", expanded=st.session_state.sidebar_visible):
        col1, col2 = st.columns(2)
        
        with col1:
            # User ID input
            user_id = st.text_input("User ID", value=st.session_state.user_id, help="Your unique user identifier")
            st.session_state.user_id = user_id
            
            # API Key input (optional)
            env_api_key = os.getenv("ANTHROPIC_API_KEY", "")
            if env_api_key:
                st.info("🔑 API Key loaded from environment variable")
                api_key = env_api_key
                st.session_state.api_key = api_key
            else:
                api_key = st.text_input("API Key (Optional)", value=st.session_state.api_key, type="password", 
                                       help="Optional API key for enhanced features. Can also be set via ANTHROPIC_API_KEY environment variable.")
                st.session_state.api_key = api_key
        
        with col2:
            # Backend status
            st.markdown("### 🔗 Backend Status")
            try:
                result = make_api_request("/health")
                if result:
                    st.success("✅ Connected")
                else:
                    st.error("❌ Disconnected")
            except:
                st.error("❌ Disconnected")
        
        st.markdown("---")
        
        # Game controls
        st.markdown("### 🎮 Game Controls")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Start Game", use_container_width=True):
                with st.spinner("Starting new game..."):
                    data = {"api_key": api_key} if api_key else {}
                    result = make_api_request(f"/game/{user_id}/start", "POST", data)
                    if result and result.get('success'):
                        st.session_state.game_state = result.get('game_state')
                        st.session_state.chat_messages = []  # Clear chat history
                        
                        # Add initial boss message
                        first_question = result.get('game_state', {}).get('current_question', '')
                        if first_question:
                            add_chat_message("boss", first_question)
                        
                        st.success("Game started!")
                        st.rerun()
                    else:
                        st.error("Failed to start game")
        
        with col2:
            if st.button("🔄 New Game", use_container_width=True):
                with st.spinner("Starting new game..."):
                    # End current game first
                    make_api_request(f"/game/{user_id}", "DELETE")
                    # Start new game
                    data = {"api_key": api_key} if api_key else {}
                    result = make_api_request(f"/game/{user_id}/start", "POST", data)
                    if result and result.get('success'):
                        st.session_state.game_state = result.get('game_state')
                        st.session_state.chat_messages = []  # Clear chat history
                        
                        # Add initial boss message
                        first_question = result.get('game_state', {}).get('current_question', '')
                        if first_question:
                            add_chat_message("boss", first_question)
                        
                        st.success("New game started!")
                        st.rerun()
                    else:
                        st.error("Failed to start new game")
    
    # Main content area
    if not st.session_state.game_state:
        # Welcome screen
        st.markdown("""
        <div class="status-card">
            <h2>🎯 Welcome to Interview Boss Battle!</h2>
            <p>This gamified interview preparation system will help you practice with AI-powered interview bosses.</p>
            <p><strong>How to play:</strong></p>
            <ul>
                <li>Click "Start Game" to begin your interview battle</li>
                <li>Answer questions from the interview boss</li>
                <li>Get scored on your responses</li>
                <li>Defeat bosses to level up!</li>
            </ul>
            <p>Make sure your backend is running before starting a game.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show API info
        if st.button("📋 Show API Information"):
            result = make_api_request("/api/info")
            if result:
                st.json(result)
    else:
        # Game is active
        game_state = st.session_state.game_state
        
        # Render game status
        render_game_status(game_state)
        
        # Progress visualization
        render_progress_chart(game_state)
        
        # Chat conversation area
        st.markdown("### 💬 Interview Conversation")
        render_conversation_history()
        
        # Answer input (only show if game is active and not over)
        if not game_state.get('game_over', False):
            st.markdown("### ✍️ Your Answer")
            answer = st.text_area(
                "Type your answer here:",
                height=150,
                placeholder="Provide a thoughtful, detailed answer to the boss's question...",
                help="Answer the most recent question from the boss",
                key=f"answer_input_{st.session_state.get('answer_counter', 0)}"
            )
            
            # Update session state when user types
            if answer != st.session_state.current_answer:
                st.session_state.current_answer = answer
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("⚔️ Submit Answer", use_container_width=True, type="primary"):
                    if answer.strip():
                        with st.spinner("Submitting answer..."):
                            # Add user message to history
                            add_chat_message("user", answer)
                            
                            result = make_api_request(
                                f"/game/{user_id}/answer", 
                                "POST", 
                                {"answer": answer}
                            )
                            if result and result.get('success'):
                                # Get feedback, score, and next question from the structured response
                                score = result.get('score', 0)
                                feedback = result.get('feedback', '')
                                next_question = result.get('next_question', '')
                                
                                # Add feedback to history
                                add_chat_message("feedback", feedback, score)
                                
                                # Show feedback
                                render_feedback(score, feedback)
                                
                                # Update game state
                                old_game_state = st.session_state.game_state
                                new_game_state = result.get('game_state')
                                st.session_state.game_state = new_game_state
                                
                                # Check if player was defeated (game over but not victory)
                                if new_game_state.get('game_over', False) and not new_game_state.get('victory', False):
                                    # Player was defeated - automatically trigger "New Game" button logic
                                    st.info("💀 You were defeated! Starting a new game...")
                                    
                                    # Clear chat history for fresh start
                                    st.session_state.chat_messages = []
                                    
                                    # Start new game (same logic as "New Game" button)
                                    with st.spinner("Starting new game..."):
                                        # End current game first
                                        make_api_request(f"/game/{user_id}", "DELETE")
                                        # Start new game
                                        data = {"api_key": api_key} if api_key else {}
                                        new_result = make_api_request(f"/game/{user_id}/start", "POST", data)
                                        if new_result and new_result.get('success'):
                                            st.session_state.game_state = new_result.get('game_state')
                                            
                                            # Add initial boss message
                                            first_question = new_result.get('game_state', {}).get('current_question', '')
                                            if first_question:
                                                add_chat_message("boss", first_question)
                                            
                                            st.success("New game started!")
                                        else:
                                            st.error("Failed to start new game")
                                    
                                    # Clear the answer field
                                    st.session_state.current_answer = ""
                                    st.session_state.answer_counter += 1
                                    
                                    st.rerun()
                                
                                # Check if player leveled up (boss defeated)
                                old_level = old_game_state.get('level', 1) if old_game_state else 1
                                new_level = new_game_state.get('level', 1)
                                
                                if new_level > old_level:
                                    # Player leveled up - show victory message and clear chat
                                    st.success(f"🎯 Boss defeated! Moving to level {new_level}!")
                                    st.info("Starting fresh conversation with the new boss...")
                                    
                                    # Clear chat history for fresh start with new boss
                                    st.session_state.chat_messages = []
                                    
                                    # Get new boss's first question
                                    with st.spinner("Getting new boss question..."):
                                        question_result = make_api_request(f"/game/{user_id}/question", "GET")
                                        if question_result and question_result.get('success'):
                                            first_question = question_result.get('question', '')
                                            if first_question:
                                                add_chat_message("boss", first_question)
                                        else:
                                            st.error("Failed to get new boss question")
                                    
                                    # Clear the answer field
                                    st.session_state.current_answer = ""
                                    st.session_state.answer_counter += 1
                                    
                                    st.rerun()
                                else:
                                    # Normal game flow - add next question if game continues
                                    if not new_game_state.get('game_over', False) and next_question:
                                        add_chat_message("boss", next_question)
                                    
                                    # Clear the answer field for the next question
                                    st.session_state.current_answer = ""
                                    st.session_state.answer_counter += 1
                                    
                                    st.rerun()
                            else:
                                st.error("Failed to submit answer")
                                # Clear the answer field even on error
                                st.session_state.current_answer = ""
                                st.session_state.answer_counter += 1
                                st.rerun()
                    else:
                        st.warning("Please enter an answer before submitting")
        else:
            # Game over
            if game_state.get('victory', False):
                # Epic Victory Animation!
                st.markdown("""
                <style>
                @keyframes confetti-fall {
                    0% { transform: translateY(-100vh) rotate(0deg); opacity: 1; }
                    100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
                }
                
                @keyframes victory-bounce {
                    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
                    40% { transform: translateY(-30px); }
                    60% { transform: translateY(-15px); }
                }
                
                @keyframes glow {
                    0%, 100% { text-shadow: 0 0 20px #ffd700, 0 0 30px #ffd700, 0 0 40px #ffd700; }
                    50% { text-shadow: 0 0 30px #ff6b6b, 0 0 40px #ff6b6b, 0 0 50px #ff6b6b; }
                }
                
                .confetti {
                    position: fixed;
                    width: 10px;
                    height: 10px;
                    background: #ffd700;
                    animation: confetti-fall 3s linear infinite;
                }
                
                .confetti:nth-child(odd) { background: #ff6b6b; }
                .confetti:nth-child(3n) { background: #4ecdc4; }
                .confetti:nth-child(4n) { background: #45b7d1; }
                .confetti:nth-child(5n) { background: #96ceb4; }
                
                .victory-container {
                    text-align: center;
                    padding: 4rem 2rem;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 20px;
                    margin: 2rem 0;
                    position: relative;
                    overflow: hidden;
                }
                
                .victory-title {
                    font-size: 4rem;
                    font-weight: bold;
                    color: #ffd700;
                    animation: victory-bounce 2s infinite, glow 3s infinite;
                    margin-bottom: 1rem;
                }
                
                .victory-subtitle {
                    font-size: 2rem;
                    color: #ffffff;
                    margin-bottom: 1rem;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                }
                
                .victory-message {
                    font-size: 1.2rem;
                    color: #f0f0f0;
                    margin-bottom: 2rem;
                }
                
                .achievement-badge {
                    display: inline-block;
                    background: linear-gradient(45deg, #ffd700, #ffed4e);
                    color: #333;
                    padding: 1rem 2rem;
                    border-radius: 50px;
                    font-weight: bold;
                    font-size: 1.1rem;
                    margin: 1rem;
                    box-shadow: 0 8px 16px rgba(255, 215, 0, 0.3);
                    animation: victory-bounce 2s infinite;
                }
                
                .stars {
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    top: 0;
                    left: 0;
                    pointer-events: none;
                }
                
                .star {
                    position: absolute;
                    color: #ffd700;
                    font-size: 2rem;
                    animation: victory-bounce 2s infinite;
                }
                
                .star:nth-child(1) { top: 20%; left: 10%; animation-delay: 0s; }
                .star:nth-child(2) { top: 30%; right: 15%; animation-delay: 0.5s; }
                .star:nth-child(3) { bottom: 25%; left: 20%; animation-delay: 1s; }
                .star:nth-child(4) { bottom: 35%; right: 10%; animation-delay: 1.5s; }
                </style>
                
                <div class="victory-container">
                    <div class="stars">
                        <div class="star">⭐</div>
                        <div class="star">🌟</div>
                        <div class="star">✨</div>
                        <div class="star">💫</div>
                    </div>
                    
                    <div class="victory-title">🏆 VICTORY! 🏆</div>
                    <div class="victory-subtitle">You've Conquered All Three Bosses!</div>
                    <div class="victory-message">
                        Congratulations! You've successfully defeated:<br>
                        <strong>Sarah</strong> (Senior Developer) → <strong>Marcus</strong> (Engineering Manager) → <strong>Dr. Chen</strong> (Staff Engineer)
                    </div>
                    
                    <div class="achievement-badge">🎯 Interview Master</div>
                    <div class="achievement-badge">💼 Staff Engineer Level</div>
                    <div class="achievement-badge">🚀 Ready for Any Interview</div>
                    
                    <div style="margin-top: 2rem; font-size: 1.1rem; color: #f0f0f0;">
                        You've proven your skills across all levels of technical interviews!<br>
                        <em>From fundamentals to system design to technical leadership</em>
                    </div>
                </div>
                
                <script>
                // Create confetti effect
                function createConfetti() {
                    for (let i = 0; i < 50; i++) {
                        const confetti = document.createElement('div');
                        confetti.className = 'confetti';
                        confetti.style.left = Math.random() * 100 + '%';
                        confetti.style.animationDelay = Math.random() * 3 + 's';
                        confetti.style.animationDuration = (Math.random() * 3 + 2) + 's';
                        document.body.appendChild(confetti);
                        
                        setTimeout(() => {
                            confetti.remove();
                        }, 5000);
                    }
                }
                
                // Start confetti
                createConfetti();
                setInterval(createConfetti, 2000);
                </script>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="feedback-negative" style="text-align: center; padding: 3rem;">
                    <h1>💀 DEFEAT 💀</h1>
                    <h2>The interview boss was too strong!</h2>
                    <p>Don't give up! Try again to improve your interview skills.</p>
                </div>
                """, unsafe_allow_html=True)
        
        

if __name__ == "__main__":
    main()
