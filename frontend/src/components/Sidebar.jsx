import React, { useState } from 'react';
import { 
  LayoutDashboard, 
  FileCheck, 
  Target, 
  Compass, 
  MessageSquareCode, 
  Edit3, 
  Users, 
  History,
  Layout,
  Kanban,
  Bot,
  BarChart3,
  Globe,
  Mail,
  Share2,
  GitCompare,
  Code2,
  Building2,
  ChevronDown,
  ChevronRight,
  Sparkles,
  Layers,
  X
} from 'lucide-react';

export default function Sidebar({ 
  activeTab, 
  setActiveTab, 
  uxMode, 
  onOpenArchitecture,
  mobileMenuOpen,
  setMobileMenuOpen
}) {
  const [tacticalOpen, setTacticalOpen] = useState(true);

  // Core Executive Items (shown in Executive Mode to adhere to the 30-Second Rule)
  const executiveItems = [
    { id: 'dashboard', label: 'Executive Overview', icon: LayoutDashboard },
    { id: 'ats', label: 'Resume ATS Analyzer', icon: FileCheck },
    { id: 'job-matcher', label: 'Job Match Comparator', icon: Target },
    { id: 'interview', label: 'AI Mock Interview', icon: MessageSquareCode },
    { id: 'recruiter', label: 'Recruiter Candidate Portal', icon: Users }
  ];

  // Extended Engineering & Tactical Items (Full Cockpit)
  const buildItems = [
    { id: 'builder', label: 'Interactive Resume Builder', icon: Layout },
    { id: 'rewriter', label: 'Resume Bullet Rewriter', icon: Edit3 },
    { id: 'portfolio', label: 'Portfolio Website Generator', icon: Globe },
    { id: 'cover-letter', label: 'Cover Letter Generator', icon: Mail },
    { id: 'tracker', label: 'Job Application Kanban', icon: Kanban }
  ];

  const careerIntelligenceItems = [
    { id: 'roadmap', label: 'Career & Learning Path', icon: Compass },
    { id: 'coach', label: 'AI Career Coach', icon: Bot },
    { id: 'github', label: 'GitHub Repo Analyzer', icon: Code2 },
    { id: 'company', label: 'Target Company Blueprint', icon: Building2 },
    { id: 'linkedin', label: 'LinkedIn Profile Optimizer', icon: Share2 },
    { id: 'version-compare', label: 'Resume Version Diff', icon: GitCompare },
    { id: 'analytics', label: 'Analytics Dashboard', icon: BarChart3 },
    { id: 'history', label: 'Resume History & Reports', icon: History }
  ];

  const handleItemClick = (id) => {
    setActiveTab(id);
    if (setMobileMenuOpen) {
      setMobileMenuOpen(false);
    }
  };

  const renderButton = (item) => {
    const Icon = item.icon;
    const isActive = activeTab === item.id;
    return (
      <button
        key={item.id}
        onClick={() => handleItemClick(item.id)}
        className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold transition-all ${
          isActive
            ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md shadow-indigo-500/20 border border-indigo-400/40'
            : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
        }`}
      >
        <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-cyan-300' : 'text-gray-400'}`} />
        <span className="truncate">{item.label}</span>
      </button>
    );
  };

  const sidebarContent = (
    <div className="flex flex-col justify-between h-full p-3.5 bg-slate-950/95 md:bg-slate-950/80">
      {/* Scrollable Navigation List */}
      <div className="space-y-4 overflow-y-auto pr-1 flex-1">
        
        {/* Mobile Header with Close Button */}
        <div className="md:hidden flex items-center justify-between pb-2 border-b border-white/10">
          <span className="text-xs font-black uppercase tracking-wider text-cyan-400">Navigation Menu</span>
          <button
            onClick={() => setMobileMenuOpen && setMobileMenuOpen(false)}
            className="p-1 rounded-lg text-gray-400 hover:text-white"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Core Primary Section */}
        <div className="space-y-1">
          <div className="px-3 py-1 text-[10px] font-black uppercase tracking-wider text-cyan-400 flex items-center justify-between">
            <span>{uxMode === 'executive' ? 'Executive Core' : 'Primary Command'}</span>
            <span className="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
          </div>
          {executiveItems.map(renderButton)}
        </div>

        {/* Tactical Section (Always in Tactical Mode; Collapsible in Executive Mode) */}
        {uxMode === 'executive' ? (
          <div className="pt-2 border-t border-white/10 space-y-1">
            <button
              onClick={() => setTacticalOpen(!tacticalOpen)}
              className="w-full px-3 py-1 text-[10px] font-black uppercase tracking-wider text-gray-400 hover:text-gray-200 flex items-center justify-between transition"
            >
              <span>Tactical Tools ({buildItems.length + careerIntelligenceItems.length})</span>
              {tacticalOpen ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
            </button>

            {tacticalOpen && (
              <div className="space-y-1 pt-1 animate-fadeIn">
                {buildItems.map(renderButton)}
                {careerIntelligenceItems.map(renderButton)}
              </div>
            )}
          </div>
        ) : (
          <>
            {/* Generation & Build Tools Section */}
            <div className="pt-2 border-t border-white/10 space-y-1">
              <div className="px-3 py-1 text-[10px] font-black uppercase tracking-wider text-indigo-400 flex items-center justify-between">
                <span>Generation & Builder</span>
                <span className="w-1.5 h-1.5 rounded-full bg-indigo-400"></span>
              </div>
              {buildItems.map(renderButton)}
            </div>

            {/* Deep Career Intelligence Section */}
            <div className="pt-2 border-t border-white/10 space-y-1">
              <div className="px-3 py-1 text-[10px] font-black uppercase tracking-wider text-purple-400 flex items-center justify-between">
                <span>Analytics & Intelligence</span>
                <span className="w-1.5 h-1.5 rounded-full bg-purple-400"></span>
              </div>
              {careerIntelligenceItems.map(renderButton)}
            </div>
          </>
        )}
      </div>

      {/* Footer Info Card with Architecture Inspector Trigger */}
      <div className="pt-3 border-t border-white/10 flex-shrink-0">
        <button
          onClick={() => {
            onOpenArchitecture();
            if (setMobileMenuOpen) setMobileMenuOpen(false);
          }}
          className="w-full p-2.5 rounded-xl bg-gradient-to-r from-indigo-950/60 to-purple-950/60 border border-indigo-500/30 hover:border-indigo-500/60 transition text-left space-y-1 group"
        >
          <div className="flex items-center justify-between text-xs font-bold text-cyan-300">
            <span className="flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5 text-cyan-400 group-hover:rotate-12 transition" />
              AWS Architecture
            </span>
            <span className="text-[10px] text-emerald-400 font-mono">LIVE 200</span>
          </div>
          <p className="text-[10px] text-gray-400 leading-tight">
            Click to inspect Bedrock, PostgreSQL RLS & Pipeline Telemetry.
          </p>
        </button>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Fixed Sidebar */}
      <aside className="hidden md:flex w-64 glass-card rounded-none border-t-0 border-l-0 border-b-0 border-r border-white/10 h-[calc(100vh-4rem)] flex-shrink-0 flex-col">
        {sidebarContent}
      </aside>

      {/* Mobile Drawer Overlay */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 z-50 md:hidden flex">
          {/* Backdrop */}
          <div 
            onClick={() => setMobileMenuOpen && setMobileMenuOpen(false)} 
            className="fixed inset-0 bg-black/70 backdrop-blur-sm transition-opacity"
          />

          {/* Drawer Canvas */}
          <div className="relative w-72 max-w-[85vw] h-full shadow-2xl z-10 border-r border-indigo-500/30 animate-fadeIn">
            {sidebarContent}
          </div>
        </div>
      )}
    </>
  );
}
