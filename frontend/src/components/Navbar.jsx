import React, { useState } from 'react';
import { Sparkles, Shield, Globe, Settings, Check, X, RefreshCw } from 'lucide-react';
import { getApiBaseUrl } from '../config';

export default function Navbar({ activeTab, setActiveTab }) {
  const [showSettings, setShowSettings] = useState(false);
  const [apiUrl, setApiUrl] = useState(getApiBaseUrl());
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState('');

  const handleSave = () => {
    const cleaned = apiUrl.trim().replace(/\/$/, "");
    localStorage.setItem('hiremind_api_url', cleaned);
    setShowSettings(false);
    window.location.reload();
  };

  const handleTest = async () => {
    setTesting(true);
    setTestResult('');
    const target = apiUrl.trim().replace(/\/$/, "");
    try {
      const res = await fetch(`${target}/health`, { signal: AbortSignal.timeout(15000) });
      if (res.ok) {
        setTestResult('online');
      } else {
        setTestResult('offline');
      }
    } catch (e) {
      setTestResult('offline');
    } finally {
      setTesting(false);
    }
  };

  return (
    <>
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
            onClick={() => setShowSettings(true)}
            className="p-2 rounded-xl text-xs font-semibold bg-slate-900 hover:bg-slate-800 text-cyan-300 border border-cyan-500/30 flex items-center gap-1.5 shadow-md transition"
            title="Configure Backend API Server URL"
          >
            <Globe className="w-4 h-4" />
            <span className="hidden sm:inline">API Config</span>
          </button>

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

      {/* API Configuration Modal */}
      {showSettings && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="glass-card max-w-md w-full p-6 space-y-4 border-indigo-500/40 animate-fade-in shadow-2xl relative">
            <div className="flex items-center justify-between border-b border-white/10 pb-3">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Globe className="w-5 h-5 text-cyan-400" />
                Backend API Configuration
              </h3>
              <button onClick={() => setShowSettings(false)} className="text-gray-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-gray-300 leading-relaxed">
              Enter your deployed FastAPI backend URL (e.g. from Render or Railway).
            </p>

            <div className="space-y-2">
              <label className="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">
                Backend Server URL
              </label>
              <input
                type="text"
                value={apiUrl}
                onChange={(e) => setApiUrl(e.target.value)}
                placeholder="https://your-backend-name.onrender.com"
                className="w-full px-3.5 py-2.5 rounded-xl bg-gray-900 border border-white/10 text-xs text-cyan-300 font-mono focus:outline-none focus:border-indigo-500"
              />
            </div>

            {testResult && (
              <div className={`p-3 rounded-xl text-xs font-bold flex items-center gap-2 ${
                testResult === 'online' ? 'bg-emerald-950/60 text-emerald-300 border border-emerald-500/30' : 'bg-red-950/60 text-red-300 border border-red-500/30'
              }`}>
                {testResult === 'online' ? '● Backend Connected Successfully!' : '⚠️ Cannot reach backend URL. Check URL or wait for Render cold start.'}
              </div>
            )}

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                onClick={handleTest}
                disabled={testing}
                className="px-4 py-2 rounded-xl text-xs font-semibold bg-gray-800 hover:bg-gray-700 text-gray-200 border border-white/10 flex items-center gap-1.5"
              >
                {testing ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Globe className="w-3.5 h-3.5" />}
                Test Connection
              </button>

              <button
                onClick={handleSave}
                className="glow-btn px-5 py-2 rounded-xl text-xs font-bold flex items-center gap-1.5"
              >
                <Check className="w-4 h-4" /> Save & Connect
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
