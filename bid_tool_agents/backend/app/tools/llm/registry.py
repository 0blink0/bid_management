"""
LLM注册表
"""
from typing import Dict, Type, Optional
from .base import BaseLLM
from .types import LLMProvider, LLMConfig


class LLMRegistry:
    """
    LLM实现注册表

    用于注册和获取不同的LLM实现
    """

    _registry: Dict[LLMProvider, Type[BaseLLM]] = {}

    @classmethod
    def register(cls, provider: LLMProvider, llm_class: Type[BaseLLM]) -> None:
        """
        注册LLM实现

        Args:
            provider: 提供者类型
            llm_class: LLM类
        """
        cls._registry[provider] = llm_class

    @classmethod
    def get(cls, config: LLMConfig) -> BaseLLM:
        """
        获取LLM实例

        Args:
            config: LLM配置

        Returns:
            LLM实例
        """
        provider = config.provider
        if provider not in cls._registry:
            raise ValueError(f"Unknown LLM provider: {provider}. Available: {list(cls._registry.keys())}")
        return cls._registry[provider](config)

    @classmethod
    def list_providers(cls) -> List[LLMProvider]:
        """列出所有已注册的提供者"""
        return list(cls._registry.keys())

    @classmethod
    def is_registered(cls, provider: LLMProvider) -> bool:
        """检查提供者是否已注册"""
        return provider in cls._registry


# 需要导入List
from typing import List
