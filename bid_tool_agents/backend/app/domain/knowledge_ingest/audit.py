"""法规入库审计记录。"""
from __future__ import annotations

import json
from pathlib import Path

from .models import IngestResult


def record_ingest_audit(result: IngestResult, output_path: str) -> None:
    """将导入结果以 JSONL 追加写入审计文件。"""
    audit_path = Path(output_path)
    audit_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "version": result.version,
        "collection": result.collection,
        "input_files": result.input_files,
        "started_at": result.started_at.isoformat(),
        "finished_at": result.finished_at.isoformat(),
        "summary": result.summary.model_dump(),
        "errors": [err.model_dump() for err in result.errors],
    }
    with audit_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
