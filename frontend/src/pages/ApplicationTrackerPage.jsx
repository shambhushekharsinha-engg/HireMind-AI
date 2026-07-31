import React, { useState, useEffect } from 'react';
import { Kanban, Plus, Building2, Calendar, Trash2 } from 'lucide-react';
import { API_BASE_URL } from '../config';

export default function ApplicationTrackerPage() {
  const [applications, setApplications] = useState([]);
  const [company, setCompany] = useState('');
  const [role, setRole] = useState('');
  const [status, setStatus] = useState('Applied');

  const fetchApps = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/applications`);
      const data = await response.json();
      setApplications(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchApps();
  }, []);

  const handleCreate = async () => {
    if (!company || !role) return;
    try {
      await fetch(`${API_BASE_URL}/api/v1/applications`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ company_name: company, job_title: role, status })
      });
      setCompany('');
      setRole('');
      fetchApps();
    } catch (err) {
      console.error(err);
    }
  };

  const stages = ['Applied', 'Interviewing', 'Offer', 'Rejected'];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          Job Application <span className="gradient-text">Tracker Board</span>
        </h2>
        <p className="text-xs text-gray-400">Kanban lifecycle management for active job applications</p>
      </div>

      <div className="glass-card p-5 flex flex-col sm:flex-row items-center gap-3">
        <input
          type="text"
          placeholder="Company Name (e.g. Google)"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          className="px-3.5 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white flex-1"
        />
        <input
          type="text"
          placeholder="Job Role (e.g. SDE II)"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className="px-3.5 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white flex-1"
        />
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          className="px-3 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white font-semibold"
        >
          {stages.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
        <button
          onClick={handleCreate}
          className="glow-btn px-5 py-2 rounded-xl text-xs font-bold flex items-center gap-1.5 shrink-0"
        >
          <Plus className="w-4 h-4" /> Add Application
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {stages.map((stage) => {
          const items = applications.filter(a => a.status.toLowerCase() === stage.toLowerCase());
          return (
            <div key={stage} className="glass-card p-4 space-y-3 min-h-[400px]">
              <div className="flex items-center justify-between border-b border-white/10 pb-2">
                <span className="text-xs font-bold text-gray-300 uppercase tracking-wider">{stage}</span>
                <span className="w-5 h-5 rounded-full bg-gray-800 text-[10px] font-bold text-gray-400 flex items-center justify-center">
                  {items.length}
                </span>
              </div>

              <div className="space-y-3">
                {items.map((app) => (
                  <div key={app.id} className="p-3 bg-gray-900/80 rounded-xl border border-white/5 space-y-1 hover:border-indigo-500/30 transition">
                    <div className="text-xs font-bold text-white flex items-center gap-1.5">
                      <Building2 className="w-3.5 h-3.5 text-indigo-400" /> {app.company_name}
                    </div>
                    <p className="text-[11px] text-gray-300">{app.job_title}</p>
                    <div className="text-[9px] text-gray-500 flex items-center gap-1 pt-1">
                      <Calendar className="w-3 h-3" /> {app.applied_date}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
