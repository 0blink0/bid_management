"""
辅助评标Agent测试
"""
import pytest


class TestEvaluationAgent:
    """辅助评标Agent测试"""

    @pytest.fixture
    def agent(self):
        from app.agents.evaluation.agent import EvaluationAgent
        return EvaluationAgent()

    def test_agent_initialization(self, agent):
        assert agent.agent_id == "evaluation"
        assert agent.name == "辅助评标Agent"
