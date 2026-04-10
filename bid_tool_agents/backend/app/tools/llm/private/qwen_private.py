"""
千问私有化部署实现
"""
import httpx
from typing import List, Dict, Any, AsyncIterator
from ..base import BaseLLM
from ..types import LLMConfig, LLMProvider


class PrivateQwenLLM(BaseLLM):
    """千问私有化部署"""

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.api_base = config.api_base.rstrip("/") if config.api_base else ""
        self.api_key = config.api_key or "dummy"

    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """同步聊天"""
        url = f"{self.api_base}/chat/completions"
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            response = await client.post(
                url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.config.model.value,
                    "messages": messages,
                    "temperature": kwargs.get("temperature", self.config.temperature),
                    "max_tokens": kwargs.get("max_tokens", self.config.max_tokens)
                }
            )
            return response.json()["choices"][0]["message"]["content"]

    async def chat_stream(self, messages: List[Dict[str, str]], **kwargs) -> AsyncIterator[str]:
        """流式聊天"""
        url = f"{self.api_base}/chat/completions"
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            async with client.stream(
                "POST",
                url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.config.model.value,
                    "messages": messages,
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
        """获取嵌入"""
        url = f"{self.api_base}/embeddings"
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            response = await client.post(
                url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"input": texts, "model": self.config.model.value}
            )
            return [item["embedding"] for item in response.json()["data"]]

    def get_token_count(self, text: str) -> int:
        """估算token数量"""
        return len(text) // 2

    @property
    def model_name(self) -> str:
        return f"private/{self.config.model.value}"
