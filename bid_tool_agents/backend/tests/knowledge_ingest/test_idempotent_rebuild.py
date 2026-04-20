"""幂等重建测试。"""
from __future__ import annotations

from pathlib import Path

from app.domain.knowledge_ingest.models import LawRecord
from app.domain.knowledge_ingest.writer import rebuild_laws_collection


class MemoryStore:
    def __init__(self):
        self.points_by_collection = {}

    def delete_collection(self, collection_name):
        self.points_by_collection[collection_name] = {}
        return True

    def create_collection(self, collection_name, vector_size=1536):
        self.points_by_collection.setdefault(collection_name, {})
        return True

    def upsert(self, collection_name, points):
        bucket = self.points_by_collection.setdefault(collection_name, {})
        for point in points:
            bucket[str(point.id)] = point.payload
        return True


def _records():
    return [
        LawRecord(
            title="法A",
            chapter="第一章",
            article_no="第一条",
            content="第一条 内容",
            source_file="docs/dataset/a.jsonl",
            chunk_id="fixed-1",
            version="2026-04-20",
            full_text="第一条 内容",
            chunk_text="第一条 内容",
        ),
        LawRecord(
            title="法A",
            chapter="第一章",
            article_no="第二条",
            content="第二条 内容",
            source_file="docs/dataset/a.jsonl",
            chunk_id="fixed-2",
            version="2026-04-20",
            full_text="第二条 内容",
            chunk_text="第二条 内容",
        ),
    ]


def test_idempotent_rebuild_consistent_state(tmp_path: Path):
    store = MemoryStore()
    audit_path = str(tmp_path / "audit.jsonl")
    records = _records()

    first = rebuild_laws_collection(records, True, store=store, audit_path=audit_path)
    first_state = dict(store.points_by_collection["laws_regulations"])

    second = rebuild_laws_collection(records, True, store=store, audit_path=audit_path)
    second_state = dict(store.points_by_collection["laws_regulations"])

    assert not first.errors and not second.errors
    assert first.summary.success == second.summary.success == 2
    assert set(first_state.keys()) == set(second_state.keys())
    assert first_state == second_state
