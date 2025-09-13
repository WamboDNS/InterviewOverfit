import { useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Textarea } from "./ui/textarea";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import { MessageSquare, Code, Zap } from "lucide-react";

interface InputSectionProps {
  onSendMessage: (content: string, isCode: boolean) => void;
  disabled?: boolean;
}

export function InputSection({ onSendMessage, disabled = false }: InputSectionProps) {
  const [chatInput, setChatInput] = useState("");
  const [codeInput, setCodeInput] = useState("");
  const [activeTab, setActiveTab] = useState("chat");

  const handleSend = () => {
    const content = activeTab === "chat" ? chatInput : codeInput;
    if (!content.trim()) return;

    onSendMessage(content, activeTab === "code");
    
    if (activeTab === "chat") {
      setChatInput("");
    } else {
      setCodeInput("");
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="p-6 bg-black border-2 border-white shadow-2xl relative">
      {/* Corner accents */}
      <div className="absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 border-white" />
      <div className="absolute top-0 right-0 w-4 h-4 border-t-2 border-r-2 border-white" />
      <div className="absolute bottom-0 left-0 w-4 h-4 border-b-2 border-l-2 border-white" />
      <div className="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-white" />
      
      {/* Inner glow */}
      <div className="absolute inset-2 bg-gradient-to-br from-white/5 to-transparent" />
      
      <div className="relative z-10">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-4 bg-gray-900 border border-gray-600">
            <TabsTrigger 
              value="chat" 
              className="data-[state=active]:bg-white data-[state=active]:text-black font-mono text-white flex items-center gap-2"
            >
              <MessageSquare className="w-4 h-4" />
              CHAT
            </TabsTrigger>
            <TabsTrigger 
              value="code" 
              className="data-[state=active]:bg-white data-[state=active]:text-black font-mono text-white flex items-center gap-2"
            >
              <Code className="w-4 h-4" />
              CODE
            </TabsTrigger>
          </TabsList>

          <TabsContent value="chat" className="space-y-4">
            <div className="relative">
              <Input
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Enter response..."
                disabled={disabled}
                className="bg-gray-900 border-gray-400 text-white placeholder:text-gray-500 focus:border-white focus:ring-white font-mono pr-20"
              />
              <Button
                onClick={handleSend}
                disabled={disabled || !chatInput.trim()}
                className="absolute right-1 top-1 h-8 bg-white text-black hover:bg-gray-200 border-0 font-mono"
                size="sm"
              >
                <Zap className="w-4 h-4 mr-1" />
                SEND
              </Button>
            </div>
          </TabsContent>

          <TabsContent value="code" className="space-y-4">
            <div className="relative">
              <Textarea
                value={codeInput}
                onChange={(e) => setCodeInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="// Execute code..."
                disabled={disabled}
                className="bg-gray-900 border-gray-400 text-green-400 placeholder:text-gray-600 focus:border-white focus:ring-white font-mono text-sm min-h-[100px] resize-none"
              />
              <Button
                onClick={handleSend}
                disabled={disabled || !codeInput.trim()}
                className="absolute right-2 bottom-2 h-8 bg-white text-black hover:bg-gray-200 border-0 font-mono"
                size="sm"
              >
                <Zap className="w-4 h-4 mr-1" />
                EXEC
              </Button>
            </div>
          </TabsContent>
        </Tabs>

        {/* System info */}
        <div className="mt-4 flex justify-between text-xs font-mono text-gray-500">
          <span>SYSTEM.READY</span>
          <span>ENTER.TO.EXECUTE</span>
        </div>
      </div>
    </div>
  );
}