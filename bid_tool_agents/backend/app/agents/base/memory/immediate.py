"""
瞬时记忆 - 原始输入 + LLM推理缓存
生命周期: < 1分钟
"""
from typing import Any, Optional, Dict
from datetime import datetime
import time
import threading


class ImmediateMemory:
    """
    瞬时记忆

    特性:
    - 毫秒级写入
    - 自动过期（TTL）
    - 存储原始输入和LLM推理缓存
    """

    def __init__(self, agent_id: str, ttl: int = 60):
        self.agent_id = agent_id
        self.ttl = ttl
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def store(
        self,
        key: str,
        raw_input: str,
        llm_output: Optional[str] = None,
        sensory_data: Any = None
    ) -> None:
        """
        存储瞬时记忆

        Args:
            key: 记忆键
            raw_input: 原始输入
            llm_output: LLM推理原始输出
            sensory_data: 感官缓存（OCR原始结果等）
        """
        with self._lock:
            self._cache[key] = {
                "raw_input": raw_input,
                "llm_raw_output": llm_output,
                "sensory_cache": sensory_data,
                "timestamp": datetime.now(),
                "expires_at": time.time() + self.ttl
            }

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        获取瞬时记忆

        Returns:
            记忆内容，如果不存在或已过期返回None
        """
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                if time.time() < entry["expires_at"]:
                    return entry
                else:
                    del self._cache[key]
            return None

    def get_or_raise(self, key: str, error_msg: str = "记忆不存在或已过期") -> Dict[str, Any]:
        """获取记忆，不存在则抛异常"""
        result = self.get(key)
        if result is None:
            raise ValueError(error_msg)
        return result

    def delete(self, key: str) -> bool:
        """删除记忆"""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def cleanup(self) -> int:
        """
        清理过期记忆

        Returns:
            清理的记忆数量
        """
        with self._lock:
            current_time = time.time()
            keys_to_delete = [
                k for k, v in self._cache.items()
                if current_time >= v["expires_at"]
            ]
            for key in keys_to_delete:
                del self._cache[key]
            return len(keys_to_delete)

    def clear_all(self) -> None:
        """清除所有记忆"""
        with self._lock:
            self._cache.clear()

    def size(self) -> int:
        """获取当前记忆数量"""
        with self._lock:
            return len(self._cache)

    def keys(self) -> list:
        """获取所有记忆键"""
        with self._lock:
            return list(self._cache.keys())

    def __len__(self) -> int:
        return self.size()
