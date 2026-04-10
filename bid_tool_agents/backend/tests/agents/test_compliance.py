"""
合规审查Agent测试
"""
import pytest
from unittest.mock import AsyncMock, patch


class TestComplianceAgent:
    """合规审查Agent测试"""

    @pytest.fixture
    def agent(self):
        """创建Agent实例"""
        from app.agents.compliance.agent import ComplianceAgent
        return ComplianceAgent()

    @pytest.fixture
    def agent_memory(self):
        """创建独立的记忆实例"""
        from app.agents.base.memory import AgentMemory
        return AgentMemory(agent_id="compliance")

    def test_agent_initialization(self, agent):
        """测试Agent初始化"""
        assert agent.agent_id == "compliance"
        assert agent.name == "合规审查Agent"
        assert agent.memory is not None

    @pytest.mark.asyncio
    async def test_compliance_check(self, agent, sample_text):
        """测试合规性检查"""
        with patch.object(
            agent.llm,
            'chat',
            return_value='{"issues": [{"type": "错敏词", "location": "第3行", "content": "xxx"}]}'
        ):
            result = await agent.process({
                "content": sample_text,
                "check_type": "full"
            })
            assert result is not None

    @pytest.mark.asyncio
    async def test_law_retrieval(self, agent):
        """测试法律检索"""
        with patch.object(
            agent.llm,
            'chat',
            return_value="相关法律条文..."
        ):
            result = await agent.process({
                "content": "资质要求是否合规",
                "check_type": "law_retrieval"
            })
            assert result is not None

    def test_memory_layers(self, agent_memory):
        """测试记忆层级"""
        # 瞬时记忆
        agent_memory.immediate.store("key1", "raw_input")
        assert agent_memory.immediate.get("key1") is not None

        # 短期记忆
        agent_memory.short_term.store_task_context("task1", {"test": "data"})
        assert agent_memory.short_term.get_task_context("task1") is not None

        # 长期记忆
        exp_id = agent_memory.long_term.add_experience(
            {"task": "test", "result": "success"},
            importance=2
        )
        assert exp_id is not None

        # 核心记忆
        agent_memory.core.set_profile(
            identity="合规审查Agent",
            capabilities=["法律检索", "合规判断"],
            boundaries=["不做文件比对"]
        )
        profile = agent_memory.core.get_profile()
        assert profile["identity"] == "合规审查Agent"
