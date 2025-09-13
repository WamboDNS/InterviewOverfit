import React from "react";
import { Role } from "../types/gameTypes";
import { gameData } from "../data/gameData";

interface RoleSelectionProps {
  onSelectRole: (role: Role) => void;
}

export function RoleSelection({ onSelectRole }: RoleSelectionProps) {
  const roles: Role[] = ['SDE'];

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

      <div className="relative z-10 max-w-6xl mx-auto py-12">
        {/* Header */}
        <div className="text-center mb-16 space-y-4">
          <h1 className="text-5xl font-bold text-white/95">Software Development Engineer</h1>
          <p className="text-white/70 text-xl max-w-2xl mx-auto">
            Master the art of software engineering through challenging technical interviews
          </p>
        </div>

        {/* Role Cards */}
        <div className="flex justify-center px-4">
          {roles.map((roleId) => {
            const role = gameData[roleId];
            return (
              <div
                key={roleId}
                onClick={() => onSelectRole(roleId)}
                className="group relative p-8 bg-black/40 backdrop-blur-xl border border-white/20 rounded-3xl shadow-2xl cursor-pointer transition-all duration-300 hover:scale-105 hover:border-white/40 max-w-md"
              >
                {/* Glass effect overlay */}
                <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-white/2 rounded-3xl" />
                
                <div className="relative z-10 text-center space-y-6">
                  {/* Icon */}
                  <div className="w-20 h-20 mx-auto bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl flex items-center justify-center text-4xl group-hover:bg-white/20 transition-all duration-300">
                    {role.icon}
                  </div>

                  {/* Title */}
                  <div className="space-y-2">
                    <h3 className="text-2xl font-bold text-white/95">{role.id}</h3>
                    <h4 className="text-lg text-white/80">{role.name}</h4>
                  </div>

                  {/* Description */}
                  <p className="text-white/60 leading-relaxed">
                    {role.description}
                  </p>

                  {/* Progress Preview */}
                  <div className="space-y-3">
                    <div className="text-white/50 text-sm">Progress</div>
                    <div className="flex gap-2 justify-center">
                      {role.levels.map((level, index) => (
                        <div
                          key={level.id}
                          className={`w-3 h-3 rounded-full ${
                            level.completed 
                              ? 'bg-white/80' 
                              : level.unlocked 
                                ? 'bg-white/40' 
                                : 'bg-white/10'
                          }`}
                        />
                      ))}
                    </div>
                    <div className="text-white/40 text-xs">
                      {role.levels.filter(l => l.completed).length} / {role.levels.length} levels completed
                    </div>
                  </div>

                  {/* Action indicator */}
                  <div className="pt-4 text-white/50 text-sm group-hover:text-white/70 transition-colors">
                    Click to begin your journey →
                  </div>
                </div>

                {/* Hover glow effect */}
                <div className="absolute inset-0 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-gradient-to-br from-white/10 to-transparent" />
              </div>
            );
          })}
        </div>

        {/* Footer */}
        <div className="text-center mt-16 space-y-4">
          <p className="text-white/50">
            Master 3 challenging levels with unique boss encounters
          </p>
          <div className="flex justify-center gap-8 text-sm text-white/40">
            <span>🟢 Beginner</span>
            <span>🟡 Intermediate</span>
            <span>🔴 Expert</span>
          </div>
        </div>
      </div>
    </div>
  );
}