import React, { useState } from 'react';
import { Globe, Download, Code, Sparkles, CheckCircle2 } from 'lucide-react';
import { API_BASE_URL } from '../config';

export default function PortfolioGeneratorPage({ latestAnalysis }) {
  const [theme, setTheme] = useState('dark');
  const [htmlCode, setHtmlCode] = useState('');
  const [generating, setGenerating] = useState(false);

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      const resumeData = {
        full_name: 'Alex Mercer',
        summary: latestAnalysis?.parsed_sections?.summary || 'Full-Stack Engineer specializing in Python, React, and Machine Learning.',
        skills: latestAnalysis?.skills_found || ['Python', 'React', 'FastAPI', 'Machine Learning', 'Docker'],
        email: 'alex.mercer@example.com',
        github: 'github.com/alexmercer',
        linkedin: 'linkedin.com/in/alexmercer',
        experience: [
          { role: 'Full-Stack Software Engineer', company: 'Apex Tech', duration: '2024 - Present' }
        ]
      };

      const response = await fetch(`${API_BASE_URL}/api/v2/resume/portfolio-html`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ theme, resume_data: resumeData })
      });
      const text = await response.text();
      setHtmlCode(text);
    } catch (err) {
      console.error(err);
    } finally {
      setGenerating(false);
    }
  };

  const handleDownload = () => {
    if (!htmlCode) return;
    const blob = new Blob([htmlCode], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'portfolio.html';
    a.click();
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          Portfolio Website <span className="gradient-text">Generator</span>
        </h2>
        <p className="text-xs text-gray-400">Convert resume data into a standalone, responsive HTML portfolio site</p>
      </div>

      <div className="glass-card p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="space-y-1">
          <label className="text-xs font-bold uppercase text-gray-300">Select Website Theme</label>
          <div className="flex gap-2 pt-1">
            <button
              onClick={() => setTheme('dark')}
              className={`px-4 py-2 rounded-xl text-xs font-bold border ${theme === 'dark' ? 'bg-indigo-600 border-indigo-400 text-white' : 'bg-gray-900 border-white/10 text-gray-400'}`}
            >
              Dark Slate Theme
            </button>
            <button
              onClick={() => setTheme('light')}
              className={`px-4 py-2 rounded-xl text-xs font-bold border ${theme === 'light' ? 'bg-indigo-600 border-indigo-400 text-white' : 'bg-gray-900 border-white/10 text-gray-400'}`}
            >
              Clean Light Theme
            </button>
          </div>
        </div>

        <div className="flex gap-3">
          <button
            onClick={handleGenerate}
            disabled={generating}
            className="glow-btn px-6 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2"
          >
            <Sparkles className="w-4 h-4" /> Generate Website Code
          </button>

          {htmlCode && (
            <button
              onClick={handleDownload}
              className="px-5 py-2.5 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white border border-emerald-400/30 flex items-center gap-2"
            >
              <Download className="w-4 h-4" /> Download HTML
            </button>
          )}
        </div>
      </div>

      {htmlCode && (
        <div className="glass-card p-6 space-y-3 border-indigo-500/30">
          <h4 className="text-xs font-bold uppercase text-indigo-400 tracking-wider flex items-center gap-2">
            <Code className="w-4 h-4" /> Generated HTML/CSS Code Preview
          </h4>
          <textarea
            rows="14"
            value={htmlCode}
            readOnly
            className="w-full p-4 rounded-xl bg-gray-950 border border-white/10 text-xs text-emerald-300 font-mono resize-none"
          />
        </div>
      )}
    </div>
  );
}
