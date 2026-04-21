#!/usr/bin/env python3
"""法规数据全量重建脚本入口。"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from app.config import get_settings
from app.domain.knowledge_ingest.audit import record_ingest_audit
from app.domain.knowledge_ingest.loader import load_jsonl_records
from app.domain.knowledge_ingest.models import IngestError, IngestResult, IngestSummary
from app.domain.knowledge_ingest.writer import rebuild_laws_collection
from app.tools.database.qdrant import QdrantStore


def _collect_jsonl_files(input_dir: str) -> list[str]:
    files = sorted(Path(input_dir).glob("*.jsonl"))
    # 过滤掉带下划线的标注/中间文件，避免误入库污染 chunk_id 稳定性。
    return [str(path) for path in files if "_" not in path.name]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="法规数据入库重建脚本")
    parser.add_argument("--input-dir", required=True, help="JSONL 数据目录")
    parser.add_argument("--version", required=True, help="数据版本号")
    parser.add_argument("--force", action="store_true", help="是否允许全量重建")
    parser.add_argument("--audit-path", required=True, help="审计输出 JSONL 文件")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    started_at = datetime.utcnow()

    if not args.force:
        message = "force=true required for rebuild"
        print(message)
        result = IngestResult(
            version=args.version,
            collection="laws_regulations",
            input_files=[],
            started_at=started_at,
            finished_at=datetime.utcnow(),
            summary=IngestSummary(total=0, success=0, failed=0, duration_seconds=0.0),
            errors=[IngestError(source_file="cli", line_no=0, message=message)],
        )
        record_ingest_audit(result, args.audit_path)
        return 1

    try:
        input_files = _collect_jsonl_files(args.input_dir)
        records = load_jsonl_records(input_files, version=args.version)
        settings = get_settings()
        store = QdrantStore(
            url=settings.vector_db.url,
            port=settings.vector_db.port,
            api_key=settings.vector_db.api_key,
        )
        result = rebuild_laws_collection(
            records=records,
            force=args.force,
            store=store,
            audit_path=args.audit_path,
            batch_size=16,
        )
        output = {
            "version": result.version,
            "total": result.summary.total,
            "success": result.summary.success,
            "failed": result.summary.failed,
            "duration_seconds": result.summary.duration_seconds,
            "errors": [err.model_dump() for err in result.errors],
        }
        print(json.dumps(output, ensure_ascii=False))
        return 0 if not result.errors else 1
    except Exception as exc:
        result = IngestResult(
            version=args.version,
            collection="laws_regulations",
            input_files=[],
            started_at=started_at,
            finished_at=datetime.utcnow(),
            summary=IngestSummary(total=0, success=0, failed=0, duration_seconds=0.0),
            errors=[IngestError(source_file="cli", line_no=0, message=str(exc))],
        )
        record_ingest_audit(result, args.audit_path)
        print(str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
