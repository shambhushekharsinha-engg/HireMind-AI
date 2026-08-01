import React, { useState } from 'react';
import { Shield, Sparkles, LogOut, LogIn, UserCheck } from 'lucide-react';
import AuthModal from './AuthModal';

export default function Navbar({ user, setUser }) {
  const [showAuthModal, setShowAuthModal] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem('hiremind_token');
    localStorage.removeItem('hiremind_user');
    setUser(null);
  };

  return (
    <>
      <header className="h-16 border-b border-indigo-500/20 bg-slate-950/80 backdrop-blur-xl px-6 flex items-center justify-between sticky top-0 z-40 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 via-indigo-500 to-purple-600 p-0.5 shadow-md flex items-center justify-center">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
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

          {user ? (
            <div className="flex items-center gap-2">
              <div className="hidden sm:block text-right">
                <p className="text-xs font-bold text-white">{user.full_name || user.email}</p>
                <p className="text-[10px] font-semibold text-cyan-300 uppercase tracking-wider">{user.role || 'student'}</p>
              </div>
              <button
                onClick={handleLogout}
                className="p-2 rounded-xl text-xs bg-slate-900 hover:bg-slate-800 text-red-400 border border-red-500/30 transition flex items-center gap-1"
                title="Sign Out"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <button
              onClick={() => setShowAuthModal(true)}
              className="px-4 py-2 rounded-xl text-xs font-bold bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white shadow-md transition flex items-center gap-1.5"
            >
              <LogIn className="w-4 h-4" /> Sign In / Recruiter Login
            </button>
          )}

          <a
            href="https://github.com/shambhushekharsinha-engg/HireMind-AI"
            target="_blank"
            rel="noopener noreferrer"
            className="px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-slate-900 hover:bg-slate-800 text-gray-300 border border-white/10 hover:border-white/20 transition flex items-center gap-1.5"
          >
            <UserCheck className="w-4 h-4 text-purple-400" /> Recruiter Portal
          </a>
        </div>
      </header>

      {showAuthModal && (
        <AuthModal
          onClose={() => setShowAuthModal(false)}
          onSuccess={(userData) => {
            setUser(userData);
            setShowAuthModal(false);
          }}
        />
      )}
    </>
  );
}
