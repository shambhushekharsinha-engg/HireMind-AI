import React, { useState } from 'react';
import { GitCompare, Plus, Minus, ArrowRight, CheckCircle2 } from 'lucide-react';
import { API_BASE_URL } from '../config';

export default function VersionComparePage() {
  const [v1Text, setV1Text] = useState('Alex Mercer. Software Engineer. Skills: Python, SQL, HTML, CSS. Worked on basic web app.');
  const [v2Text, setV2Text] = useState('Alex Mercer. Senior Software Engineer. Skills: Python, SQL, FastAPI, React, Docker, Machine Learning. Engineered high-throughput REST APIs handling 50k+ daily requests.');
  const [loading, setLoading] = useState(false);
  const [diffResult, setDiffResult] = useState(null);

  const handleCompare = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/v2/resume/compare-versions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ v1_text: v1Text, v2_text: v2Text })
      });
      const data = await response.json();
      setDiffResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          Resume Version <span className="gradient-text">Diff Control</span>
        </h2>
        <p className="text-xs text-gray-400">Git-style side-by-side version comparison & ATS score progression</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="glass-card p-5 space-y-2">
          <label className="text-xs font-bold text-gray-400 uppercase">Version 1 (Previous Draft)</label>
          <textarea
            rows="8"
            value={v1Text}
            onChange={(e) => setV1Text(e.target.value)}
            className="w-full p-3 rounded-xl bg-gray-900 border border-white/10 text-xs text-white resize-none font-mono"
          />
        </div>

        <div className="glass-card p-5 space-y-2 border-indigo-500/30">
          <label className="text-xs font-bold text-indigo-400 uppercase">Version 2 (New Revised Draft)</label>
          <textarea
            rows="8"
            value={v2Text}
            onChange={(e) => setV2Text(e.target.value)}
            className="w-full p-3 rounded-xl bg-gray-900 border border-white/10 text-xs text-white resize-none font-mono"
          />
        </div>
      </div>

      <div className="flex justify-center">
        <button
          onClick={handleCompare}
          disabled={loading}
          className="glow-btn px-8 py-3 rounded-xl text-xs font-bold flex items-center gap-2"
        >
          <GitCompare className="w-4 h-4" /> Compare Versions & Compute ATS Delta
        </button>
      </div>

      {diffResult && (
        <div className="space-y-6 animate-fade-in">
          <div className="glass-card p-6 border-emerald-500/30 flex items-center justify-between">
            <div>
              <span className="text-xs font-bold text-gray-400">ATS Score Delta Improvement</span>
              <div className="text-3xl font-black text-emerald-400">
                {diffResult.v1_ats_score} → {diffResult.v2_ats_score} ({diffResult.score_delta > 0 ? `+${diffResult.score_delta}` : diffResult.score_delta} pts)
              </div>
            </div>

            <span className="px-3.5 py-1.5 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-bold border border-emerald-500/30">
              {diffResult.improvement_status}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass-card p-6 space-y-3 border-emerald-500/20">
              <h4 className="text-xs font-bold text-emerald-400 uppercase flex items-center gap-1.5">
                <Plus className="w-4 h-4" /> Newly Added Technical Skills ({diffResult.added_skills.length})
              </h4>
              <div className="flex flex-wrap gap-2">
                {diffResult.added_skills.map((s, i) => (
                  <span key={i} className="px-2.5 py-1 rounded-lg bg-emerald-950/80 border border-emerald-500/30 text-emerald-300 text-xs font-semibold">
                    +{s}
                  </span>
                ))}
              </div>
            </div>

            <div className="glass-card p-6 space-y-3 border-red-500/20">
              <h4 className="text-xs font-bold text-red-400 uppercase flex items-center gap-1.5">
                <Minus className="w-4 h-4" /> Removed Skills ({diffResult.removed_skills.length})
              </h4>
              <div className="flex flex-wrap gap-2">
                {diffResult.removed_skills.map((s, i) => (
                  <span key={i} className="px-2.5 py-1 rounded-lg bg-red-950/80 border border-red-500/30 text-red-300 text-xs font-semibold">
                    -{s}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
