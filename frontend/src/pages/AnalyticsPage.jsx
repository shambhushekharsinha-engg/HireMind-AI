import React, { useState, useEffect } from 'react';
import { BarChart3, ShieldCheck, Zap, Activity, Users, FileText } from 'lucide-react';

export default function AnalyticsPage() {
  const [userAnalytics, setUserAnalytics] = useState(null);
  const [adminAnalytics, setAdminAnalytics] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/v1/analytics/user')
      .then(res => res.json())
      .then(data => setUserAnalytics(data))
      .catch(err => console.error(err));

    fetch('http://127.0.0.1:8000/api/v1/analytics/admin')
      .then(res => res.json())
      .then(data => setAdminAnalytics(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          System & Career <span className="gradient-text">Analytics</span>
        </h2>
        <p className="text-xs text-gray-400">Personal performance tracking and platform infrastructure metrics</p>
      </div>

      {/* Candidate Performance Metrics */}
      {userAnalytics && (
        <div className="space-y-4">
          <h3 className="text-sm font-bold text-gray-300 uppercase tracking-wider">Candidate Progress Metrics</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
            <div className="glass-card p-5 space-y-1 border-indigo-500/20">
              <span className="text-xs text-gray-400">Total Resumes Evaluated</span>
              <div className="text-3xl font-black text-white">{userAnalytics.total_resumes_analyzed}</div>
            </div>

            <div className="glass-card p-5 space-y-1 border-emerald-500/20">
              <span className="text-xs text-gray-400">Average ATS Score</span>
              <div className="text-3xl font-black text-emerald-400">{userAnalytics.avg_ats_score} / 100</div>
            </div>

            <div className="glass-card p-5 space-y-1 border-cyan-500/20">
              <span className="text-xs text-gray-400">Skill Growth Velocity</span>
              <div className="text-lg font-bold text-cyan-300">{userAnalytics.skill_growth_rate}</div>
            </div>

            <div className="glass-card p-5 space-y-1 border-purple-500/20">
              <span className="text-xs text-gray-400">Funnel Conversion</span>
              <div className="text-lg font-bold text-purple-300">
                {userAnalytics.application_funnel.Interviewing || 0} Interviews Scheduled
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Admin Infrastructure Metrics */}
      {adminAnalytics && (
        <div className="space-y-4 pt-4 border-t border-white/10">
          <h3 className="text-sm font-bold text-gray-300 uppercase tracking-wider flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-cyan-400" />
            Admin & System Infrastructure Health
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="glass-card p-6 space-y-2 border-indigo-500/30">
              <div className="flex items-center justify-between text-xs text-gray-400">
                <span>Total Registered Users</span>
                <Users className="w-4 h-4 text-indigo-400" />
              </div>
              <div className="text-3xl font-black text-white">{adminAnalytics.total_active_users}</div>
              <p className="text-[11px] text-gray-400">Role-based access (Student, Recruiter, Admin)</p>
            </div>

            <div className="glass-card p-6 space-y-2 border-cyan-500/30">
              <div className="flex items-center justify-between text-xs text-gray-400">
                <span>AI Calls Processed</span>
                <Zap className="w-4 h-4 text-amber-400" />
              </div>
              <div className="text-3xl font-black text-amber-300">{adminAnalytics.ai_api_calls_processed}</div>
              <p className="text-[11px] text-gray-400">Fast local spaCy & TF-IDF vectors</p>
            </div>

            <div className="glass-card p-6 space-y-2 border-emerald-500/30">
              <div className="flex items-center justify-between text-xs text-gray-400">
                <span>Average API Latency</span>
                <Activity className="w-4 h-4 text-emerald-400" />
              </div>
              <div className="text-3xl font-black text-emerald-300">{adminAnalytics.avg_latency_ms} ms</div>
              <p className="text-[11px] text-emerald-400 font-semibold">{adminAnalytics.system_status}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
