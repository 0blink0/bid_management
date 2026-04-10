"""
档案管理Agent测试
"""
import pytest


class TestArchiveAgent:
    """档案管理Agent测试"""

    @pytest.fixture
    def agent(self):
        from app.agents.archive.agent import ArchiveAgent
        return ArchiveAgent()

    def test_agent_initialization(self, agent):
        assert agent.agent_id == "archive"
        assert agent.name == "档案管理Agent"
