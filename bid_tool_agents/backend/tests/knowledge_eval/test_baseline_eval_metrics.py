from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.domain.knowledge_eval.baseline_eval import (
    DEFAULT_KNOWLEDGE_TYPE,
    evaluate_cases,
    load_eval_cases,
    summarize_metrics,
)

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "fixtures" / "knowledge_eval_cases.jsonl"


def test_fixture_count():
    lines = [line for line in FIXTURE_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(lines) == 30


def test_fixture_shape():
    lines = [line for line in FIXTURE_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    for line in lines:
        payload = json.loads(line)
        assert set(payload.keys()) == {"query", "golden_chunk_id"}
        assert payload["query"].strip()
        assert payload["golden_chunk_id"].strip()


def test_load_eval_cases_fail_fast_for_malformed_case(tmp_path: Path):
    bad_file = tmp_path / "bad_cases.jsonl"
    bad_file.write_text('{"query": "x"}\n', encoding="utf-8")
    with pytest.raises(ValueError):
        load_eval_cases(bad_file)


def test_recall_at_5():
    cases = [{"query": "q1", "golden_chunk_id": "c1"}, {"query": "q2", "golden_chunk_id": "missing"}]

    def query_fn(query: str, knowledge_type: str, limit: int):
        assert knowledge_type == DEFAULT_KNOWLEDGE_TYPE
        assert limit == 5
        if query == "q1":
            return {"items": [{"chunk_id": "c1"}], "took_ms": 10, "trace": {"request_id": "r1"}}
        return {"items": [{"chunk_id": "c2"}], "took_ms": 20, "trace": {"request_id": "r2"}}

    summary = summarize_metrics(evaluate_cases(cases, query_fn))
    assert summary["recall_at_5"] == 0.5


def test_mrr():
    cases = [{"query": "q1", "golden_chunk_id": "c1"}, {"query": "q2", "golden_chunk_id": "c9"}]

    def query_fn(query: str, knowledge_type: str, limit: int):
        if query == "q1":
            return {
                "items": [{"chunk_id": "x"}, {"chunk_id": "c1"}],
                "took_ms": 10,
                "trace": {"request_id": "r1"},
            }
        return {"items": [{"chunk_id": "x"}], "took_ms": 20, "trace": {"request_id": "r2"}}

    summary = summarize_metrics(evaluate_cases(cases, query_fn))
    assert summary["mrr"] == 0.25


def test_latency_summary():
    cases = [{"query": "q1", "golden_chunk_id": "c1"}, {"query": "q2", "golden_chunk_id": "c2"}]

    def query_fn(query: str, knowledge_type: str, limit: int):
        return {"items": [{"chunk_id": "x"}], "took_ms": 100 if query == "q1" else 300, "trace": {}}

    summary = summarize_metrics(evaluate_cases(cases, query_fn))
    assert summary["latency_ms"]["avg"] == 200
    assert summary["latency_ms"]["p50"] == 100
    assert summary["latency_ms"]["p95"] == 300
