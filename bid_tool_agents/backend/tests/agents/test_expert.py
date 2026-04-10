"""
专家抽取Agent测试
"""
import pytest


class TestExpertAgent:
    """专家抽取Agent测试"""

    @pytest.fixture
    def agent(self):
        from app.agents.expert.agent import ExpertAgent
        return ExpertAgent()

    def test_agent_initialization(self, agent):
        assert agent.agent_id == "expert"
        assert agent.name == "专家抽取Agent"
