"""
Redis连接
"""
from typing import Optional, Any
import redis.asyncio as redis


class RedisClient:
    """Redis客户端"""

    def __init__(self, url: str):
        self.url = url
        self._client: Optional[redis.Redis] = None

    async def connect(self):
        """连接"""
        self._client = redis.from_url(self.url, decode_responses=True)

    async def close(self):
        """关闭"""
        if self._client:
            await self._client.close()

    async def get(self, key: str) -> Optional[str]:
        """获取"""
        return await self._client.get(key)

    async def set(
        self,
        key: str,
        value: str,
        ex: Optional[int] = None
    ) -> bool:
        """设置"""
        return await self._client.set(key, value, ex=ex)

    async def delete(self, key: str) -> int:
        """删除"""
        return await self._client.delete(key)

    async def exists(self, key: str) -> bool:
        """是否存在"""
        return await self._client.exists(key)

    async def expire(self, key: str, seconds: int) -> bool:
        """设置过期"""
        return await self._client.expire(key, seconds)

    async def ttl(self, key: str) -> int:
        """获取TTL"""
        return await self._client.ttl(key)


# 全局实例
_redis: Optional[RedisClient] = None


def init_redis(url: str) -> RedisClient:
    """初始化Redis"""
    global _redis
    _redis = RedisClient(url)
    return _redis


def get_redis() -> RedisClient:
    """获取Redis实例"""
    if _redis is None:
        raise RuntimeError("Redis not initialized")
    return _redis
