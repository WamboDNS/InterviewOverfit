import React, { useState } from "react";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { Send } from "lucide-react";

interface ChatInputProps {
  onSendMessage: (content: string, isCode: boolean) => void;
  disabled?: boolean;
}

export function ChatInput({ onSendMessage, disabled = false }: ChatInputProps) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;

    // Detect if input looks like code (contains common code patterns)
    const isCode = /[{}\[\];()=>]|\/\/|\/\*|\*\/|function|const|let|var|import|export|class|if|for|while/.test(input);
    
    onSendMessage(input, isCode);
    setInput("");
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="relative p-6 bg-black/40 backdrop-blur-xl border border-white/20 rounded-3xl shadow-2xl">
      {/* Glass effect overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-white/2 rounded-3xl" />
      
      <div className="relative z-10 space-y-4">
        <div className="relative">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Type your response or code here..."
            disabled={disabled}
            className="bg-white/5 backdrop-blur-sm border-white/20 text-white placeholder:text-white/50 focus:border-white/40 focus:ring-white/20 rounded-2xl min-h-[120px] resize-none pr-16"
          />
          
          <Button
            onClick={handleSend}
            disabled={disabled || !input.trim()}
            className="absolute right-3 bottom-3 h-10 w-10 p-0 bg-white/90 hover:bg-white text-black border-0 rounded-xl backdrop-blur-sm"
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>

        {/* Hint text */}
        <div className="text-center">
          <span className="text-xs text-white/40">
            Cmd/Ctrl + Enter to send • Auto-detects code vs text
          </span>
        </div>
      </div>
    </div>
  );
}