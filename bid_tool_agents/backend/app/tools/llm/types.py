"""
LLM类型定义
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


class LLMProvider(Enum):
    """LLM提供者类型"""
    ALI_QWEN = "ali_qwen"              # 阿里云API
    PRIVATE_QWEN = "private_qwen"      # 千问私有化
    PRIVATE_DEEPSEEK = "private_deepseek"  # DeepSeek私有化


class LLMModel(Enum):
    """具体模型枚举"""

    # 阿里云
    QWEN_MAX = "qwen-max"
    QWEN_PLUS = "qwen-plus"
    QWEN_TURBO = "qwen-turbo"

    # 私有化 - 千问
    QWEN3_14B = "qwen3-14b"
    QWEN3_72B = "qwen3-72b"

    # 私有化 - DeepSeek
    DEEPSEEK_V3 = "deepseek-v3"
    DEEPSEEK_CODER = "deepseek-coder"


@dataclass
class LLMConfig:
    """LLM配置"""
    provider: LLMProvider
    model: LLMModel
    api_base: Optional[str] = None           # 私有化地址
    api_key: Optional[str] = None            # API密钥
    max_tokens: int = 4096                   # 最大token数
    temperature: float = 0.7                 # 温度参数
    timeout: int = 120                       # 超时时间(秒)
    retry_times: int = 3                    # 重试次数
    stream: bool = True                     # 是否支持流式
    top_p: float = 0.9                      # top_p采样
    top_k: int = 50                         # top_k采样

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "provider": self.provider.value,
            "model": self.model.value,
            "api_base": self.api_base,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "timeout": self.timeout,
            "stream": self.stream
        }


class ChatMessage:
    """聊天消息"""

    def __init__(
        self,
        role: str,
        content: str,
        name: Optional[str] = None
    ):
        self.role = role
        self.content = content
        self.name = name

    def to_dict(self) -> Dict[str, str]:
        d = {"role": self.role, "content": self.content}
        if self.name:
            d["name"] = self.name
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, str]) -> "ChatMessage":
        return cls(
            role=d["role"],
            content=d["content"],
            name=d.get("name")
        )


class ChatCompletion:
    """聊天完成响应"""

    def __init__(
        self,
        content: str,
        model: str,
        finish_reason: str = "stop",
        usage: Optional[Dict[str, int]] = None
    ):
        self.content = content
        self.model = model
        self.finish_reason = finish_reason
        self.usage = usage or {}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ChatCompletion":
        return cls(
            content=d.get("content", ""),
            model=d.get("model", ""),
            finish_reason=d.get("finish_reason", "stop"),
            usage=d.get("usage", {})
        )
