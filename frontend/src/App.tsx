import React, { useState, useEffect } from "react";
import { GameScreen, Role, LevelData, GameProgress } from "./types/gameTypes";
import { LoadingScreen } from "./components/LoadingScreen";
import { RoleSelection } from "./components/RoleSelection";
import { GameMap } from "./components/GameMap";
import { GameBattle } from "./components/GameBattle";
import { WinLossScreen } from "./components/WinLossScreen";
import { 
  initializeGameProgress, 
  updateProgressAfterVictory, 
  saveGameProgress, 
  loadGameProgress,
  getStarsForLevel 
} from "./utils/gameProgress";

export default function App() {
  const [currentScreen, setCurrentScreen] = useState<GameScreen>('loading');
  const [selectedRole, setSelectedRole] = useState<Role | null>(null);
  const [selectedLevel, setSelectedLevel] = useState<LevelData | null>(null);
  const [gameProgress, setGameProgress] = useState<GameProgress>(() => loadGameProgress());
  const [battleResult, setBattleResult] = useState<{
    result: 'victory' | 'defeat';
    score: number;
    stars: number;
  } | null>(null);

  // Save progress whenever it changes
  useEffect(() => {
    saveGameProgress(gameProgress);
  }, [gameProgress]);

  // Screen transition handlers
  const handleLoadingComplete = () => {
    setCurrentScreen('roleSelection');
  };

  const handleRoleSelect = (role: Role) => {
    setSelectedRole(role);
    setCurrentScreen('map');
  };

  const handleLevelSelect = (level: LevelData) => {
    setSelectedLevel(level);
    setCurrentScreen('battle');
  };

  const handleBattleComplete = (result: 'victory' | 'defeat', score: number, stars: number) => {
    setBattleResult({ result, score, stars });
    
    // Update progress if victory
    if (result === 'victory' && selectedRole && selectedLevel) {
      const newProgress = updateProgressAfterVictory(
        gameProgress, 
        selectedRole, 
        selectedLevel.id, 
        stars
      );
      setGameProgress(newProgress);
    }
    
    setCurrentScreen('winLoss');
  };

  const handleWinLossContinue = () => {
    setSelectedLevel(null);
    setBattleResult(null);
    setCurrentScreen('map');
  };

  const handleRetryBattle = () => {
    setBattleResult(null);
    setCurrentScreen('battle');
  };

  const handleBackToRoles = () => {
    setSelectedRole(null);
    setSelectedLevel(null);
    setCurrentScreen('roleSelection');
  };

  // Create progress summary for GameMap
  const getProgressSummary = () => {
    if (!selectedRole) return {};
    
    const summary: Record<string, { completed: boolean; stars: number }> = {};
    const roleProgress = gameProgress.roleProgress[selectedRole];
    
    roleProgress.unlockedLevels.forEach(levelId => {
      const stars = getStarsForLevel(gameProgress, selectedRole!, levelId);
      summary[levelId] = {
        completed: stars > 0,
        stars
      };
    });
    
    return summary;
  };

  // Render current screen
  const renderCurrentScreen = () => {
    switch (currentScreen) {
      case 'loading':
        return <LoadingScreen onComplete={handleLoadingComplete} />;
      
      case 'roleSelection':
        return <RoleSelection onSelectRole={handleRoleSelect} />;
      
      case 'map':
        return selectedRole ? (
          <GameMap
            role={selectedRole}
            onSelectLevel={handleLevelSelect}
            onBack={handleBackToRoles}
            progress={getProgressSummary()}
          />
        ) : null;
      
      case 'battle':
        return selectedLevel ? (
          <GameBattle
            level={selectedLevel}
            onComplete={handleBattleComplete}
            onBack={() => setCurrentScreen('map')}
          />
        ) : null;
      
      case 'winLoss':
        return battleResult && selectedLevel ? (
          <WinLossScreen
            result={battleResult.result}
            level={selectedLevel}
            score={battleResult.score}
            stars={battleResult.stars}
            onContinue={handleWinLossContinue}
            onRetry={battleResult.result === 'defeat' ? handleRetryBattle : undefined}
          />
        ) : null;
      
      default:
        return <LoadingScreen onComplete={handleLoadingComplete} />;
    }
  };

  return (
    <div className="min-h-screen">
      {renderCurrentScreen()}
    </div>
  );
}