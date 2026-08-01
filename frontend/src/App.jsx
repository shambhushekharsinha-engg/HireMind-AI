import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import AuthLandingPage from './pages/AuthLandingPage';
import DashboardPage from './pages/DashboardPage';
import ATSAnalyzerPage from './pages/ATSAnalyzerPage';
import JobMatcherPage from './pages/JobMatcherPage';
import CareerRoadmapPage from './pages/CareerRoadmapPage';
import InterviewPrepPage from './pages/InterviewPrepPage';
import BulletRewriterPage from './pages/BulletRewriterPage';
import RecruiterPage from './pages/RecruiterPage';
import HistoryPage from './pages/HistoryPage';
import ResumeBuilderPage from './pages/ResumeBuilderPage';
import ApplicationTrackerPage from './pages/ApplicationTrackerPage';
import CoachPage from './pages/CoachPage';
import AnalyticsPage from './pages/AnalyticsPage';

import PortfolioGeneratorPage from './pages/PortfolioGeneratorPage';
import CoverLetterPage from './pages/CoverLetterPage';
import LinkedInOptimizerPage from './pages/LinkedInOptimizerPage';
import VersionComparePage from './pages/VersionComparePage';
import GitHubAnalyzerPage from './pages/GitHubAnalyzerPage';
import CompanyInsightsPage from './pages/CompanyInsightsPage';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [latestAnalysis, setLatestAnalysis] = useState(null);
  const [user, setUser] = useState(null);

  useEffect(() => {
    try {
      const savedUser = localStorage.getItem('hiremind_user');
      if (savedUser) {
        setUser(JSON.parse(savedUser));
      }
    } catch (e) {
      console.error("Failed to load saved user session:", e);
    }
  }, []);

  const handleAnalysisComplete = (data) => {
    setLatestAnalysis(data);
  };

  const handleLoginSuccess = (userData) => {
    setUser(userData);
  };

  // Auth Protection Gate: Display Auth Landing Page if not signed in
  if (!user) {
    return <AuthLandingPage onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="min-h-screen bg-[#0b0f19] text-gray-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* Top Navbar */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} user={user} setUser={setUser} />

      {/* Main Layout Container */}
      <div className="flex flex-1">
        {/* Left Sidebar */}
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

        {/* Main Content Area */}
        <main className="flex-1 p-6 md:p-8 overflow-y-auto max-w-7xl mx-auto w-full">
          {activeTab === 'dashboard' && (
            <DashboardPage setActiveTab={setActiveTab} latestAnalysis={latestAnalysis} />
          )}

          {activeTab === 'builder' && (
            <ResumeBuilderPage />
          )}

          {activeTab === 'ats' && (
            <ATSAnalyzerPage 
              onAnalysisComplete={handleAnalysisComplete} 
              analysisData={latestAnalysis} 
              setAnalysisData={setLatestAnalysis} 
            />
          )}

          {activeTab === 'job-matcher' && (
            <JobMatcherPage latestAnalysis={latestAnalysis} />
          )}

          {activeTab === 'tracker' && (
            <ApplicationTrackerPage />
          )}

          {activeTab === 'portfolio' && (
            <PortfolioGeneratorPage latestAnalysis={latestAnalysis} />
          )}

          {activeTab === 'cover-letter' && (
            <CoverLetterPage latestAnalysis={latestAnalysis} />
          )}

          {activeTab === 'linkedin' && (
            <LinkedInOptimizerPage />
          )}

          {activeTab === 'version-compare' && (
            <VersionComparePage />
          )}

          {activeTab === 'github' && (
            <GitHubAnalyzerPage />
          )}

          {activeTab === 'company' && (
            <CompanyInsightsPage />
          )}

          {activeTab === 'coach' && (
            <CoachPage />
          )}

          {activeTab === 'roadmap' && (
            <CareerRoadmapPage latestAnalysis={latestAnalysis} />
          )}

          {activeTab === 'interview' && (
            <InterviewPrepPage latestAnalysis={latestAnalysis} />
          )}

          {activeTab === 'rewriter' && (
            <BulletRewriterPage />
          )}

          {activeTab === 'recruiter' && (
            <RecruiterPage />
          )}

          {activeTab === 'analytics' && (
            <AnalyticsPage />
          )}

          {activeTab === 'history' && (
            <HistoryPage />
          )}
        </main>
      </div>
    </div>
  );
}