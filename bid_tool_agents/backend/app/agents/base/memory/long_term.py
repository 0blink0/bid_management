"""
长期记忆 - 情景记忆 + 语义记忆
生命周期: 月~年
"""
from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
import threading


class MemoryImportance(Enum):
    """记忆重要性"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class LongTermMemory:
    """
    长期记忆

    包含:
    - 情景记忆(Episodic): 任务历史、经验反思、案例索引
    - 语义记忆(Semantic): 知识库、规则库、模板库

    特性:
    - 持久化存储
    - 按重要性保留
    - 支持向量检索
    """

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self._lock = threading.Lock()

        # 情景记忆
        self._experiences: List[Dict[str, Any]] = []
        self._reflections: List[Dict[str, Any]] = []
        self._case_index: List[Dict[str, Any]] = []

        # 语义记忆
        self._knowledge_base: List[Dict[str, Any]] = []
        self._rules: List[Dict[str, Any]] = []
        self._templates: List[Dict[str, Any]] = []

    # ==================== 情景记忆 ====================

    def add_experience(
        self,
        experience: Dict[str, Any],
        importance: MemoryImportance = MemoryImportance.MEDIUM
    ) -> str:
        """
        添加经验

        Args:
            experience: 经验内容
            importance: 重要性等级

        Returns:
            经验ID
        """
        with self._lock:
            exp_id = f"exp_{len(self._experiences)}_{datetime.now().timestamp()}"
            self._experiences.append({
                "id": exp_id,
                "experience": experience,
                "importance": importance.value,
                "created_at": datetime.now()
            })
            return exp_id

    def get_experience(self, exp_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取经验"""
        with self._lock:
            for exp in self._experiences:
                if exp["id"] == exp_id:
                    return exp
            return None

    def get_all_experiences(self) -> List[Dict[str, Any]]:
        """获取所有经验"""
        with self._lock:
            return self._experiences.copy()

    def add_reflection(
        self,
        reflection: str,
        lessons: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        添加反思

        Args:
            reflection: 反思内容
            lessons: 经验教训
            context: 上下文

        Returns:
            反思ID
        """
        with self._lock:
            refl_id = f"refl_{len(self._reflections)}_{datetime.now().timestamp()}"
            self._reflections.append({
                "id": refl_id,
                "reflection": reflection,
                "lessons": lessons,
                "context": context,
                "created_at": datetime.now()
            })
            return refl_id

    def get_recent_reflections(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最近的反思"""
        with self._lock:
            return sorted(
                self._reflections,
                key=lambda x: x["created_at"],
                reverse=True
            )[:limit]

    def add_case(self, case: Dict[str, Any]) -> str:
        """添加案例"""
        with self._lock:
            case_id = f"case_{len(self._case_index)}_{datetime.now().timestamp()}"
            case["id"] = case_id
            case["created_at"] = datetime.now()
            self._case_index.append(case)
            return case_id

    # ==================== 语义记忆 ====================

    def search_knowledge(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        搜索语义记忆（知识库）

        TODO: 实现向量检索
        """
        with self._lock:
            # 简单模糊匹配，实际应通过Qdrant向量检索
            results = [
                kb for kb in self._knowledge_base
                if query.lower() in str(kb.get("content", "")).lower()
            ]
            return results[:limit]

    def add_knowledge(
        self,
        knowledge_type: str,
        title: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        添加知识

        Args:
            knowledge_type: 知识类型
            title: 标题
            content: 内容
            metadata: 元数据
        """
        with self._lock:
            kb_id = f"kb_{len(self._knowledge_base)}_{datetime.now().timestamp()}"
            self._knowledge_base.append({
                "id": kb_id,
                "type": knowledge_type,
                "title": title,
                "content": content,
                "metadata": metadata or {},
                "created_at": datetime.now()
            })
            return kb_id

    def add_rule(
        self,
        rule_type: str,
        condition: str,
        action: str,
        description: Optional[str] = None
    ) -> str:
        """添加规则"""
        with self._lock:
            rule_id = f"rule_{len(self._rules)}_{datetime.now().timestamp()}"
            self._rules.append({
                "id": rule_id,
                "type": rule_type,
                "condition": condition,
                "action": action,
                "description": description,
                "created_at": datetime.now()
            })
            return rule_id

    def get_rules(self, rule_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取规则"""
        with self._lock:
            if rule_type:
                return [r for r in self._rules if r["type"] == rule_type]
            return self._rules.copy()

    def add_template(
        self,
        template_type: str,
        name: str,
        content: str,
        variables: Optional[List[str]] = None
    ) -> str:
        """添加模板"""
        with self._lock:
            tmpl_id = f"tmpl_{len(self._templates)}_{datetime.now().timestamp()}"
            self._templates.append({
                "id": tmpl_id,
                "type": template_type,
                "name": name,
                "content": content,
                "variables": variables or [],
                "created_at": datetime.now()
            })
            return tmpl_id

    def get_template(self, template_type: str, name: str) -> Optional[Dict[str, Any]]:
        """获取模板"""
        with self._lock:
            for tmpl in self._templates:
                if tmpl["type"] == template_type and tmpl["name"] == name:
                    return tmpl
            return None

    # ==================== 持久化接口 ====================

    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        with self._lock:
            return {
                "agent_id": self.agent_id,
                "experiences": self._experiences,
                "reflections": self._reflections,
                "case_index": self._case_index,
                "knowledge_base": self._knowledge_base,
                "rules": self._rules,
                "templates": self._templates
            }

    @classmethod
    def from_dict(cls, agent_id: str, data: Dict[str, Any]) -> "LongTermMemory":
        """从字典恢复"""
        memory = cls(agent_id)
        with memory._lock:
            memory._experiences = data.get("experiences", [])
            memory._reflections = data.get("reflections", [])
            memory._case_index = data.get("case_index", [])
            memory._knowledge_base = data.get("knowledge_base", [])
            memory._rules = data.get("rules", [])
            memory._templates = data.get("templates", [])
        return memory
