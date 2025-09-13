import React, { useState, useEffect } from "react";
import { LevelData, ChatMessage } from "../types/gameTypes";
import { BossSection } from "./BossSection";
import { ChatFeed } from "./ChatFeed";
import { HUD } from "./HUD";
import { ChatInput } from "./ChatInput";
import { api, GameState, APIError } from "../services/api";

interface GameBattleProps {
  level: LevelData;
  onComplete: (result: 'victory' | 'defeat', score: number, stars: number) => void;
  onBack: () => void;
}

export function GameBattle({ level, onComplete, onBack }: GameBattleProps) {
  // Game state from API
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<string>("");
  const [apiKeyInput, setApiKeyInput] = useState<string>("");

  // Initialize game on component mount
  useEffect(() => {
    initializeGame();
  }, []);

  // Check for game end
  useEffect(() => {
    if (gameState) {
      if (gameState.boss_hp <= 0 && gameState.victory) {
        onComplete('victory', gameState.turn_count, 3); // Max stars for victory
      } else if (gameState.user_hp <= 0 || gameState.game_over) {
        onComplete('defeat', gameState.turn_count, 0);
      }
    }
  }, [gameState, onComplete]);

  const initializeGame = async () => {
    setLoading(true);
    setError(null);
    try {
      // Try to start the game (will need API key)
      const response = await api.startGame();
      if (response.success) {
        setGameState(response.game_state);
        setCurrentQuestion(response.question);
        
        // Add initial boss question to chat
        const bossMessage: ChatMessage = {
          id: Date.now().toString(),
          type: "boss",
          content: response.question,
          timestamp: new Date(),
        };
        setMessages([bossMessage]);
      } else {
        setError(response.error || "Failed to start game");
      }
    } catch (err) {
      if (err instanceof APIError) {
        setError(err.message);
      } else {
        setError("Failed to connect to game server");
      }
    } finally {
      setLoading(false);
    }
  };

  const startGameWithApiKey = async () => {
    if (!apiKeyInput.trim()) {
      setError("Please enter your Anthropic API key");
      return;
    }
    
    setLoading(true);
    setError(null);
    try {
      const response = await api.startGame(apiKeyInput);
      if (response.success) {
        setGameState(response.game_state);
        setCurrentQuestion(response.question);
        
        // Add initial boss question to chat
        const bossMessage: ChatMessage = {
          id: Date.now().toString(),
          type: "boss",
          content: response.question,
          timestamp: new Date(),
        };
        setMessages([bossMessage]);
      } else {
        setError(response.error || "Failed to start game");
      }
    } catch (err) {
      if (err instanceof APIError) {
        setError(err.message);
      } else {
        setError("Failed to connect to game server");
      }
    } finally {
      setLoading(false);
    }
  };

  // Handle user messages with real API
  const handleSendMessage = async (content: string, isCode: boolean) => {
    if (!gameState || loading) return;
    
    // Add user message immediately
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: "user",
      content,
      isCode,
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);
    setError(null);

    try {
      // Submit answer to API
      const response = await api.submitAnswer(content);
      
      if (response.success) {
        // Update game state
        setGameState(response.game_state);
        
        // Add boss response to chat
        const bossMessage: ChatMessage = {
          id: (Date.now() + 1).toString(),
          type: "boss",
          content: response.feedback,
          timestamp: new Date(),
        };
        
        setMessages(prev => [...prev, bossMessage]);
        
        // Get next question if game continues
        if (!response.game_state.game_over) {
          setTimeout(async () => {
            try {
              const questionResponse = await api.getQuestion();
              if (questionResponse.success && questionResponse.question !== currentQuestion) {
                setCurrentQuestion(questionResponse.question);
                const nextQuestionMessage: ChatMessage = {
                  id: (Date.now() + 2).toString(),
                  type: "boss",
                  content: questionResponse.question,
                  timestamp: new Date(),
                };
                setMessages(prev => [...prev, nextQuestionMessage]);
              }
            } catch (err) {
              console.error("Failed to get next question:", err);
            }
          }, 1000);
        }
      } else {
        setError(response.error || "Failed to submit answer");
      }
    } catch (err) {
      if (err instanceof APIError) {
        setError(err.message);
      } else {
        setError("Failed to submit answer");
      }
    } finally {
      setLoading(false);
    }
  };

  const gameOver = gameState?.game_over || false;
  const needsApiKey = error?.includes("API key");

  // Show API key input if needed
  if (needsApiKey) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black p-4 flex items-center justify-center">
        <div className="bg-black/60 backdrop-blur-xl border border-white/20 rounded-2xl p-8 max-w-md w-full">
          <h2 className="text-2xl font-bold text-white mb-4 text-center">🔑 API Key Required</h2>
          <p className="text-white/70 mb-6 text-center">
            To start the Boss Battle, please enter your Anthropic API key.
          </p>
          
          <div className="space-y-4">
            <input
              type="password"
              placeholder="Enter your Anthropic API key..."
              value={apiKeyInput}
              onChange={(e) => setApiKeyInput(e.target.value)}
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:border-white/40"
              onKeyPress={(e) => e.key === 'Enter' && startGameWithApiKey()}
            />
            
            <div className="flex gap-3">
              <button
                onClick={startGameWithApiKey}
                disabled={loading}
                className="flex-1 px-4 py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded-xl transition-all"
              >
                {loading ? "Starting Game..." : "Start Boss Battle"}
              </button>
              
              <button
                onClick={onBack}
                className="px-4 py-3 bg-gray-600 hover:bg-gray-700 text-white rounded-xl transition-all"
              >
                Back
              </button>
            </div>
          </div>
          
          {error && (
            <div className="mt-4 p-3 bg-red-500/20 border border-red-500/30 rounded-xl">
              <p className="text-red-200 text-sm">{error}</p>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Show loading state
  if (loading || !gameState) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black p-4 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-white text-xl">Loading Boss Battle...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black p-4 relative overflow-hidden">
      {/* Background pattern */}
      <div className="fixed inset-0">
        <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent" />
        <div 
          className="absolute inset-0 opacity-5"
          style={{
            backgroundImage: `
              radial-gradient(circle at 1px 1px, rgba(255,255,255,0.3) 1px, transparent 0)
            `,
            backgroundSize: '50px 50px'
          }}
        />
      </div>

      {/* Back button */}
      <div className="absolute top-4 left-4 z-20">
        <button
          onClick={onBack}
          disabled={gameOver || loading}
          className="px-4 py-2 bg-black/40 backdrop-blur-xl border border-white/20 rounded-xl text-white/80 hover:text-white hover:border-white/40 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          ← Back to Map
        </button>
      </div>

      {/* Error display */}
      {error && !needsApiKey && (
        <div className="absolute top-4 right-4 z-20 max-w-md">
          <div className="bg-red-500/20 backdrop-blur-xl border border-red-500/30 rounded-xl p-4">
            <p className="text-red-200 text-sm">{error}</p>
            <button 
              onClick={() => setError(null)}
              className="text-red-200 hover:text-white mt-2 text-xs underline"
            >
              Dismiss
            </button>
          </div>
        </div>
      )}

      <div className="relative z-10 max-w-7xl mx-auto grid grid-cols-12 gap-6 h-screen pt-16">
        {/* Top Section - Boss Area */}
        <div className="col-span-12">
          <BossSection
            bossHp={gameState.boss_hp}
            maxBossHp={gameState.max_hp}
            currentQuestion={currentQuestion}
            bossAvatar={level.boss.avatar}
          />
        </div>

        {/* Middle Section - Chat Feed */}
        <div className="col-span-8 h-96">
          <ChatFeed messages={messages} />
        </div>

        {/* Right Section - HUD */}
        <div className="col-span-4 h-96">
          <HUD
            userHp={gameState.user_hp}
            maxUserHp={gameState.max_hp}
            score={gameState.turn_count}
            combo={gameState.level}
          />
        </div>

        {/* Bottom Section - Input */}
        <div className="col-span-12">
          <ChatInput
            onSendMessage={handleSendMessage}
            disabled={gameOver || loading}
          />
        </div>
      </div>

      {/* Game status overlay */}
      {gameState && (
        <div className="absolute top-20 left-1/2 transform -translate-x-1/2 z-20">
          <div className="bg-black/60 backdrop-blur-xl border border-white/20 rounded-xl px-6 py-3">
            <p className="text-white text-sm">
              Level {gameState.level}/{gameState.max_level} • 
              {gameState.boss_name} • 
              Turn {gameState.turn_count}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}