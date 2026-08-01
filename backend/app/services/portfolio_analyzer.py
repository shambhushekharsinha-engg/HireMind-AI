from typing import Dict, Any, List

class GitHubAnalyzer:
    @staticmethod
    def analyze(username: str = "demo_dev") -> Dict[str, Any]:
        return {
            "public_repos": 12,
            "stars_count": 48,
            "top_languages": ["Python", "JavaScript", "Dockerfile"],
            "score": 85.0
        }

class LinkedInAnalyzer:
    @staticmethod
    def analyze(profile_url: str = "linkedin.com/in/demodev") -> Dict[str, Any]:
        return {
            "connections_count": "500+",
            "endorsements": ["FastAPI", "Docker", "Machine Learning"],
            "score": 80.0
        }

class ResumeAnalyzerSignal:
    @staticmethod
    def analyze(skills: List[str] = None) -> Dict[str, Any]:
        count = len(skills or ["Python", "FastAPI"])
        return {"skill_count": count, "score": min(100.0, count * 10.0)}

class ProjectAnalyzer:
    @staticmethod
    def analyze(projects: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {"quantified_projects_count": 3, "score": 88.0}

class ModularPortfolioAnalyzer:
    """
    Modular Portfolio Analyzer composing signals from:
    GitHub Analyzer + LinkedIn Analyzer + Resume Analyzer + Project Analyzer -> Overall Candidate Score.
    """
    def analyze_candidate_portfolio(
        self,
        github_username: str = "demo_dev",
        linkedin_url: str = "linkedin.com/in/demodev",
        skills: List[str] = None
    ) -> Dict[str, Any]:
        gh_data = GitHubAnalyzer.analyze(github_username)
        li_data = LinkedInAnalyzer.analyze(linkedin_url)
        res_data = ResumeAnalyzerSignal.analyze(skills)
        proj_data = ProjectAnalyzer.analyze()

        overall_score = round(
            (gh_data["score"] * 0.35) +
            (li_data["score"] * 0.25) +
            (res_data["score"] * 0.20) +
            (proj_data["score"] * 0.20),
            1
        )

        return {
            "overall_candidate_score": overall_score,
            "tier": "Top-Tier Candidate" if overall_score >= 80 else "Competitive Candidate",
            "modules": {
                "github_analyzer": gh_data,
                "linkedin_analyzer": li_data,
                "resume_analyzer": res_data,
                "project_analyzer": proj_data
            }
        }

portfolio_analyzer = ModularPortfolioAnalyzer()
