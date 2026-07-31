import React, { useState, useEffect } from 'react';
import { Target, Plus, Building2, MapPin, DollarSign, Trash2 } from 'lucide-react';

const COLUMNS = ["Saved", "Applied", "Interviewing", "Offer", "Rejected"];

export default function ApplicationTrackerPage() {
  const [applications, setApplications] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newApp, setNewApp] = useState({ company: '', position: '', location: '', salary_range: '', status: 'Saved' });

  const fetchApplications = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/applications');
      const data = await response.json();
      setApplications(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchApplications();
  }, []);

  const handleCreateApp = async () => {
    if (!newApp.company || !newApp.position) {
      alert('Please provide company name and position title.');
      return;
    }
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/applications', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newApp)
      });
      const created = await response.json();
      setApplications([created, ...applications]);
      setShowAddModal(false);
      setNewApp({ company: '', position: '', location: '', salary_range: '', status: 'Saved' });
    } catch (err) {
      console.error(err);
    }
  };

  const handleUpdateStatus = async (appId, newStatus) => {
    try {
      await fetch(`http://127.0.0.1:8000/api/v1/applications/${appId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
      });
      setApplications(applications.map(a => a.id === appId ? { ...a, status: newStatus } : a));
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteApp = async (appId) => {
    try {
      await fetch(`http://127.0.0.1:8000/api/v1/applications/${appId}`, { method: 'DELETE' });
      setApplications(applications.filter(a => a.id !== appId));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            Job Application <span className="gradient-text">Kanban Tracker</span>
          </h2>
          <p className="text-xs text-gray-400">Track and manage your entire application pipeline</p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="glow-btn px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2"
        >
          <Plus className="w-4 h-4" /> Add Application
        </button>
      </div>

      {/* Kanban Board Grid */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 overflow-x-auto">
        {COLUMNS.map((col) => {
          const colApps = applications.filter(a => a.status === col);
          return (
            <div key={col} className="glass-card p-4 space-y-3 min-h-[500px] flex flex-col justify-between border-white/5">
              <div>
                <div className="flex items-center justify-between pb-2 border-b border-white/10 mb-3">
                  <span className="text-xs font-bold uppercase tracking-wider text-gray-300 flex items-center gap-2">
                    <span className={`w-2 h-2 rounded-full ${
                      col === 'Offer' ? 'bg-emerald-400' :
                      col === 'Interviewing' ? 'bg-purple-400' :
                      col === 'Applied' ? 'bg-cyan-400' :
                      col === 'Saved' ? 'bg-indigo-400' : 'bg-red-400'
                    }`}></span>
                    {col}
                  </span>
                  <span className="text-[10px] font-bold text-gray-400 px-2 py-0.5 rounded-full bg-gray-800">
                    {colApps.length}
                  </span>
                </div>

                <div className="space-y-3">
                  {colApps.map((app) => (
                    <div key={app.id} className="bg-gray-900/80 p-3.5 rounded-xl border border-white/10 hover:border-indigo-500/40 transition space-y-2 group">
                      <div className="flex items-start justify-between">
                        <div>
                          <h4 className="text-xs font-bold text-white line-clamp-1">{app.position}</h4>
                          <span className="text-[11px] font-semibold text-indigo-300 flex items-center gap-1 mt-0.5">
                            <Building2 className="w-3 h-3 text-gray-400" /> {app.company}
                          </span>
                        </div>

                        <button 
                          onClick={() => handleDeleteApp(app.id)}
                          className="opacity-0 group-hover:opacity-100 text-gray-500 hover:text-red-400 transition"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>

                      {app.salary_range && (
                        <div className="text-[10px] text-emerald-400 font-mono flex items-center gap-1">
                          <DollarSign className="w-3 h-3" /> {app.salary_range}
                        </div>
                      )}

                      {/* Move Column Select */}
                      <select
                        value={app.status}
                        onChange={(e) => handleUpdateStatus(app.id, e.target.value)}
                        className="w-full mt-2 px-2 py-1 rounded bg-gray-800 border border-white/10 text-[10px] text-gray-300 font-semibold cursor-pointer"
                      >
                        {COLUMNS.map(c => <option key={c} value={c}>{c}</option>)}
                      </select>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Add Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="glass-card p-6 w-full max-w-md space-y-4 border-indigo-500/40">
            <h3 className="text-base font-bold text-white">Add Job Application</h3>
            <div className="space-y-3">
              <input
                type="text"
                placeholder="Company Name (e.g. Google, Amazon)"
                value={newApp.company}
                onChange={(e) => setNewApp({ ...newApp, company: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white"
              />
              <input
                type="text"
                placeholder="Position Title (e.g. AI Engineer)"
                value={newApp.position}
                onChange={(e) => setNewApp({ ...newApp, position: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white"
              />
              <input
                type="text"
                placeholder="Location (e.g. Remote, San Francisco)"
                value={newApp.location}
                onChange={(e) => setNewApp({ ...newApp, location: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white"
              />
              <input
                type="text"
                placeholder="Estimated Salary (e.g. $120,000)"
                value={newApp.salary_range}
                onChange={(e) => setNewApp({ ...newApp, salary_range: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white"
              />
            </div>
            <div className="flex justify-end gap-3 pt-2">
              <button
                onClick={() => setShowAddModal(false)}
                className="px-4 py-2 rounded-xl text-xs font-semibold bg-gray-800 text-gray-300"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateApp}
                className="glow-btn px-5 py-2 rounded-xl text-xs font-bold"
              >
                Save Application
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
