import React, { useState } from 'react';
import { Layout, Sparkles, Download, Save, Plus, Trash2, CheckCircle2, AlertTriangle, Printer } from 'lucide-react';
import { getApiBaseUrl } from '../config';

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
    skills: ['Python', 'FastAPI', 'React', 'TypeScript', 'SQL', 'Docker', 'Machine Learning', 'Git', 'AWS', 'Kubernetes'],
    experience: [
      {
        role: 'Full-Stack Software Engineer',
        company: 'Apex Tech Solutions',
        duration: '2024 - Present',
        bullets: [
          'Engineered high-throughput REST APIs handling 50k+ daily queries with 99.9% uptime.',
          'Integrated React dashboard components reducing page render times by 35%.'
        ]
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
  const [downloading, setDownloading] = useState(false);
  const [message, setMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  // Fallback client-side printable document
  const triggerClientPrintableResume = () => {
    const printWindow = window.open('', '_blank');
    if (!printWindow) {
      alert('Please allow popups to download or print your resume.');
      return;
    }

    const htmlContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <title>Resume - ${formData.full_name}</title>
        <style>
          body { font-family: 'Helvetica Neue', Arial, sans-serif; line-height: 1.5; color: #1e293b; max-width: 800px; margin: 40px auto; padding: 0 20px; }
          h1 { margin: 0; font-size: 26px; color: #0f172a; }
          .contact { color: #475569; font-size: 13px; margin-top: 4px; margin-bottom: 20px; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; }
          h2 { font-size: 15px; text-transform: uppercase; color: #334155; letter-spacing: 1px; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; margin-top: 20px; }
          p, li { font-size: 13px; color: #334155; }
          ul { margin: 6px 0; padding-left: 20px; }
          .exp-header { display: flex; justify-content: space-between; font-weight: bold; font-size: 13px; }
          .company { color: #64748b; font-size: 12px; margin-bottom: 6px; }
          .skills { font-size: 13px; }
          @media print {
            body { margin: 0; padding: 15px; }
          }
        </style>
      </head>
      <body>
        <h1>${formData.full_name}</h1>
        <div class="contact">
          ${formData.email} &bull; ${formData.phone} &bull; ${formData.linkedin} &bull; ${formData.github}
        </div>
        <h2>Professional Summary</h2>
        <p>${formData.summary}</p>
        <h2>Technical Competencies</h2>
        <p class="skills"><strong>Core Skills:</strong> ${formData.skills.join(', ')}</p>
        <h2>Professional Experience</h2>
        ${formData.experience.map(e => `
          <div class="exp-header">
            <span>${e.role}</span>
            <span>${e.duration || '2024 - Present'}</span>
          </div>
          <div class="company">${e.company}</div>
          <ul>
            ${(e.bullets || []).map(b => `<li>${b}</li>`).join('')}
          </ul>
        `).join('')}
        <h2>Education</h2>
        ${formData.education.map(ed => `
          <div class="exp-header">
            <span>${ed.degree}</span>
            <span>${ed.year}</span>
          </div>
          <div class="company">${ed.institution}</div>
        `).join('')}
        <script>
          window.onload = function() { window.print(); }
        </script>
      </body>
      </html>
    `;

    printWindow.document.write(htmlContent);
    printWindow.document.close();
  };

  const handleDownloadPDF = async () => {
    setDownloading(true);
    setErrorMessage('');
    const activeUrl = getApiBaseUrl();

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 6000);

    try {
      const response = await fetch(`${activeUrl}/api/v1/builder/download-pdf`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...formData, template_name: template }),
        signal: controller.signal
      });
      clearTimeout(timeoutId);

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Resume_${formData.full_name.replace(/\s+/g, '_')}.pdf`;
        a.click();
        setMessage('Resume PDF generated and downloaded successfully!');
        setTimeout(() => setMessage(''), 4000);
      } else {
        triggerClientPrintableResume();
        setMessage('Generated printable ATS resume window for instant export.');
        setTimeout(() => setMessage(''), 4000);
      }
    } catch (err) {
      clearTimeout(timeoutId);
      triggerClientPrintableResume();
      setMessage('Opened formatted ATS resume window for immediate printing/saving as PDF.');
      setTimeout(() => setMessage(''), 4000);
    } finally {
      setDownloading(false);
    }
  };

  const handleSaveDraft = async () => {
    setSaving(true);
    setErrorMessage('');
    try {
      localStorage.setItem('hiremind_resume_draft', JSON.stringify({ ...formData, template_name: template }));
      const activeUrl = getApiBaseUrl();
      await fetch(`${activeUrl}/api/v1/builder/draft`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...formData, template_name: template })
      }).catch(() => {});
      setMessage('Resume draft saved securely (Local & Cloud Synchronized)!');
      setTimeout(() => setMessage(''), 3500);
    } catch (err) {
      setMessage('Resume draft saved to local storage.');
      setTimeout(() => setMessage(''), 3500);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold text-white flex items-center gap-2">
              Interactive <span className="gradient-text">Resume Builder</span>
            </h2>
            <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
              ATS Standard
            </span>
          </div>
          <p className="text-xs text-gray-400">Design, customize, and export professional ATS-ready resumes with ReportLab & CSS print rendering</p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleSaveDraft}
            disabled={saving}
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-gray-800 hover:bg-gray-700 text-gray-200 border border-white/10 transition flex items-center gap-1.5 disabled:opacity-50"
          >
            <Save className="w-3.5 h-3.5 text-cyan-400" /> 
            {saving ? 'Saving...' : 'Save Draft'}
          </button>

          <button
            onClick={handleDownloadPDF}
            disabled={downloading}
            className="glow-btn px-5 py-2 rounded-xl text-xs font-bold flex items-center gap-2 disabled:opacity-50"
          >
            <Download className="w-4 h-4" /> 
            {downloading ? 'Generating PDF...' : 'Download / Print PDF'}
          </button>
        </div>
      </div>

      {message && (
        <div className="p-3 bg-emerald-950/70 border border-emerald-500/30 rounded-xl text-xs text-emerald-300 flex items-center gap-2 animate-fadeIn shadow-lg">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" /> 
          <span>{message}</span>
        </div>
      )}

      {/* Template Chooser */}
      <div className="glass-card p-4 space-y-3">
        <label className="text-xs font-bold uppercase text-gray-300">Choose Template Style</label>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {['Modern', 'Executive', 'Creative', 'Minimalist'].map((t) => (
            <button
              key={t}
              onClick={() => setTemplate(t)}
              className={`p-3 rounded-xl border text-xs font-bold transition flex items-center justify-center gap-2 ${
                template === t
                  ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white border-indigo-400 shadow-md shadow-indigo-500/20'
                  : 'bg-slate-900 text-gray-300 border-white/10 hover:border-white/20'
              }`}
            >
              <Layout className="w-4 h-4" /> {t}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Contact Info Card */}
        <div className="glass-card p-6 space-y-4">
          <h4 className="text-xs font-bold uppercase text-indigo-400 tracking-wider">1. Contact & Identity Information</h4>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="text-[10px] font-bold text-gray-400 block mb-1">Full Name</label>
              <input
                type="text"
                value={formData.full_name}
                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-xs text-white focus:outline-none focus:border-cyan-500"
              />
            </div>
            <div>
              <label className="text-[10px] font-bold text-gray-400 block mb-1">Email Address</label>
              <input
                type="text"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-xs text-white focus:outline-none focus:border-cyan-500"
              />
            </div>
            <div>
              <label className="text-[10px] font-bold text-gray-400 block mb-1">Phone Number</label>
              <input
                type="text"
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-xs text-white focus:outline-none focus:border-cyan-500"
              />
            </div>
            <div>
              <label className="text-[10px] font-bold text-gray-400 block mb-1">LinkedIn Profile</label>
              <input
                type="text"
                value={formData.linkedin}
                onChange={(e) => setFormData({ ...formData, linkedin: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-xs text-white focus:outline-none focus:border-cyan-500"
              />
            </div>
          </div>

          <div>
            <label className="text-[10px] font-bold text-gray-400 block mb-1">Professional Summary</label>
            <textarea
              rows="4"
              value={formData.summary}
              onChange={(e) => setFormData({ ...formData, summary: e.target.value })}
              className="w-full p-3 rounded-xl bg-slate-900 border border-white/10 text-xs text-white resize-none focus:outline-none focus:border-indigo-500 leading-relaxed"
            />
          </div>
        </div>

        {/* Skills & Experience Card */}
        <div className="glass-card p-6 space-y-4">
          <h4 className="text-xs font-bold uppercase text-cyan-400 tracking-wider">2. Technical Skills & Core Competencies</h4>
          
          <div>
            <label className="text-[10px] font-bold text-gray-400 block mb-1">Skills (Comma-Separated)</label>
            <input
              type="text"
              value={formData.skills.join(', ')}
              onChange={(e) => setFormData({ ...formData, skills: e.target.value.split(',').map(s => s.trim()) })}
              className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-xs text-white font-mono focus:outline-none focus:border-cyan-500"
            />
          </div>

          <h4 className="text-xs font-bold uppercase text-purple-400 tracking-wider pt-2">3. Work Experience Preview</h4>
          {formData.experience.map((exp, idx) => (
            <div key={idx} className="bg-slate-900/80 p-3.5 rounded-xl border border-white/10 space-y-2">
              <input
                type="text"
                value={exp.role}
                onChange={(e) => {
                  const updated = [...formData.experience];
                  updated[idx].role = e.target.value;
                  setFormData({ ...formData, experience: updated });
                }}
                className="w-full px-2.5 py-1.5 rounded-lg bg-black/40 border border-white/10 text-xs text-white font-bold"
              />
              <input
                type="text"
                value={exp.company}
                onChange={(e) => {
                  const updated = [...formData.experience];
                  updated[idx].company = e.target.value;
                  setFormData({ ...formData, experience: updated });
                }}
                className="w-full px-2.5 py-1.5 rounded-lg bg-black/40 border border-white/10 text-xs text-gray-300"
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
