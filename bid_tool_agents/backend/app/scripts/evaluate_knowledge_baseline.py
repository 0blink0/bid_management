#!/usr/bin/env python3
"""Run baseline evaluation and enforce acceptance gate thresholds."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

# 允许 `python app/scripts/evaluate_knowledge_baseline.py` 直接执行。
if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.domain.knowledge_eval.baseline_eval import evaluate_cases, load_eval_cases, summarize_metrics
from app.main import create_app

THRESHOLDS = {
    "recall_at_5": 0.80,
    "mrr": 0.60,
    "latency_p95_ms": 1500.0,
}


class QueryDependencyError(RuntimeError):
    def __init__(self, message: str, request_id: str = "") -> None:
        super().__init__(message)
        self.request_id = request_id


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="评测法规检索基线并执行验收闸门")
    parser.add_argument(
        "--cases-path",
        default="tests/fixtures/knowledge_eval_cases.jsonl",
        help="评测样例 JSONL 路径",
    )
    return parser


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate_with_client(cases_path: str | Path) -> dict[str, Any]:
    client = TestClient(create_app())

    def query_fn(query: str, knowledge_type: str, limit: int) -> dict[str, Any]:
        response = client.post(
            "/api/v1/knowledge/query",
            json={"query": query, "knowledge_type": knowledge_type, "limit": limit},
        )
        body = response.json()
        if response.status_code != 200:
            message = body.get("message", "knowledge query failed")
            request_id = str(body.get("request_id", ""))
            error_code = body.get("error_code", "UNKNOWN_ERROR")
            raise QueryDependencyError(f"{error_code}: {message}", request_id=request_id)
        return body

    case_file = Path(cases_path)
    cases = load_eval_cases(case_file)
    case_results = evaluate_cases(cases, query_fn)
    return build_gate_report(case_file, case_results)


def build_gate_report(case_file: Path, case_results: list[dict[str, Any]]) -> dict[str, Any]:
    metrics = summarize_metrics(case_results)
    checks = {
        "recall_at_5": metrics["recall_at_5"] >= THRESHOLDS["recall_at_5"],
        "mrr": metrics["mrr"] >= THRESHOLDS["mrr"],
        "latency_p95_ms": metrics["latency_ms"]["p95"] <= THRESHOLDS["latency_p95_ms"],
    }
    blocked = (not all(checks.values())) or metrics["failed_case_count"] > 0

    failures = []
    for item in case_results:
        if item.get("failure_reason"):
            failures.append(
                {
                    "query": item["query"],
                    "failure_reason": item["failure_reason"],
                    "request_id": item.get("request_id", ""),
                }
            )

    remediation = []
    if not checks["recall_at_5"]:
        remediation.append("提高召回：检查召回链路与向量质量。")
    if not checks["mrr"]:
        remediation.append("提高排序质量：优化重排策略或 query 改写。")
    if not checks["latency_p95_ms"]:
        remediation.append("降低 p95 延迟：排查依赖与检索配置。")
    if failures:
        remediation.append("修复依赖异常：根据 request_id 在日志中定位失败请求。")

    return {
        "cases_file": str(case_file.as_posix()),
        "cases_file_sha256": file_sha256(case_file),
        "metrics": metrics,
        "thresholds": THRESHOLDS,
        "checks": checks,
        "blocked": blocked,
        "remediation": remediation,
        "failures": failures,
    }


def main() -> int:
    args = build_parser().parse_args()
    report = evaluate_with_client(args.cases_path)
    print(json.dumps(report, ensure_ascii=False))
    return 1 if report["blocked"] else 0


if __name__ == "__main__":
    sys.exit(main())
