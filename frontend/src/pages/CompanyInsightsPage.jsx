import React, { useState, useEffect } from 'react';
import { Building2, Sparkles, CheckCircle2, DollarSign, Award, ArrowRight } from 'lucide-react';
import { API_BASE_URL } from '../config';

export default function CompanyInsightsPage() {
  const [targetCompany, setTargetCompany] = useState('microsoft');
  const [loading, setLoading] = useState(false);
  const [blueprint, setBlueprint] = useState(null);

  const fetchBlueprint = async (companyStr) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/v2/ai/company-blueprint`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_company: companyStr || targetCompany })
      });
      const data = await response.json();
      setBlueprint(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBlueprint(targetCompany);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            Target Company <span className="gradient-text">Blueprint</span>
          </h2>
          <p className="text-xs text-gray-400">Pre-application hiring insights, expected skills, and interview rounds</p>
        </div>

        <select
          value={targetCompany}
          onChange={(e) => {
            setTargetCompany(e.target.value);
            fetchBlueprint(e.target.value);
          }}
          className="px-4 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white focus:outline-none focus:border-indigo-500 font-semibold cursor-pointer"
        >
          <option value="microsoft">Microsoft SDE</option>
          <option value="google">Google SWE</option>
          <option value="amazon">Amazon SDE</option>
        </select>
      </div>

      {blueprint && (
        <div className="space-y-6 animate-fade-in">
          <div className="glass-card p-6 border-indigo-500/30 flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="space-y-1 text-center md:text-left">
              <span className="px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-bold border border-indigo-500/30">
                {blueprint.company_name} — {blueprint.role}
              </span>
              <h3 className="text-2xl font-black text-white pt-1">
                Interview Difficulty: <span className="text-amber-400">{blueprint.interview_difficulty}</span>
              </h3>
              <p className="text-xs text-gray-400">{blueprint.hiring_trends}</p>
            </div>

            <div className="bg-indigo-950/60 p-4 rounded-2xl border border-indigo-500/30 flex items-center gap-4">
              <DollarSign className="w-8 h-8 text-emerald-400" />
              <div>
                <span className="text-[10px] uppercase font-bold text-gray-400">Target Salary Range</span>
                <div className="text-base font-black text-emerald-300">{blueprint.salary_range}</div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass-card p-6 space-y-3 border-cyan-500/20">
              <h4 className="text-xs font-bold uppercase text-cyan-400 flex items-center gap-2">
                <Award className="w-4 h-4" /> Core Expected Tech Stack Skills
              </h4>
              <div className="flex flex-wrap gap-2">
                {blueprint.expected_skills.map((s, i) => (
                  <span key={i} className="px-3 py-1.5 rounded-xl bg-cyan-950/60 border border-cyan-500/30 text-cyan-300 text-xs font-semibold uppercase">
                    {s}
                  </span>
                ))}
              </div>
            </div>

            <div className="glass-card p-6 space-y-3 border-purple-500/20">
              <h4 className="text-xs font-bold uppercase text-purple-400 flex items-center gap-2">
                <Building2 className="w-4 h-4" /> Interview Rounds & Structure
              </h4>
              <div className="space-y-2">
                {blueprint.interview_rounds.map((r, i) => (
                  <div key={i} className="p-3 bg-gray-900/60 rounded-xl border border-white/5 text-xs text-gray-200 font-medium flex items-start gap-2">
                    <ArrowRight className="w-3.5 h-3.5 text-purple-400 shrink-0 mt-0.5" /> {r}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
