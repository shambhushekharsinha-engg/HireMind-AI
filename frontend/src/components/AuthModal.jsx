import React, { useState } from 'react';
import { User, Mail, Phone, Lock, Sparkles, X, Shield, ArrowRight, KeyRound } from 'lucide-react';
import { API_BASE_URL } from '../config';

export default function AuthModal({ isOpen, onClose, onLoginSuccess }) {
  const [isRegister, setIsRegister] = useState(false);
  const [role, setRole] = useState('recruiter'); // Default recruiter as requested
  const [email, setEmail] = useState('');
  const [mobileNumber, setMobileNumber] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const endpoint = isRegister ? `${API_BASE_URL}/api/v1/auth/register` : `${API_BASE_URL}/api/v1/auth/login`;
      const payload = isRegister ? {
        email,
        mobile_number: mobileNumber,
        password,
        full_name: fullName,
        role
      } : {
        email: email || undefined,
        mobile_number: mobileNumber || undefined,
        password
      };

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Authentication failed.');
      }

      const data = await response.json();
      const userObj = data.user || data;
      localStorage.setItem('hiremind_token', data.access_token || 'demo_token');
      localStorage.setItem('hiremind_user', JSON.stringify(userObj));
      
      onLoginSuccess(userObj);
      onClose();
    } catch (err) {
      console.error(err);
      setError(err.message || 'Error communicating with server.');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickDemoLogin = async (demoRole) => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/demo-login?role=${demoRole}`, {
        method: 'POST'
      });
      const data = await response.json();
      localStorage.setItem('hiremind_token', data.access_token);
      localStorage.setItem('hiremind_user', JSON.stringify(data.user));
      onLoginSuccess(data.user);
      onClose();
    } catch (err) {
      console.error(err);
      // Fallback local mock login
      const mockUser = {
        id: demoRole === 'recruiter' ? 2 : 1,
        email: demoRole === 'recruiter' ? 'recruiter@apextech.com' : 'student@hiremind.ai',
        full_name: demoRole === 'recruiter' ? 'Sarah Recruiter (Demo)' : 'Alex Student (Demo)',
        role: demoRole
      };
      localStorage.setItem('hiremind_user', JSON.stringify(mockUser));
      onLoginSuccess(mockUser);
      onClose();
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
      <div className="glass-card max-w-md w-full p-6 space-y-5 border-indigo-500/40 animate-fade-in shadow-2xl relative">
        <div className="flex items-center justify-between border-b border-white/10 pb-3">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-500 to-cyan-400 flex items-center justify-center text-white font-bold">
              <Shield className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">
                {isRegister ? 'Create HireMind Account' : 'Portal Sign In'}
              </h3>
              <p className="text-[10px] text-indigo-300 font-medium">Authentication & Role Access</p>
            </div>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* 1-Click Quick Demo Login Row */}
        <div className="bg-indigo-950/60 p-3 rounded-2xl border border-indigo-500/30 space-y-2">
          <span className="text-[10px] font-bold text-cyan-300 uppercase tracking-wider block">
            ⚡ 1-Click Direct Demo Authentication
          </span>
          <div className="grid grid-cols-2 gap-2">
            <button
              onClick={() => handleQuickDemoLogin('recruiter')}
              className="px-3 py-2 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white text-xs font-bold shadow-md flex items-center justify-center gap-1"
            >
              <User className="w-3.5 h-3.5" /> Direct Recruiter Login
            </button>
            <button
              onClick={() => handleQuickDemoLogin('student')}
              className="px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-cyan-500/30 text-xs font-bold flex items-center justify-center gap-1"
            >
              <Sparkles className="w-3.5 h-3.5 text-cyan-400" /> Student Login
            </button>
          </div>
        </div>

        {/* Form Mode Toggle */}
        <div className="flex rounded-xl bg-gray-900 p-1 border border-white/10 text-xs font-bold">
          <button
            onClick={() => setIsRegister(false)}
            className={`flex-1 py-1.5 rounded-lg transition ${!isRegister ? 'bg-indigo-600 text-white shadow' : 'text-gray-400'}`}
          >
            Sign In
          </button>
          <button
            onClick={() => setIsRegister(true)}
            className={`flex-1 py-1.5 rounded-lg transition ${isRegister ? 'bg-indigo-600 text-white shadow' : 'text-gray-400'}`}
          >
            Register Account
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-3">
          {/* Role Selection */}
          <div className="space-y-1">
            <label className="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">Select Account Role</label>
            <div className="grid grid-cols-3 gap-2">
              {['recruiter', 'student', 'admin'].map((r) => (
                <button
                  type="button"
                  key={r}
                  onClick={() => setRole(r)}
                  className={`py-1.5 rounded-xl border text-[11px] font-bold uppercase transition ${
                    role === r ? 'bg-indigo-600 text-white border-indigo-400 shadow-sm' : 'bg-gray-900/60 text-gray-400 border-white/10'
                  }`}
                >
                  {r}
                </button>
              ))}
            </div>
          </div>

          {isRegister && (
            <div>
              <label className="text-[10px] font-bold text-gray-400 block mb-1">Full Name</label>
              <div className="relative">
                <input
                  type="text"
                  placeholder="e.g. Sarah Jenkins"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full pl-9 pr-3 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white"
                />
                <User className="w-3.5 h-3.5 text-gray-400 absolute left-3 top-3" />
              </div>
            </div>
          )}

          <div>
            <label className="text-[10px] font-bold text-gray-400 block mb-1">Email Address</label>
            <div className="relative">
              <input
                type="email"
                placeholder="name@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full pl-9 pr-3 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white"
              />
              <Mail className="w-3.5 h-3.5 text-gray-400 absolute left-3 top-3" />
            </div>
          </div>

          <div>
            <label className="text-[10px] font-bold text-gray-400 block mb-1">Mobile Number (OTP Enabled)</label>
            <div className="relative">
              <input
                type="text"
                placeholder="+91 98765 43210"
                value={mobileNumber}
                onChange={(e) => setMobileNumber(e.target.value)}
                className="w-full pl-9 pr-3 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white"
              />
              <Phone className="w-3.5 h-3.5 text-gray-400 absolute left-3 top-3" />
            </div>
          </div>

          <div>
            <label className="text-[10px] font-bold text-gray-400 block mb-1">Password / OTP</label>
            <div className="relative">
              <input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-9 pr-3 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white"
              />
              <Lock className="w-3.5 h-3.5 text-gray-400 absolute left-3 top-3" />
            </div>
          </div>

          {error && (
            <p className="text-[11px] text-red-400 font-medium pt-1">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full glow-btn py-2.5 rounded-xl text-xs font-bold flex items-center justify-center gap-2 mt-2"
          >
            {isRegister ? 'Register & Access Portal' : `Login as ${role.toUpperCase()}`}
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
