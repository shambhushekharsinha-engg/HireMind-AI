import React, { useState, useEffect } from 'react';
import { Users, Search, Award, Download, Filter } from 'lucide-react';

export default function RecruiterPage() {
  const [minAts, setMinAts] = useState(0);
  const [skillFilter, setSkillFilter] = useState('');
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchCandidates = async () => {
    setLoading(true);
    try {
      let url = `http://127.0.0.1:8000/api/v1/recruiter/candidates?min_ats=${minAts}`;
      if (skillFilter.trim()) {
        url += `&skills=${encodeURIComponent(skillFilter)}`;
      }
      const response = await fetch(url);
      const data = await response.json();
      setCandidates(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCandidates();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          Recruiter Candidate <span className="gradient-text">Portal</span>
        </h2>
        <p className="text-xs text-gray-400">Search, filter, and rank candidate resumes by ATS scores and verified skills</p>
      </div>

      {/* Filter Bar */}
      <div className="glass-card p-5 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex flex-col sm:flex-row items-center gap-4 w-full md:w-auto">
          <div className="space-y-1 w-full sm:w-64">
            <label className="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">
              Skill Search Keywords
            </label>
            <div className="relative">
              <input
                type="text"
                placeholder="e.g. python, react, sql"
                value={skillFilter}
                onChange={(e) => setSkillFilter(e.target.value)}
                className="w-full pl-9 pr-3 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
              />
              <Search className="w-3.5 h-3.5 text-gray-400 absolute left-3 top-3" />
            </div>
          </div>

          <div className="space-y-1 w-full sm:w-48">
            <label className="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">
              Min ATS Score Threshold: {minAts}
            </label>
            <input
              type="range"
              min="0"
              max="100"
              step="5"
              value={minAts}
              onChange={(e) => setMinAts(Number(e.target.value))}
              className="w-full accent-indigo-500 cursor-pointer"
            />
          </div>
        </div>

        <button
          onClick={fetchCandidates}
          className="glow-btn px-6 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 shrink-0"
        >
          <Filter className="w-4 h-4" />
          Filter Candidates
        </button>
      </div>

      {/* Candidate Ranking Table */}
      <div className="glass-card overflow-hidden">
        <div className="p-4 border-b border-white/10 flex items-center justify-between">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Users className="w-4 h-4 text-cyan-400" />
            Ranked Candidates ({candidates.length})
          </h3>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-900/80 border-b border-white/10 text-[10px] uppercase font-bold text-gray-400 tracking-wider">
                <th className="p-4">Rank</th>
                <th className="p-4">Candidate Name</th>
                <th className="p-4">ATS Score</th>
                <th className="p-4">Rating</th>
                <th className="p-4">Verified Skills</th>
                <th className="p-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 text-xs text-gray-300">
              {candidates.length > 0 ? (
                candidates.map((cand, idx) => (
                  <tr key={cand.analysis_id} className="hover:bg-white/5 transition">
                    <td className="p-4 font-bold text-indigo-400">#{idx + 1}</td>
                    <td className="p-4 font-semibold text-white">
                      {cand.candidate_name}
                      <span className="block text-[10px] text-gray-400 font-normal">{cand.filename}</span>
                    </td>
                    <td className="p-4 font-black text-emerald-400 text-sm">
                      {cand.ats_score} / 100
                    </td>
                    <td className="p-4">
                      <span className="px-2.5 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-[10px] font-bold">
                        {cand.rating}
                      </span>
                    </td>
                    <td className="p-4">
                      <div className="flex flex-wrap gap-1 max-w-xs">
                        {cand.skills.slice(0, 4).map((s, i) => (
                          <span key={i} className="px-2 py-0.5 rounded bg-gray-800 text-[10px] text-gray-300 font-mono">
                            {s}
                          </span>
                        ))}
                        {cand.skills.length > 4 && (
                          <span className="text-[10px] text-gray-400 font-bold">+{cand.skills.length - 4} more</span>
                        )}
                      </div>
                    </td>
                    <td className="p-4 text-right">
                      <button
                        onClick={() => window.open(`http://127.0.0.1:8000/api/v1/reports/download/${cand.analysis_id}`, '_blank')}
                        className="px-3 py-1.5 rounded-lg bg-indigo-600/80 hover:bg-indigo-500 text-white text-[11px] font-semibold inline-flex items-center gap-1 transition"
                      >
                        <Download className="w-3 h-3" /> Report
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="6" className="p-8 text-center text-xs text-gray-500">
                    No candidates match the current filter criteria.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
