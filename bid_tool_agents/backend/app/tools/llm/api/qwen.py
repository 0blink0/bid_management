"""
阿里云通义千问API实现
"""
import httpx
from typing import List, Dict, Any, AsyncIterator
from ..base import BaseLLM
from ..types import LLMConfig, LLMProvider, LLMModel


class AliQwenLLM(BaseLLM):
    """阿里云通义千问API"""

    API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.api_key = config.api_key

    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """同步聊天"""
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            response = await client.post(
                self.API_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.config.model.value,
                    "messages": messages,
                    "temperature": kwargs.get("temperature", self.config.temperature),
                    "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
                    "stream": False
                }
            )
            result = response.json()
            return result["choices"][0]["message"]["content"]

    async def chat_stream(self, messages: List[Dict[str, str]], **kwargs) -> AsyncIterator[str]:
        """流式聊天"""
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            async with client.stream(
                "POST",
                self.API_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.config.model.value,
                    "messages": messages,
                    "temperature": kwargs.get("temperature", self.config.temperature),
                    "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
                    "stream": True
                }
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data != "[DONE]":
                            import json
                            chunk = json.loads(data)
                            content = chunk["choices"][0]["delta"].get("content", "")
                            if content:
                                yield content

    async def embeddings(self, texts: List[str]) -> List[List[float]]:
        """获取嵌入 - 调用阿里云embedding接口"""
        # TODO: 实现阿里云embedding API
        raise NotImplementedError("Embedding not implemented for AliQwen")

    def get_token_count(self, text: str) -> int:
        """估算token数量"""
        # 简单估算
        return len(text) // 2

    @property
    def model_name(self) -> str:
        return f"{self.config.provider.value}/{self.config.model.value}"
