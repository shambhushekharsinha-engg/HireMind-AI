import React, { useState } from 'react';
import { Layout, Sparkles, Download, Save, Plus, Trash2, CheckCircle2 } from 'lucide-react';

export default function ResumeBuilderPage() {
  const [template, setTemplate] = useState('Modern');
  const [formData, setFormData] = useState({
    title: 'My Software Engineering Resume',
    full_name: 'Alex Mercer',
    email: 'alex.mercer@example.com',
    phone: '+1 (555) 234-5678',
    linkedin: 'linkedin.com/in/alexmercer',
    github: 'github.com/alexmercer',
    summary: 'Driven Software Engineer with expertise in Python, React, FastAPI, and Machine Learning. Passionate about building high-throughput cloud microservices and scalable AI features.',
    skills: ['Python', 'FastAPI', 'React', 'TypeScript', 'SQL', 'Docker', 'Machine Learning', 'Git'],
    experience: [
      {
        role: 'Full-Stack Software Engineer',
        company: 'Apex Tech Solutions',
        duration: '2024 - Present',
        bullets: ['Engineered high-throughput REST APIs handling 50k+ daily queries with 99.9% uptime.', 'Integrated React dashboard components reducing page render times by 35%.']
      }
    ],
    education: [
      {
        degree: 'B.Tech in Computer Science & Engineering',
        institution: 'Institute of Technology',
        year: '2020 - 2024'
      }
    ]
  });

  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  const handleDownloadPDF = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/builder/download-pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...formData, template_name: template })
      });
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Resume_${formData.full_name.replace(' ', '_')}.pdf`;
      a.click();
    } catch (err) {
      console.error(err);
    }
  };

  const handleSaveDraft = async () => {
    setSaving(true);
    try {
      await fetch('http://127.0.0.1:8000/api/v1/builder/draft', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...formData, template_name: template })
      });
      setMessage('Draft saved successfully to cloud database!');
      setTimeout(() => setMessage(''), 3000);
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            Interactive <span className="gradient-text">Resume Builder</span>
          </h2>
          <p className="text-xs text-gray-400">Design, customize, and export professional ATS-ready resumes</p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleSaveDraft}
            disabled={saving}
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-gray-800 hover:bg-gray-700 text-gray-200 border border-white/10 transition flex items-center gap-1.5"
          >
            <Save className="w-3.5 h-3.5" /> Save Draft
          </button>

          <button
            onClick={handleDownloadPDF}
            className="glow-btn px-5 py-2 rounded-xl text-xs font-bold flex items-center gap-2"
          >
            <Download className="w-4 h-4" /> Download PDF
          </button>
        </div>
      </div>

      {message && (
        <div className="p-3 bg-emerald-950/60 border border-emerald-500/30 rounded-xl text-xs text-emerald-300 flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" /> {message}
        </div>
      )}

      {/* Template Selection Cards */}
      <div className="glass-card p-4 space-y-3">
        <label className="text-xs font-bold uppercase text-gray-400">Choose Template Style</label>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {['Modern', 'Executive', 'Creative', 'Minimalist'].map((t) => (
            <button
              key={t}
              onClick={() => setTemplate(t)}
              className={`p-3 rounded-xl border text-xs font-bold transition flex items-center justify-center gap-2 ${
                template === t
                  ? 'bg-indigo-600/90 text-white border-indigo-400 shadow-lg shadow-indigo-500/20'
                  : 'bg-gray-900/60 text-gray-300 border-white/10 hover:border-white/20'
              }`}
            >
              <Layout className="w-4 h-4" /> {t}
            </button>
          ))}
        </div>
      </div>

      {/* Form Fields */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Personal Details */}
        <div className="glass-card p-6 space-y-4">
          <h4 className="text-xs font-bold uppercase text-indigo-400 tracking-wider">1. Contact & Identity Information</h4>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="text-[10px] font-bold text-gray-400 block mb-1">Full Name</label>
              <input
                type="text"
                value={formData.full_name}
                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white"
              />
            </div>
            <div>
              <label className="text-[10px] font-bold text-gray-400 block mb-1">Email Address</label>
              <input
                type="text"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white"
              />
            </div>
            <div>
              <label className="text-[10px] font-bold text-gray-400 block mb-1">Phone Number</label>
              <input
                type="text"
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white"
              />
            </div>
            <div>
              <label className="text-[10px] font-bold text-gray-400 block mb-1">LinkedIn Profile</label>
              <input
                type="text"
                value={formData.linkedin}
                onChange={(e) => setFormData({ ...formData, linkedin: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white"
              />
            </div>
          </div>

          <div>
            <label className="text-[10px] font-bold text-gray-400 block mb-1">Professional Summary</label>
            <textarea
              rows="4"
              value={formData.summary}
              onChange={(e) => setFormData({ ...formData, summary: e.target.value })}
              className="w-full p-3 rounded-xl bg-gray-900 border border-white/10 text-xs text-white resize-none"
            />
          </div>
        </div>

        {/* Experience & Skills */}
        <div className="glass-card p-6 space-y-4">
          <h4 className="text-xs font-bold uppercase text-cyan-400 tracking-wider">2. Technical Skills & Core Competencies</h4>
          
          <div>
            <label className="text-[10px] font-bold text-gray-400 block mb-1">Skills (Comma-Separated)</label>
            <input
              type="text"
              value={formData.skills.join(', ')}
              onChange={(e) => setFormData({ ...formData, skills: e.target.value.split(',').map(s => s.trim()) })}
              className="w-full px-3 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white font-mono"
            />
          </div>

          <h4 className="text-xs font-bold uppercase text-purple-400 tracking-wider pt-2">3. Work Experience Preview</h4>
          {formData.experience.map((exp, idx) => (
            <div key={idx} className="bg-gray-900/60 p-3 rounded-xl border border-white/5 space-y-2">
              <input
                type="text"
                value={exp.role}
                onChange={(e) => {
                  const updated = [...formData.experience];
                  updated[idx].role = e.target.value;
                  setFormData({ ...formData, experience: updated });
                }}
                className="w-full px-2.5 py-1 rounded bg-black/40 border border-white/10 text-xs text-white font-bold"
              />
              <input
                type="text"
                value={exp.company}
                onChange={(e) => {
                  const updated = [...formData.experience];
                  updated[idx].company = e.target.value;
                  setFormData({ ...formData, experience: updated });
                }}
                className="w-full px-2.5 py-1 rounded bg-black/40 border border-white/10 text-xs text-gray-300"
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
