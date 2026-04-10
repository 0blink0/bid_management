"""
Pytest配置和共享fixture
"""
import pytest
import sys
import os
from typing import Generator

# 添加项目根目录到path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import get_settings
from app.tools.llm import LLMManager, LLMConfig, LLMProvider, LLMModel


@pytest.fixture(scope="session")
def settings():
    """获取配置"""
    return get_settings()


@pytest.fixture(scope="session")
def llm_manager(settings) -> LLMManager:
    """LLM管理器（使用测试配置）"""
    manager = LLMManager()

    # 添加阿里云API（测试用）
    if settings.llm.ali_qwen:
        config = LLMConfig(
            provider=LLMProvider.ALI_QWEN,
            model=LLMModel[settings.llm.ali_qwen.model.upper().replace("-", "_")],
            api_key=settings.llm.ali_qwen.api_key or "test-key",
            max_tokens=settings.llm.ali_qwen.max_tokens,
            temperature=settings.llm.ali_qwen.temperature,
            timeout=settings.llm.ali_qwen.timeout
        )
        manager.add_llm("ali_qwen", config)
        manager.set_default("ali_qwen")

    return manager


@pytest.fixture
def mock_llm_response():
    """Mock LLM响应"""
    from unittest.mock import AsyncMock, patch

    async def mock_chat(messages, **kwargs):
        return "这是Mock LLM的响应"

    async def mock_embeddings(texts):
        return [[0.1, 0.2, 0.3] for _ in texts]

    return mock_chat, mock_embeddings


@pytest.fixture
def sample_text():
    """示例文本"""
    return """
    招标项目名称：智慧城市数据中心建设项目
    招标编号：ZB-2024-001
    招标单位：某市政府信息中心

    一、资格要求
    1. 具有独立法人资格的企业
    2. 注册资金不低于5000万元
    3. 具有ISO27001信息安全管理体系认证
    4. 近三年内完成过类似项目不少于3个

    二、技术要求
    1. 采用云计算架构，支持弹性扩展
    2. 数据中心等级不低于Tier 3
    3. 支持国产密码算法

    三、商务要求
    1. 工期：12个月
    2. 质保期：不少于3年
    3. 付款方式：按进度付款
    """


@pytest.fixture
def sample_bid_text():
    """示例投标文件"""
    return """
    投标单位：XX科技有限公司
    投标日期：2024-03-15

    一、公司概况
    我司成立于2010年，注册资本6000万元，具有ISO27001认证。

    二、项目响应
    1. 完全响应招标文件的资格要求
    2. 技术方案采用云计算架构，支持弹性扩展
    3. 数据中心等级达到Tier 3标准
    4. 支持国产密码算法

    三、项目团队
    项目经理：张三，高级工程师，PMP认证
    技术负责人：李四，15年行业经验

    四、报价
    总报价：5800万元
    """
