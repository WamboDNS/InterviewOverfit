import React, { useState, useEffect } from "react";
import { LevelData, ChatMessage } from "../types/gameTypes";
import { BossSection } from "./BossSection";
import { ChatFeed } from "./ChatFeed";
import { HUD } from "./HUD";
import { ChatInput } from "./ChatInput";
import { getGameConfig, getGameLogic, initializeGameConfig } from "../utils/gameConfig";

interface GameBattleProps {
  level: LevelData;
  onComplete: (result: 'victory' | 'defeat', score: number, stars: number) => void;
  onBack: () => void;
}

export function GameBattle({ level, onComplete, onBack }: GameBattleProps) {
  // Initialize game configuration
  const [config, setConfig] = useState<any>(null);
  const [gameLogic, setGameLogic] = useState<any>(null);
  
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

  // Initialize game configuration
  useEffect(() => {
    const initConfig = async () => {
      try {
        const gameConfig = await initializeGameConfig();
        const logic = getGameLogic();
        setConfig(gameConfig);
        setGameLogic(logic);
        
        // Update initial state with config values
        setUserHp(gameConfig.gameMechanics.initialStats.userHp);
        setTimeLeft(gameConfig.gameMechanics.initialStats.timeLimit);
        setCombo(gameConfig.gameMechanics.initialStats.combo);
      } catch (error) {
        console.error('Failed to initialize game configuration:', error);
      }
    };
    
    initConfig();
  }, []);

  // Timer countdown
  useEffect(() => {
    if (!config || !gameLogic) return;
    
    if (timeLeft > 0 && bossHp > 0 && userHp > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else if (timeLeft === 0) {
      // Time's up - boss attacks
      const newUserHp = gameLogic.applyPenalty(userHp, 'timeout');
      setUserHp(newUserHp);
      setTimeLeft(config.gameMechanics.initialStats.timeLimit);
      setCombo(config.gameMechanics.initialStats.combo);
    }
  }, [timeLeft, bossHp, userHp, config, gameLogic]);

  // Check for game end
  useEffect(() => {
    if (!config || !gameLogic) return;
    
    if (bossHp <= 0) {
      const stars = gameLogic.calculateStars(score, userHp, timeLeft);
      setTimeout(() => onComplete('victory', score, stars), config.timing.gameEndDelay);
    } else if (userHp <= 0) {
      setTimeout(() => onComplete('defeat', score, 0), config.timing.gameEndDelay);
    }
  }, [bossHp, userHp, score, onComplete, config, gameLogic]);

  const evaluateAnswer = (content: string): number => {
    if (!gameLogic) return 0;
    
    const question = level.boss.questions[currentQuestionIndex];
    const evaluationResult = gameLogic.evaluateAnswer(content, question);
    return evaluationResult.damage;
  };

  const getBossResponse = (damage: number): string => {
    if (!gameLogic) return "I'm not ready yet...";
    
    const { responses } = level.boss;
    const responseType = gameLogic.getBossResponseType(damage);
    
    return responses[responseType][Math.floor(Math.random() * responses[responseType].length)];
  };

  // Handle user messages
  const handleSendMessage = (content: string, isCode: boolean) => {
    if (!config || !gameLogic) return;
    
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
    const scoreIncrease = gameLogic.calculateScore(damage, combo);
    setScore(prev => prev + scoreIncrease);
    
    // Update combo
    const newCombo = gameLogic.calculateCombo(combo, damage);
    setCombo(newCombo);

    // Reset timer
    setTimeLeft(config.gameMechanics.initialStats.timeLimit);

    // Boss response after short delay
    setTimeout(() => {
      let bossResponse = "";
      
      if (newBossHp <= 0) {
        bossResponse = level.boss.responses.victory;
      } else {
        bossResponse = getBossResponse(damage);
        
        // Boss counter-attacks on poor answers
        if (damage < config.evaluation.damageThresholds.poor) {
          const newUserHp = gameLogic.applyPenalty(userHp, 'poorAnswer');
          setUserHp(newUserHp);
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
        }, config.timing.nextQuestionDelay);
      }
    }, config.timing.bossResponseDelay);
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
            maxUserHp={config?.gameMechanics.initialStats.userHp || 100}
            timeLeft={timeLeft}
            maxTime={config?.gameMechanics.initialStats.timeLimit || 90}
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