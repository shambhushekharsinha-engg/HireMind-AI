import React, { useState } from 'react';
import { Bot, Send, User, Sparkles } from 'lucide-react';
import { API_BASE_URL } from '../config';

export default function CoachPage() {
  const [messages, setMessages] = useState([
    { sender: 'ai', text: "Hello! I am your HireMind AI Career Coach. Ask me anything about resume optimization, target companies, or interview strategy!" }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = input;
    setInput('');
    setMessages(prev => [...prev, { sender: 'user', text: userMsg }]);
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/coach/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userMsg })
      });
      const data = await response.json();
      setMessages(prev => [...prev, { sender: 'ai', text: data.response }]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          AI Career <span className="gradient-text">Mentor</span>
        </h2>
        <p className="text-xs text-gray-400">Conversational AI advisor for career growth and interview guidance</p>
      </div>

      <div className="glass-card p-6 flex flex-col h-[520px] justify-between border-indigo-500/30">
        <div className="space-y-4 overflow-y-auto pr-2 flex-1">
          {messages.map((m, i) => (
            <div key={i} className={`flex items-start gap-3 ${m.sender === 'user' ? 'flex-row-reverse' : ''}`}>
              <div className={`w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold shrink-0 ${
                m.sender === 'user' ? 'bg-indigo-600 text-white' : 'bg-purple-600/30 text-purple-300 border border-purple-500/30'
              }`}>
                {m.sender === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>
              <div className={`p-4 rounded-2xl text-xs max-w-xl leading-relaxed ${
                m.sender === 'user' ? 'bg-indigo-600 text-white' : 'bg-gray-900/80 border border-white/10 text-gray-200'
              }`}>
                {m.text}
              </div>
            </div>
          ))}
        </div>

        <div className="pt-4 border-t border-white/10 flex items-center gap-3">
          <input
            type="text"
            placeholder="Ask AI Coach e.g. 'How do I prepare for Microsoft SDE interview?'"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            className="flex-1 px-4 py-3 rounded-xl bg-gray-900 border border-white/10 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
          />
          <button
            onClick={handleSend}
            disabled={loading}
            className="glow-btn px-6 py-3 rounded-xl text-xs font-bold flex items-center gap-2 shrink-0"
          >
            <Send className="w-4 h-4" /> Send
          </button>
        </div>
      </div>
    </div>
  );
}
