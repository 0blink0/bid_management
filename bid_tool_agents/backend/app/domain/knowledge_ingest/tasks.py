"""法规知识库重建异步任务管理。"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from threading import Lock
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.domain.knowledge_ingest.loader import load_jsonl_records
from app.domain.knowledge_ingest.writer import rebuild_laws_collection
from app.tools.database.qdrant import get_qdrant

TASK_STATUS_QUEUED = "queued"
TASK_STATUS_RUNNING = "running"
TASK_STATUS_SUCCEEDED = "succeeded"
TASK_STATUS_FAILED = "failed"

_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="knowledge-rebuild")
_tasks: Dict[str, Dict[str, Any]] = {}
_lock = Lock()


def _now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def _is_retryable_error(exc: Exception) -> bool:
    msg = str(exc).lower()
    retryable_markers = ("qdrant", "connect", "timeout", "connection", "unavailable", "initialized")
    return any(marker in msg for marker in retryable_markers)


def _build_error(error_code: str, message: str, request_id: str, retryable: bool) -> Dict[str, Any]:
    return {
        "error_code": error_code,
        "message": message,
        "details": {"retryable": retryable},
        "request_id": request_id,
    }


def _run_rebuild_task(
    task_id: str,
    request_id: str,
    input_paths: List[str],
    version: str,
    force: bool,
    audit_path: str,
) -> None:
    with _lock:
        task = _tasks[task_id]
        task["status"] = TASK_STATUS_RUNNING
        task["started_at"] = task["started_at"] or _now_iso()
        task["updated_at"] = _now_iso()

    try:
        records = load_jsonl_records(input_paths=input_paths, version=version)
        result = rebuild_laws_collection(
            records=records,
            force=force,
            store=get_qdrant(),
            audit_path=audit_path,
        )
        summary = {
            "total": result.summary.total,
            "success": result.summary.success,
            "failed": result.summary.failed,
            "duration_seconds": result.summary.duration_seconds,
            "collection": result.collection,
            "version": result.version,
        }
        with _lock:
            task = _tasks[task_id]
            task["status"] = TASK_STATUS_SUCCEEDED if not result.errors else TASK_STATUS_FAILED
            task["summary"] = summary
            task["updated_at"] = _now_iso()
            if result.errors:
                task["error"] = _build_error(
                    error_code="KNOWLEDGE_REBUILD_FAILED",
                    message=result.errors[0].message,
                    request_id=request_id,
                    retryable=False,
                )
    except Exception as exc:  # noqa: BLE001 - convert to stable API error
        with _lock:
            task = _tasks[task_id]
            task["status"] = TASK_STATUS_FAILED
            task["updated_at"] = _now_iso()
            task["error"] = _build_error(
                error_code="KNOWLEDGE_REBUILD_DEPENDENCY_ERROR",
                message="knowledge rebuild task failed",
                request_id=request_id,
                retryable=_is_retryable_error(exc),
            )
            task["details"] = {"raw_error": str(exc)}


def create_rebuild_task(
    *,
    knowledge_type: str,
    input_paths: List[str],
    version: str,
    force: bool,
    audit_path: str,
    request_id: Optional[str] = None,
) -> Dict[str, Any]:
    """创建并提交法规重建任务。"""
    task_id = str(uuid4())
    req_id = request_id or str(uuid4())
    now = _now_iso()
    with _lock:
        _tasks[task_id] = {
            "task_id": task_id,
            "status": TASK_STATUS_QUEUED,
            "knowledge_type": knowledge_type,
            "started_at": now,
            "updated_at": now,
            "summary": None,
            "error": None,
            "request_id": req_id,
        }

    _executor.submit(_run_rebuild_task, task_id, req_id, input_paths, version, force, audit_path)
    return get_task_status(task_id) or {}


def get_task_status(task_id: str) -> Optional[Dict[str, Any]]:
    """获取任务状态快照。"""
    with _lock:
        task = _tasks.get(task_id)
        if task is None:
            return None
        return dict(task)
