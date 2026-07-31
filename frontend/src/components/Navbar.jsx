import React from 'react';
import { Sparkles, Shield, User, FileText } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab }) {
  return (
    <header className="sticky top-0 z-50 glass-card rounded-none border-t-0 border-x-0 border-b border-white/10 px-6 py-3.5 flex items-center justify-between">
      <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-cyan-400 flex items-center justify-center shadow-lg shadow-indigo-500/25">
          <Sparkles className="w-5 h-5 text-white animate-pulse" />
        </div>
        <div>
          <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
            HireMind <span className="gradient-text font-black">AI</span>
          </h1>
          <p className="text-xs text-gray-400 font-medium">Career Intelligence Platform</p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="hidden md:flex items-center gap-2 bg-gray-900/60 px-3.5 py-1.5 rounded-full border border-white/5 text-xs text-gray-300">
          <Shield className="w-3.5 h-3.5 text-cyan-400" />
          <span>SaaS Production v2.0</span>
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
        </div>

        <button 
          onClick={() => setActiveTab('recruiter')}
          className="px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-gray-800 hover:bg-gray-700 text-gray-200 border border-white/10 transition"
        >
          Recruiter Portal
        </button>

        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-purple-500 to-indigo-600 flex items-center justify-center text-white text-xs font-bold shadow-md">
          HM
        </div>
      </div>
    </header>
  );
}
