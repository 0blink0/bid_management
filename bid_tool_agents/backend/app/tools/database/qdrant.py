"""
Qdrant向量数据库连接
"""
from typing import Optional, List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


class QdrantClient:
    """Qdrant向量数据库客户端"""

    def __init__(self, url: str, port: int = 6333):
        self.client = QdrantClient(url=url, port=port)

    def create_collection(
        self,
        collection_name: str,
        vector_size: int = 1536,
        distance: Distance = Distance.COSINE
    ) -> bool:
        """创建集合"""
        collections = self.client.get_collections().collections
        if collection_name in [c.name for c in collections]:
            return True

        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=distance
            )
        )
        return True

    def upsert(
        self,
        collection_name: str,
        points: List[PointStruct]
    ) -> bool:
        """插入/更新向量"""
        self.client.upsert(collection_name=collection_name, points=points)
        return True

    def search(
        self,
        collection_name: str,
        query_vector: List[float],
        limit: int = 10,
        score_threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """搜索"""
        results = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold
        )
        return [
            {
                "id": r.id,
                "score": r.score,
                "payload": r.payload
            }
            for r in results
        ]

    def delete(self, collection_name: str, point_ids: List[str]) -> bool:
        """删除"""
        self.client.delete(
            collection_name=collection_name,
            points_selector=point_ids
        )
        return True


# 全局实例
_qdrant: Optional[QdrantClient] = None


def init_qdrant(url: str, port: int = 6333) -> QdrantClient:
    """初始化Qdrant"""
    global _qdrant
    _qdrant = QdrantClient(url=url, port=port)
    return _qdrant


def get_qdrant() -> QdrantClient:
    """获取Qdrant实例"""
    if _qdrant is None:
        raise RuntimeError("Qdrant not initialized")
    return _qdrant
