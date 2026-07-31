import React from 'react';
import { Sparkles, Shield } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab }) {
  return (
    <header className="sticky top-0 z-50 glass-card rounded-none border-t-0 border-x-0 border-b border-white/10 px-6 py-3.5 flex items-center justify-between shadow-2xl backdrop-blur-xl bg-slate-950/80">
      <div className="flex items-center gap-3.5 cursor-pointer group" onClick={() => setActiveTab('dashboard')}>
        <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-cyan-400 p-0.5 shadow-lg shadow-indigo-500/30 group-hover:scale-105 transition duration-300">
          <div className="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-cyan-400 animate-pulse" />
          </div>
        </div>
        <div>
          <h1 className="text-xl font-black tracking-tight text-white flex items-center gap-2">
            HireMind <span className="gradient-text font-black">AI</span>
          </h1>
          <p className="text-[10px] text-indigo-300 font-semibold tracking-wider uppercase">Enterprise Career Operating System</p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden lg:flex items-center gap-2.5 bg-slate-900/80 px-4 py-1.5 rounded-full border border-indigo-500/20 text-xs text-gray-300 shadow-inner">
          <Shield className="w-3.5 h-3.5 text-cyan-400" />
          <span className="font-semibold text-gray-200">Production Enterprise v3.0</span>
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
        </div>

        <button 
          onClick={() => setActiveTab('recruiter')}
          className="px-4 py-2 rounded-xl text-xs font-bold bg-slate-900 hover:bg-slate-800 text-indigo-300 border border-indigo-500/30 hover:border-indigo-500/60 shadow-md transition"
        >
          Recruiter Portal
        </button>

        <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-indigo-600 to-purple-600 p-0.5 shadow-md flex items-center justify-center text-white text-xs font-black">
          HM
        </div>
      </div>
    </header>
  );
}
