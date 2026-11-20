import React, { useState } from 'react';
import { Bot, Send, User, Sparkles, RefreshCw, Cpu, Zap } from 'lucide-react';
import { getApiBaseUrl } from '../config';

const INITIAL_MESSAGES = [
  { 
    sender: 'ai', 
    text: "Hello! I am your HireMind AI Career Coach. Ask me anything about ATS resume tuning, FAANG interview loops, salary negotiation strategies, or transitioning to AI/ML systems!",
    time: "Just now",
    engine: "🤖 Amazon Bedrock (Claude 3.5 Haiku)"
  }
];

export default function CoachPage() {
  const [messages, setMessages] = useState(INITIAL_MESSAGES);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const generateFallbackResponse = (query) => {
    const q = query.toLowerCase();
    if (q.includes('salary') || q.includes('negotiat') || q.includes('offer')) {
      return "When negotiating an engineering offer, always ground your counter-offer in objective market percentiles (e.g., Levels.fyi P75/P90). Focus first on Base Salary and Sign-on Bonus before Equity vesting schedules. State clearly: 'Based on my track record in high-throughput microservices and current market benchmarks, I was targeting $X base salary with standard equity.' Never reveal your current or past compensation.";
    }
    if (q.includes('resume') || q.includes('ats') || q.includes('score')) {
      return "To score in the top 5% of ATS systems: 1) Use single-column layouts without complex tables or textboxes. 2) Structure every bullet point using the Google XYZ formula: 'Accomplished [X], as measured by [Y], by doing [Z]'. 3) Ensure at least 80% of your bullets start with decisive past-tense action verbs (Engineered, Architected, Spearheaded). 4) Include a dedicated 'Technical Skills' section with exact keyword matches.";
    }
    if (q.includes('interview') || q.includes('system design') || q.includes('faang') || q.includes('google') || q.includes('amazon')) {
      return "For tier-1 tech interviews: 1) In coding rounds, speak before coding: clarify inputs, edge cases (empty arrays, integer overflow), and state worst-case time/space complexity upfront. 2) In system design, begin with functional vs non-functional requirements, calculate back-of-the-envelope RPS and storage requirements, establish high-level API contracts, and then drill into caching and partition strategies.";
    }
    return `That is a critical engineering career question. My core recommendation is to focus on measurable business impact: whether you are optimizing model inference latency, writing clean TypeScript microservices, or leading technical RFCs, employers prioritize engineers who demonstrate direct ownership of reliability and performance metrics.`;
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setInput('');
    setMessages(prev => [...prev, { sender: 'user', text: userMsg, time: "Just now" }]);
    setLoading(true);

    const activeUrl = getApiBaseUrl();
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 6000);

    try {
      const response = await fetch(`${activeUrl}/api/v1/coach/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userMsg }),
        signal: controller.signal
      });
      clearTimeout(timeoutId);

      if (response.ok) {
        const data = await response.json();
        setMessages(prev => [
          ...prev, 
          { 
            sender: 'ai', 
            text: data.response || generateFallbackResponse(userMsg),
            time: "Just now",
            engine: "🤖 Amazon Bedrock (Claude 3.5 Haiku)"
          }
        ]);
      } else {
        const fallbackText = generateFallbackResponse(userMsg);
        setMessages(prev => [
          ...prev, 
          { 
            sender: 'ai', 
            text: fallbackText,
            time: "Just now",
            engine: "⚡ Deterministic Heuristic Advisor Failover"
          }
        ]);
      }
    } catch (err) {
      clearTimeout(timeoutId);
      const fallbackText = generateFallbackResponse(userMsg);
      setMessages(prev => [
        ...prev, 
        { 
          sender: 'ai', 
          text: fallbackText,
          time: "Just now",
          engine: "⚡ Deterministic Heuristic Advisor Failover"
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center gap-2">
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            AI Career <span className="gradient-text">Mentor</span>
          </h2>
          <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
            Claude 3.5 Haiku & Redundant
          </span>
        </div>
        <p className="text-xs text-gray-400">Conversational AI mentor for engineering career growth, interview preparation, and compensation negotiation</p>
      </div>

      <div className="glass-card p-5 sm:p-6 flex flex-col h-[560px] justify-between border-indigo-500/30">
        
        {/* Messages Stream */}
        <div className="space-y-4 overflow-y-auto pr-2 flex-1">
          {messages.map((m, i) => (
            <div key={i} className={`flex items-start gap-3 ${m.sender === 'user' ? 'flex-row-reverse' : ''}`}>
              <div className={`w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold shrink-0 ${
                m.sender === 'user' 
                  ? 'bg-gradient-to-tr from-cyan-600 to-indigo-600 text-white shadow-md' 
                  : 'bg-purple-900/40 text-cyan-300 border border-indigo-500/30 shadow-md'
              }`}>
                {m.sender === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>
              
              <div className="space-y-1 max-w-xl">
                <div className={`p-4 rounded-2xl text-xs leading-relaxed ${
                  m.sender === 'user' 
                    ? 'bg-indigo-600 text-white shadow-md' 
                    : 'bg-slate-900/90 border border-white/10 text-gray-200'
                }`}>
                  {m.text}
                </div>
                {m.engine && (
                  <div className="text-[10px] text-gray-500 font-mono flex items-center gap-1.5 px-1">
                    <Cpu className="w-3 h-3 text-cyan-400" />
                    <span>{m.engine}</span>
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-xl bg-purple-900/40 text-cyan-300 border border-indigo-500/30 flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4 animate-pulse" />
              </div>
              <div className="p-3.5 rounded-2xl bg-slate-900 border border-white/10 text-xs text-cyan-300 flex items-center gap-2">
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                <span>AI Mentor synthesizing strategic advice...</span>
              </div>
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div className="pt-4 border-t border-white/10 flex items-center gap-3">
          <input
            type="text"
            placeholder="Ask about resume improvements, salary negotiation, system design, or interview loops..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            className="flex-1 bg-slate-900 border border-white/10 rounded-xl px-4 py-3 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500"
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="glow-btn px-5 py-3 rounded-xl text-xs font-bold flex items-center gap-1.5 disabled:opacity-50"
          >
            <Send className="w-4 h-4 text-cyan-300" />
            <span className="hidden sm:inline">Send</span>
          </button>
        </div>
      </div>
    </div>
  );
}
