"""法规加载与切分测试。"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.domain.knowledge_ingest.chunker import split_article
from app.domain.knowledge_ingest.loader import build_stable_chunk_id, load_jsonl_records
from app.domain.knowledge_ingest.models import LawRecord, validate_required_fields


def test_model_contract_serialization():
    record = LawRecord(
        title="中华人民共和国招标投标法",
        chapter="第一章 总则",
        article_no="第一条",
        content="第一条 为了规范招标投标活动。",
        source_file="docs/dataset/law.jsonl",
        chunk_id="abc123",
        version="2026-04-20",
        full_text="第一条 为了规范招标投标活动。",
        chunk_text="第一条 为了规范招标投标活动。",
    )
    dumped = record.model_dump()
    assert dumped["article_no"] == "第一条"
    assert dumped["chunk_id"] == "abc123"
    assert dumped["version"] == "2026-04-20"
    assert dumped["source_file"] == "docs/dataset/law.jsonl"


@pytest.mark.parametrize("field", ["title", "chapter", "content", "version", "source_file"])
def test_model_contract_missing_required_field(field):
    payload = {
        "title": "a",
        "chapter": "b",
        "content": "c",
        "version": "v",
        "source_file": "docs/file.jsonl",
    }
    payload[field] = ""
    with pytest.raises(ValueError) as exc:
        validate_required_fields(payload, "docs/file.jsonl", 10)
    assert "docs/file.jsonl:10" in str(exc.value)
    assert field in str(exc.value)


def test_stable_chunk_id():
    a = build_stable_chunk_id("T", "C", "X")
    b = build_stable_chunk_id("T", "C", "X")
    c = build_stable_chunk_id("T", "C", "Y")
    assert a == b
    assert a != c


def test_load_jsonl_and_fail_fast(tmp_path: Path):
    good = tmp_path / "good.jsonl"
    bad = tmp_path / "bad.jsonl"
    good.write_text(
        json.dumps({"title": "法A", "chapter": "第一章", "content": "第一条 内容"}) + "\n",
        encoding="utf-8",
    )
    bad.write_text("{broken-json}\n", encoding="utf-8")

    records = load_jsonl_records([str(good)], version="2026-04-20")
    assert records
    assert records[0].version == "2026-04-20"
    assert records[0].article_no.startswith("第")

    with pytest.raises(ValueError) as exc:
        load_jsonl_records([str(bad)], version="2026-04-20")
    assert "invalid json" in str(exc.value)
    assert "bad.jsonl:1" in str(exc.value)


def test_split_article_short_and_long_overlap():
    short = "第一条 这是一个短文本。"
    assert split_article(short, max_chars=50, overlap_chars=10) == [short]

    long_text = "。".join([f"第{i}句内容较长" for i in range(1, 25)]) + "。"
    chunks = split_article(long_text, max_chars=50, overlap_chars=10)
    assert len(chunks) > 1
    assert chunks[0][-10:] in chunks[1]


def test_split_article_fallback_without_delimiter():
    text = "A" * 210
    chunks = split_article(text, max_chars=80, overlap_chars=10)
    assert len(chunks) >= 3


def test_full_text_chunk_text_fields(tmp_path: Path):
    path = tmp_path / "law.jsonl"
    content = "。".join(["第一条 " + ("内容" * 80), "补充说明"]) + "。"
    path.write_text(
        json.dumps({"title": "法A", "chapter": "第一章", "content": content}) + "\n",
        encoding="utf-8",
    )
    records = load_jsonl_records([str(path)], version="2026-04-20")
    assert len(records) > 1
    for record in records:
        assert record.full_text == content
        assert record.chunk_text
