import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, Users, Target, Shield } from 'lucide-react';
import { API_BASE_URL } from '../config';

export default function AnalyticsPage() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/v1/analytics/user`)
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          Platform <span className="gradient-text">Analytics Dashboard</span>
        </h2>
        <p className="text-xs text-gray-400">User activity metrics and platform performance telemetry</p>
      </div>

      {stats && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="glass-card p-6 border-indigo-500/30">
            <span className="text-xs text-gray-400 font-semibold">Total Resumes Processed</span>
            <div className="text-3xl font-black text-white mt-1">{stats.total_resumes_analyzed}</div>
          </div>
          <div className="glass-card p-6 border-cyan-500/30">
            <span className="text-xs text-gray-400 font-semibold">Average ATS Score</span>
            <div className="text-3xl font-black text-cyan-300 mt-1">{stats.average_ats_score}</div>
          </div>
          <div className="glass-card p-6 border-purple-500/30">
            <span className="text-xs text-gray-400 font-semibold">Applications Tracked</span>
            <div className="text-3xl font-black text-purple-300 mt-1">{stats.applications_count}</div>
          </div>
          <div className="glass-card p-6 border-emerald-500/30">
            <span className="text-xs text-gray-400 font-semibold">System Health</span>
            <div className="text-xl font-black text-emerald-400 mt-1">{stats.system_status}</div>
          </div>
        </div>
      )}
    </div>
  );
}
