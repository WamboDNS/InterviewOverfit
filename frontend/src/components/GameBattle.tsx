import React, { useState, useEffect } from "react";
import { LevelData, ChatMessage } from "../types/gameTypes";
import { BossSection } from "./BossSection";
import { ChatFeed } from "./ChatFeed";
import { HUD } from "./HUD";
import { ChatInput } from "./ChatInput";
import { loadGameConfig } from "../config/loader";
import { GameLogic } from "../utils/gameLogic";

interface GameBattleProps {
  level: LevelData;
  onComplete: (result: 'victory' | 'defeat', score: number, stars: number) => void;
  onBack: () => void;
}

export function GameBattle({ level, onComplete, onBack }: GameBattleProps) {
  // Load game configuration
  const config = loadGameConfig();
  const gameLogic = new GameLogic(config);
  const initialStats = gameLogic.getInitialStats();
  
  // Game state - initialized from config
  const [bossHp, setBossHp] = useState(initialStats.bossHp);
  const [userHp, setUserHp] = useState(initialStats.userHp);
  const [combo, setCombo] = useState(initialStats.combo);
  const [messages, setMessages] = useState<ChatMessage[]>([]);



  // Check for game end - using config timing
  useEffect(() => {
    if (bossHp <= 0) {
      setTimeout(() => onComplete('victory', 0, 1), config.timing.gameEndDelay);
    } else if (userHp <= 0) {
      setTimeout(() => onComplete('defeat', 0, 0), config.timing.gameEndDelay);
    }
  }, [bossHp, userHp, onComplete, config]);

  const evaluateAnswer = (content: string): number => {
    // Use game logic to calculate damage from config
    return gameLogic.calculateDamage();
  };

  // Handle user messages - using config-driven logic
  const handleSendMessage = (content: string, isCode: boolean) => {
    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: "user",
      content,
      isCode,
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, userMessage]);

    // Calculate damage using game logic
    const damage = evaluateAnswer(content);
    const totalDamage = damage * combo;
    const newBossHp = Math.max(0, bossHp - totalDamage);
    setBossHp(newBossHp);
    
    // Update combo using game logic
    const newCombo = gameLogic.calculateCombo(combo, damage);
    setCombo(newCombo);

  };

  const gameOver = bossHp <= 0 || userHp <= 0;

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
          disabled={gameOver}
          className="px-4 py-2 bg-black/40 backdrop-blur-xl border border-white/20 rounded-xl text-white/80 hover:text-white hover:border-white/40 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          ← Back to Map
        </button>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto grid grid-cols-12 gap-6 h-screen pt-16">
        {/* Top Section - Boss Area */}
        <div className="col-span-12">
          <BossSection
            bossHp={bossHp}
            maxBossHp={initialStats.bossHp}
            currentQuestion=""
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
            userHp={userHp}
            maxUserHp={initialStats.userHp}
            timeLeft={0}
            maxTime={0}
            score={0}
            combo={combo}
          />
        </div>

        {/* Bottom Section - Input */}
        <div className="col-span-12">
          <ChatInput
            onSendMessage={handleSendMessage}
            disabled={gameOver}
          />
        </div>
      </div>
    </div>
  );
}