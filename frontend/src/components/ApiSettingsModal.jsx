import React, { useState, useEffect } from 'react';
import { Settings, Server, CheckCircle2, AlertCircle, RefreshCw, X, Link } from 'lucide-react';
import { getApiBaseUrl } from '../config';

export default function ApiSettingsModal({ isOpen, onClose }) {
  const [apiUrl, setApiUrl] = useState('');
  const [status, setStatus] = useState(null); // { type: 'success' | 'error', message: string }
  const [testing, setTesting] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setApiUrl(getApiBaseUrl());
      setStatus(null);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleTestConnection = async () => {
    if (!apiUrl.trim()) {
      setStatus({ type: 'error', message: 'Please enter a valid Backend API URL.' });
      return;
    }

    setTesting(true);
    setStatus(null);
    const targetUrl = apiUrl.trim().replace(/\/$/, "");

    try {
      const res = await fetch(`${targetUrl}/health`, { method: 'GET' });
      if (res.ok) {
        const data = await res.json();
        setStatus({
          type: 'success',
          message: `Connected successfully to ${data.service || 'HireMind AI Backend'} (v${data.version || '3.0.0'})!`
        });
      } else {
        setStatus({ type: 'error', message: `Server returned status code ${res.status}.` });
      }
    } catch (err) {
      setStatus({
        type: 'error',
        message: `Connection Failed: Unable to reach '${targetUrl}'. Ensure server is online and CORS is allowed.`
      });
    } finally {
      setTesting(false);
    }
  };

  const handleSave = () => {
    if (!apiUrl.trim()) return;
    const cleanUrl = apiUrl.trim().replace(/\/$/, "");
    localStorage.setItem('hiremind_api_url', cleanUrl);
    window.location.reload();
  };

  const handleResetDefault = () => {
    localStorage.removeItem('hiremind_api_url');
    window.location.reload();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in">
      <div className="relative w-full max-w-lg glass-card rounded-3xl p-6 md:p-8 border border-white/20 shadow-2xl bg-slate-900/95 text-white">
        
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-white/10 mb-6">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-2xl bg-gradient-to-tr from-indigo-600 to-purple-600 shadow-lg shadow-indigo-500/30">
              <Server className="w-6 h-6 text-cyan-300" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">Backend API Server Settings</h3>
              <p className="text-xs text-indigo-300">Configure or test your HireMind AI backend URL</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-xl text-gray-400 hover:text-white hover:bg-white/10 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Input */}
        <div className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">
              Backend Server URL
            </label>
            <div className="relative">
              <Link className="absolute left-3.5 top-3.5 w-4 h-4 text-indigo-400" />
              <input
                type="url"
                value={apiUrl}
                onChange={(e) => setApiUrl(e.target.value)}
                placeholder="https://hiremind-ai-au7b.onrender.com or http://127.0.0.1:8000"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950 border border-indigo-500/30 focus:border-cyan-400 text-sm text-white placeholder-gray-500 outline-none transition"
              />
            </div>
          </div>

          {/* Preset Buttons */}
          <div className="flex flex-wrap gap-2 text-xs">
            <button
              onClick={() => setApiUrl('https://hiremind-ai-au7b.onrender.com')}
              className="px-3 py-1.5 rounded-lg bg-indigo-950/80 hover:bg-indigo-900 border border-indigo-500/30 text-indigo-200 transition"
            >
              Set Production (Render)
            </button>
            <button
              onClick={() => setApiUrl('http://127.0.0.1:8000')}
              className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 border border-gray-600/30 text-gray-300 transition"
            >
              Set Localhost (8000)
            </button>
          </div>

          {/* Connection Status Box */}
          {status && (
            <div
              className={`p-4 rounded-2xl border text-xs flex items-start gap-3 ${
                status.type === 'success'
                  ? 'bg-emerald-950/50 border-emerald-500/30 text-emerald-300'
                  : 'bg-red-950/50 border-red-500/30 text-red-300'
              }`}
            >
              {status.type === 'success' ? (
                <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0" />
              ) : (
                <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
              )}
              <div>
                <p className="font-semibold">{status.type === 'success' ? 'Connection Successful' : 'Connection Failed'}</p>
                <p className="mt-0.5 opacity-90">{status.message}</p>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="pt-4 flex flex-col sm:flex-row gap-3">
            <button
              onClick={handleTestConnection}
              disabled={testing}
              className="flex-1 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs border border-white/10 flex items-center justify-center gap-2 transition"
            >
              {testing ? <RefreshCw className="w-4 h-4 animate-spin text-cyan-400" /> : <RefreshCw className="w-4 h-4 text-cyan-400" />}
              Test Connection
            </button>
            
            <button
              onClick={handleSave}
              className="flex-1 py-2.5 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold text-xs shadow-lg transition"
            >
              Save & Apply URL
            </button>
          </div>

          <div className="text-center pt-2">
            <button
              onClick={handleResetDefault}
              className="text-[11px] text-gray-400 hover:text-indigo-300 underline transition"
            >
              Reset to Default Dynamic Server
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
