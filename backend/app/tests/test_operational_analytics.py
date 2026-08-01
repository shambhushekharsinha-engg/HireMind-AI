import pytest
from app.services.analytics_service import analytics_service

def test_operational_analytics():
    analytics_service.record_feature_usage("ResumeRewrite")
    analytics_service.record_feature_usage("InterviewSimulator")
    analytics_service.record_report_download()

    summary = analytics_service.get_metrics_summary()
    assert summary["total_resume_analyses"] > 0
    assert summary["rewrite_recommendation_acceptance_rate_pct"] > 0.0
    assert summary["feature_usage_breakdown"]["ResumeRewrite"] > 0
