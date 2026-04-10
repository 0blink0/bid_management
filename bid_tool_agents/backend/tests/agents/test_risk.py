"""
风险识别Agent测试
"""
import pytest
from unittest.mock import AsyncMock, patch


class TestRiskAgent:
    """风险识别Agent测试"""

    @pytest.fixture
    def agent(self):
        """创建Agent实例"""
        from app.agents.risk.agent import RiskAgent
        return RiskAgent()

    def test_agent_initialization(self, agent):
        """测试Agent初始化"""
        assert agent.agent_id == "risk"
        assert agent.name == "风险识别Agent"

    @pytest.mark.asyncio
    async def test_similarity_analysis(self, agent):
        """测试相似度分析"""
        with patch.object(
            agent.llm,
            'chat',
            return_value='{"similarity": 0.85, "similar_paragraphs": []}'
        ):
            result = await agent.process({
                "type": "similarity",
                "documents": ["文本1", "文本2"]
            })
            assert result is not None

    @pytest.mark.asyncio
    async def test_risk_detection(self, agent, sample_text):
        """测试风险检测"""
        with patch.object(
            agent.llm,
            'chat',
            return_value='{"risks": [{"level": "high", "type": "串标嫌疑"}]}'
        ):
            result = await agent.process({
                "content": sample_text,
                "type": "risk_detection"
            })
            assert result is not None

    @pytest.mark.asyncio
    async def test_contact_analysis(self, agent):
        """测试联系方式分析"""
        result = await agent.process({
            "type": "contact_analysis",
            "documents": [
                {"name": "公司A", "phone": "13800138000"},
                {"name": "公司B", "phone": "13800138000"}
            ]
        })
        assert result is not None
