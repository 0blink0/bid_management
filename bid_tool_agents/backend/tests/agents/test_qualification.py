"""
资质核验Agent测试
"""
import pytest


class TestQualificationAgent:
    """资质核验Agent测试"""

    @pytest.fixture
    def agent(self):
        from app.agents.qualification.agent import QualificationAgent
        return QualificationAgent()

    def test_agent_initialization(self, agent):
        assert agent.agent_id == "qualification"
        assert agent.name == "资质核验Agent"
