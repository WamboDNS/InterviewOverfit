import { ScrollArea } from "./ui/scroll-area";
import { Avatar, AvatarFallback } from "./ui/avatar";
import { ChatMessage } from "../types/gameTypes";

interface ChatFeedProps {
  messages: ChatMessage[];
}

export function ChatFeed({ messages }: ChatFeedProps) {
  const CodeBlock = ({ code }: { code: string }) => (
    <pre className="bg-black/40 backdrop-blur-sm border border-white/10 rounded-xl p-3 overflow-x-auto text-sm">
      <code className="text-white/80">{code}</code>
    </pre>
  );

  return (
    <div className="h-full bg-black/40 backdrop-blur-xl border border-white/20 rounded-3xl shadow-2xl overflow-hidden relative">
      {/* Glass effect overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-white/2 rounded-3xl" />
      
      <div className="relative z-10 h-full p-6">
        <div className="flex items-center justify-center mb-6 pb-3 border-b border-white/10">
          <h3 className="text-white/90">Battle Log</h3>
          <div className="ml-3 w-2 h-2 bg-white/60 rounded-full animate-pulse" />
        </div>
        
        <ScrollArea className="h-[calc(100%-4rem)] pr-4">
          <div className="space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${message.type === 'user' ? 'flex-row-reverse' : ''}`}
              >
                <Avatar className="w-8 h-8 border border-white/20 bg-black/20 backdrop-blur-sm">
                  <AvatarFallback className={`text-xs backdrop-blur-sm ${
                    message.type === 'boss' 
                      ? 'bg-black/40 text-white/80' 
                      : 'bg-white/20 text-white/90'
                  }`}>
                    {message.type === 'boss' ? 'AI' : 'YOU'}
                  </AvatarFallback>
                </Avatar>

                <div className={`max-w-[70%] ${message.type === 'user' ? 'text-right' : ''}`}>
                  <div className={`relative p-3 backdrop-blur-md border rounded-2xl shadow-lg ${
                    message.type === 'boss'
                      ? 'bg-black/30 border-white/20 text-white/90'
                      : 'bg-white/10 border-white/30 text-white/95'
                  }`}>
                    {message.isCode ? (
                      <CodeBlock code={message.content} />
                    ) : (
                      <p className="text-sm leading-relaxed">{message.content}</p>
                    )}
                  </div>
                  
                  <div className={`text-xs text-white/40 mt-1 ${
                    message.type === 'user' ? 'text-right' : ''
                  }`}>
                    {message.timestamp.toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>
      </div>
    </div>
  );
}