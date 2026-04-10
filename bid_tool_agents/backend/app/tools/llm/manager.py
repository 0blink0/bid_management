"""
LLM管理器 - 统一管理LLM实例
"""
from typing import Optional, Dict, List
from .base import BaseLLM
from .types import LLMConfig, LLMProvider
from .registry import LLMRegistry

# 注册实现
from .api.qwen import AliQwenLLM
from .private.qwen_private import PrivateQwenLLM
from .private.deepseek import PrivateDeepSeekLLM

# 注册LLM实现
LLMRegistry.register(LLMProvider.ALI_QWEN, AliQwenLLM)
LLMRegistry.register(LLMProvider.PRIVATE_QWEN, PrivateQwenLLM)
LLMRegistry.register(LLMProvider.PRIVATE_DEEPSEEK, PrivateDeepSeekLLM)


class LLMManager:
    """
    LLM管理器

    功能:
    - 管理多个LLM实例
    - 支持默认LLM设置
    - 支持LLM路由（按条件选择）
    - 支持热切换
    """

    def __init__(self):
        self._instances: Dict[str, BaseLLM] = {}
        self._default: Optional[str] = None
        self._routing_enabled = False
        self._routing_rules: List[Dict] = []

    def add_llm(self, name: str, config: LLMConfig) -> None:
        """
        添加LLM实例

        Args:
            name: 实例名称
            config: LLM配置
        """
        instance = LLMRegistry.get(config)
        self._instances[name] = instance
        if self._default is None:
            self._default = name

    def set_default(self, name: str) -> None:
        """设置默认LLM"""
        if name not in self._instances:
            raise ValueError(f"LLM instance '{name}' not found")
        self._default = name

    def get_llm(self, name: Optional[str] = None) -> BaseLLM:
        """获取LLM实例"""
        if name is None:
            name = self._default
        if name not in self._instances:
            raise ValueError(f"LLM instance '{name}' not found")
        return self._instances[name]

    def remove_llm(self, name: str) -> None:
        """移除LLM实例"""
        if name in self._instances:
            del self._instances[name]
        if self._default == name:
            self._default = list(self._instances.keys())[0] if self._instances else None

    def list_llms(self) -> List[str]:
        """列出所有LLM实例"""
        return list(self._instances.keys())

    def get_default_name(self) -> Optional[str]:
        """获取默认LLM名称"""
        return self._default

    # ==================== 路由功能 ====================

    def enable_routing(self) -> None:
        """启用LLM路由"""
        self._routing_enabled = True

    def disable_routing(self) -> None:
        """禁用LLM路由"""
        self._routing_enabled = False

    def add_routing_rule(
        self,
        condition: callable,
        target: str,
        priority: int = 0
    ) -> None:
        """
        添加路由规则

        Args:
            condition: 条件函数，接受context参数
            target: 目标LLM名称
            priority: 优先级
        """
        self._routing_rules.append({
            "condition": condition,
            "target": target,
            "priority": priority
        })
        # 按优先级排序
        self._routing_rules.sort(key=lambda x: x.get("priority", 0), reverse=True)

    def route(self, context: Dict) -> BaseLLM:
        """
        根据上下文路由到合适的LLM

        Args:
            context: 上下文信息 {"task_type": "...", ...}

        Returns:
            选中的LLM实例
        """
        if not self._routing_enabled or not self._routing_rules:
            return self.get_llm()

        for rule in self._routing_rules:
            if rule["condition"](context):
                target = rule["target"]
                if target in self._instances:
                    return self._instances[target]

        return self.get_llm()

    # ==================== 便捷调用 ====================

    async def chat(
        self,
        messages: List[Dict[str, str]],
        llm_name: Optional[str] = None,
        **kwargs
    ) -> str:
        """聊天"""
        llm = self.get_llm(llm_name)
        return await llm.chat(messages, **kwargs)

    async def chat_stream(
        self,
        messages: List[Dict[str, str]],
        llm_name: Optional[str] = None,
        **kwargs
    ):
        """流式聊天"""
        llm = self.get_llm(llm_name)
        return await llm.chat_stream(messages, **kwargs)

    async def embeddings(
        self,
        texts: List[str],
        llm_name: Optional[str] = None
    ) -> List[List[float]]:
        """获取嵌入"""
        llm = self.get_llm(llm_name)
        return await llm.embeddings(texts)

    def __repr__(self) -> str:
        return f"<LLMManager(default={self._default}, instances={len(self._instances)})>"
