"""
Agent抽象基类
所有Agent继承此类
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from langgraph.graph import StateGraph
from .memory import AgentMemory


class BaseAgent(ABC):
    """
    Agent抽象基类

    职责:
    - 定义Agent的统一接口
    - 管理Agent的生命周期
    - 整合四层记忆机制
    """

    def __init__(self, agent_id: str, name: str, description: str = ""):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.memory = AgentMemory(agent_id)
        self.graph: Optional[StateGraph] = None
        self._is_initialized = False

    @abstractmethod
    def _build_graph(self) -> StateGraph:
        """
        构建LangGraph
        子类必须实现此方法
        """
        pass

    @abstractmethod
    async def process(self, input_data: Any) -> Dict[str, Any]:
        """
        处理输入
        子类必须实现此方法
        """
        pass

    def initialize(self) -> None:
        """初始化Agent"""
        if not self._is_initialized:
            self.graph = self._build_graph()
            self._is_initialized = True

    async def invoke(self, input_data: Any, **kwargs) -> Dict[str, Any]:
        """调用Agent"""
        if not self._is_initialized:
            self.initialize()

        # 存入瞬时记忆
        task_id = kwargs.get("task_id", "default")
        self.memory.immediate.store(
            key=f"{self.agent_id}:{task_id}",
            raw_input=str(input_data)
        )

        # 处理输入
        result = await self.process(input_data)

        # 更新短期记忆
        self.memory.short_term.update_agent_state({
            "last_task_id": task_id,
            "last_result": result
        })

        return result

    def get_memory(self) -> AgentMemory:
        """获取Agent记忆"""
        return self.memory

    def get_capabilities(self) -> Dict[str, Any]:
        """获取Agent能力"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "skills": getattr(self, "skills", []),
            "boundaries": getattr(self, "boundaries", [])
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.agent_id}, name={self.name})>"
