"""
LLM抽象基类
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncIterator
from .types import LLMConfig, ChatMessage


class BaseLLM(ABC):
    """
    LLM抽象基类

    定义LLM的统一接口
    """

    def __init__(self, config: LLMConfig):
        self.config = config

    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> str:
        """
        同步聊天

        Args:
            messages: 消息列表 [{"role": "user", "content": "..."}]

        Returns:
            助手回复内容
        """
        pass

    @abstractmethod
    async def chat_stream(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> AsyncIterator[str]:
        """
        流式聊天

        Args:
            messages: 消息列表

        Yields:
            增量回复内容
        """
        pass

    @abstractmethod
    async def embeddings(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """
        获取文本嵌入

        Args:
            texts: 文本列表

        Returns:
            嵌入向量列表
        """
        pass

    @abstractmethod
    def get_token_count(self, text: str) -> int:
        """
        获取token数量

        Args:
            text: 文本

        Returns:
            token数量
        """
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """模型名称"""
        pass

    def supports_function_call(self) -> bool:
        """是否支持函数调用"""
        return False

    def supports_vision(self) -> bool:
        """是否支持视觉"""
        return False

    async def close(self) -> None:
        """关闭连接"""
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(model={self.model_name})>"
