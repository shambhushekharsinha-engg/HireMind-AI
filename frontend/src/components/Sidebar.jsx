import React from 'react';
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
  Building2
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab }) {
  const menuItems = [
    { id: 'dashboard', label: 'Overview Dashboard', icon: LayoutDashboard },
    { id: 'builder', label: 'Interactive Resume Builder', icon: Layout },
    { id: 'ats', label: 'Resume ATS Analyzer', icon: FileCheck },
    { id: 'job-matcher', label: 'Job Match Comparator', icon: Target },
    { id: 'tracker', label: 'Job Application Tracker', icon: Kanban },
    { id: 'portfolio', label: 'Portfolio Website Generator', icon: Globe },
    { id: 'cover-letter', label: 'Cover Letter Generator', icon: Mail },
    { id: 'linkedin', label: 'LinkedIn Profile Optimizer', icon: Share2 },
    { id: 'version-compare', label: 'Resume Version Diff', icon: GitCompare },
    { id: 'github', label: 'GitHub Repo Analyzer', icon: Code2 },
    { id: 'company', label: 'Target Company Blueprint', icon: Building2 },
    { id: 'coach', label: 'AI Career Coach', icon: Bot },
    { id: 'roadmap', label: 'Career & Learning Path', icon: Compass },
    { id: 'interview', label: 'Interview Prep AI', icon: MessageSquareCode },
    { id: 'rewriter', label: 'Resume Bullet Rewriter', icon: Edit3 },
    { id: 'recruiter', label: 'Recruiter Candidate Portal', icon: Users },
    { id: 'analytics', label: 'Analytics Dashboard', icon: BarChart3 },
    { id: 'history', label: 'Resume History & Reports', icon: History }
  ];

  return (
    <aside className="w-64 glass-card rounded-none border-t-0 border-l-0 border-b-0 border-r border-white/10 p-4 flex flex-col justify-between min-h-[calc(100vh-61px)]">
      <div className="space-y-1 overflow-y-auto max-h-[calc(100vh-140px)]">
        <div className="px-3 py-1.5 text-[10px] font-bold uppercase tracking-wider text-gray-500">
          Career OS Modules
        </div>

        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium transition-all ${
                isActive
                  ? 'bg-gradient-to-r from-indigo-600/90 to-purple-600/90 text-white shadow-lg shadow-indigo-500/20 border border-indigo-400/30'
                  : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
              }`}
            >
              <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-cyan-300' : 'text-gray-400'}`} />
              <span className="truncate">{item.label}</span>
            </button>
          );
        })}
      </div>

      <div className="p-3 glass-card bg-indigo-950/30 border border-indigo-500/20 rounded-xl space-y-1 mt-2">
        <div className="flex items-center gap-2 text-xs font-semibold text-indigo-300">
          <span className="w-2 h-2 rounded-full bg-cyan-400"></span>
          Career OS Enterprise v3.0
        </div>
        <p className="text-[10px] text-gray-400 leading-tight">
          Multi-Model AI, API v2 & Observability.
        </p>
      </div>
    </aside>
  );
}
