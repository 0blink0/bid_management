"""
统计分析Agent测试
"""
import pytest


class TestStatisticsAgent:
    """统计分析Agent测试"""

    @pytest.fixture
    def agent(self):
        from app.agents.statistics.agent import StatisticsAgent
        return StatisticsAgent()

    def test_agent_initialization(self, agent):
        assert agent.agent_id == "statistics"
        assert agent.name == "统计分析Agent"
