import React, { useState } from 'react';
import { Code, Sparkles, CheckCircle2, AlertTriangle, ExternalLink } from 'lucide-react';
import { API_BASE_URL } from '../config';

export default function GitHubAnalyzerPage() {
  const [repoUrl, setRepoUrl] = useState('https://github.com/shambhushekharsinha-engg/HireMind-AI');
  const [loading, setLoading] = useState(false);
  const [repoData, setRepoData] = useState(null);

  const handleAnalyze = async () => {
    if (!repoUrl) return;
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/v2/integrations/github-analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo_url: repoUrl })
      });
      const data = await response.json();
      setRepoData(data);
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
          GitHub Repository <span className="gradient-text">Analyzer</span>
        </h2>
        <p className="text-xs text-gray-400">Evaluate open-source code quality, README documentation, and commit health</p>
      </div>

      <div className="glass-card p-6 flex flex-col sm:flex-row items-center gap-4">
        <input
          type="text"
          placeholder="https://github.com/username/repository"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
          className="flex-1 px-4 py-2.5 rounded-xl bg-gray-900 border border-white/10 text-xs text-white"
        />
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="glow-btn px-6 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 shrink-0"
        >
          <Sparkles className="w-4 h-4" /> Analyze Repository
        </button>
      </div>

      {repoData && (
        <div className="space-y-6 animate-fade-in">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="glass-card p-6 border-indigo-500/30">
              <span className="text-xs font-bold text-gray-400">Overall Quality Score</span>
              <div className="text-3xl font-black text-white">{repoData.overall_repo_quality_score} / 100</div>
              <p className="text-[11px] text-indigo-300 mt-1">{repoData.commit_consistency}</p>
            </div>

            <div className="glass-card p-6 border-cyan-500/30">
              <span className="text-xs font-bold text-gray-400">README Documentation Score</span>
              <div className="text-3xl font-black text-cyan-300">{repoData.readme_quality_score} / 100</div>
              <p className="text-[11px] text-gray-400 mt-1">Setup commands & endpoint docs present</p>
            </div>

            <div className="glass-card p-6 border-purple-500/30">
              <span className="text-xs font-bold text-gray-400">Repository Name</span>
              <div className="text-lg font-bold text-white truncate">{repoData.owner} / {repoData.repo_name}</div>
              <div className="flex flex-wrap gap-1 mt-2">
                {repoData.detected_languages.map((l, i) => (
                  <span key={i} className="px-2 py-0.5 rounded bg-gray-800 text-[10px] text-purple-300 font-mono">
                    {l}
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div className="glass-card p-6 space-y-3 border-amber-500/20">
            <h4 className="text-xs font-bold uppercase text-amber-400 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4" /> Actionable Repository Enhancements
            </h4>
            <ul className="space-y-2">
              {repoData.actionable_improvements.map((imp, idx) => (
                <li key={idx} className="text-xs text-gray-300 flex items-start gap-2">
                  <span className="text-amber-400 font-bold">•</span> {imp}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
