import React, { useState } from 'react';
import { Bot, User, Sparkles, Send, RefreshCw, BookOpen } from 'lucide-react';

export default function CoachPage() {
  const [messages, setMessages] = useState([
    {
      sender: 'assistant',
      text: 'Hello! I am your HireMind AI Career Coach. Ask me anything about learning roadmaps, resume improvements, interview strategy, or target career roles!',
      suggested_followups: ['What should I learn next for ML?', 'Why is my ATS score low?', 'Suggest projects for my portfolio.'],
      recommended_resources: ['HireMind AI Learning Hub', 'Resume Rewriter Engine']
    }
  ]);

  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAsk = async (queryText) => {
    const q = queryText || input;
    if (!q.trim()) return;

    const userMsg = { sender: 'user', text: q };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/coach/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q })
      });
      const data = await response.json();
      const assistantMsg = {
        sender: 'assistant',
        text: data.answer,
        suggested_followups: data.suggested_followups,
        recommended_resources: data.recommended_resources
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          AI Career <span className="gradient-text">Coach Assistant</span>
        </h2>
        <p className="text-xs text-gray-400">Conversational AI guidance for learning paths, resume bullets & interview tactics</p>
      </div>

      {/* Chat Messages Container */}
      <div className="glass-card p-6 min-h-[500px] max-h-[600px] overflow-y-auto space-y-4 flex flex-col justify-between border-indigo-500/30">
        <div className="space-y-4">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex gap-3 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              {msg.sender === 'assistant' && (
                <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-600 to-cyan-400 flex items-center justify-center text-white shrink-0">
                  <Bot className="w-4 h-4 animate-pulse" />
                </div>
              )}

              <div className={`max-w-xl p-4 rounded-2xl text-xs space-y-2 leading-relaxed ${
                msg.sender === 'user'
                  ? 'bg-indigo-600 text-white rounded-tr-none'
                  : 'bg-gray-900/90 text-gray-200 border border-white/10 rounded-tl-none'
              }`}>
                <p>{msg.text}</p>

                {msg.suggested_followups && (
                  <div className="pt-2 border-t border-white/10 space-y-1.5">
                    <span className="text-[10px] font-bold text-indigo-300 uppercase block">Suggested Questions</span>
                    <div className="flex flex-wrap gap-1.5">
                      {msg.suggested_followups.map((f, i) => (
                        <button
                          key={i}
                          onClick={() => handleAsk(f)}
                          className="px-2.5 py-1 rounded-lg bg-indigo-950/80 hover:bg-indigo-900 border border-indigo-500/30 text-[10px] font-semibold text-indigo-300 text-left transition"
                        >
                          {f}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {msg.sender === 'user' && (
                <div className="w-8 h-8 rounded-xl bg-purple-600 flex items-center justify-center text-white shrink-0 font-bold text-xs">
                  ME
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Input Bar */}
        <div className="pt-4 border-t border-white/10 flex gap-2">
          <input
            type="text"
            placeholder="Ask AI Coach anything (e.g. 'How do I become an ML Engineer?')..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
            className="flex-1 px-4 py-3 rounded-xl bg-gray-900/90 border border-white/10 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 font-sans"
          />
          <button
            onClick={() => handleAsk()}
            disabled={loading}
            className="glow-btn px-6 py-3 rounded-xl text-xs font-bold flex items-center gap-2 disabled:opacity-50"
          >
            {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
          </button>
        </div>
      </div>
    </div>
  );
}
