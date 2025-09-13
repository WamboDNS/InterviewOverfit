import React from "react";
import { LevelData } from "../types/gameTypes";

interface WinLossScreenProps {
  result: 'victory' | 'defeat';
  level: LevelData;
  score: number;
  stars: number;
  onContinue: () => void;
  onRetry?: () => void;
}

export function WinLossScreen({ result, level, score, stars, onContinue, onRetry }: WinLossScreenProps) {
  const isVictory = result === 'victory';

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black flex items-center justify-center relative overflow-hidden">
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

      {/* Floating particles */}
      {isVictory && (
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          {[...Array(20)].map((_, i) => (
            <div
              key={i}
              className="absolute w-2 h-2 bg-white/30 rounded-full animate-bounce"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 2}s`,
                animationDuration: `${2 + Math.random() * 2}s`
              }}
            />
          ))}
        </div>
      )}

      <div className="relative z-10 bg-black/40 backdrop-blur-xl border border-white/20 rounded-3xl p-12 text-center shadow-2xl max-w-2xl mx-4">
        {/* Glass effect overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-white/2 rounded-3xl" />
        
        <div className="relative z-10 space-y-8">
          {/* Result Icon */}
          <div className="text-8xl mb-6">
            {isVictory ? '🎉' : '💀'}
          </div>

          {/* Result Title */}
          <div className="space-y-2">
            <h1 className={`text-5xl font-bold ${
              isVictory ? 'text-green-400' : 'text-red-400'
            }`}>
              {isVictory ? 'Victory!' : 'Defeat!'}
            </h1>
            <h2 className="text-2xl text-white/80">
              {isVictory ? `You defeated ${level.boss.name}!` : `${level.boss.name} proved too strong...`}
            </h2>
          </div>

          {/* Level Info */}
          <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
            <div className="flex items-center justify-center gap-4 mb-4">
              <span className="text-3xl">{level.boss.avatar}</span>
              <div className="text-left">
                <h3 className="text-xl font-bold text-white/90">{level.name}</h3>
                <p className="text-white/60 capitalize">{level.level} Level</p>
              </div>
            </div>
          </div>

          {/* Score and Stats */}
          <div className="grid grid-cols-2 gap-6">
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
              <div className="text-3xl font-bold text-white/95">{score.toLocaleString()}</div>
              <div className="text-white/60">Final Score</div>
            </div>
            
            {isVictory && (
              <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
                <div className="flex justify-center gap-1 mb-2">
                  {[1, 2, 3].map((star) => (
                    <span
                      key={star}
                      className={`text-2xl ${
                        star <= stars ? 'text-yellow-400' : 'text-gray-500'
                      }`}
                    >
                      ⭐
                    </span>
                  ))}
                </div>
                <div className="text-white/60">Performance</div>
              </div>
            )}
          </div>

          {/* Performance Message */}
          <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
            <p className="text-white/80 text-lg leading-relaxed">
              {isVictory ? (
                stars === 3 ? "Perfect execution! You've mastered this level completely!" :
                stars === 2 ? "Great job! You showed strong understanding and skill!" :
                "Well done! You've proven your capabilities and defeated the boss!"
              ) : (
                "Don't give up! Every defeat is a learning opportunity. Study the questions and try again!"
              )}
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4 justify-center pt-4">
            {!isVictory && onRetry && (
              <button
                onClick={onRetry}
                className="px-8 py-4 bg-blue-600/80 backdrop-blur-sm text-white font-medium rounded-2xl hover:bg-blue-600 transition-all border border-blue-400/20"
              >
                Try Again
              </button>
            )}
            
            <button
              onClick={onContinue}
              className="px-8 py-4 bg-white/90 backdrop-blur-sm text-black font-medium rounded-2xl hover:bg-white transition-all border border-white/20"
            >
              {isVictory ? 'Continue Journey' : 'Back to Map'}
            </button>
          </div>

          {/* Progress Hint */}
          {isVictory && (
            <div className="text-white/50 text-sm">
              🎯 Level unlocked! New challenges await you on the map.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}