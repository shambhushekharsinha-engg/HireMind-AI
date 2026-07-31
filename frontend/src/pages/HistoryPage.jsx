import React, { useState, useEffect } from 'react';
import { History, FileText, Download, Award, Calendar } from 'lucide-react';

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/resumes/history');
      const data = await response.json();
      setHistory(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          Resume History & <span className="gradient-text">Saved Reports</span>
        </h2>
        <p className="text-xs text-gray-400">View past analysis evaluations and download PDF executive reports</p>
      </div>

      <div className="glass-card overflow-hidden">
        <div className="p-4 border-b border-white/10 flex items-center justify-between">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <History className="w-4 h-4 text-cyan-400" />
            Evaluation Log ({history.length})
          </h3>
        </div>

        <div className="divide-y divide-white/5">
          {history.length > 0 ? (
            history.map((item) => (
              <div key={item.analysis_id} className="p-4 flex items-center justify-between gap-4 hover:bg-white/5 transition">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
                    <FileText className="w-5 h-5" />
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-white">{item.filename}</h4>
                    <p className="text-[11px] text-gray-400 flex items-center gap-2 mt-0.5">
                      <span className="flex items-center gap-1"><Calendar className="w-3 h-3 text-gray-500" /> {item.created_at}</span>
                      <span>•</span>
                      <span className="text-indigo-300 font-semibold">{item.rating}</span>
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <span className="text-xs text-gray-400 block">ATS Score</span>
                    <span className="text-lg font-black text-emerald-400">{item.ats_score} / 100</span>
                  </div>

                  <button
                    onClick={() => window.open(`http://127.0.0.1:8000/api/v1/reports/download/${item.analysis_id}`, '_blank')}
                    className="glow-btn px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-1.5"
                  >
                    <Download className="w-3.5 h-3.5" /> PDF Report
                  </button>
                </div>
              </div>
            ))
          ) : (
            <div className="p-8 text-center text-xs text-gray-500">
              No historical resume analyses stored yet. Upload a resume to create your first evaluation record.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
