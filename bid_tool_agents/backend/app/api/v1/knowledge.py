"""知识库接口。"""
from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from fastapi import APIRouter, Body, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError

from app.config import get_settings
from app.domain.knowledge_ingest import vectorizer
from app.domain.knowledge_ingest.tasks import create_rebuild_task, get_task_status
from app.domain.knowledge_ingest.writer import COLLECTION_NAME
from app.tools.database.qdrant import get_qdrant

router = APIRouter()


class KnowledgeItem(BaseModel):
    """知识库条目"""
    id: str
    type: str
    title: str
    content: str
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


class KnowledgeQuery(BaseModel):
    """知识库查询"""
    query: str
    knowledge_type: Optional[str] = None
    limit: int = 10


class ApiErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Dict[str, Any] = Field(default_factory=dict)
    request_id: str


class KnowledgeQueryRequest(BaseModel):
    query: str = Field(min_length=1)
    knowledge_type: Optional[str] = None
    limit: Optional[int] = None


class KnowledgeHit(BaseModel):
    title: str
    chapter: str
    source_file: str
    chunk_id: str
    version: str
    score: float


class KnowledgeQueryResponse(BaseModel):
    items: List[KnowledgeHit]
    total: int
    took_ms: float
    trace: Dict[str, Any]


class RebuildRequest(BaseModel):
    input_paths: List[str] = Field(min_length=1)
    version: str = Field(min_length=1)
    force: bool = True
    audit_path: Optional[str] = None


def _error(error_code: str, message: str, request_id: str, details: Optional[Dict[str, Any]] = None) -> ApiErrorResponse:
    return ApiErrorResponse(
        error_code=error_code,
        message=message,
        details=details or {},
        request_id=request_id,
    )


def _extract_validation_details(exc: ValidationError) -> Dict[str, Any]:
    return {"validation_errors": exc.errors()}


@router.post("/query", response_model=KnowledgeQueryResponse)
async def query_knowledge(payload: Dict[str, Any] = Body(...)) -> Any:
    """查询知识库。"""
    request_id = str(uuid4())
    settings = get_settings()
    started = time.perf_counter()

    try:
        query = KnowledgeQueryRequest.model_validate(payload)
    except ValidationError as exc:
        err = _error(
            error_code="VALIDATION_ERROR",
            message="request payload validation failed",
            request_id=request_id,
            details=_extract_validation_details(exc),
        )
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=err.model_dump())

    knowledge_type = (query.knowledge_type or "").strip() or settings.knowledge_query.default_knowledge_type
    raw_limit = query.limit if query.limit is not None else settings.knowledge_query.default_limit
    limit = max(1, min(raw_limit, settings.knowledge_query.max_limit))

    try:
        query_vector = vectorizer.embed_chunks([query.query])[0]
        hits = get_qdrant().search(
            collection_name=knowledge_type,
            query_vector=query_vector,
            limit=limit,
        )
    except Exception:  # noqa: BLE001 - map dependency errors to API contract
        err = _error(
            error_code="KNOWLEDGE_QUERY_DEPENDENCY_ERROR",
            message="knowledge query dependency failed",
            request_id=request_id,
            details={"retryable": True},
        )
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=err.model_dump())

    normalized_items: List[KnowledgeHit] = []
    for item in hits:
        payload_data = item.get("payload") or {}
        normalized_items.append(
            KnowledgeHit(
                title=str(payload_data.get("title", "")),
                chapter=str(payload_data.get("chapter", "")),
                source_file=str(payload_data.get("source_file", "")),
                chunk_id=str(payload_data.get("chunk_id", item.get("id", ""))),
                version=str(payload_data.get("version", "")),
                score=float(item.get("score", 0.0)),
            )
        )

    normalized_items.sort(key=lambda x: x.score, reverse=True)
    took_ms = round((time.perf_counter() - started) * 1000, 3)
    return KnowledgeQueryResponse(
        items=normalized_items,
        total=len(normalized_items),
        took_ms=took_ms,
        trace={
            "request_id": request_id,
            "knowledge_type": knowledge_type,
            "limit": limit,
            "timings": {"query_ms": took_ms},
        },
    )


@router.post("/ingest/rebuild", status_code=status.HTTP_202_ACCEPTED)
async def rebuild_knowledge_ingest(request: Request, payload: Dict[str, Any] = Body(...)) -> Any:
    """触发法规知识库重建任务。"""
    request_id = str(uuid4())
    try:
        req = RebuildRequest.model_validate(payload)
    except ValidationError as exc:
        err = _error(
            error_code="VALIDATION_ERROR",
            message="request payload validation failed",
            request_id=request_id,
            details=_extract_validation_details(exc),
        )
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=err.model_dump())

    try:
        task = create_rebuild_task(
            knowledge_type=COLLECTION_NAME,
            input_paths=req.input_paths,
            version=req.version,
            force=req.force,
            audit_path=req.audit_path or str(Path("storage") / "knowledge_ingest_audit.log"),
            request_id=request_id,
        )
    except Exception:
        err = _error(
            error_code="KNOWLEDGE_INGEST_DEPENDENCY_ERROR",
            message="knowledge ingest dependency failed",
            request_id=request_id,
            details={"retryable": True},
        )
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=err.model_dump())

    base = str(request.base_url).rstrip("/")
    return {
        "task_id": task["task_id"],
        "status_url": f"{base}/api/v1/knowledge/tasks/{task['task_id']}",
        "request_id": request_id,
    }


@router.get("/tasks/{task_id}")
async def query_task_status(task_id: str) -> Any:
    """查询知识库异步任务状态。"""
    task = get_task_status(task_id)
    if task is None:
        err = _error(
            error_code="TASK_NOT_FOUND",
            message="knowledge task not found",
            request_id=str(uuid4()),
            details={"task_id": task_id},
        )
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=err.model_dump())

    if task.get("status") == "failed" and (task.get("error") or {}).get("details", {}).get("retryable") is True:
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=task)

    return task


@router.get("/types")
async def list_knowledge_types() -> List[str]:
    """列出知识库类型"""
    return [
        "laws_regulations",  # 法律法规
        "internal_rules",    # 内部规则
        "policies",          # 制度
        "qualifications",    # 资质证书
        "cases",             # 案例库
        "experts",           # 专家库
        "templates",         # 模板库
        "sensitive_words"    # 错敏词库
    ]


@router.post("/add")
async def add_knowledge(item: KnowledgeItem) -> Dict[str, str]:
    """添加知识库条目"""
    # TODO: 实现知识库添加
    return {"id": item.id, "message": "Knowledge added successfully"}


@router.delete("/{knowledge_id}")
async def delete_knowledge(knowledge_id: str):
    """删除知识库条目"""
    # TODO: 实现知识库删除
    return {"success": True, "message": f"Knowledge {knowledge_id} deleted"}
