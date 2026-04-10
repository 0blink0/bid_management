"""
核心记忆 - Agent最核心的信息
生命周期: 永久
更新方式: 人工触发
"""
from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
import threading


class EssenceLevel(Enum):
    """精华级别"""
    STANDARD = "standard"      # 标准精华
    IMPORTANT = "important"    # 重要精华
    CRITICAL = "critical"      # 关键精华


class CoreMemory:
    """
    核心记忆

    包含Agent最核心、最本质的信息:
    - Agent能力画像
    - 记忆精华（关键经验）
    - 决策模式
    - Agent间共享上下文

    特性:
    - 只增不减
    - 人工触发更新
    - 持久化存储
    """

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self._lock = threading.Lock()

        # Agent能力画像
        self._profile: Dict[str, Any] = {}

        # 记忆精华
        self._essence: List[Dict[str, Any]] = []

        # 决策模式
        self._decision_patterns: List[Dict[str, Any]] = []

        # Agent间共享上下文（引用）
        self._shared_context_refs: Dict[str, str] = {}

    # ==================== Agent画像 ====================

    def set_profile(
        self,
        identity: str,
        capabilities: List[str],
        boundaries: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        设置Agent画像

        Args:
            identity: Agent身份描述
            capabilities: 能力列表
            boundaries: 职责边界
            metadata: 其他元数据
        """
        with self._lock:
            self._profile = {
                "identity": identity,
                "capabilities": capabilities,
                "boundaries": boundaries,
                "metadata": metadata or {},
                "updated_at": datetime.now()
            }

    def get_profile(self) -> Dict[str, Any]:
        """获取Agent画像"""
        with self._lock:
            return self._profile.copy()

    def update_profile_field(self, key: str, value: Any) -> None:
        """更新画像字段"""
        with self._lock:
            if "metadata" not in self._profile:
                self._profile["metadata"] = {}
            self._profile["metadata"][key] = value
            self._profile["updated_at"] = datetime.now()

    # ==================== 记忆精华 ====================

    def promote_essence(
        self,
        memory_id: str,
        annotation: str,
        essence_content: Dict[str, Any],
        level: EssenceLevel = EssenceLevel.STANDARD
    ) -> str:
        """
        人工触发：将记忆沉淀为核心记忆精华

        Args:
            memory_id: 原记忆ID
            annotation: 人工注释/标注
            essence_content: 精华内容
            level: 精华级别

        Returns:
            精华ID
        """
        with self._lock:
            essence_id = f"essence_{len(self._essence)}_{datetime.now().timestamp()}"
            self._essence.append({
                "id": essence_id,
                "source_memory_id": memory_id,
                "annotation": annotation,
                "content": essence_content,
                "level": level.value,
                "promoted_at": datetime.now(),
                "promoted_by": "human"  # 人工触发标志
            })
            return essence_id

    def get_all_essence(self) -> List[Dict[str, Any]]:
        """获取所有记忆精华"""
        with self._lock:
            return self._essence.copy()

    def get_essence_by_level(self, level: EssenceLevel) -> List[Dict[str, Any]]:
        """按级别获取精华"""
        with self._lock:
            return [e for e in self._essence if e["level"] == level.value]

    def get_critical_essence(self) -> List[Dict[str, Any]]:
        """获取关键精华"""
        return self.get_essence_by_level(EssenceLevel.CRITICAL)

    # ==================== 决策模式 ====================

    def add_decision_pattern(
        self,
        pattern_type: str,
        situation: str,
        decision: str,
        outcome: str,
        success: bool
    ) -> str:
        """
        添加决策模式

        Args:
            pattern_type: 模式类型
            situation: 情境描述
            decision: 决策内容
            outcome: 结果
            success: 是否成功
        """
        with self._lock:
            pattern_id = f"pattern_{len(self._decision_patterns)}_{datetime.now().timestamp()}"
            self._decision_patterns.append({
                "id": pattern_id,
                "type": pattern_type,
                "situation": situation,
                "decision": decision,
                "outcome": outcome,
                "success": success,
                "created_at": datetime.now()
            })
            return pattern_id

    def get_patterns_for_situation(self, situation_type: str) -> List[Dict[str, Any]]:
        """获取适用于某情境的模式"""
        with self._lock:
            return [
                p for p in self._decision_patterns
                if p.get("type") == situation_type
            ]

    # ==================== 共享上下文 ====================

    def set_shared_context_ref(self, context_key: str, ref_id: str) -> None:
        """
        设置共享上下文引用

        Args:
            context_key: 上下文键
            ref_id: 引用ID（指向全局共享上下文）
        """
        with self._lock:
            self._shared_context_refs[context_key] = ref_id

    def get_shared_context_ref(self, context_key: str) -> Optional[str]:
        """获取共享上下文引用"""
        with self._lock:
            return self._shared_context_refs.get(context_key)

    def get_all_shared_context_refs(self) -> Dict[str, str]:
        """获取所有共享上下文引用"""
        with self._lock:
            return self._shared_context_refs.copy()

    # ==================== 持久化接口 ====================

    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        with self._lock:
            return {
                "agent_id": self.agent_id,
                "profile": self._profile,
                "essence": self._essence,
                "decision_patterns": self._decision_patterns,
                "shared_context_refs": self._shared_context_refs
            }

    @classmethod
    def from_dict(cls, agent_id: str, data: Dict[str, Any]) -> "CoreMemory":
        """从字典恢复"""
        memory = cls(agent_id)
        with memory._lock:
            memory._profile = data.get("profile", {})
            memory._essence = data.get("essence", [])
            memory._decision_patterns = data.get("decision_patterns", [])
            memory._shared_context_refs = data.get("shared_context_refs", {})
        return memory


class AgentMemory:
    """
    Agent完整记忆管理器

    整合四层记忆:
    - 瞬时记忆 (Immediate)
    - 短期记忆 (ShortTerm)
    - 长期记忆 (LongTerm)
    - 核心记忆 (Core)
    """

    def __init__(self, agent_id: str):
        self.agent_id = agent_id

        # 各层记忆
        self.immediate = ImmediateMemory(agent_id)
        self.short_term = ShortTermMemory(agent_id)
        self.long_term = LongTermMemory(agent_id)
        self.core = CoreMemory(agent_id)

    def get_summary(self) -> Dict[str, Any]:
        """获取记忆摘要"""
        return {
            "agent_id": self.agent_id,
            "immediate_size": len(self.immediate),
            "short_term_tasks": len(self.short_term.get_all_tasks()),
            "long_term_experiences": len(self.long_term.get_all_experiences()),
            "core_essence": len(self.core.get_all_essence())
        }

    def clear_all(self) -> None:
        """清除所有记忆（谨慎使用）"""
        # 注意：核心记忆通常不应该被清除
        self.immediate.clear_all()
        self.short_term.clear_all()
        # self.long_term.clear_all()  # 可选
        # self.core.clear_all()  # 不应该清除

    def to_dict(self) -> Dict[str, Any]:
        """完整序列化"""
        return {
            "agent_id": self.agent_id,
            "immediate": {},  # 瞬时记忆不持久化
            "short_term": {},  # 短期记忆按需持久化
            "long_term": self.long_term.to_dict(),
            "core": self.core.to_dict()
        }
