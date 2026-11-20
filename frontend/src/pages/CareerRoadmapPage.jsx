import React, { useState, useEffect } from 'react';
import { 
  Compass, 
  Sparkles, 
  CheckCircle2, 
  BookOpen, 
  Award, 
  DollarSign, 
  ArrowRight, 
  Layers, 
  Clock, 
  ChevronRight,
  TrendingUp
} from 'lucide-react';
import { getApiBaseUrl } from '../config';

const DEFAULT_ROADMAPS = {
  'AI / Machine Learning Engineer': {
    target_role: 'Senior AI & Machine Learning Systems Engineer',
    estimated_timeline: '6 - 9 Months Structured Progression',
    average_salary: '$165,000 - $225,000 / year',
    phases: [
      {
        phase_number: 1,
        title: 'Phase 1: Advanced Mathematical & Statistical Foundations',
        duration: 'Month 1 - 2',
        description: 'Master core vector algebra, matrix factorizations, and gradient descent optimization routines.',
        skills: ['NumPy / SciPy', 'Vector Math (Linear Algebra)', 'Probability Distributions', 'Calculus & Backpropagation'],
        milestone_project: 'Implement a Multi-Layer Perceptron (MLP) from scratch with manual backprop in pure Python.'
      },
      {
        phase_number: 2,
        title: 'Phase 2: Deep Learning, PyTorch & Transformer Architecture',
        duration: 'Month 3 - 4',
        description: 'Construct and fine-tune modern Transformer models, attention mechanisms, and embedding spaces.',
        skills: ['PyTorch 2.x', 'Hugging Face Transformers', 'Self-Attention / Multi-Head Attention', 'LoRA / QLoRA Fine-Tuning'],
        milestone_project: 'Fine-tune an open-source LLM on custom technical documentation with evaluation metrics (ROUGE/BLEU).'
      },
      {
        phase_number: 3,
        title: 'Phase 3: Vector Retrieval & High-Throughput RAG Systems',
        duration: 'Month 5 - 6',
        description: 'Architect scalable vector retrieval-augmented generation pipelines using approximate nearest neighbors.',
        skills: ['FAISS / Pinecone', 'LangChain / LlamaIndex', 'Cosine Vector Space Similarity', 'Cross-Encoders & Re-Ranking'],
        milestone_project: 'Build a production-grade multimodal RAG pipeline serving sub-100ms semantic similarity queries.'
      },
      {
        phase_number: 4,
        title: 'Phase 4: Cloud MLOps, Triton Serving & Production Scale',
        duration: 'Month 7 - 9',
        description: 'Containerize, orchestrate, and monitor deep learning models with automated CI/CD and GPU optimization.',
        skills: ['AWS Bedrock / SageMaker', 'Docker & Kubernetes', 'Triton Inference Server', 'Model Drift & DataDog Telemetry'],
        milestone_project: 'Deploy a high-availability serverless model serving endpoint with automatic horizontal autoscaling.'
      }
    ]
  },
  'Full-Stack Cloud Engineer': {
    target_role: 'Staff Full-Stack Cloud & Distributed Systems Engineer',
    estimated_timeline: '4 - 6 Months Structured Progression',
    average_salary: '$150,000 - $210,000 / year',
    phases: [
      {
        phase_number: 1,
        title: 'Phase 1: High-Performance Backend & Asynchronous I/O',
        duration: 'Month 1',
        description: 'Architect asynchronous REST APIs and event-driven microservices using modern concurrency paradigms.',
        skills: ['Python FastAPI', 'AsyncIO Concurrency', 'Pydantic V2', 'SQLAlchemy 2.0 ORM'],
        milestone_project: 'Build a 50k req/min async rate-limited microservice gateway with Redis token-bucket caching.'
      },
      {
        phase_number: 2,
        title: 'Phase 2: Reactive Modern Frontend & State Virtualization',
        duration: 'Month 2 - 3',
        description: 'Construct reactive user interfaces with sub-millisecond interaction times and zero layout shifts.',
        skills: ['React 19', 'TypeScript', 'Tailwind CSS v4', 'Virtual DOM & Memoization'],
        milestone_project: 'Develop a high-density, real-time analytics telemetry dashboard with WebSocket streaming.'
      },
      {
        phase_number: 3,
        title: 'Phase 3: Database Isolation & Row-Level Security',
        duration: 'Month 4',
        description: 'Master relational schema migrations, connection pooling, and multi-tenant security barriers.',
        skills: ['PostgreSQL 16', 'Row-Level Security (RLS)', 'PgBouncer Pooling', 'Database Indexing & Query Plans'],
        milestone_project: 'Implement multi-tenant database isolation with automated column migrations and zero-downtime rollouts.'
      },
      {
        phase_number: 4,
        title: 'Phase 4: Cloud Infrastructure as Code & Continuous Delivery',
        duration: 'Month 5 - 6',
        description: 'Automate serverless infrastructure, container builds, and blue-green zero-downtime deployment pipelines.',
        skills: ['Docker Multi-Stage', 'AWS / Render PaaS', 'GitHub Actions CI/CD', 'Security Linting & Pytest'],
        milestone_project: 'Author an automated CI/CD pipeline achieving 100% test coverage and automatic canary deployment.'
      }
    ]
  }
};

export default function CareerRoadmapPage({ latestAnalysis }) {
  const [targetRole, setTargetRole] = useState('AI / Machine Learning Engineer');
  const [loading, setLoading] = useState(false);
  const [roadmapData, setRoadmapData] = useState(() => DEFAULT_ROADMAPS['AI / Machine Learning Engineer']);

  const fetchRoadmap = async (role) => {
    const fallback = DEFAULT_ROADMAPS[role] || DEFAULT_ROADMAPS['AI / Machine Learning Engineer'];
    setRoadmapData(fallback);

    setLoading(true);
    try {
      const activeUrl = getApiBaseUrl();
      const response = await fetch(`${activeUrl}/api/v1/career/roadmap`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          target_role: role || targetRole,
          resume_text: latestAnalysis?.parsed_sections ? Object.values(latestAnalysis.parsed_sections).join('\n') : ''
        })
      });
      if (response.ok) {
        const data = await response.json();
        if (data && data.phases && data.phases.length > 0) {
          setRoadmapData(data);
        }
      }
    } catch (err) {
      // Kept fallback
    } finally {
      setLoading(false);
    }
  };

  const handleRoleSelect = (newRole) => {
    setTargetRole(newRole);
    fetchRoadmap(newRole);
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold text-white flex items-center gap-2">
              Career & <span className="gradient-text">Learning Roadmap</span>
            </h2>
            <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
              4-Phase Milestone
            </span>
          </div>
          <p className="text-xs text-gray-400">Step-by-step technical progression, milestone projects, and skill acquisition trajectory</p>
        </div>

        <select 
          value={targetRole}
          onChange={(e) => handleRoleSelect(e.target.value)}
          className="px-4 py-2.5 rounded-xl bg-slate-900 border border-white/10 text-xs text-white focus:outline-none focus:border-cyan-500 font-semibold cursor-pointer shadow-md"
        >
          <option value="AI / Machine Learning Engineer">AI / Machine Learning Engineer</option>
          <option value="Full-Stack Cloud Engineer">Full-Stack Cloud Engineer</option>
        </select>
      </div>

      {/* Target Role Overview Banner */}
      {roadmapData && (
        <div className="glass-card p-6 sm:p-7 border-indigo-500/30 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 text-xs font-bold border border-cyan-500/30">
                Target Role
              </span>
              <h3 className="text-base sm:text-lg font-bold text-white">{roadmapData.target_role}</h3>
            </div>
            <p className="text-xs text-gray-300 flex items-center gap-2 font-mono">
              <Clock className="w-3.5 h-3.5 text-indigo-400" />
              <span>Recommended Pace: <strong>{roadmapData.estimated_timeline}</strong></span>
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900 border border-emerald-500/30 text-right flex-shrink-0">
            <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">Target Market Comp</span>
            <div className="text-sm font-black text-emerald-400 font-mono mt-0.5">
              {roadmapData.average_salary}
            </div>
          </div>
        </div>
      )}

      {/* 4-Phase Roadmap Step Sequence */}
      {roadmapData && roadmapData.phases && (
        <div className="space-y-4">
          <h4 className="text-xs font-bold uppercase tracking-wider text-gray-400 flex items-center gap-2">
            <Compass className="w-4 h-4 text-cyan-400" />
            Sequential Learning Milestones
          </h4>

          <div className="space-y-4">
            {roadmapData.phases.map((phase, idx) => (
              <div 
                key={idx}
                className="glass-card p-6 space-y-3 border-l-4 border-l-indigo-500 hover:border-l-cyan-400 transition"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-white/5 pb-2.5">
                  <div className="flex items-center gap-2.5">
                    <span className="w-7 h-7 rounded-lg bg-indigo-600/30 text-indigo-300 flex items-center justify-center font-bold text-xs border border-indigo-500/30">
                      {phase.phase_number || idx + 1}
                    </span>
                    <h5 className="text-sm font-bold text-white">{phase.title}</h5>
                  </div>
                  <span className="text-xs text-cyan-300 font-mono font-semibold">
                    {phase.duration}
                  </span>
                </div>

                <p className="text-xs text-gray-300 leading-relaxed">
                  {phase.description}
                </p>

                {/* Skills Chips */}
                <div className="pt-1">
                  <span className="text-[10px] font-bold text-gray-400 uppercase tracking-tight block mb-1.5">
                    Key Competencies Mastered:
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {(phase.skills || []).map((sk, sIdx) => (
                      <span key={sIdx} className="px-2.5 py-1 rounded-lg bg-slate-900 border border-white/10 text-[11px] font-mono text-cyan-300">
                        {sk}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Milestone Capstone */}
                {phase.milestone_project && (
                  <div className="mt-2 p-3 rounded-xl bg-slate-900/80 border border-indigo-500/20 text-xs text-gray-300 flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                    <div>
                      <strong className="text-white">Milestone Capstone: </strong>
                      {phase.milestone_project}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
