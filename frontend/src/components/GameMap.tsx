import React from "react";
import { Role, LevelData } from "../types/gameTypes";
import { gameData } from "../data/gameData";

interface GameMapProps {
  role: Role;
  onSelectLevel: (level: LevelData) => void;
  onBack: () => void;
  progress: Record<string, { completed: boolean }>;
}

export function GameMap({ role, onSelectLevel, onBack, progress }: GameMapProps) {
  const roleData = gameData[role];
  
  const getLevelColor = (level: LevelData, index: number) => {
    if (progress[level.id]?.completed) return 'bg-green-500/80';
    if (level.unlocked || index === 0) return 'bg-blue-500/80';
    return 'bg-gray-500/40';
  };

  const getLevelBorderColor = (level: LevelData, index: number) => {
    if (progress[level.id]?.completed) return 'border-green-400/60';
    if (level.unlocked || index === 0) return 'border-blue-400/60';
    return 'border-gray-400/30';
  };

  const isLevelAccessible = (level: LevelData, index: number) => {
    return level.unlocked || index === 0 || progress[roleData.levels[index - 1]?.id]?.completed;
  };

  return (
    <div className="min-h-screen max-h-screen bg-gradient-to-br from-black via-gray-900 to-black p-4 relative overflow-hidden">
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

      <div className="relative z-10 max-w-6xl mx-auto py-6 lg:py-8 h-full flex flex-col overflow-y-auto">
        {/* Header */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between mb-8 lg:mb-12 space-y-4 lg:space-y-0">
          <button
            onClick={onBack}
            className="px-4 py-2 lg:px-6 lg:py-3 bg-black/40 backdrop-blur-xl border border-white/20 rounded-2xl text-white/80 hover:text-white hover:border-white/40 transition-all text-sm lg:text-base self-start"
          >
            ← Back to Roles
          </button>
          
          <div className="text-center">
            <div className="flex flex-col lg:flex-row items-center gap-2 lg:gap-4 justify-center mb-2">
              <span className="text-3xl lg:text-4xl">{roleData.icon}</span>
              <h1 className="text-2xl lg:text-3xl font-bold text-white/95">{roleData.name}</h1>
            </div>
            <p className="text-white/60 text-sm lg:text-base">Choose your challenge level</p>
          </div>
          
          <div className="hidden lg:block w-32" />
        </div>

        {/* Map Path */}
        <div className="relative flex-1 flex flex-col justify-center">
          {/* Connecting Path - Only show on larger screens */}
          <div className="absolute top-1/2 left-0 right-0 h-1 bg-gradient-to-r from-white/20 via-white/40 to-white/20 transform -translate-y-1/2 rounded-full hidden lg:block">
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse rounded-full" />
          </div>

          {/* Level Nodes */}
          <div className="flex flex-col lg:flex-row justify-center lg:justify-between items-center space-y-8 lg:space-y-0 relative z-10">
            {roleData.levels.map((level, index) => {
              const accessible = isLevelAccessible(level, index);
              const completed = progress[level.id]?.completed;

              return (
                <div key={level.id} className="flex flex-col items-center space-y-4">
                  {/* Node */}
                  <div
                    onClick={() => accessible && onSelectLevel(level)}
                    className={`relative w-24 h-24 lg:w-32 lg:h-32 rounded-3xl border-4 shadow-2xl cursor-pointer transition-all duration-300 ${
                      accessible ? 'hover:scale-110' : 'cursor-not-allowed'
                    } ${getLevelColor(level, index)} ${getLevelBorderColor(level, index)}`}
                  >
                    {/* Glass effect */}
                    <div className="absolute inset-0 bg-gradient-to-br from-white/20 to-white/5 rounded-3xl" />
                    
                    <div className="relative z-10 h-full flex flex-col items-center justify-center text-center p-2 lg:p-4">
                      {/* Boss Avatar */}
                      <div className="text-2xl lg:text-3xl mb-1 lg:mb-2">{level.boss.avatar}</div>
                      
                      {/* Level Number */}
                      <div className="text-white font-bold text-xs lg:text-sm">
                        Level {index + 1}
                      </div>
                      
                      {/* Completion Status */}
                      {completed && (
                        <div className="absolute -top-1 -right-1 lg:-top-2 lg:-right-2 w-6 h-6 lg:w-8 lg:h-8 bg-green-500 rounded-full flex items-center justify-center text-white text-xs lg:text-sm">
                          ✓
                        </div>
                      )}
                      
                      {/* Lock for inaccessible levels */}
                      {!accessible && (
                        <div className="absolute inset-0 bg-black/60 rounded-3xl flex items-center justify-center">
                          <span className="text-white/60 text-xl lg:text-2xl">🔒</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Level Info */}
                  <div className="text-center space-y-1 lg:space-y-2 max-w-32 lg:max-w-none">
                    <h3 className="text-white/90 font-bold text-sm lg:text-base">{level.name}</h3>
                    <p className="text-white/60 text-xs lg:text-sm capitalize">{level.level}</p>
                    
                    {/* Boss Name */}
                    <p className="text-white/50 text-xs">
                      vs {level.boss.name}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Progress Summary */}
        <div className="mt-8 lg:mt-16 text-center">
          <div className="bg-black/40 backdrop-blur-xl border border-white/20 rounded-3xl p-4 lg:p-6 max-w-2xl mx-auto relative">
            <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-white/2 rounded-3xl" />
            
            <div className="relative z-10">
              <h3 className="text-white/90 font-bold mb-3 lg:mb-4 text-sm lg:text-base">Your Progress</h3>
              <div className="grid grid-cols-2 gap-4 lg:gap-6 text-center">
                <div>
                  <div className="text-xl lg:text-2xl font-bold text-white/95">
                    {Object.values(progress).filter(p => p.completed).length}
                  </div>
                  <div className="text-white/60 text-xs lg:text-sm">Levels Completed</div>
                </div>
                <div>
                  <div className="text-xl lg:text-2xl font-bold text-white/95">
                    {Math.round((Object.values(progress).filter(p => p.completed).length / roleData.levels.length) * 100)}%
                  </div>
                  <div className="text-white/60 text-xs lg:text-sm">Completion</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}