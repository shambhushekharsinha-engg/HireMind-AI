import React, { useState } from 'react';
import { Target, Sparkles, CheckCircle2, XCircle, ArrowRight, RefreshCw } from 'lucide-react';

export default function JobMatcherPage({ latestAnalysis }) {
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [resumeText, setResumeText] = useState(latestAnalysis?.parsed_sections ? Object.values(latestAnalysis.parsed_sections).join('\n') : '');
  const [loading, setLoading] = useState(false);
  const [matchResult, setMatchResult] = useState(null);

  const handleMatch = async () => {
    if (!jobDescription.trim()) {
      alert('Please paste a Job Description.');
      return;
    }
    if (!resumeText.trim()) {
      alert('Please paste resume text or analyze a resume file first.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/jobs/match', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          job_title: jobTitle || 'Target Role',
          job_description: jobDescription,
          resume_text: resumeText,
          resume_id: latestAnalysis?.resume_id
        })
      });

      const data = await response.json();
      setMatchResult(data);
    } catch (err) {
      console.error(err);
      alert('Failed to perform job match.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          Job Match <span className="gradient-text">Comparator</span>
        </h2>
        <p className="text-xs text-gray-400">TF-IDF Vector Space & Cosine Similarity Semantic Matching</p>
      </div>

      {/* Dual Input Area */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="glass-card p-5 space-y-3">
          <label className="text-xs font-bold text-gray-300 uppercase tracking-wider block">
            Target Job Description
          </label>
          <input 
            type="text" 
            placeholder="e.g. Senior Machine Learning Engineer / Full-Stack Dev"
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
            className="w-full px-3.5 py-2 rounded-xl bg-gray-900/80 border border-white/10 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
          />
          <textarea
            rows="10"
            placeholder="Paste Job Description requirements, qualifications, and core duties..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            className="w-full p-3 rounded-xl bg-gray-900/80 border border-white/10 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 resize-none font-mono"
          />
        </div>

        <div className="glass-card p-5 space-y-3">
          <label className="text-xs font-bold text-gray-300 uppercase tracking-wider block">
            Resume Content
          </label>
          <div className="text-[11px] text-gray-400">
            {latestAnalysis ? `Auto-populated from uploaded: ${latestAnalysis.filename}` : "Paste your resume text below"}
          </div>
          <textarea
            rows="12"
            placeholder="Paste your full resume text here..."
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            className="w-full p-3 rounded-xl bg-gray-900/80 border border-white/10 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 resize-none font-mono"
          />
        </div>
      </div>

      <div className="flex justify-center">
        <button
          onClick={handleMatch}
          disabled={loading}
          className="glow-btn px-8 py-3 rounded-xl text-sm font-bold flex items-center gap-2 disabled:opacity-50"
        >
          {loading ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin" />
              Computing Vector Similarity...
            </>
          ) : (
            <>
              <Target className="w-4 h-4 text-cyan-300" />
              Calculate Job Compatibility Score
            </>
          )}
        </button>
      </div>

      {/* Match Result Display */}
      {matchResult && (
        <div className="space-y-6 animate-fade-in">
          <div className="glass-card p-6 border-cyan-500/30 flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="space-y-2 text-center md:text-left">
              <span className="px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 text-xs font-bold border border-cyan-500/30">
                {matchResult.role_fit}
              </span>
              <h3 className="text-3xl font-black text-white">
                Job Match Score: <span className="gradient-text">{matchResult.match_score}%</span>
              </h3>
              <p className="text-xs text-gray-400">Calculated via 60% Skill Overlap + 40% TF-IDF Cosine Similarity</p>
            </div>

            <div className="w-48 bg-gray-900 h-4 rounded-full overflow-hidden p-0.5 border border-white/10">
              <div 
                className="h-full bg-gradient-to-r from-indigo-500 via-purple-500 to-cyan-400 rounded-full transition-all duration-700"
                style={{ width: `${matchResult.match_score}%` }}
              ></div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass-card p-6 space-y-3 border-emerald-500/20">
              <h4 className="text-sm font-bold text-emerald-400 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" />
                Matched Skills ({matchResult.matched_skills.length})
              </h4>
              <div className="flex flex-wrap gap-2">
                {matchResult.matched_skills.map((skill, idx) => (
                  <span key={idx} className="px-3 py-1 rounded-lg bg-emerald-950/60 border border-emerald-500/30 text-emerald-300 text-xs font-semibold uppercase">
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            <div className="glass-card p-6 space-y-3 border-red-500/20">
              <h4 className="text-sm font-bold text-red-400 flex items-center gap-2">
                <XCircle className="w-4 h-4" />
                Missing Required Job Skills ({matchResult.missing_skills.length})
              </h4>
              <div className="flex flex-wrap gap-2">
                {matchResult.missing_skills.map((skill, idx) => (
                  <span key={idx} className="px-3 py-1 rounded-lg bg-red-950/60 border border-red-500/30 text-red-300 text-xs font-semibold uppercase">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div className="glass-card p-6 space-y-3 border-indigo-500/20">
            <h4 className="text-sm font-bold text-indigo-300 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-cyan-400" />
              Tailoring Recommendations for Application
            </h4>
            <ul className="space-y-2">
              {matchResult.recommendations.map((rec, idx) => (
                <li key={idx} className="text-xs text-gray-300 flex items-start gap-2">
                  <ArrowRight className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
                  {rec}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
