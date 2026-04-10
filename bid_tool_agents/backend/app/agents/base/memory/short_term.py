"""
短期记忆 - 当前任务上下文、Agent运行状态
生命周期: 任务周期
"""
from typing import Any, Dict, Optional, List
from datetime import datetime
from enum import Enum
import threading


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ShortTermMemory:
    """
    短期记忆

    特性:
    - 任务级别的上下文存储
    - Agent运行状态管理
    - 会话级状态跟踪
    """

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self._task_context: Dict[str, Dict[str, Any]] = {}
        self._agent_state: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def store_task_context(
        self,
        task_id: str,
        context: Dict[str, Any],
        status: TaskStatus = TaskStatus.PENDING
    ) -> None:
        """
        存储任务上下文

        Args:
            task_id: 任务ID
            context: 任务上下文
            status: 任务状态
        """
        with self._lock:
            self._task_context[task_id] = {
                "context": context,
                "status": status.value,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }

    def get_task_context(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务上下文"""
        with self._lock:
            return self._task_context.get(task_id)

    def update_task_status(self, task_id: str, status: TaskStatus) -> bool:
        """更新任务状态"""
        with self._lock:
            if task_id in self._task_context:
                self._task_context[task_id]["status"] = status.value
                self._task_context[task_id]["updated_at"] = datetime.now()
                return True
            return False

    def update_task_context(self, task_id: str, updates: Dict[str, Any]) -> bool:
        """更新任务上下文的某些字段"""
        with self._lock:
            if task_id in self._task_context:
                self._task_context[task_id]["context"].update(updates)
                self._task_context[task_id]["updated_at"] = datetime.now()
                return True
            return False

    def clear_task(self, task_id: str) -> bool:
        """清除任务记忆"""
        with self._lock:
            if task_id in self._task_context:
                del self._task_context[task_id]
                return True
            return False

    def get_all_tasks(self) -> List[str]:
        """获取所有任务ID"""
        with self._lock:
            return list(self._task_context.keys())

    def update_agent_state(self, state: Dict[str, Any]) -> None:
        """更新Agent状态"""
        with self._lock:
            self._agent_state.update(state)
            self._agent_state["updated_at"] = datetime.now()

    def get_agent_state(self) -> Dict[str, Any]:
        """获取Agent状态"""
        with self._lock:
            return self._agent_state.copy()

    def clear_agent_state(self) -> None:
        """清除Agent状态"""
        with self._lock:
            self._agent_state.clear()

    def clear_all_tasks(self) -> None:
        """清除所有任务"""
        with self._lock:
            self._task_context.clear()

    def clear_all(self) -> None:
        """清除所有短期记忆"""
        with self._lock:
            self._task_context.clear()
            self._agent_state.clear()
