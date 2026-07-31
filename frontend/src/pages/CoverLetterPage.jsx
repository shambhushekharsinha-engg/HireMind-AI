import React, { useState } from 'react';
import { Mail, Sparkles, Copy, Check, Download } from 'lucide-react';

export default function CoverLetterPage({ latestAnalysis }) {
  const [candidateName, setCandidateName] = useState('Alex Mercer');
  const [companyName, setCompanyName] = useState('Google');
  const [jobTitle, setJobTitle] = useState('AI Engineer');
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [letterResult, setLetterResult] = useState(null);
  const [copied, setCopied] = useState(false);

  const handleGenerate = async () => {
    if (!companyName || !jobTitle) {
      alert('Please specify target company name and job title.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v2/ai/cover-letter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          candidate_name: candidateName,
          company_name: companyName,
          job_title: jobTitle,
          resume_text: latestAnalysis?.parsed_sections ? Object.values(latestAnalysis.parsed_sections).join('\n') : 'Python, React, FastAPI',
          job_description: jobDescription
        })
      });
      const data = await response.json();
      setLetterResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (!letterResult) return;
    navigator.clipboard.writeText(letterResult.cover_letter_text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          Personalized Cover Letter <span className="gradient-text">Generator</span>
        </h2>
        <p className="text-xs text-gray-400">Tailored cover letters based on candidate resume and target company requirements</p>
      </div>

      <div className="glass-card p-6 space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label className="text-[10px] font-bold text-gray-400 block mb-1">Your Full Name</label>
            <input
              type="text"
              value={candidateName}
              onChange={(e) => setCandidateName(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white"
            />
          </div>
          <div>
            <label className="text-[10px] font-bold text-gray-400 block mb-1">Target Company Name</label>
            <input
              type="text"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white"
            />
          </div>
          <div>
            <label className="text-[10px] font-bold text-gray-400 block mb-1">Target Job Title</label>
            <input
              type="text"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white"
            />
          </div>
        </div>

        <div className="flex justify-end">
          <button
            onClick={handleGenerate}
            disabled={loading}
            className="glow-btn px-6 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2"
          >
            <Sparkles className="w-4 h-4" /> Generate Cover Letter
          </button>
        </div>
      </div>

      {letterResult && (
        <div className="glass-card p-6 space-y-4 border-indigo-500/30">
          <div className="flex items-center justify-between border-b border-white/10 pb-3">
            <span className="text-xs font-bold uppercase text-indigo-400">Generated Cover Letter</span>
            <button
              onClick={handleCopy}
              className="px-3.5 py-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 text-xs font-semibold text-gray-300 border border-white/10 flex items-center gap-1.5"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              {copied ? 'Copied to Clipboard' : 'Copy Text'}
            </button>
          </div>

          <pre className="text-xs text-gray-200 whitespace-pre-wrap font-sans leading-relaxed p-4 bg-gray-900/60 rounded-xl border border-white/5">
            {letterResult.cover_letter_text}
          </pre>
        </div>
      )}
    </div>
  );
}
