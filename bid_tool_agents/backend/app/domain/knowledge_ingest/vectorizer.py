"""法规向量化接口。"""
from __future__ import annotations

import hashlib
import os
from functools import lru_cache
from pathlib import Path
from typing import List

VECTOR_SIZE = 1024

# 主权重文件至少应有该体积，避免把「只有 config/modules、权重未下完」误判为就绪。
_MIN_BGE_M3_WEIGHT_BYTES = 32 * 1024 * 1024


def bge_m3_weights_present(model_dir: Path) -> bool:
    for name in ("model.safetensors", "pytorch_model.bin"):
        candidate = model_dir / name
        if candidate.is_file() and candidate.stat().st_size >= _MIN_BGE_M3_WEIGHT_BYTES:
            return True
    for shard in model_dir.glob("model-*.safetensors"):
        if shard.is_file() and shard.stat().st_size >= _MIN_BGE_M3_WEIGHT_BYTES:
            return True
    return False


def bge_m3_local_ready(model_dir: Path) -> bool:
    return (
        (model_dir / "config.json").is_file()
        and (model_dir / "modules.json").is_file()
        and bge_m3_weights_present(model_dir)
    )


def default_bge_m3_storage_dir() -> Path:
    return Path(__file__).resolve().parents[3] / "storage" / "models" / "BAAI-bge-m3"


def _resolve_embedding_backend() -> str:
    explicit = (os.getenv("EMBEDDING_BACKEND", "") or "").strip().lower()
    if explicit:
        return explicit
    # 测试环境默认走确定性伪向量，避免在 CI/本地测试下载大模型。
    if (os.getenv("ENV", "development") or "").strip().lower() == "testing":
        return "deterministic"
    return "bge-m3"


def _default_local_bge_m3_dir() -> Path:
    return default_bge_m3_storage_dir()


def _resolve_bge_m3_model_id() -> str:
    override = (os.getenv("BGE_M3_MODEL_PATH", "") or "").strip()
    if override:
        return override
    local_dir = _default_local_bge_m3_dir()
    if bge_m3_local_ready(local_dir):
        return str(local_dir)
    return "BAAI/bge-m3"


@lru_cache(maxsize=1)
def _get_bge_m3_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(_resolve_bge_m3_model_id())


def _deterministic_embedding(text: str) -> List[float]:
    """生成稳定伪向量，便于离线测试。"""
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    values = [b / 255.0 for b in digest]
    repeated = (values * ((VECTOR_SIZE // len(values)) + 1))[:VECTOR_SIZE]
    return repeated


def embed_chunks(chunks: List[str]) -> List[List[float]]:
    """将文本列表转为向量列表并做维度校验。"""
    backend = _resolve_embedding_backend()
    if backend == "deterministic":
        vectors = [_deterministic_embedding(chunk) for chunk in chunks]
    elif backend == "bge-m3":
        model = _get_bge_m3_model()
        dense_vecs = model.encode(
            chunks,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        vectors = [vec.tolist() for vec in dense_vecs]
    else:
        raise ValueError(f"unsupported embedding backend: {backend}")

    if len(vectors) != len(chunks):
        raise ValueError("embedding result count mismatch")

    for idx, vector in enumerate(vectors):
        if len(vector) != VECTOR_SIZE:
            raise ValueError(f"embedding length invalid at index={idx}, expected {VECTOR_SIZE}")
    return vectors
