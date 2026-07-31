import React from 'react';
import { 
  Sparkles, 
  FileUp, 
  Target, 
  Compass, 
  Award, 
  CheckCircle2, 
  Zap, 
  ArrowRight,
  Globe,
  Mail,
  Share2,
  GitCompare,
  Code2,
  Building2,
  Kanban,
  Bot
} from 'lucide-react';

export default function DashboardPage({ setActiveTab, latestAnalysis }) {
  const score = latestAnalysis ? latestAnalysis.ats_score : 84;
  const rating = latestAnalysis ? latestAnalysis.rating : "Excellent (ATS Benchmark Passed)";
  const skills = latestAnalysis ? latestAnalysis.skills_found : ["Python", "FastAPI", "React", "SQL", "Docker", "Machine Learning"];

  return (
    <div className="space-y-8">
      {/* 3D Hero Banner */}
      <div className="glass-card p-8 md:p-10 relative overflow-hidden bg-gradient-to-r from-indigo-950/80 via-purple-950/50 to-slate-950 border border-indigo-500/30 shadow-2xl">
        <div className="absolute top-0 right-0 w-96 h-96 bg-indigo-500/15 rounded-full blur-3xl -z-10 animate-pulse"></div>
        <div className="max-w-3xl space-y-4">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-bold border border-indigo-500/30 shadow-inner">
            <Sparkles className="w-4 h-4 text-cyan-400 animate-spin" />
            AI Career Operating System v3.0
          </div>
          
          <h2 className="text-3xl sm:text-4xl font-black text-white tracking-tight leading-tight">
            Accelerate Your Engineering Career with <span className="gradient-text">Intelligent Automation</span>
          </h2>
          
          <p className="text-sm text-gray-300 leading-relaxed max-w-2xl">
            Build ATS-optimized resumes, generate responsive portfolio websites, compare job descriptions with TF-IDF vector space similarity, practice voice mock interviews, and track your application pipeline.
          </p>

          <div className="pt-2 flex flex-wrap items-center gap-4">
            <button 
              onClick={() => setActiveTab('ats')}
              className="glow-btn px-6 py-3 rounded-2xl text-xs font-black flex items-center gap-2"
            >
              <FileUp className="w-4 h-4" />
              Analyze Resume Now
            </button>

            <button 
              onClick={() => setActiveTab('portfolio')}
              className="px-6 py-3 rounded-2xl text-xs font-black bg-slate-900/80 hover:bg-slate-800 text-cyan-300 border border-cyan-500/30 hover:border-cyan-500/60 shadow-lg transition flex items-center gap-2"
            >
              <Globe className="w-4 h-4" />
              Generate Portfolio Site
            </button>

            <button 
              onClick={() => setActiveTab('job-matcher')}
              className="px-6 py-3 rounded-2xl text-xs font-black bg-white/10 hover:bg-white/15 text-white border border-white/10 transition flex items-center gap-2"
            >
              <Target className="w-4 h-4 text-indigo-400" />
              Job Matcher
            </button>
          </div>
        </div>
      </div>

      {/* 3D Metric Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="glass-card glass-card-hover p-6 space-y-3 border-indigo-500/30">
          <div className="flex items-center justify-between text-gray-400 text-xs font-semibold">
            <span>ATS Compatibility</span>
            <Zap className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-4xl font-black text-white flex items-baseline gap-1">
            {score}<span className="text-sm text-gray-400 font-normal">/100</span>
          </div>
          <div className="w-full bg-slate-900 h-2.5 rounded-full overflow-hidden p-0.5 border border-white/10">
            <div 
              className="h-full bg-gradient-to-r from-amber-400 via-indigo-500 to-cyan-400 rounded-full transition-all duration-700"
              style={{ width: `${score}%` }}
            ></div>
          </div>
          <p className="text-[11px] text-emerald-400 font-bold truncate">{rating}</p>
        </div>

        <div className="glass-card glass-card-hover p-6 space-y-3 border-cyan-500/30">
          <div className="flex items-center justify-between text-gray-400 text-xs font-semibold">
            <span>Verified Skills</span>
            <Award className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-4xl font-black text-white">
            {skills.length}
          </div>
          <p className="text-[11px] text-gray-400 font-medium">Core technical competencies tagged</p>
        </div>

        <div className="glass-card glass-card-hover p-6 space-y-3 border-purple-500/30">
          <div className="flex items-center justify-between text-gray-400 text-xs font-semibold">
            <span>Target Role Fit</span>
            <Compass className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-xl font-black text-white truncate">
            Full-Stack / ML
          </div>
          <p className="text-[11px] text-indigo-300 font-semibold">+18% Annual Market Demand</p>
        </div>

        <div className="glass-card glass-card-hover p-6 space-y-3 border-emerald-500/30">
          <div className="flex items-center justify-between text-gray-400 text-xs font-semibold">
            <span>Infrastructure Status</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-xl font-black text-emerald-300">
            API v2 Active
          </div>
          <p className="text-[11px] text-gray-400 font-medium">PostgreSQL & Multi-Model NLP</p>
        </div>
      </div>

      {/* Enterprise Feature Cards Grid */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider px-1">Platform Modules & Tools</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div 
            onClick={() => setActiveTab('portfolio')}
            className="glass-card glass-card-hover p-6 cursor-pointer space-y-3 group border-cyan-500/20"
          >
            <div className="w-12 h-12 rounded-2xl bg-cyan-500/20 border border-cyan-500/30 flex items-center justify-center text-cyan-400 group-hover:scale-110 transition">
              <Globe className="w-6 h-6" />
            </div>
            <h4 className="text-lg font-bold text-white group-hover:text-cyan-300 transition">Portfolio Generator</h4>
            <p className="text-xs text-gray-400 leading-relaxed">
              Instantly generate responsive, modern HTML/CSS portfolio websites from resume data.
            </p>
            <div className="text-xs font-bold text-cyan-400 flex items-center gap-1">
              Build Portfolio Site <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </div>

          <div 
            onClick={() => setActiveTab('cover-letter')}
            className="glass-card glass-card-hover p-6 cursor-pointer space-y-3 group border-indigo-500/20"
          >
            <div className="w-12 h-12 rounded-2xl bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400 group-hover:scale-110 transition">
              <Mail className="w-6 h-6" />
            </div>
            <h4 className="text-lg font-bold text-white group-hover:text-indigo-300 transition">Cover Letter Generator</h4>
            <p className="text-xs text-gray-400 leading-relaxed">
              Create tailored cover letters customized for target job descriptions and company names.
            </p>
            <div className="text-xs font-bold text-indigo-400 flex items-center gap-1">
              Generate Cover Letter <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </div>

          <div 
            onClick={() => setActiveTab('linkedin')}
            className="glass-card glass-card-hover p-6 cursor-pointer space-y-3 group border-purple-500/20"
          >
            <div className="w-12 h-12 rounded-2xl bg-purple-500/20 border border-purple-500/30 flex items-center justify-center text-purple-400 group-hover:scale-110 transition">
              <Share2 className="w-6 h-6" />
            </div>
            <h4 className="text-lg font-bold text-white group-hover:text-purple-300 transition">LinkedIn Optimizer</h4>
            <p className="text-xs text-gray-400 leading-relaxed">
              Analyze LinkedIn headlines and summaries for recruiter searchability and SEO rank.
            </p>
            <div className="text-xs font-bold text-purple-400 flex items-center gap-1">
              Optimize Profile <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </div>

          <div 
            onClick={() => setActiveTab('version-compare')}
            className="glass-card glass-card-hover p-6 cursor-pointer space-y-3 group border-emerald-500/20"
          >
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 group-hover:scale-110 transition">
              <GitCompare className="w-6 h-6" />
            </div>
            <h4 className="text-lg font-bold text-white group-hover:text-emerald-300 transition">Resume Version Control</h4>
            <p className="text-xs text-gray-400 leading-relaxed">
              Git-style side-by-side version comparison highlighting skill deltas and ATS score gains.
            </p>
            <div className="text-xs font-bold text-emerald-400 flex items-center gap-1">
              Compare Versions <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </div>

          <div 
            onClick={() => setActiveTab('company')}
            className="glass-card glass-card-hover p-6 cursor-pointer space-y-3 group border-amber-500/20"
          >
            <div className="w-12 h-12 rounded-2xl bg-amber-500/20 border border-amber-500/30 flex items-center justify-center text-amber-400 group-hover:scale-110 transition">
              <Building2 className="w-6 h-6" />
            </div>
            <h4 className="text-lg font-bold text-white group-hover:text-amber-300 transition">Target Company Blueprint</h4>
            <p className="text-xs text-gray-400 leading-relaxed">
              Pre-application company intelligence for Microsoft, Google, Amazon & top tier tech firms.
            </p>
            <div className="text-xs font-bold text-amber-400 flex items-center gap-1">
              View Company Blueprint <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </div>

          <div 
            onClick={() => setActiveTab('coach')}
            className="glass-card glass-card-hover p-6 cursor-pointer space-y-3 group border-indigo-500/20"
          >
            <div className="w-12 h-12 rounded-2xl bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400 group-hover:scale-110 transition">
              <Bot className="w-6 h-6" />
            </div>
            <h4 className="text-lg font-bold text-white group-hover:text-indigo-300 transition">AI Career Coach</h4>
            <p className="text-xs text-gray-400 leading-relaxed">
              Conversational AI assistant providing personalized roadmap guidance and portfolio advice.
            </p>
            <div className="text-xs font-bold text-indigo-400 flex items-center gap-1">
              Chat with AI Coach <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
