import React, { useState } from 'react';
import { Award, Sparkles, CheckCircle2, AlertTriangle } from 'lucide-react';

export default function LinkedInOptimizerPage() {
  const [headline, setHeadline] = useState('Software Engineering Student at Tech Institute | Interested in ML & Web Dev');
  const [summary, setSummary] = useState('Passionate about coding. Worked on Python and React projects.');
  const [targetRole, setTargetRole] = useState('Software Engineer');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleOptimize = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v2/ai/linkedin-optimize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ headline, summary, target_role: targetRole })
      });
      const data = await response.json();
      setResult(data);
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
          LinkedIn Profile <span className="gradient-text">Optimizer</span>
        </h2>
        <p className="text-xs text-gray-400">Maximize recruiter searchability and headline SEO impact</p>
      </div>

      <div className="glass-card p-6 space-y-4">
        <div className="space-y-3">
          <div>
            <label className="text-xs font-bold text-gray-300 block mb-1">Current LinkedIn Headline</label>
            <input
              type="text"
              value={headline}
              onChange={(e) => setHeadline(e.target.value)}
              className="w-full px-3.5 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white"
            />
          </div>

          <div>
            <label className="text-xs font-bold text-gray-300 block mb-1">Current About Summary</label>
            <textarea
              rows="4"
              value={summary}
              onChange={(e) => setSummary(e.target.value)}
              className="w-full p-3 rounded-xl bg-gray-900 border border-white/10 text-xs text-white resize-none"
            />
          </div>
        </div>

        <div className="flex justify-end">
          <button
            onClick={handleOptimize}
            disabled={loading}
            className="glow-btn px-6 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2"
          >
            <Sparkles className="w-4 h-4" /> Optimize LinkedIn Profile
          </button>
        </div>
      </div>

      {result && (
        <div className="space-y-6 animate-fade-in">
          <div className="glass-card p-6 border-indigo-500/30 flex items-center justify-between">
            <div>
              <span className="text-xs font-bold text-gray-400">Recruiter Searchability Score</span>
              <div className="text-3xl font-black text-white">{result.headline_seo_score} / 100</div>
            </div>
            <span className="px-3.5 py-1.5 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-bold border border-indigo-500/30">
              {result.recruiter_searchability_rating}
            </span>
          </div>

          <div className="glass-card p-6 space-y-3">
            <h4 className="text-xs font-bold uppercase text-indigo-400">High-Impact Headline Suggestions</h4>
            <div className="space-y-2">
              {result.suggested_headlines.map((h, i) => (
                <div key={i} className="p-3 bg-gray-900/60 rounded-xl border border-white/5 text-xs text-gray-200 font-medium">
                  {h}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
