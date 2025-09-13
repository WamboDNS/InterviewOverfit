import React, { useState, useEffect } from "react";
import { LevelData, ChatMessage } from "../types/gameTypes";
import { BossSection } from "./BossSection";
import { ChatFeed } from "./ChatFeed";
import { HUD } from "./HUD";
import { ChatInput } from "./ChatInput";

interface GameBattleProps {
  level: LevelData;
  onComplete: (result: 'victory' | 'defeat', score: number, stars: number) => void;
  onBack: () => void;
}

export function GameBattle({ level, onComplete, onBack }: GameBattleProps) {
  // Game state
  const [bossHp, setBossHp] = useState(level.boss.hp);
  const [userHp, setUserHp] = useState(100);
  const [timeLeft, setTimeLeft] = useState(90); // Longer time for more complex questions
  const [score, setScore] = useState(0);
  const [combo, setCombo] = useState(1);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "1",
      type: "boss",
      content: `You dare challenge ${level.boss.name}? Let's see what you're made of!`,
      timestamp: new Date(),
    },
    {
      id: "2",
      type: "boss", 
      content: level.boss.questions[0],
      timestamp: new Date(),
    },
  ]);

  // Timer countdown
  useEffect(() => {
    if (timeLeft > 0 && bossHp > 0 && userHp > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else if (timeLeft === 0) {
      // Time's up - boss attacks
      setUserHp(Math.max(0, userHp - 25));
      setTimeLeft(90);
      setCombo(1);
    }
  }, [timeLeft, bossHp, userHp]);

  // Check for game end
  useEffect(() => {
    if (bossHp <= 0) {
      const stars = calculateStars(score, userHp, timeLeft);
      setTimeout(() => onComplete('victory', score, stars), 2000);
    } else if (userHp <= 0) {
      setTimeout(() => onComplete('defeat', score, 0), 2000);
    }
  }, [bossHp, userHp, score, onComplete]);

  const calculateStars = (finalScore: number, remainingHp: number, remainingTime: number): number => {
    let stars = 1; // Base star for completion
    
    // Bonus star for high score
    if (finalScore > 1000) stars++;
    
    // Bonus star for maintaining health and time
    if (remainingHp > 50 && remainingTime > 30) stars++;
    
    return Math.min(stars, 3);
  };

  const evaluateAnswer = (content: string): number => {
    // Simple keyword-based evaluation (in a real app, this could use AI)
    const keywordCount = level.boss.questions[currentQuestionIndex]
      .toLowerCase()
      .split(' ')
      .filter(word => content.toLowerCase().includes(word))
      .length;
    
    const contentLength = content.length;
    const hasCodePatterns = /[{}\[\];()=>]|\/\/|\/\*|\*\/|function|const|let|var|import|export|class|if|for|while/.test(content);
    
    // Calculate damage based on various factors
    let baseDamage = Math.min(20, Math.max(5, keywordCount * 2));
    
    // Bonus for detailed answers
    if (contentLength > 100) baseDamage += 5;
    if (contentLength > 300) baseDamage += 5;
    
    // Bonus for code examples
    if (hasCodePatterns) baseDamage += 10;
    
    return Math.min(baseDamage, 25);
  };

  const getBossResponse = (damage: number): string => {
    const { responses } = level.boss;
    
    if (damage >= 20) {
      return responses.excellent[Math.floor(Math.random() * responses.excellent.length)];
    } else if (damage >= 12) {
      return responses.good[Math.floor(Math.random() * responses.good.length)];
    } else {
      return responses.poor[Math.floor(Math.random() * responses.poor.length)];
    }
  };

  // Handle user messages
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

    // Calculate damage
    const damage = evaluateAnswer(content);
    const totalDamage = damage * combo;
    const newBossHp = Math.max(0, bossHp - totalDamage);
    setBossHp(newBossHp);

    // Update score
    setScore(prev => prev + totalDamage * 15);
    
    // Update combo
    if (damage >= 15) {
      setCombo(prev => Math.min(prev + 1, 5));
    } else if (damage < 8) {
      setCombo(1);
    }

    // Reset timer
    setTimeLeft(90);

    // Boss response after short delay
    setTimeout(() => {
      let bossResponse = "";
      
      if (newBossHp <= 0) {
        bossResponse = level.boss.responses.victory;
      } else {
        bossResponse = getBossResponse(damage);
        
        // Boss counter-attacks on poor answers
        if (damage < 8) {
          setUserHp(prev => Math.max(0, prev - 15));
        }
      }

      const bossMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: "boss",
        content: bossResponse,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, bossMessage]);

      // Next question if boss is still alive
      if (newBossHp > 0) {
        setTimeout(() => {
          const nextQuestionIndex = (currentQuestionIndex + 1) % level.boss.questions.length;
          setCurrentQuestionIndex(nextQuestionIndex);
          
          const questionMessage: ChatMessage = {
            id: (Date.now() + 2).toString(),
            type: "boss",
            content: level.boss.questions[nextQuestionIndex],
            timestamp: new Date(),
          };
          
          setMessages(prev => [...prev, questionMessage]);
        }, 1500);
      }
    }, 1000);
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
            maxBossHp={level.boss.hp}
            currentQuestion={level.boss.questions[currentQuestionIndex]}
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
            maxUserHp={100}
            timeLeft={timeLeft}
            maxTime={90}
            score={score}
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