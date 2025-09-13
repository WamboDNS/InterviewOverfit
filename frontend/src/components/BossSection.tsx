import React from "react";
import { Avatar, AvatarFallback } from "./ui/avatar";

interface BossSectionProps {
  bossHp: number;
  maxBossHp: number;
  currentQuestion: string;
}

export function BossSection({ bossHp, maxBossHp, currentQuestion }: BossSectionProps) {
  const hpPercentage = (bossHp / maxBossHp) * 100;

  return (
    <div className="relative p-6 bg-black/40 backdrop-blur-xl border border-white/20 rounded-3xl shadow-2xl">
      {/* Glass effect overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-white/2 rounded-3xl" />
      
      <div className="relative z-10 flex items-start gap-6">
        {/* Boss Avatar */}
        <div className="relative">
          <Avatar className="w-20 h-20 border-2 border-white/30 bg-black/20 backdrop-blur-sm">
            <AvatarFallback className="bg-black/40 text-white text-2xl backdrop-blur-sm">
              🤖
            </AvatarFallback>
          </Avatar>
          <div className="absolute -top-1 -right-1 w-4 h-4 bg-white/80 rounded-full animate-pulse" />
        </div>

        <div className="flex-1 space-y-4">
          {/* Boss HP Bar */}
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-white/90">Boss HP</span>
              <span className="text-white/70 text-sm">{bossHp}/{maxBossHp}</span>
            </div>
            <div className="relative">
              <div className="h-3 bg-black/30 backdrop-blur-sm rounded-full overflow-hidden border border-white/10">
                <div 
                  className="h-full bg-gradient-to-r from-white/80 to-white/60 transition-all duration-500 ease-out relative rounded-full"
                  style={{ width: `${hpPercentage}%` }}
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-white/20 via-white/40 to-white/20 animate-pulse rounded-full" />
                </div>
              </div>
            </div>
          </div>

          {/* Boss Chat Bubble - only show if there's a question */}
          {currentQuestion && (
            <div className="relative">
              <div className="bg-black/30 backdrop-blur-md border border-white/20 rounded-2xl p-4 shadow-xl relative">
                <div className="absolute -bottom-2 left-8 w-4 h-4 bg-black/30 backdrop-blur-md border-r border-b border-white/20 rotate-45" />
                <p className="text-white/90 leading-relaxed">{currentQuestion}</p>
                <div className="mt-2 text-white/60 text-sm animate-pulse">▊</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}