"""
文档解析Agent测试
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock


class TestParserAgent:
    """文档解析Agent测试"""

    @pytest.fixture
    def agent(self):
        """创建Agent实例"""
        from app.agents.parser.agent import ParserAgent
        return ParserAgent()

    def test_agent_initialization(self, agent):
        """测试Agent初始化"""
        assert agent.agent_id == "parser"
        assert agent.name == "文档解析Agent"
        assert agent.memory is not None

    @pytest.mark.asyncio
    async def test_parse_pdf(self, agent, sample_text):
        """测试PDF解析"""
        # 模拟LLM响应
        with patch.object(
            agent.llm,
            'chat',
            return_value="解析后的结构化文本"
        ):
            result = await agent.process({
                "type": "pdf",
                "content": sample_text
            })
            assert result is not None

    @pytest.mark.asyncio
    async def test_parse_docx(self, agent, sample_text):
        """测试Word解析"""
        with patch.object(
            agent.llm,
            'chat',
            return_value="解析后的Word内容"
        ):
            result = await agent.process({
                "type": "docx",
                "content": sample_text
            })
            assert result is not None

    @pytest.mark.asyncio
    async def test_ocr_recognize(self, agent):
        """测试OCR识别"""
        with patch.object(
            agent.llm,
            'chat',
            return_value="识别出的文字"
        ):
            result = await agent.process({
                "type": "image",
                "content": "base64_encoded_image"
            })
            assert result is not None

    @pytest.mark.asyncio
    async def test_memory_integration(self, agent, sample_text):
        """测试记忆整合"""
        task_id = "test_task_001"

        # 处理输入
        await agent.invoke(
            {"type": "pdf", "content": sample_text},
            task_id=task_id
        )

        # 验证瞬时记忆
        immediate = agent.memory.immediate.get(f"parser:{task_id}")
        assert immediate is not None

        # 验证短期记忆
        context = agent.memory.short_term.get_task_context(task_id)
        assert context is not None


class TestParserAgentMemory:
    """文档解析Agent记忆测试"""

    def test_immediate_memory(self):
        """测试瞬时记忆"""
        from app.agents.base.memory import ImmediateMemory

        memory = ImmediateMemory(agent_id="parser", ttl=60)

        memory.store(
            key="test_key",
            raw_input="原始输入",
            llm_output="LLM输出",
            sensory_data={"ocr": "result"}
        )

        result = memory.get("test_key")
        assert result is not None
        assert result["raw_input"] == "原始输入"
        assert result["llm_raw_output"] == "LLM输出"

    def test_short_term_memory(self):
        """测试短期记忆"""
        from app.agents.base.memory import ShortTermMemory, TaskStatus

        memory = ShortTermMemory(agent_id="parser")

        memory.store_task_context(
            task_id="task_001",
            context={"file": "test.pdf", "pages": 10},
            status=TaskStatus.RUNNING
        )

        context = memory.get_task_context("task_001")
        assert context is not None
        assert context["context"]["file"] == "test.pdf"
        assert context["status"] == "running"
