import React, { useState, useEffect } from 'react';
import { 
  Kanban, 
  Plus, 
  Building2, 
  Calendar, 
  Trash2, 
  Briefcase, 
  CheckCircle2, 
  Clock, 
  Award, 
  XCircle 
} from 'lucide-react';
import { getApiBaseUrl } from '../config';

const INITIAL_DEMO_APPLICATIONS = [
  { id: 1, company_name: 'Google', job_title: 'Senior Software Engineer (AI)', status: 'Interviewing', applied_date: '2026-11-12' },
  { id: 2, company_name: 'Stripe', job_title: 'Full-Stack Platform Engineer', status: 'Applied', applied_date: '2026-11-15' },
  { id: 3, company_name: 'Anthropic', job_title: 'AI Systems & Reliability Engineer', status: 'Offer', applied_date: '2026-11-04' },
  { id: 4, company_name: 'Amazon Web Services', job_title: 'Cloud Solutions Architect', status: 'Interviewing', applied_date: '2026-11-10' },
  { id: 5, company_name: 'Meta', job_title: 'Distributed Systems Engineer', status: 'Rejected', applied_date: '2026-10-25' }
];

export default function ApplicationTrackerPage() {
  const [applications, setApplications] = useState(() => {
    try {
      const saved = localStorage.getItem('hiremind_applications');
      if (saved) return JSON.parse(saved);
    } catch (e) {}
    return INITIAL_DEMO_APPLICATIONS;
  });

  const [company, setCompany] = useState('');
  const [role, setRole] = useState('');
  const [status, setStatus] = useState('Applied');

  // Persist locally
  useEffect(() => {
    try {
      localStorage.setItem('hiremind_applications', JSON.stringify(applications));
    } catch (e) {}
  }, [applications]);

  const fetchAppsFromBackend = async () => {
    try {
      const activeUrl = getApiBaseUrl();
      const response = await fetch(`${activeUrl}/api/v1/applications`);
      if (response.ok) {
        const data = await response.json();
        if (Array.isArray(data) && data.length > 0) {
          setApplications(data);
        }
      }
    } catch (err) {
      // Keep local state
    }
  };

  useEffect(() => {
    fetchAppsFromBackend();
  }, []);

  const handleCreate = async () => {
    if (!company.trim() || !role.trim()) return;

    const newApp = {
      id: Date.now(),
      company_name: company.trim(),
      job_title: role.trim(),
      status,
      applied_date: new Date().toISOString().split('T')[0]
    };

    // Optimistic UI update
    setApplications(prev => [newApp, ...prev]);
    setCompany('');
    setRole('');

    try {
      const activeUrl = getApiBaseUrl();
      await fetch(`${activeUrl}/api/v1/applications`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ company_name: newApp.company_name, job_title: newApp.job_title, status })
      });
    } catch (err) {
      // Local state already updated
    }
  };

  const handleDelete = async (id) => {
    setApplications(prev => prev.filter(app => app.id !== id));
    try {
      const activeUrl = getApiBaseUrl();
      await fetch(`${activeUrl}/api/v1/applications/${id}`, { method: 'DELETE' });
    } catch (e) {}
  };

  const stages = [
    { name: 'Applied', color: 'border-cyan-500/40 text-cyan-400 bg-cyan-950/20', icon: Clock },
    { name: 'Interviewing', color: 'border-indigo-500/40 text-indigo-400 bg-indigo-950/20', icon: Briefcase },
    { name: 'Offer', color: 'border-emerald-500/40 text-emerald-400 bg-emerald-950/20', icon: Award },
    { name: 'Rejected', color: 'border-red-500/40 text-red-400 bg-red-950/20', icon: XCircle }
  ];

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center gap-2">
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            Job Application <span className="gradient-text">Tracker Board</span>
          </h2>
          <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
            Kanban Lifecycle
          </span>
        </div>
        <p className="text-xs text-gray-400">Manage candidate interviews, offers, and active corporate recruitment pipelines</p>
      </div>

      {/* Add Application Bar */}
      <div className="glass-card p-4 sm:p-5 flex flex-col sm:flex-row items-center gap-3">
        <input
          type="text"
          placeholder="Target Company (e.g. Microsoft, Google)"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          className="w-full sm:flex-1 px-3.5 py-2.5 rounded-xl bg-slate-900 border border-white/10 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500"
        />
        <input
          type="text"
          placeholder="Job Role (e.g. Principal AI Engineer)"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className="w-full sm:flex-1 px-3.5 py-2.5 rounded-xl bg-slate-900 border border-white/10 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500"
        />
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          className="w-full sm:w-auto px-3.5 py-2.5 rounded-xl bg-slate-900 border border-white/10 text-xs text-white font-semibold focus:outline-none focus:border-cyan-500"
        >
          {stages.map((s) => (
            <option key={s.name} value={s.name}>{s.name}</option>
          ))}
        </select>
        <button
          onClick={handleCreate}
          className="glow-btn px-5 py-2.5 rounded-xl text-xs font-bold w-full sm:w-auto flex items-center justify-center gap-1.5 shrink-0"
        >
          <Plus className="w-4 h-4" /> Add Application
        </button>
      </div>

      {/* Kanban Board Columns */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stages.map((stage) => {
          const StageIcon = stage.icon;
          const stageApps = applications.filter((a) => a.status === stage.name);
          return (
            <div key={stage.name} className="flex flex-col space-y-3">
              <div className={`p-3 rounded-xl border ${stage.color} flex items-center justify-between`}>
                <div className="flex items-center gap-2">
                  <StageIcon className="w-4 h-4" />
                  <span className="text-xs font-bold uppercase tracking-wider">{stage.name}</span>
                </div>
                <span className="px-2 py-0.5 rounded-full bg-slate-900 text-xs font-mono font-bold text-white border border-white/10">
                  {stageApps.length}
                </span>
              </div>

              <div className="space-y-3 flex-1 min-h-[300px] p-2 bg-slate-950/40 rounded-xl border border-white/5">
                {stageApps.length === 0 ? (
                  <div className="h-32 flex items-center justify-center text-[11px] text-gray-500 italic">
                    No applications in {stage.name}
                  </div>
                ) : (
                  stageApps.map((app) => (
                    <div 
                      key={app.id} 
                      className="glass-card p-4 space-y-2.5 hover:border-indigo-500/40 transition group relative"
                    >
                      <div className="flex items-start justify-between">
                        <div>
                          <h4 className="text-xs font-bold text-white group-hover:text-cyan-300 transition">{app.company_name}</h4>
                          <p className="text-[11px] text-gray-300">{app.job_title}</p>
                        </div>
                        <button
                          onClick={() => handleDelete(app.id)}
                          className="opacity-0 group-hover:opacity-100 p-1 text-gray-500 hover:text-red-400 transition"
                          title="Remove Application"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>

                      <div className="flex items-center justify-between text-[10px] text-gray-500 pt-1 border-t border-white/5">
                        <span className="flex items-center gap-1 font-mono">
                          <Calendar className="w-3 h-3 text-gray-400" />
                          {app.applied_date || 'Active'}
                        </span>
                        <span className="text-indigo-400 font-semibold">Priority A</span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
