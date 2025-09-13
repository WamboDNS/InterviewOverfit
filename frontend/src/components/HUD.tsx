import React from "react";

interface HUDProps {
  userHp: number;
  maxUserHp: number;
  score: number;
  combo: number;
}

export function HUD({ userHp, maxUserHp, score, combo }: HUDProps) {
  const hpPercentage = (userHp / maxUserHp) * 100;
  
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
        </div>        {/* Combo - only show if combo > 1 */}
        {combo > 1 && (
          <div className="space-y-4">
            <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl p-3 animate-pulse">
              <div className="text-center">
                <span className="text-white/70 text-sm">Combo</span>
                <div className="text-white/95 text-lg font-bold">×{combo}</div>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}