"""法规向量化接口。"""
from __future__ import annotations

import hashlib
from typing import List

VECTOR_SIZE = 1536


def _deterministic_embedding(text: str) -> List[float]:
    """生成稳定伪向量，便于离线测试。"""
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    values = [b / 255.0 for b in digest]
    repeated = (values * ((VECTOR_SIZE // len(values)) + 1))[:VECTOR_SIZE]
    return repeated


def embed_chunks(chunks: List[str]) -> List[List[float]]:
    """将文本列表转为向量列表并做维度校验。"""
    vectors = [_deterministic_embedding(chunk) for chunk in chunks]
    if len(vectors) != len(chunks):
        raise ValueError("embedding result count mismatch")

    for idx, vector in enumerate(vectors):
        if len(vector) != VECTOR_SIZE:
            raise ValueError(f"embedding length invalid at index={idx}, expected 1536")
    return vectors
