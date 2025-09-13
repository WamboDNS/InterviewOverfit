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
    let interval: NodeJS.Timeout;
    let timeoutId: NodeJS.Timeout;
    
    const startLoading = () => {
      interval = setInterval(() => {
        setProgress(prev => {
          const newProgress = Math.min(prev + Math.random() * 3 + 1, 100);
          
          // Update loading text based on progress
          const stepIndex = Math.floor((newProgress / 100) * loadingSteps.length);
          if (stepIndex < loadingSteps.length && stepIndex !== Math.floor((prev / 100) * loadingSteps.length)) {
            setLoadingText(loadingSteps[stepIndex]);
          }

          if (newProgress >= 100) {
            clearInterval(interval);
            timeoutId = setTimeout(() => {
              onComplete();
            }, 800);
            return 100;
          }
          return newProgress;
        });
      }, 100);
    };

    // Add a small delay before starting to ensure smooth animation
    const startDelay = setTimeout(startLoading, 200);

    return () => {
      clearTimeout(startDelay);
      clearInterval(interval);
      clearTimeout(timeoutId);
    };
  }, [onComplete, loadingSteps]);

  return (
    <div className="min-h-screen max-h-screen bg-gradient-to-br from-black via-gray-900 to-black flex items-center justify-center relative overflow-hidden p-4">
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

      <div className="relative z-10 text-center space-y-6 lg:space-y-8 max-w-md mx-auto px-4">
        {/* App Logo/Title */}
        <div className="space-y-3 lg:space-y-4">
          <div className="w-20 h-20 lg:w-24 lg:h-24 mx-auto bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl flex items-center justify-center text-3xl lg:text-4xl">
            🎯
          </div>
          <h1 className="text-3xl lg:text-5xl font-bold text-white/95 tracking-tight">
            Interview<span className="text-white/70">Overfit</span>
          </h1>
          <p className="text-white/60 text-base lg:text-lg">
            Master technical interviews through gamified learning
          </p>
        </div>

        {/* Progress Bar */}
        <div className="space-y-4">
          <div className="relative">
            <div className="h-2 bg-black/30 backdrop-blur-sm rounded-full overflow-hidden border border-white/10">
              <div 
                className="h-full bg-gradient-to-r from-white/80 to-white/60 transition-all duration-500 ease-out relative rounded-full"
                style={{ width: `${progress}%` }}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-white/20 via-white/40 to-white/20 animate-pulse rounded-full" />
              </div>
            </div>
          </div>
          
          <div className="text-white/70 text-sm font-medium min-h-[1.25rem]">
            {loadingText}
          </div>
          
          <div className="text-white/50 text-xs">
            {Math.round(progress)}% Complete
          </div>
        </div>

        {/* Floating elements */}
        <div className="absolute top-16 lg:top-20 left-8 lg:left-10 w-3 h-3 bg-white/20 rounded-full animate-bounce" style={{ animationDelay: '0s' }} />
        <div className="absolute top-24 lg:top-32 right-12 lg:right-16 w-2 h-2 bg-white/30 rounded-full animate-bounce" style={{ animationDelay: '0.5s' }} />
        <div className="absolute bottom-32 lg:bottom-40 left-16 lg:left-20 w-4 h-4 bg-white/15 rounded-full animate-bounce" style={{ animationDelay: '1s' }} />
        <div className="absolute bottom-20 lg:bottom-24 right-10 lg:right-12 w-2 h-2 bg-white/25 rounded-full animate-bounce" style={{ animationDelay: '1.5s' }} />
      </div>
    </div>
  );
}