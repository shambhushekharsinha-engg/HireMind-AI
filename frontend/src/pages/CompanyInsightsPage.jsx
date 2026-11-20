import React, { useState, useEffect } from 'react';
import { 
  Building2, 
  Sparkles, 
  CheckCircle2, 
  DollarSign, 
  Award, 
  ArrowRight, 
  ShieldCheck, 
  Layers, 
  Briefcase, 
  Clock, 
  Target 
} from 'lucide-react';
import { getApiBaseUrl } from '../config';

const COMPANY_BLUEPRINTS = {
  microsoft: {
    company_name: 'Microsoft',
    role: 'Software Development Engineer II (L61/L62)',
    compensation: '$185,000 - $240,000 Total Target Compensation',
    hiring_bar: 'Exceptional emphasis on clean object-oriented architecture, SOLID principles, asynchronous concurrency, and customer empathy.',
    core_stack: ['C# / .NET Core', 'Python', 'Azure Cloud Microservices', 'React / TypeScript', 'CosmosDB', 'Kubernetes'],
    interview_rounds: [
      { name: '1. Technical Screen (60 mins)', focus: 'Live coding on data structures, algorithmic complexity (O(N) time/space), and edge-case handling.' },
      { name: '2. System Design Loop (60 mins)', focus: 'High-level cloud architecture on Azure/AWS, distributed rate limiting, and SQL vs NoSQL trade-offs.' },
      { name: '3. Deep Dive Problem Solving (60 mins)', focus: 'Low-level object-oriented design, design patterns, and unit test coverage strategy.' },
      { name: '4. As-Appropriate ("AA") Director Round', focus: 'Growth mindset, cross-team collaboration, and handling ambiguous engineering requirements.' }
    ],
    preparation_tips: [
      'Microsoft interviewers prize collaborative thinking: talk through trade-offs before writing code.',
      'Familiarize yourself with distributed caching strategies (Redis, CDN caching, and read-replicas).',
      'Frame behavioral answers around the Growth Mindset philosophy (how you learned from failure).'
    ]
  },
  google: {
    company_name: 'Google',
    role: 'Software Engineer III (L4 / L5)',
    compensation: '$240,000 - $350,000 Total Target Compensation',
    hiring_bar: 'World-class algorithmic fluency, rigorous mathematical complexity analysis, and massive-scale distributed system design.',
    core_stack: ['C++', 'Python', 'Go', 'Borg / Kubernetes', 'Spanner', 'gRPC / Protocol Buffers', 'Angular / Lit'],
    interview_rounds: [
      { name: '1. Recruiter Screen & Technical Phone Screen (45 mins)', focus: 'Medium/Hard LeetCode graph traversal, dynamic programming, or bitwise algorithms in Google Docs.' },
      { name: '2. Coding Round 1: Algorithms (45 mins)', focus: 'Optimizing worst-case time/space complexity with bug-free code.' },
      { name: '3. Coding Round 2: Data Structures (45 mins)', focus: 'Trie structures, heaps, segment trees, and concurrent data structures.' },
      { name: '4. Large-Scale System Design (45 mins)', focus: 'Global scale data ingestion, consistency models (CAP/PACELC), and Sharding.' },
      { name: '5. Googleyness & Leadership (45 mins)', focus: 'Intellectual humility, doing the right thing, and elevating colleagues.' }
    ],
    preparation_tips: [
      'Write production-quality code on a whiteboard/doc without compiler assistance.',
      'Explicitly state time and space complexity in Big-O notation before beginning implementation.',
      'Review Spanner consistency, Chubby locks, and MapReduce/dataflow architectures.'
    ]
  },
  amazon: {
    company_name: 'Amazon',
    role: 'Software Development Engineer II (SDE II)',
    compensation: '$210,000 - $285,000 Total Target Compensation',
    hiring_bar: 'Rigorous alignment with the 16 Leadership Principles (LPs) paired with practical, scalable AWS cloud systems engineering.',
    core_stack: ['Java', 'Python', 'AWS (DynamoDB, Lambda, SQS, ECS, S3)', 'Distributed Microservices', 'React'],
    interview_rounds: [
      { name: '1. Online Assessment (OA)', focus: 'Two algorithmic coding questions + Work Style Assessment evaluating Leadership Principles.' },
      { name: '2. Onsite Coding 1: Data Structures', focus: 'Trees, graphs, and clean OOP abstractions with 20 minutes of LP behavioral questions.' },
      { name: '3. Onsite Coding 2: Problem Solving', focus: 'Algorithmic efficiency with deep LP exploration (Customer Obsession, Bias for Action).' },
      { name: '4. System Design (OOD & Cloud)', focus: 'Architecting high-availability AWS pipelines, DynamoDB single-table design, and throttling.' },
      { name: '5. The Bar Raiser Round', focus: 'High-stakes evaluation on whether the candidate exceeds the 50th percentile of current SDE IIs.' }
    ],
    preparation_tips: [
      'Have at least 2 distinct STAR stories prepared for every one of the 16 Leadership Principles.',
      'In system design, prioritize single-table DynamoDB schemas and event-driven decoupling.',
      'Never blame teammates or external factors; exhibit Ownership and Deliver Results.'
    ]
  }
};

export default function CompanyInsightsPage() {
  const [targetCompany, setTargetCompany] = useState('microsoft');
  const [loading, setLoading] = useState(false);
  const [blueprint, setBlueprint] = useState(() => COMPANY_BLUEPRINTS['microsoft']);

  const fetchBlueprint = async (companyStr) => {
    const key = (companyStr || targetCompany).toLowerCase();
    const fallback = COMPANY_BLUEPRINTS[key] || COMPANY_BLUEPRINTS['microsoft'];
    setBlueprint(fallback);

    setLoading(true);
    try {
      const activeUrl = getApiBaseUrl();
      const response = await fetch(`${activeUrl}/api/v2/ai/company-blueprint`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_company: key })
      });
      if (response.ok) {
        const data = await response.json();
        setBlueprint(data);
      }
    } catch (err) {
      // Kept fallback
    } finally {
      setLoading(false);
    }
  };

  const handleCompanyChange = (newComp) => {
    setTargetCompany(newComp);
    fetchBlueprint(newComp);
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold text-white flex items-center gap-2">
              Target Company <span className="gradient-text">Blueprint</span>
            </h2>
            <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
              Tier-1 Tech Intelligence
            </span>
          </div>
          <p className="text-xs text-gray-400">Pre-application hiring bars, expected tech stacks, compensation benchmarks, and interview loop breakdowns</p>
        </div>

        <select
          value={targetCompany}
          onChange={(e) => handleCompanyChange(e.target.value)}
          className="px-4 py-2.5 rounded-xl bg-slate-900 border border-white/10 text-xs text-white focus:outline-none focus:border-cyan-500 font-semibold cursor-pointer shadow-md"
        >
          <option value="microsoft">Microsoft SDE II</option>
          <option value="google">Google SWE III (L4/L5)</option>
          <option value="amazon">Amazon SDE II</option>
        </select>
      </div>

      {/* Blueprint Content Canvas (Guaranteed to render!) */}
      {blueprint && (
        <div className="space-y-6 animate-fadeIn">
          
          {/* Executive Summary Card */}
          <div className="glass-card p-6 sm:p-7 border-indigo-500/30 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="px-3 py-1 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white text-xs font-bold shadow-sm">
                  {blueprint.company_name}
                </span>
                <span className="text-sm font-bold text-cyan-300">{blueprint.role}</span>
              </div>
              <p className="text-xs text-gray-300 max-w-2xl leading-relaxed">
                <strong className="text-white">Hiring Bar: </strong>{blueprint.hiring_bar}
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-900/90 border border-emerald-500/30 space-y-1 flex-shrink-0">
              <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">Estimated Compensation</span>
              <div className="text-base font-black text-emerald-400 flex items-center gap-1 font-mono">
                <DollarSign className="w-4 h-4 text-emerald-400" />
                {blueprint.compensation}
              </div>
            </div>
          </div>

          {/* Tech Stack Chips */}
          <div className="glass-card p-5 space-y-3">
            <h4 className="text-xs font-bold uppercase text-gray-400 flex items-center gap-2">
              <Target className="w-4 h-4 text-cyan-400" />
              Core Technologies & Expected Production Competencies
            </h4>
            <div className="flex flex-wrap gap-2 pt-1">
              {(blueprint.core_stack || []).map((tech, idx) => (
                <span key={idx} className="px-3 py-1.5 rounded-xl bg-slate-900 border border-white/10 text-xs font-semibold text-cyan-300 font-mono">
                  {tech}
                </span>
              ))}
            </div>
          </div>

          {/* Interview Loop Stages Grid */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase text-gray-400 flex items-center gap-2">
              <Layers className="w-4 h-4 text-indigo-400" />
              Verified Interview Loop Structure
            </h4>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {(blueprint.interview_rounds || []).map((round, idx) => (
                <div key={idx} className="glass-card p-5 space-y-2 border-l-4 border-l-indigo-500 hover:border-l-cyan-400 transition">
                  <div className="text-xs font-bold text-white flex items-center justify-between">
                    <span>{round.name}</span>
                    <span className="text-[10px] text-gray-400 font-mono">Round {idx + 1}</span>
                  </div>
                  <p className="text-xs text-gray-300 leading-relaxed">{round.focus}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Strategic Preparation Directives */}
          <div className="glass-card p-6 border-amber-500/20 space-y-3">
            <h4 className="text-xs font-bold uppercase text-amber-400 flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              Insider Engineering Recommendations for Candidate Success
            </h4>
            <ul className="space-y-2 text-xs text-gray-300">
              {(blueprint.preparation_tips || []).map((tip, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-amber-400 font-bold">•</span>
                  <span>{tip}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
