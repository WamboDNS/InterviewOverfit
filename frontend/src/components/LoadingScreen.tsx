import React, { useEffect, useState } from "react";

interface LoadingScreenProps {
  onComplete: () => void;
}

export function LoadingScreen({ onComplete }: LoadingScreenProps) {
  const [progress, setProgress] = useState(0);
  const [loadingText, setLoadingText] = useState("Initializing InterviewOverfit...");

  const loadingSteps = [
    "Initializing InterviewOverfit...",
    "Loading interview challenges...",
    "Preparing boss encounters...",
    "Optimizing your learning path...",
    "Almost ready to begin..."
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress(prev => {
        const newProgress = prev + 2;
        
        // Update loading text based on progress
        const stepIndex = Math.floor((newProgress / 100) * loadingSteps.length);
        if (stepIndex < loadingSteps.length) {
          setLoadingText(loadingSteps[stepIndex]);
        }

        if (newProgress >= 100) {
          clearInterval(interval);
          setTimeout(onComplete, 500);
          return 100;
        }
        return newProgress;
      });
    }, 50);

    return () => clearInterval(interval);
  }, [onComplete]);

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

      <div className="relative z-10 text-center space-y-8 max-w-md mx-auto px-6">
        {/* App Logo/Title */}
        <div className="space-y-4">
          <div className="w-24 h-24 mx-auto bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl flex items-center justify-center text-4xl">
            🎯
          </div>
          <h1 className="text-5xl font-bold text-white/95 tracking-tight">
            Interview<span className="text-white/70">Overfit</span>
          </h1>
          <p className="text-white/60 text-lg">
            Master technical interviews through gamified learning
          </p>
        </div>

        {/* Progress Bar */}
        <div className="space-y-4">
          <div className="relative">
            <div className="h-2 bg-black/30 backdrop-blur-sm rounded-full overflow-hidden border border-white/10">
              <div 
                className="h-full bg-gradient-to-r from-white/80 to-white/60 transition-all duration-300 ease-out relative rounded-full"
                style={{ width: `${progress}%` }}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-white/20 via-white/40 to-white/20 animate-pulse rounded-full" />
              </div>
            </div>
          </div>
          
          <div className="text-white/70 text-sm font-medium">
            {loadingText}
          </div>
          
          <div className="text-white/50 text-xs">
            {progress}% Complete
          </div>
        </div>

        {/* Floating elements */}
        <div className="absolute top-20 left-10 w-3 h-3 bg-white/20 rounded-full animate-bounce" style={{ animationDelay: '0s' }} />
        <div className="absolute top-32 right-16 w-2 h-2 bg-white/30 rounded-full animate-bounce" style={{ animationDelay: '0.5s' }} />
        <div className="absolute bottom-40 left-20 w-4 h-4 bg-white/15 rounded-full animate-bounce" style={{ animationDelay: '1s' }} />
        <div className="absolute bottom-24 right-12 w-2 h-2 bg-white/25 rounded-full animate-bounce" style={{ animationDelay: '1.5s' }} />
      </div>
    </div>
  );
}