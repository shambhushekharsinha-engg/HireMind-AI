import React, { useState, useEffect } from 'react';
import { MessageSquareCode, Sparkles, CheckCircle2, AlertTriangle, RefreshCw, Send } from 'lucide-react';

export default function InterviewPrepPage({ latestAnalysis }) {
  const [targetRole, setTargetRole] = useState('Full-Stack Web Developer');
  const [questions, setQuestions] = useState([]);
  const [activeQIndex, setActiveQIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState('');
  const [evaluating, setEvaluating] = useState(false);
  const [evalResult, setEvalResult] = useState(null);

  const fetchQuestions = async (role) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/interview/questions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          target_role: role || targetRole,
          resume_text: latestAnalysis?.parsed_sections ? Object.values(latestAnalysis.parsed_sections).join('\n') : ''
        })
      });
      const data = await response.json();
      setQuestions(data.questions || []);
      setActiveQIndex(0);
      setUserAnswer('');
      setEvalResult(null);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchQuestions(targetRole);
  }, []);

  const handleEvaluateAnswer = async () => {
    if (!userAnswer.trim()) {
      alert('Please type or dictate your answer before evaluating.');
      return;
    }

    const currentQ = questions[activeQIndex];
    setEvaluating(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/interview/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: currentQ.question,
          user_answer: userAnswer,
          expected_points: currentQ.key_points_expected || []
        })
      });
      const data = await response.json();
      setEvalResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setEvaluating(false);
    }
  };

  const currentQ = questions[activeQIndex];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            Interview Prep <span className="gradient-text">AI Workshop</span>
          </h2>
          <p className="text-xs text-gray-400">Domain-tailored technical & behavioral interview practice</p>
        </div>

        <select 
          value={targetRole}
          onChange={(e) => {
            setTargetRole(e.target.value);
            fetchQuestions(e.target.value);
          }}
          className="px-4 py-2 rounded-xl bg-gray-900 border border-white/10 text-xs text-white focus:outline-none focus:border-indigo-500 font-semibold cursor-pointer"
        >
          <option value="Full-Stack Web Developer">Full-Stack Web Developer</option>
          <option value="AI / Machine Learning Engineer">AI / Machine Learning Engineer</option>
        </select>
      </div>

      {questions.length > 0 && currentQ && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Question List Sidebar */}
          <div className="space-y-2">
            <h4 className="text-xs font-bold uppercase text-gray-400 px-1">Questions List ({questions.length})</h4>
            {questions.map((q, idx) => (
              <button
                key={q.id}
                onClick={() => {
                  setActiveQIndex(idx);
                  setUserAnswer('');
                  setEvalResult(null);
                }}
                className={`w-full text-left p-3.5 rounded-xl border text-xs font-medium transition ${
                  activeQIndex === idx
                    ? 'bg-indigo-600/90 text-white border-indigo-400 shadow-md'
                    : 'glass-card text-gray-300 hover:bg-white/5 border-white/5'
                }`}
              >
                <div className="flex items-center justify-between gap-2 mb-1">
                  <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-black/30">
                    {q.category}
                  </span>
                  <span className="text-[10px] opacity-75">Q{idx + 1}</span>
                </div>
                <div className="line-clamp-2">{q.question}</div>
              </button>
            ))}
          </div>

          {/* Active Question Workspace */}
          <div className="md:col-span-2 space-y-6">
            <div className="glass-card p-6 space-y-4 border-indigo-500/30">
              <div className="flex items-center justify-between">
                <span className="px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-bold">
                  {currentQ.category} Question
                </span>
                <span className="text-xs text-gray-400 font-medium">Question {activeQIndex + 1} of {questions.length}</span>
              </div>

              <h3 className="text-lg font-bold text-white leading-relaxed">{currentQ.question}</h3>

              {currentQ.hints && (
                <div className="bg-gray-900/60 p-3 rounded-xl border border-white/5 text-xs text-gray-400 space-y-1">
                  <span className="font-bold text-amber-400">Hint / Approach:</span> {currentQ.hints[0]}
                </div>
              )}

              <div className="space-y-2">
                <label className="text-xs font-bold text-gray-300 uppercase tracking-wider block">
                  Your Response
                </label>
                <textarea
                  rows="6"
                  placeholder="Type your structured answer here. Include technical concepts, metrics, or personal project context..."
                  value={userAnswer}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  className="w-full p-3 rounded-xl bg-gray-900/80 border border-white/10 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 resize-none font-sans"
                />
              </div>

              <div className="flex justify-end">
                <button
                  onClick={handleEvaluateAnswer}
                  disabled={evaluating}
                  className="glow-btn px-6 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 disabled:opacity-50"
                >
                  {evaluating ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin" />
                      Evaluating Rubric...
                    </>
                  ) : (
                    <>
                      <Send className="w-4 h-4" />
                      Submit & Evaluate Answer
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Answer Feedback Result */}
            {evalResult && (
              <div className="glass-card p-6 space-y-4 border-cyan-500/30 animate-fade-in">
                <div className="flex items-center justify-between border-b border-white/10 pb-3">
                  <div>
                    <span className="text-xs text-gray-400">Answer Score</span>
                    <div className="text-2xl font-black text-white">{evalResult.score} / 100</div>
                  </div>
                  <div className="text-right">
                    <span className="text-xs text-indigo-300 font-semibold">{evalResult.feedback}</span>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="bg-emerald-950/40 p-4 rounded-xl border border-emerald-500/20 space-y-2">
                    <h5 className="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4" /> Strong Points Identified
                    </h5>
                    <ul className="space-y-1">
                      {evalResult.strengths.map((str, i) => (
                        <li key={i} className="text-xs text-gray-300">• {str}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="bg-amber-950/40 p-4 rounded-xl border border-amber-500/20 space-y-2">
                    <h5 className="text-xs font-bold text-amber-400 flex items-center gap-1.5">
                      <AlertTriangle className="w-4 h-4" /> Key Concept Improvements
                    </h5>
                    <ul className="space-y-1">
                      {evalResult.improvements.map((imp, i) => (
                        <li key={i} className="text-xs text-gray-300">• {imp}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
