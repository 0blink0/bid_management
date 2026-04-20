from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.scripts import evaluate_knowledge_baseline as runner


def _case_results(recall_hit: float, mrr_score: float, p95: float):
    return [
        {
            "query": "q1",
            "golden_chunk_id": "c1",
            "hit_rank": 1 if recall_hit else None,
            "recall_hit": recall_hit,
            "mrr_score": mrr_score,
            "latency_ms": p95,
            "request_id": "",
            "failure_reason": None,
        }
    ]


def test_recall_gate(tmp_path: Path):
    case_file = tmp_path / "cases.jsonl"
    case_file.write_text('{"query":"q","golden_chunk_id":"c"}\n', encoding="utf-8")
    report = runner.build_gate_report(case_file, _case_results(recall_hit=0.0, mrr_score=1.0, p95=100))
    assert report["blocked"] is True
    assert report["checks"]["recall_at_5"] is False


def test_mrr_gate(tmp_path: Path):
    case_file = tmp_path / "cases.jsonl"
    case_file.write_text('{"query":"q","golden_chunk_id":"c"}\n', encoding="utf-8")
    report = runner.build_gate_report(case_file, _case_results(recall_hit=1.0, mrr_score=0.5, p95=100))
    assert report["blocked"] is True
    assert report["checks"]["mrr"] is False


def test_latency_gate(tmp_path: Path):
    case_file = tmp_path / "cases.jsonl"
    case_file.write_text('{"query":"q","golden_chunk_id":"c"}\n', encoding="utf-8")
    report = runner.build_gate_report(case_file, _case_results(recall_hit=1.0, mrr_score=1.0, p95=1600))
    assert report["blocked"] is True
    assert report["checks"]["latency_p95_ms"] is False


def test_blocked_exit_code(monkeypatch):
    monkeypatch.setattr(
        runner,
        "evaluate_with_client",
        lambda _path: {"blocked": True, "metrics": {}, "checks": {}, "thresholds": {}, "remediation": []},
    )
    monkeypatch.setattr(runner, "build_parser", lambda: type("P", (), {"parse_args": lambda self: type("A", (), {"cases_path": "x"})()})())
    assert runner.main() == 1


def test_failure_reason(monkeypatch, tmp_path: Path):
    case_file = tmp_path / "cases.jsonl"
    case_file.write_text('{"query":"q","golden_chunk_id":"c"}\n', encoding="utf-8")
    case_results = [
        {
            "query": "q",
            "golden_chunk_id": "c",
            "hit_rank": None,
            "recall_hit": 0.0,
            "mrr_score": 0.0,
            "latency_ms": 0.0,
            "request_id": "req-1",
            "failure_reason": "KNOWLEDGE_QUERY_DEPENDENCY_ERROR",
        }
    ]
    report = runner.build_gate_report(case_file, case_results)
    assert report["blocked"] is True
    assert report["failures"][0]["failure_reason"] == "KNOWLEDGE_QUERY_DEPENDENCY_ERROR"
    assert report["failures"][0]["request_id"] == "req-1"


def test_malformed_case(tmp_path: Path):
    bad_file = tmp_path / "bad_cases.jsonl"
    bad_file.write_text('{"query":"only-query"}\n', encoding="utf-8")
    with pytest.raises(ValueError):
        runner.evaluate_with_client(bad_file)
