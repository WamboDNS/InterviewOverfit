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

      <div className="relative z-10 max-w-4xl mx-auto py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-12">
          <button
            onClick={onBack}
            className="px-6 py-3 bg-black/40 backdrop-blur-xl border border-white/20 rounded-2xl text-white/80 hover:text-white hover:border-white/40 transition-all"
          >
            ← Back to Roles
          </button>
          
          <div className="text-center">
            <div className="flex items-center gap-4 justify-center mb-2">
              <span className="text-4xl">{roleData.icon}</span>
              <h1 className="text-3xl font-bold text-white/95">{roleData.name}</h1>
            </div>
            <p className="text-white/60">Choose your challenge level</p>
          </div>
          
          <div className="w-32" /> {/* Spacer */}
        </div>

        {/* Map Path */}
        <div className="relative">
          {/* Connecting Path */}
          <div className="absolute top-1/2 left-0 right-0 h-1 bg-gradient-to-r from-white/20 via-white/40 to-white/20 transform -translate-y-1/2 rounded-full">
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse rounded-full" />
          </div>

          {/* Level Nodes */}
          <div className="flex justify-between items-center relative z-10">
            {roleData.levels.map((level, index) => {
              const accessible = isLevelAccessible(level, index);
              const completed = progress[level.id]?.completed;

              return (
                <div key={level.id} className="flex flex-col items-center space-y-4">
                  {/* Node */}
                  <div
                    onClick={() => accessible && onSelectLevel(level)}
                    className={`relative w-32 h-32 rounded-3xl border-4 shadow-2xl cursor-pointer transition-all duration-300 ${
                      accessible ? 'hover:scale-110' : 'cursor-not-allowed'
                    } ${getLevelColor(level, index)} ${getLevelBorderColor(level, index)}`}
                  >
                    {/* Glass effect */}
                    <div className="absolute inset-0 bg-gradient-to-br from-white/20 to-white/5 rounded-3xl" />
                    
                    <div className="relative z-10 h-full flex flex-col items-center justify-center text-center p-4">
                      {/* Boss Avatar */}
                      <div className="text-3xl mb-2">{level.boss.avatar}</div>
                      
                      {/* Level Number */}
                      <div className="text-white font-bold text-sm">
                        Level {index + 1}
                      </div>
                      
                      {/* Completion Status */}
                      {completed && (
                        <div className="absolute -top-2 -right-2 w-8 h-8 bg-green-500 rounded-full flex items-center justify-center text-white text-sm">
                          ✓
                        </div>
                      )}
                      
                      {/* Lock for inaccessible levels */}
                      {!accessible && (
                        <div className="absolute inset-0 bg-black/60 rounded-3xl flex items-center justify-center">
                          <span className="text-white/60 text-2xl">🔒</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Level Info */}
                  <div className="text-center space-y-2">
                    <h3 className="text-white/90 font-bold">{level.name}</h3>
                    <p className="text-white/60 text-sm capitalize">{level.level}</p>
                    
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
        <div className="mt-16 text-center space-y-6">
          <div className="bg-black/40 backdrop-blur-xl border border-white/20 rounded-3xl p-6 max-w-2xl mx-auto">
            <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-white/2 rounded-3xl" />
            
            <div className="relative z-10">
              <h3 className="text-white/90 font-bold mb-4">Your Progress</h3>
              <div className="grid grid-cols-2 gap-6 text-center">
                <div>
                  <div className="text-2xl font-bold text-white/95">
                    {Object.values(progress).filter(p => p.completed).length}
                  </div>
                  <div className="text-white/60 text-sm">Levels Completed</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-white/95">
                    {Math.round((Object.values(progress).filter(p => p.completed).length / roleData.levels.length) * 100)}%
                  </div>
                  <div className="text-white/60 text-sm">Completion</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}