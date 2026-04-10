"""
比对分析Agent测试
"""
import pytest


class TestComparisonAgent:
    """比对分析Agent测试"""

    @pytest.fixture
    def agent(self):
        from app.agents.comparison.agent import ComparisonAgent
        return ComparisonAgent()

    def test_agent_initialization(self, agent):
        assert agent.agent_id == "comparison"
        assert agent.name == "比对分析Agent"
