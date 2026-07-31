import React, { useState, useEffect } from 'react';
import { Compass, Sparkles, CheckCircle2, BookOpen, Award, DollarSign, ArrowRight } from 'lucide-react';

export default function CareerRoadmapPage({ latestAnalysis }) {
  const [targetRole, setTargetRole] = useState('AI / Machine Learning Engineer');
  const [loading, setLoading] = useState(false);
  const [roadmapData, setRoadmapData] = useState(null);

  const fetchRoadmap = async (role) => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/career/roadmap', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          target_role: role || targetRole,
          resume_text: latestAnalysis?.parsed_sections ? Object.values(latestAnalysis.parsed_sections).join('\n') : ''
        })
      });
      const data = await response.json();
      setRoadmapData(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRoadmap(targetRole);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          Career & <span className="gradient-text">Learning Roadmap</span>
        </h2>
        <p className="text-xs text-gray-400">Personalized 4-Phase Step-by-Step Growth & Skill Gap Blueprint</p>
      </div>

      {/* Role Selection */}
      <div className="glass-card p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="space-y-1">
          <label className="text-xs font-bold text-gray-300 uppercase tracking-wider block">
            Select Target Career Role
          </label>
          <select 
            value={targetRole}
            onChange={(e) => {
              setTargetRole(e.target.value);
              fetchRoadmap(e.target.value);
            }}
            className="px-4 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white focus:outline-none focus:border-indigo-500 font-semibold cursor-pointer"
          >
            <option value="AI / Machine Learning Engineer">AI / Machine Learning Engineer</option>
            <option value="Full-Stack Web Developer">Full-Stack Web Developer</option>
            <option value="Backend Engineer">Backend Engineer</option>
            <option value="Data Scientist / Data Analyst">Data Scientist / Data Analyst</option>
            <option value="DevOps / Cloud Engineer">DevOps / Cloud Engineer</option>
          </select>
        </div>

        {roadmapData?.estimated_salary && (
          <div className="bg-indigo-950/60 p-4 rounded-2xl border border-indigo-500/30 flex items-center gap-4">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
              <DollarSign className="w-5 h-5" />
            </div>
            <div>
              <div className="text-[10px] uppercase font-bold text-gray-400">Estimated Salary Range</div>
              <div className="text-sm font-black text-emerald-300">{roadmapData.estimated_salary.range}</div>
              <div className="text-[10px] text-indigo-300">{roadmapData.estimated_salary.growth_projection}</div>
            </div>
          </div>
        )}
      </div>

      {/* Roadmap Step Timeline */}
      {roadmapData && (
        <div className="space-y-6">
          <div className="glass-card p-6 border-indigo-500/30">
            <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
              <Compass className="w-5 h-5 text-indigo-400" />
              Structured 4-Phase Learning Timeline for {roadmapData.target_role}
            </h3>

            <div className="space-y-6 relative before:absolute before:inset-0 before:left-5 before:w-0.5 before:bg-indigo-500/20">
              {roadmapData.roadmap.map((step) => (
                <div key={step.step} className="relative flex items-start gap-6 pl-2 group">
                  <div className="w-10 h-10 rounded-2xl bg-indigo-600 border border-indigo-400 text-white font-black text-sm flex items-center justify-center shrink-0 shadow-lg shadow-indigo-500/30 group-hover:scale-110 transition">
                    {step.step}
                  </div>

                  <div className="glass-card p-5 flex-1 space-y-3 border-white/5 group-hover:border-indigo-500/30 transition">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 border-b border-white/5 pb-2">
                      <h4 className="text-sm font-bold text-white">{step.title}</h4>
                      <span className="px-2.5 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-[10px] font-bold">
                        {step.duration}
                      </span>
                    </div>

                    <p className="text-xs text-gray-300 leading-relaxed">{step.focus}</p>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
                      <div className="bg-gray-900/60 p-3 rounded-xl border border-white/5 space-y-1">
                        <div className="text-[10px] font-bold text-cyan-400 uppercase flex items-center gap-1">
                          <BookOpen className="w-3 h-3" /> Recommended Project
                        </div>
                        <p className="text-xs font-semibold text-gray-200">{step.recommended_projects[0]}</p>
                      </div>

                      <div className="bg-gray-900/60 p-3 rounded-xl border border-white/5 space-y-1">
                        <div className="text-[10px] font-bold text-purple-400 uppercase flex items-center gap-1">
                          <Award className="w-3 h-3" /> Target Certification
                        </div>
                        <p className="text-xs font-semibold text-gray-200">{step.recommended_certifications[0]}</p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
