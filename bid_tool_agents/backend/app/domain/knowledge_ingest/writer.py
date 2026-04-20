"""法规写库与重建执行。"""
from __future__ import annotations

from datetime import datetime
from typing import List

from qdrant_client.models import PointStruct

from app.domain.knowledge_ingest.audit import record_ingest_audit
from app.domain.knowledge_ingest.models import (
    IngestError,
    IngestResult,
    IngestSummary,
    LawRecord,
)
from app.domain.knowledge_ingest.vectorizer import VECTOR_SIZE, embed_chunks
from app.tools.database.qdrant import QdrantStore

COLLECTION_NAME = "laws_regulations"


def _to_points(records: List[LawRecord], vectors: List[List[float]]) -> List[PointStruct]:
    points: List[PointStruct] = []
    for record, vector in zip(records, vectors):
        payload = {
            "title": record.title,
            "chapter": record.chapter,
            "article_no": record.article_no,
            "source_file": record.source_file,
            "chunk_id": record.chunk_id,
            "version": record.version,
            "full_text": record.full_text,
            "chunk_text": record.chunk_text,
        }
        points.append(
            PointStruct(
                id=record.chunk_id,
                vector=vector,
                payload=payload,
            )
        )
    return points


def rebuild_laws_collection(
    records: List[LawRecord],
    force: bool,
    store: QdrantStore,
    audit_path: str,
    vector_size: int = VECTOR_SIZE,
    batch_size: int = 128,
) -> IngestResult:
    """在 force 模式下执行法规集合全量重建。"""
    started_at = datetime.utcnow()
    version = records[0].version if records else ""
    input_files = sorted({r.source_file for r in records})
    errors: List[IngestError] = []

    summary = IngestSummary(total=len(records), success=0, failed=0, duration_seconds=0.0)
    try:
        if vector_size != VECTOR_SIZE:
            raise ValueError("vector_size must be 1536")
        if not force:
            raise ValueError("force=true required for rebuild")

        store.delete_collection(COLLECTION_NAME)
        store.create_collection(COLLECTION_NAME, vector_size=vector_size)

        chunks = [item.chunk_text for item in records]
        vectors = embed_chunks(chunks)
        points = _to_points(records, vectors)

        for idx in range(0, len(points), batch_size):
            store.upsert(COLLECTION_NAME, points[idx:idx + batch_size])

        summary.success = len(records)
        summary.failed = 0
    except Exception as exc:
        summary.failed = len(records) - summary.success
        errors.append(
            IngestError(
                source_file="writer",
                line_no=0,
                message=str(exc),
            )
        )
    finally:
        finished_at = datetime.utcnow()
        summary.duration_seconds = (finished_at - started_at).total_seconds()
        result = IngestResult(
            version=version,
            collection=COLLECTION_NAME,
            input_files=input_files,
            started_at=started_at,
            finished_at=finished_at,
            summary=summary,
            errors=errors,
        )
        record_ingest_audit(result, audit_path)
    return result
