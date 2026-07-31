import React from 'react';
import { 
  Sparkles, 
  FileUp, 
  Target, 
  Compass, 
  Award, 
  CheckCircle2, 
  Zap, 
  ArrowRight 
} from 'lucide-react';

export default function DashboardPage({ setActiveTab, latestAnalysis }) {
  const score = latestAnalysis ? latestAnalysis.ats_score : 78;
  const rating = latestAnalysis ? latestAnalysis.rating : "Good (Minor Optimization Needed)";
  const skills = latestAnalysis ? latestAnalysis.skills_found : ["python", "fastapi", "react", "sql", "machine learning"];

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="glass-card p-8 relative overflow-hidden bg-gradient-to-r from-indigo-950/60 via-purple-950/40 to-gray-900/80 border border-indigo-500/20">
        <div className="absolute top-0 right-0 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl -z-10"></div>
        <div className="max-w-2xl space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-semibold border border-indigo-500/30">
            <Sparkles className="w-3.5 h-3.5" />
            AI Career Intelligence Hub
          </div>
          <h2 className="text-3xl font-extrabold text-white tracking-tight leading-tight">
            Accelerate Your Job Applications with <span className="gradient-text">Precision AI</span>
          </h2>
          <p className="text-sm text-gray-300 leading-relaxed">
            Optimize your resume for ATS algorithms, match job descriptions with TF-IDF vector similarity, generate tailored interview questions, and follow step-by-step career roadmaps.
          </p>
          <div className="pt-2 flex items-center gap-4">
            <button 
              onClick={() => setActiveTab('ats')}
              className="glow-btn px-5 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2"
            >
              <FileUp className="w-4 h-4" />
              Analyze Resume Now
            </button>
            <button 
              onClick={() => setActiveTab('job-matcher')}
              className="px-5 py-2.5 rounded-xl text-xs font-bold bg-white/10 hover:bg-white/15 text-white border border-white/10 transition flex items-center gap-2"
            >
              <Target className="w-4 h-4 text-cyan-400" />
              Compare Job Description
            </button>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
        <div className="glass-card p-5 space-y-2 border-indigo-500/20">
          <div className="flex items-center justify-between text-gray-400 text-xs font-medium">
            <span>Current ATS Health</span>
            <Zap className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-3xl font-black text-white flex items-baseline gap-1">
            {score}<span className="text-sm text-gray-400 font-normal">/100</span>
          </div>
          <div className="w-full bg-gray-800 h-2 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-amber-400 via-indigo-500 to-emerald-400 transition-all duration-500"
              style={{ width: `${score}%` }}
            ></div>
          </div>
          <p className="text-[11px] text-emerald-400 font-semibold truncate">{rating}</p>
        </div>

        <div className="glass-card p-5 space-y-2 border-cyan-500/20">
          <div className="flex items-center justify-between text-gray-400 text-xs font-medium">
            <span>Detected Skills</span>
            <Award className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-3xl font-black text-white">
            {skills.length}
          </div>
          <p className="text-[11px] text-gray-400">Verified core technical competencies</p>
        </div>

        <div className="glass-card p-5 space-y-2 border-purple-500/20">
          <div className="flex items-center justify-between text-gray-400 text-xs font-medium">
            <span>Target Role Fit</span>
            <Compass className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-lg font-bold text-white truncate">
            Full-Stack / ML
          </div>
          <p className="text-[11px] text-indigo-300">High growth market demand</p>
        </div>

        <div className="glass-card p-5 space-y-2 border-emerald-500/20">
          <div className="flex items-center justify-between text-gray-400 text-xs font-medium">
            <span>Platform Status</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-lg font-bold text-emerald-300">
            Engine Ready
          </div>
          <p className="text-[11px] text-gray-400">Fast local NLP & TF-IDF vectors</p>
        </div>
      </div>

      {/* Feature Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div 
          onClick={() => setActiveTab('ats')}
          className="glass-card glass-card-hover p-6 cursor-pointer space-y-3 group"
        >
          <div className="w-12 h-12 rounded-2xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400 group-hover:scale-110 transition">
            <FileUp className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white group-hover:text-indigo-300 transition">Resume ATS Parser</h3>
          <p className="text-xs text-gray-400 leading-relaxed">
            Instant multi-factor ATS evaluation, section completeness score, action verb analysis, and detailed strengths.
          </p>
          <div className="text-xs font-semibold text-indigo-400 flex items-center gap-1">
            Analyze Resume <ArrowRight className="w-3.5 h-3.5" />
          </div>
        </div>

        <div 
          onClick={() => setActiveTab('job-matcher')}
          className="glass-card glass-card-hover p-6 cursor-pointer space-y-3 group"
        >
          <div className="w-12 h-12 rounded-2xl bg-cyan-600/20 border border-cyan-500/30 flex items-center justify-center text-cyan-400 group-hover:scale-110 transition">
            <Target className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white group-hover:text-cyan-300 transition">Job Match Comparator</h3>
          <p className="text-xs text-gray-400 leading-relaxed">
            Paste any job description to compute semantic TF-IDF cosine similarity, matched skills, and gap analysis.
          </p>
          <div className="text-xs font-semibold text-cyan-400 flex items-center gap-1">
            Compare Jobs <ArrowRight className="w-3.5 h-3.5" />
          </div>
        </div>

        <div 
          onClick={() => setActiveTab('interview')}
          className="glass-card glass-card-hover p-6 cursor-pointer space-y-3 group"
        >
          <div className="w-12 h-12 rounded-2xl bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-purple-400 group-hover:scale-110 transition">
            <Sparkles className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white group-hover:text-purple-300 transition">Mock Interview AI</h3>
          <p className="text-xs text-gray-400 leading-relaxed">
            Practice technical and behavioral interview questions tailored to your skills with live answer scoring.
          </p>
          <div className="text-xs font-semibold text-purple-400 flex items-center gap-1">
            Practice Practice <ArrowRight className="w-3.5 h-3.5" />
          </div>
        </div>
      </div>
    </div>
  );
}
