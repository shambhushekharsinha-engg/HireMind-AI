import React, { useState } from 'react';
import { 
  FileUp, 
  CheckCircle2, 
  AlertTriangle, 
  Award, 
  Download, 
  Sparkles, 
  RefreshCw,
  Layers,
  ChevronDown
} from 'lucide-react';
import { API_BASE_URL } from '../config';

export default function ATSAnalyzerPage({ onAnalysisComplete, analysisData, setAnalysisData }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showRawText, setShowRawText] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a PDF or DOCX resume file.');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/resumes/upload`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to upload and analyze resume.');
      }

      const data = await response.json();
      setAnalysisData(data);
      if (onAnalysisComplete) onAnalysisComplete(data);
    } catch (err) {
      console.error(err);
      setError(err.message || 'Error communicating with backend server.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = () => {
    if (!analysisData || !analysisData.analysis_id) {
      alert('Analysis ID missing. Please analyze a resume first.');
      return;
    }
    window.open(`${API_BASE_URL}/api/v1/reports/download/${analysisData.analysis_id}`, '_blank');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            Resume <span className="gradient-text">ATS Analyzer</span>
          </h2>
          <p className="text-xs text-gray-400">Multi-factor ATS algorithm parsing & scoring engine</p>
        </div>

        {analysisData && (
          <button 
            onClick={handleDownloadPDF}
            className="glow-btn px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2"
          >
            <Download className="w-4 h-4" />
            Download PDF Report
          </button>
        )}
      </div>

      {/* Upload Zone */}
      <div className="glass-card p-8 border-dashed border-2 border-indigo-500/30 hover:border-indigo-500/60 transition text-center space-y-4">
        <div className="w-16 h-16 rounded-2xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400 mx-auto">
          <FileUp className="w-8 h-8 animate-bounce" />
        </div>
        
        <div className="space-y-1">
          <h3 className="text-base font-bold text-white">Upload Resume File (PDF / DOCX)</h3>
          <p className="text-xs text-gray-400">Fast text extraction, section segmentation & NLP skill tagging</p>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
          <input 
            type="file" 
            accept=".pdf,.docx,.doc,.txt"
            onChange={(e) => {
              setFile(e.target.files[0]);
              setError('');
            }}
            className="text-xs text-gray-300 file:mr-3 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-indigo-600 file:text-white hover:file:bg-indigo-500 cursor-pointer"
          />

          <button
            onClick={handleUpload}
            disabled={loading}
            className="glow-btn px-6 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 disabled:opacity-50"
          >
            {loading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                Parsing & Evaluating...
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                Analyze Resume
              </>
            )}
          </button>
        </div>

        {error && (
          <div className="p-3 bg-red-950/50 border border-red-500/30 rounded-xl text-xs text-red-300 flex items-center justify-center gap-2">
            <AlertTriangle className="w-4 h-4 text-red-400" />
            {error}
          </div>
        )}
      </div>

      {/* Analysis Results View */}
      {analysisData && (
        <div className="space-y-6 animate-fade-in">
          {/* Top Score Summary Banner */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="glass-card p-6 border-indigo-500/30 flex items-center gap-5">
              <div className="relative w-24 h-24 flex items-center justify-center">
                <svg className="w-full h-full transform -rotate-90">
                  <circle cx="48" cy="48" r="38" stroke="currentColor" strokeWidth="8" className="text-gray-800" fill="transparent" />
                  <circle 
                    cx="48" cy="48" r="38" 
                    stroke="currentColor" 
                    strokeWidth="8" 
                    className="text-indigo-500 transition-all duration-1000" 
                    fill="transparent"
                    strokeDasharray={2 * Math.PI * 38}
                    strokeDashoffset={2 * Math.PI * 38 * (1 - (analysisData.ats_score / 100))}
                  />
                </svg>
                <div className="absolute flex flex-col items-center">
                  <span className="text-2xl font-black text-white">{analysisData.ats_score}</span>
                  <span className="text-[10px] text-gray-400">/ 100</span>
                </div>
              </div>
              <div className="space-y-1">
                <div className="text-xs font-semibold text-gray-400">ATS Score Rating</div>
                <div className="text-lg font-bold text-indigo-300">{analysisData.rating}</div>
                <div className="text-[11px] text-gray-400">File: {analysisData.filename}</div>
              </div>
            </div>

            {/* Section Breakdown Scores */}
            <div className="md:col-span-2 glass-card p-6 space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-gray-400 flex items-center gap-2">
                <Layers className="w-4 h-4 text-cyan-400" />
                Detailed Section Score Breakdown
              </h4>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-1">
                {analysisData.section_scores && Object.entries(analysisData.section_scores).map(([key, val]) => (
                  <div key={key} className="bg-gray-900/60 p-3 rounded-xl border border-white/5 space-y-1">
                    <span className="text-[10px] text-gray-400 uppercase tracking-tight block truncate">
                      {key.replace('_', ' ')}
                    </span>
                    <span className="text-base font-bold text-cyan-300">{val} pts</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Detected Skills */}
          <div className="glass-card p-6 space-y-3">
            <h4 className="text-sm font-bold text-white flex items-center gap-2">
              <Award className="w-4 h-4 text-cyan-400" />
              Detected Core Technical & Soft Skills ({analysisData.skills_found.length})
            </h4>
            <div className="flex flex-wrap gap-2">
              {analysisData.skills_found.map((skill, idx) => (
                <span key={idx} className="px-3 py-1.5 rounded-xl bg-indigo-950/60 border border-indigo-500/30 text-indigo-300 text-xs font-semibold uppercase tracking-wide">
                  {skill}
                </span>
              ))}
            </div>
          </div>

          {/* Strengths & Suggestions Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass-card p-6 space-y-3 border-emerald-500/20">
              <h4 className="text-sm font-bold text-emerald-400 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" />
                Resume Strengths Identified
              </h4>
              <ul className="space-y-2">
                {analysisData.strengths.map((str, idx) => (
                  <li key={idx} className="text-xs text-gray-300 flex items-start gap-2">
                    <span className="text-emerald-400 font-bold">•</span>
                    {str}
                  </li>
                ))}
              </ul>
            </div>

            <div className="glass-card p-6 space-y-3 border-amber-500/20">
              <h4 className="text-sm font-bold text-amber-400 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" />
                Actionable ATS Suggestions
              </h4>
              <ul className="space-y-2">
                {analysisData.suggestions.map((sug, idx) => (
                  <li key={idx} className="text-xs text-gray-300 flex items-start gap-2">
                    <span className="text-amber-400 font-bold">•</span>
                    {sug}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Parsed Text Accordion */}
          {analysisData.parsed_sections && (
            <div className="glass-card p-5 space-y-3">
              <button 
                onClick={() => setShowRawText(!showRawText)}
                className="w-full flex items-center justify-between text-xs font-semibold text-gray-300 hover:text-white"
              >
                <span>View Extracted Resume Sections</span>
                <ChevronDown className={`w-4 h-4 transition-transform ${showRawText ? 'rotate-180' : ''}`} />
              </button>

              {showRawText && (
                <div className="pt-2 grid grid-cols-1 md:grid-cols-2 gap-4">
                  {Object.entries(analysisData.parsed_sections).map(([sec, text]) => (
                    text ? (
                      <div key={sec} className="bg-gray-900/80 p-3 rounded-xl border border-white/5 space-y-1">
                        <span className="text-[10px] font-bold text-indigo-400 uppercase">{sec}</span>
                        <pre className="text-[11px] text-gray-300 whitespace-pre-wrap font-mono h-28 overflow-y-auto">
                          {text}
                        </pre>
                      </div>
                    ) : null
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
