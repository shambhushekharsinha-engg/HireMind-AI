import React, { useState } from 'react';
import { Sparkles, Shield, Lock, ArrowRight, CheckCircle2, UserCheck, KeyRound, Mail, User, Briefcase, Zap, AlertCircle } from 'lucide-react';
import { getApiBaseUrl } from '../config';

export default function AuthLandingPage({ onLoginSuccess }) {
  const [authMode, setAuthMode] = useState('login'); // 'login' or 'register'
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [role, setRole] = useState('student');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleDemoLogin = async () => {
    setLoading(true);
    setError('');
    try {
      const activeUrl = getApiBaseUrl();
      const resp = await fetch(`${activeUrl}/api/v1/auth/demo-login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });

      if (resp.ok) {
        const data = await resp.json();
        localStorage.setItem('hiremind_token', data.access_token);
        const demoUser = {
          email: 'demo@hiremind.ai',
          full_name: 'Alex Student (Demo)',
          role: 'student'
        };
        localStorage.setItem('hiremind_user', JSON.stringify(demoUser));
        onLoginSuccess(demoUser);
      } else {
        // Direct local fallback if backend offline
        const demoUser = { email: 'alex@hiremind.ai', full_name: 'Alex Student (Demo)', role: 'student' };
        localStorage.setItem('hiremind_user', JSON.stringify(demoUser));
        onLoginSuccess(demoUser);
      }
    } catch (err) {
      const demoUser = { email: 'alex@hiremind.ai', full_name: 'Alex Student (Demo)', role: 'student' };
      localStorage.setItem('hiremind_user', JSON.stringify(demoUser));
      onLoginSuccess(demoUser);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email || !password) {
      setError('Please fill in both email and password.');
      return;
    }

    setLoading(true);
    setError('');
    const activeUrl = getApiBaseUrl();

    try {
      if (authMode === 'login') {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const resp = await fetch(`${activeUrl}/api/v1/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: formData
        });

        if (!resp.ok) {
          const errData = await resp.json();
          throw new Error(errData.detail || 'Invalid email or password.');
        }

        const data = await resp.json();
        localStorage.setItem('hiremind_token', data.access_token);
        const userData = { email, full_name: fullName || email.split('@')[0], role: 'student' };
        localStorage.setItem('hiremind_user', JSON.stringify(userData));
        onLoginSuccess(userData);
      } else {
        const resp = await fetch(`${activeUrl}/api/v1/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password, full_name: fullName, role })
        });

        if (!resp.ok) {
          const errData = await resp.json();
          throw new Error(errData.detail || 'Failed to create account.');
        }

        const data = await resp.json();
        const userData = { email: data.email, full_name: data.full_name || email.split('@')[0], role: data.role || 'student' };
        localStorage.setItem('hiremind_user', JSON.stringify(userData));
        onLoginSuccess(userData);
      }
    } catch (err) {
      setError(err.message || 'Authentication service unreachable.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#060812] text-white flex flex-col items-center justify-center p-4 md:p-8 relative overflow-hidden">
      {/* Background Animated Gradient Orbs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-600/20 rounded-full blur-3xl pointer-events-none animate-pulse"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-3xl pointer-events-none animate-pulse"></div>

      {/* Main Header / Branding */}
      <div className="text-center max-w-3xl mb-8 relative z-10">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-900/90 border border-indigo-500/30 text-xs font-semibold text-cyan-400 mb-4 shadow-lg backdrop-blur-md">
          <Shield className="w-3.5 h-3.5 text-cyan-400" />
          <span>Enterprise Security Architecture v3.0</span>
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
        </div>

        <h1 className="text-4xl md:text-6xl font-black tracking-tight text-white mb-4">
          HireMind <span className="gradient-text font-black">AI</span>
        </h1>
        <p className="text-sm md:text-lg text-gray-300 font-medium max-w-2xl mx-auto leading-relaxed">
          Enterprise Career Operating System — Multimodal ATS Scoring, Vector RAG Interview Prep & Live AI Career Intelligence.
        </p>
      </div>

      {/* Main Auth & Demo Gateway Card */}
      <div className="w-full max-w-md glass-card p-6 md:p-8 relative z-10 border-indigo-500/30 shadow-2xl">
        {/* Toggle Mode Tabs */}
        <div className="grid grid-cols-2 gap-2 bg-slate-950/80 p-1.5 rounded-2xl border border-white/10 mb-6">
          <button
            type="button"
            onClick={() => { setAuthMode('login'); setError(''); }}
            className={`py-2.5 rounded-xl text-xs font-bold transition flex items-center justify-center gap-2 ${
              authMode === 'login'
                ? 'bg-indigo-600 text-white shadow-md'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <KeyRound className="w-3.5 h-3.5" /> Sign In
          </button>

          <button
            type="button"
            onClick={() => { setAuthMode('register'); setError(''); }}
            className={`py-2.5 rounded-xl text-xs font-bold transition flex items-center justify-center gap-2 ${
              authMode === 'register'
                ? 'bg-purple-600 text-white shadow-md'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <UserCheck className="w-3.5 h-3.5" /> Create Account
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-xl bg-red-950/80 border border-red-500/40 text-xs text-red-300 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-red-400 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* 1-Click Demo Login 3D Button */}
        <div className="mb-6">
          <button
            type="button"
            onClick={handleDemoLogin}
            disabled={loading}
            className="w-full btn-3d-emerald py-3 px-4 rounded-xl text-xs font-black uppercase tracking-wider text-white flex items-center justify-center gap-2 shadow-lg"
          >
            <Zap className="w-4 h-4 text-yellow-300 animate-bounce" />
            <span>⚡ Launch Instant Demo Access (No Password)</span>
          </button>
          <p className="text-[11px] text-emerald-400/80 text-center mt-2 font-semibold">
            Instant 1-Click Sandbox Environment for Student / Recruiter Evaluation
          </p>
        </div>

        <div className="relative flex items-center my-4">
          <div className="flex-grow border-t border-gray-800"></div>
          <span className="flex-shrink mx-3 text-[10px] uppercase font-bold text-gray-500 tracking-wider">Or Continue With Credentials</span>
          <div className="flex-grow border-t border-gray-800"></div>
        </div>

        {/* Auth Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {authMode === 'register' && (
            <div>
              <label className="block text-[11px] font-semibold text-gray-300 mb-1">Full Name</label>
              <div className="relative">
                <User className="w-4 h-4 text-gray-500 absolute left-3 top-3" />
                <input
                  type="text"
                  placeholder="Shambhu Shekhar Sinha"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-900/90 border border-white/10 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-[11px] font-semibold text-gray-300 mb-1">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-gray-500 absolute left-3 top-3" />
              <input
                type="email"
                placeholder="name@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-900/90 border border-white/10 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-[11px] font-semibold text-gray-300 mb-1">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-gray-500 absolute left-3 top-3" />
              <input
                type="password"
                placeholder="••••••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-900/90 border border-white/10 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          {authMode === 'register' && (
            <div>
              <label className="block text-[11px] font-semibold text-gray-300 mb-1">Account Role</label>
              <div className="relative">
                <Briefcase className="w-4 h-4 text-gray-500 absolute left-3 top-3" />
                <select
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-900/90 border border-white/10 text-xs text-white focus:outline-none focus:border-indigo-500"
                >
                  <option value="student">Student / Job Seeker</option>
                  <option value="recruiter">Recruiter / Employer</option>
                </select>
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full btn-3d-primary py-3 px-4 rounded-xl text-xs font-bold uppercase tracking-wider text-white flex items-center justify-center gap-2 mt-4 shadow-lg"
          >
            {loading ? (
              <Sparkles className="w-4 h-4 animate-spin" />
            ) : (
              <>
                <span>{authMode === 'login' ? 'Sign In to Career OS' : 'Create Enterprise Account'}</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>
      </div>

      {/* Security Privacy Protection Notice */}
      <div className="mt-8 flex items-center gap-2 text-xs text-gray-400 max-w-md text-center">
        <Lock className="w-4 h-4 text-cyan-400 shrink-0" />
        <span>End-to-End Privacy Protection — All candidate resumes, vector embeddings, and analytics metrics are isolated and secured.</span>
      </div>
    </div>
  );
}
