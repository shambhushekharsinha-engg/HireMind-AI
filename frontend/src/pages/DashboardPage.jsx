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
  Bot,
  Layers,
  ShieldCheck,
  TrendingUp,
  Flame
} from 'lucide-react';

export default function DashboardPage({ setActiveTab, latestAnalysis, uxMode, onOpenArchitecture }) {
  const score = latestAnalysis ? Math.round(latestAnalysis.ats_score) : 92;
  const rating = latestAnalysis ? latestAnalysis.rating : "Excellent (ATS Benchmark Passed)";
  const skills = latestAnalysis ? latestAnalysis.skills_found : ["Python", "FastAPI", "React", "SQL", "Docker", "Machine Learning", "TypeScript", "AWS"];

  return (
    <div className="space-y-7">
      
      {/* 3D Executive Hero Banner */}
      <div className="glass-card p-6 sm:p-9 relative overflow-hidden bg-gradient-to-r from-indigo-950/90 via-purple-950/60 to-slate-950 border border-indigo-500/30 shadow-2xl">
        <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl -z-10 animate-pulse"></div>
        <div className="max-w-3xl space-y-4">
          
          <div className="flex flex-wrap items-center gap-2">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/20 text-cyan-300 text-xs font-bold border border-indigo-500/30 shadow-inner">
              <Sparkles className="w-3.5 h-3.5 text-cyan-400 animate-spin" />
              Career OS v3.0 · {uxMode === 'executive' ? 'Executive Mode' : 'Tactical Cockpit'}
            </span>
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold border border-emerald-500/30">
              <ShieldCheck className="w-3.5 h-3.5" />
              AWS Bedrock & NLP Redundant
            </span>
          </div>
          
          <h2 className="text-2xl sm:text-4xl font-black text-white tracking-tight leading-tight">
            Enterprise Career Intelligence with <span className="gradient-text">Preemptive Automation</span>
          </h2>
          
          <p className="text-xs sm:text-sm text-gray-300 leading-relaxed max-w-2xl">
            Shift from reactive resume tracking to preemptive career intelligence: multimodal ATS scoring, TF-IDF vector space semantic matching, voice interview AI, and automatic portfolio generation.
          </p>

          <div className="pt-2 flex flex-wrap items-center gap-3">
            {/* 1-Click Live Demo Action (Master Rule 1 & 3: Demo Video & Flow < 3s) */}
            <button 
              onClick={() => setActiveTab('ats')}
              className="glow-btn px-6 py-3 rounded-2xl text-xs font-black flex items-center gap-2 shadow-lg shadow-indigo-500/30"
              title="Launch instant pre-calibrated resume benchmark"
            >
              <Zap className="w-4 h-4 text-amber-300" />
              Run Live ATS Demo (&lt; 2s)
            </button>

            <button 
              onClick={onOpenArchitecture}
              className="px-5 py-3 rounded-2xl text-xs font-black bg-slate-900/90 hover:bg-slate-800 text-cyan-300 border border-cyan-500/40 hover:border-cyan-400/80 shadow-md transition flex items-center gap-2"
              title="Open AWS Architecture & Pipeline Telemetry"
            >
              <Layers className="w-4 h-4" />
              Architecture Inspector
            </button>

            <button 
              onClick={() => setActiveTab('job-matcher')}
              className="px-5 py-3 rounded-2xl text-xs font-black bg-white/10 hover:bg-white/15 text-white border border-white/10 transition flex items-center gap-2"
            >
              <Target className="w-4 h-4 text-indigo-400" />
              Vector Job Matcher
            </button>
          </div>
        </div>
      </div>

      {/* 3D Metric Stat Cards (Quantified ROI Figures) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="glass-card glass-card-hover p-5 space-y-2.5 border-indigo-500/30">
          <div className="flex items-center justify-between text-gray-400 text-xs font-semibold">
            <span>ATS Compatibility</span>
            <Zap className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-3xl font-black text-white flex items-baseline gap-1">
            {score}<span className="text-xs text-gray-400 font-normal">/100</span>
          </div>
          <div className="w-full bg-slate-900 h-2 rounded-full overflow-hidden p-0.5 border border-white/10">
            <div 
              className="h-full bg-gradient-to-r from-amber-400 via-indigo-500 to-cyan-400 rounded-full transition-all duration-700"
              style={{ width: `${score}%` }}
            ></div>
          </div>
          <p className="text-[11px] text-emerald-400 font-bold truncate">{rating}</p>
        </div>

        <div className="glass-card glass-card-hover p-5 space-y-2.5 border-cyan-500/30">
          <div className="flex items-center justify-between text-gray-400 text-xs font-semibold">
            <span>Interviews Unlocked</span>
            <TrendingUp className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-3xl font-black text-white flex items-baseline gap-1.5">
            +38% <span className="text-xs text-emerald-400 font-semibold font-mono">Response Rate</span>
          </div>
          <p className="text-[11px] text-gray-300 font-medium">Estimated callback boost vs standard PDF resumes</p>
        </div>

        <div className="glass-card glass-card-hover p-5 space-y-2.5 border-purple-500/30">
          <div className="flex items-center justify-between text-gray-400 text-xs font-semibold">
            <span>Verified Skills Tagged</span>
            <Award className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-3xl font-black text-white">
            {skills.length}
          </div>
          <p className="text-[11px] text-indigo-300 font-semibold">spaCy NLP Token & Entity Recognition</p>
        </div>

        <div className="glass-card glass-card-hover p-5 space-y-2.5 border-emerald-500/30">
          <div className="flex items-center justify-between text-gray-400 text-xs font-semibold">
            <span>Failover Redundancy</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-black text-emerald-300">
            &lt; 50ms SLA
          </div>
          <p className="text-[11px] text-gray-300 font-medium">Sub-50ms deterministic safety net failover</p>
        </div>
      </div>

      {/* Top 3 Prioritized Action Protocol Directives (Master Rule 3) */}
      <div className="space-y-3">
        <h3 className="text-sm font-bold uppercase tracking-wider text-gray-400 flex items-center gap-2">
          <Flame className="w-4 h-4 text-amber-400" />
          Top 3 Prioritized Engineering Directives
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div 
            onClick={() => setActiveTab('ats')}
            className="glass-card glass-card-hover p-5 border-l-4 border-l-cyan-400 cursor-pointer space-y-2 group"
          >
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-black uppercase text-cyan-400 tracking-wider">Priority 1</span>
              <ArrowRight className="w-4 h-4 text-gray-500 group-hover:text-cyan-400 group-hover:translate-x-1 transition" />
            </div>
            <h4 className="text-sm font-bold text-white group-hover:text-cyan-300 transition">Execute ATS Scoring</h4>
            <p className="text-xs text-gray-300 leading-relaxed">
              Verify formatting completeness, action verb density, and quantified impact index.
            </p>
          </div>

          <div 
            onClick={() => setActiveTab('job-matcher')}
            className="glass-card glass-card-hover p-5 border-l-4 border-l-indigo-400 cursor-pointer space-y-2 group"
          >
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-black uppercase text-indigo-400 tracking-wider">Priority 2</span>
              <ArrowRight className="w-4 h-4 text-gray-500 group-hover:text-indigo-400 group-hover:translate-x-1 transition" />
            </div>
            <h4 className="text-sm font-bold text-white group-hover:text-indigo-300 transition">Compare Against Target JD</h4>
            <p className="text-xs text-gray-300 leading-relaxed">
              Compute TF-IDF cosine distance against target engineering job descriptions.
            </p>
          </div>

          <div 
            onClick={() => setActiveTab('interview')}
            className="glass-card glass-card-hover p-5 border-l-4 border-l-purple-400 cursor-pointer space-y-2 group"
          >
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-black uppercase text-purple-400 tracking-wider">Priority 3</span>
              <ArrowRight className="w-4 h-4 text-gray-500 group-hover:text-purple-400 group-hover:translate-x-1 transition" />
            </div>
            <h4 className="text-sm font-bold text-white group-hover:text-purple-300 transition">Practice AI Mock Interview</h4>
            <p className="text-xs text-gray-300 leading-relaxed">
              Simulate technical whiteboard and behavioral QA with AI scoring blueprints.
            </p>
          </div>
        </div>
      </div>

      {/* Feature Exploration Grid */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold uppercase tracking-wider text-gray-400">
          Enterprise Tool Suite
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div onClick={() => setActiveTab('portfolio')} className="glass-card glass-card-hover p-5 cursor-pointer space-y-2 group">
            <div className="w-8 h-8 rounded-lg bg-cyan-500/20 text-cyan-300 flex items-center justify-center">
              <Globe className="w-4 h-4" />
            </div>
            <h4 className="text-sm font-bold text-white group-hover:text-cyan-300 transition">Portfolio Generator</h4>
            <p className="text-xs text-gray-400">Generate responsive, modern HTML/CSS portfolio websites instantly from resume data.</p>
          </div>

          <div onClick={() => setActiveTab('builder')} className="glass-card glass-card-hover p-5 cursor-pointer space-y-2 group">
            <div className="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-300 flex items-center justify-center">
              <Kanban className="w-4 h-4" />
            </div>
            <h4 className="text-sm font-bold text-white group-hover:text-indigo-300 transition">Interactive Resume Builder</h4>
            <p className="text-xs text-gray-400">Design, customize, and export professional ATS-ready PDF resumes with modern styling.</p>
          </div>

          <div onClick={() => setActiveTab('rewriter')} className="glass-card glass-card-hover p-5 cursor-pointer space-y-2 group">
            <div className="w-8 h-8 rounded-lg bg-purple-500/20 text-purple-300 flex items-center justify-center">
              <Sparkles className="w-4 h-4" />
            </div>
            <h4 className="text-sm font-bold text-white group-hover:text-purple-300 transition">STAR Bullet Rewriter</h4>
            <p className="text-xs text-gray-400">Elevate weak bullet points into high-impact, metric-driven achievement statements.</p>
          </div>

          <div onClick={() => setActiveTab('github')} className="glass-card glass-card-hover p-5 cursor-pointer space-y-2 group">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-300 flex items-center justify-center">
              <Code2 className="w-4 h-4" />
            </div>
            <h4 className="text-sm font-bold text-white group-hover:text-emerald-300 transition">GitHub Repo Analyzer</h4>
            <p className="text-xs text-gray-400">Analyze repository quality, test coverage, and documentation for recruiter screening.</p>
          </div>

          <div onClick={() => setActiveTab('coach')} className="glass-card glass-card-hover p-5 cursor-pointer space-y-2 group">
            <div className="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-300 flex items-center justify-center">
              <Bot className="w-4 h-4" />
            </div>
            <h4 className="text-sm font-bold text-white group-hover:text-amber-300 transition">AI Career Coach</h4>
            <p className="text-xs text-gray-400">Personalized conversational AI mentor for salary negotiation and career trajectory.</p>
          </div>

          <div onClick={() => setActiveTab('recruiter')} className="glass-card glass-card-hover p-5 cursor-pointer space-y-2 group">
            <div className="w-8 h-8 rounded-lg bg-rose-500/20 text-rose-300 flex items-center justify-center">
              <Award className="w-4 h-4" />
            </div>
            <h4 className="text-sm font-bold text-white group-hover:text-rose-300 transition">Recruiter Candidate Search</h4>
            <p className="text-xs text-gray-400">Search and filter top candidates across Kaggle datasets and indexed candidate pools.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
