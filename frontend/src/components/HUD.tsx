import React from "react";

interface HUDProps {
  userHp: number;
  maxUserHp: number;
  timeLeft: number;
  maxTime: number;
  score: number;
  combo: number;
}

export function HUD({ userHp, maxUserHp, timeLeft, maxTime, score, combo }: HUDProps) {
  const hpPercentage = (userHp / maxUserHp) * 100;
  const timePercentage = (timeLeft / maxTime) * 100;
  
  return (
    <div className="space-y-6 p-6 bg-black/40 backdrop-blur-xl border border-white/20 rounded-3xl shadow-2xl relative">
      {/* Glass effect overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-white/2 rounded-3xl" />
      
      <div className="relative z-10 space-y-6">
        {/* User HP */}
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-white/90">Your HP</span>
            <span className="text-white/70 text-sm">{userHp}/{maxUserHp}</span>
          </div>
          <div className="relative">
            <div className="h-3 bg-black/30 backdrop-blur-sm rounded-full overflow-hidden border border-white/10">
              <div 
                className="h-full bg-gradient-to-r from-white/80 to-white/60 transition-all duration-300 ease-out relative rounded-full"
                style={{ width: `${hpPercentage}%` }}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-white/20 via-white/40 to-white/20 animate-pulse rounded-full" />
              </div>
            </div>
          </div>
        </div>

        {/* Timer */}
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-white/90">Time</span>
            <span className="text-white/70 text-sm">{Math.ceil(timeLeft)}s</span>
          </div>
          
          {/* Circular Timer */}
          <div className="relative w-24 h-24 mx-auto">
            <div className="absolute inset-0 rounded-full border-2 border-white/10 bg-black/20 backdrop-blur-sm" />
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="currentColor"
                strokeWidth="4"
                strokeLinecap="round"
                strokeDasharray={`${timePercentage * 2.83} 283`}
                className={`transition-all duration-1000 ${
                  timePercentage > 30 ? 'text-white/80' : 'text-white/40'
                }`}
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className={`text-lg font-bold ${
                timePercentage > 30 ? 'text-white/90' : 'text-white/60'
              }`}>
                {Math.ceil(timeLeft)}
              </span>
            </div>
          </div>
        </div>

        {/* Score & Combo */}
        <div className="space-y-4">
          <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-2xl p-4">
            <div className="text-center space-y-2">
              <div>
                <span className="text-white/60 text-sm">Score</span>
                <div className="text-white/90 text-xl font-bold">{score.toLocaleString()}</div>
              </div>
            </div>
          </div>

          {combo > 1 && (
            <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl p-3 animate-pulse">
              <div className="text-center">
                <span className="text-white/70 text-sm">Combo</span>
                <div className="text-white/95 text-lg font-bold">×{combo}</div>
              </div>
            </div>
          )}
        </div>

        {/* System Status */}
        <div className="border-t border-white/10 pt-4 space-y-1">
          <div className="flex justify-between text-xs text-white/50">
            <span>System</span>
            <span className="text-white/70">Online</span>
          </div>
          <div className="flex justify-between text-xs text-white/50">
            <span>Network</span>
            <span className="text-white/70">Connected</span>
          </div>
        </div>
      </div>
    </div>
  );
}