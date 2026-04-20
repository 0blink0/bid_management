"""Baseline evaluation utilities for knowledge query quality gates."""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Callable

DEFAULT_KNOWLEDGE_TYPE = "laws_regulations"
DEFAULT_TOP_K = 5


def load_eval_cases(path: str | Path) -> list[dict[str, str]]:
    """Load and validate eval cases from JSONL file."""
    file_path = Path(path)
    cases: list[dict[str, str]] = []
    with file_path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line_text = line.strip()
            if not line_text:
                continue
            try:
                payload = json.loads(line_text)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{file_path}:{line_no} invalid json: {exc.msg}") from exc

            query = str(payload.get("query", "")).strip()
            golden_chunk_id = str(payload.get("golden_chunk_id", "")).strip()
            if not query or not golden_chunk_id:
                raise ValueError(f"{file_path}:{line_no} missing query/golden_chunk_id")

            cases.append({"query": query, "golden_chunk_id": golden_chunk_id})
    return cases


def evaluate_cases(
    cases: list[dict[str, str]],
    query_fn: Callable[[str, str, int], dict[str, Any]],
    knowledge_type: str = DEFAULT_KNOWLEDGE_TYPE,
    top_k: int = DEFAULT_TOP_K,
) -> list[dict[str, Any]]:
    """Evaluate each case against query function and collect raw outcomes."""
    results: list[dict[str, Any]] = []

    for case in cases:
        query = case["query"]
        golden_chunk_id = case["golden_chunk_id"]
        try:
            response = query_fn(query, knowledge_type, top_k)
            items = response.get("items", [])
            trace = response.get("trace", {}) or {}
            chunk_ids = [str(item.get("chunk_id", "")) for item in items[:top_k]]
            rank = next((idx + 1 for idx, cid in enumerate(chunk_ids) if cid == golden_chunk_id), None)
            results.append(
                {
                    "query": query,
                    "golden_chunk_id": golden_chunk_id,
                    "hit_rank": rank,
                    "recall_hit": 1.0 if rank is not None else 0.0,
                    "mrr_score": (1.0 / rank) if rank is not None else 0.0,
                    "latency_ms": float(response.get("took_ms", 0.0)),
                    "request_id": str(trace.get("request_id", "")),
                    "failure_reason": None,
                }
            )
        except Exception as exc:  # noqa: BLE001 - preserve failure reason in report
            request_id = str(getattr(exc, "request_id", "") or "")
            results.append(
                {
                    "query": query,
                    "golden_chunk_id": golden_chunk_id,
                    "hit_rank": None,
                    "recall_hit": 0.0,
                    "mrr_score": 0.0,
                    "latency_ms": 0.0,
                    "request_id": request_id,
                    "failure_reason": str(exc),
                }
            )
    return results


def summarize_metrics(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate result list into fixed metric contract."""
    total = len(results)
    if total == 0:
        return {
            "case_count": 0,
            "failed_case_count": 0,
            "recall_at_5": 0.0,
            "mrr": 0.0,
            "latency_ms": {"avg": 0.0, "p50": 0.0, "p95": 0.0},
        }

    recall = sum(float(item["recall_hit"]) for item in results) / total
    mrr = sum(float(item["mrr_score"]) for item in results) / total
    latencies = [float(item["latency_ms"]) for item in results]
    failed = sum(1 for item in results if item.get("failure_reason"))
    return {
        "case_count": total,
        "failed_case_count": failed,
        "recall_at_5": round(recall, 6),
        "mrr": round(mrr, 6),
        "latency_ms": {
            "avg": round(sum(latencies) / total, 3),
            "p50": _percentile(latencies, 50),
            "p95": _percentile(latencies, 95),
        },
    }


def _percentile(values: list[float], percentile: int) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    rank = max(0, math.ceil((percentile / 100) * len(ordered)) - 1)
    return round(ordered[rank], 3)
