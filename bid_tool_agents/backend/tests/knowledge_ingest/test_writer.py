"""法规写库与审计测试。"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.domain.knowledge_ingest.models import LawRecord
from app.domain.knowledge_ingest.vectorizer import VECTOR_SIZE, embed_chunks
from app.domain.knowledge_ingest.writer import rebuild_laws_collection


class DummyStore:
    def __init__(self):
        self.calls = []
        self.upsert_payload_sizes = []

    def delete_collection(self, collection_name):
        self.calls.append(("delete_collection", collection_name))
        return True

    def create_collection(self, collection_name, vector_size=1536):
        self.calls.append(("create_collection", collection_name, vector_size))
        return True

    def upsert(self, collection_name, points):
        self.calls.append(("upsert", collection_name))
        self.upsert_payload_sizes.append(len(points))
        return True


def _records(n: int = 3):
    return [
        LawRecord(
            title="法A",
            chapter="第一章",
            article_no=f"第{i + 1}条",
            content=f"第{i + 1}条 内容",
            source_file="docs/dataset/law.jsonl",
            chunk_id=f"id-{i}",
            version="2026-04-20",
            full_text=f"第{i + 1}条 内容",
            chunk_text=f"第{i + 1}条 内容",
        )
        for i in range(n)
    ]


def test_embed_chunks_dimension_check():
    vectors = embed_chunks(["a", "b"])
    assert len(vectors) == 2
    assert len(vectors[0]) == VECTOR_SIZE


def test_rebuild_requires_force(tmp_path: Path):
    store = DummyStore()
    result = rebuild_laws_collection(
        records=_records(1),
        force=False,
        store=store,
        audit_path=str(tmp_path / "audit.jsonl"),
    )
    assert result.errors
    assert "force=true required" in result.errors[0].message
    assert store.calls == []


def test_rebuild_call_order_and_collection(tmp_path: Path):
    store = DummyStore()
    result = rebuild_laws_collection(
        records=_records(3),
        force=True,
        store=store,
        audit_path=str(tmp_path / "audit.jsonl"),
        batch_size=2,
    )

    assert not result.errors
    assert store.calls[0] == ("delete_collection", "laws_regulations")
    assert store.calls[1] == ("create_collection", "laws_regulations", VECTOR_SIZE)
    assert store.calls[2][0] == "upsert"
    assert sum(store.upsert_payload_sizes) == 3


def test_audit_written_on_failure(tmp_path: Path):
    class BrokenStore(DummyStore):
        def upsert(self, collection_name, points):
            raise RuntimeError("write failed")

    audit_path = tmp_path / "audit.jsonl"
    result = rebuild_laws_collection(
        records=_records(2),
        force=True,
        store=BrokenStore(),
        audit_path=str(audit_path),
    )
    assert result.errors
    lines = audit_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert payload["errors"]
    assert payload["version"] == "2026-04-20"
