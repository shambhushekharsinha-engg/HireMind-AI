import React, { useState } from 'react';
import { Edit3, Sparkles, Copy, Check, ArrowRight, RefreshCw } from 'lucide-react';

export default function BulletRewriterPage() {
  const [bullet, setBullet] = useState('Built a web app using React and Python for data analysis.');
  const [targetRole, setTargetRole] = useState('Software Engineer');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [copiedIndex, setCopiedIndex] = useState(null);

  const handleRewrite = async () => {
    if (!bullet.trim()) {
      alert('Please enter a bullet point.');
      return;
    }
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/rewriter/rewrite', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bullet_point: bullet, target_role: targetRole })
      });
      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (text, index) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          AI Resume Bullet <span className="gradient-text">Rewriter</span>
        </h2>
        <p className="text-xs text-gray-400">Transform weak resume bullets into high-impact Google XYZ formula items</p>
      </div>

      <div className="glass-card p-6 space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="sm:col-span-2 space-y-2">
            <label className="text-xs font-bold text-gray-300 uppercase tracking-wider block">
              Original Resume Bullet Point
            </label>
            <textarea
              rows="3"
              value={bullet}
              onChange={(e) => setBullet(e.target.value)}
              placeholder="e.g. Worked on database optimization and API integration."
              className="w-full p-3 rounded-xl bg-gray-900/80 border border-white/10 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 resize-none font-sans"
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-gray-300 uppercase tracking-wider block">
              Target Role Focus
            </label>
            <select
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              className="w-full px-3 py-2.5 rounded-xl bg-gray-900 border border-white/10 text-xs text-white focus:outline-none focus:border-indigo-500 font-semibold cursor-pointer"
            >
              <option value="Software Engineer">Software Engineer</option>
              <option value="Machine Learning Engineer">Machine Learning Engineer</option>
              <option value="Full-Stack Developer">Full-Stack Developer</option>
              <option value="Data Scientist">Data Scientist</option>
            </select>

            <button
              onClick={handleRewrite}
              disabled={loading}
              className="w-full glow-btn py-2.5 rounded-xl text-xs font-bold flex items-center justify-center gap-2 disabled:opacity-50 mt-2"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  Enhancing Bullets...
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  Rewrite & Optimize
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Options Display */}
      {result && (
        <div className="space-y-4 animate-fade-in">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-indigo-300 uppercase tracking-wider">
              AI Rewritten Options ({result.rewritten_options.length})
            </span>
            <span className="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-bold border border-emerald-500/30">
              {result.impact_score_boost}
            </span>
          </div>

          <div className="space-y-3">
            {result.rewritten_options.map((opt, idx) => (
              <div key={idx} className="glass-card p-4 flex items-center justify-between gap-4 border-indigo-500/20 hover:border-indigo-500/40 transition">
                <div className="space-y-1">
                  <span className="text-[10px] font-bold text-indigo-400 uppercase">
                    Option {idx + 1} ({idx === 1 ? "Quantifiable XYZ Formula" : idx === 2 ? "Tech Stack Focused" : "Action Verb Enhanced"})
                  </span>
                  <p className="text-xs font-medium text-gray-100 leading-relaxed">{opt}</p>
                </div>

                <button
                  onClick={() => handleCopy(opt, idx)}
                  className="px-3 py-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 text-xs font-semibold flex items-center gap-1.5 border border-white/10 transition shrink-0"
                >
                  {copiedIndex === idx ? (
                    <>
                      <Check className="w-3.5 h-3.5 text-emerald-400" />
                      Copied!
                    </>
                  ) : (
                    <>
                      <Copy className="w-3.5 h-3.5 text-gray-400" />
                      Copy
                    </>
                  )}
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
