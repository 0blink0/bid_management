"""法规入库数据契约。"""
from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class CompatBaseModel(BaseModel):
    """兼容 pydantic v1/v2 的序列化接口。"""

    def model_dump(self, *args, **kwargs):  # type: ignore[override]
        base_dump = getattr(super(), "model_dump", None)
        if callable(base_dump):
            return base_dump(*args, **kwargs)
        return self.dict(*args, **kwargs)


class LawRecord(CompatBaseModel):
    """单条待入库法规记录。"""

    title: str
    chapter: str
    article_no: str
    content: str
    source_file: str
    chunk_id: str
    version: str
    full_text: str
    chunk_text: str


class IngestError(CompatBaseModel):
    """导入错误明细。"""

    source_file: str
    line_no: int = 0
    message: str


class IngestSummary(CompatBaseModel):
    """导入汇总信息。"""

    total: int = 0
    success: int = 0
    failed: int = 0
    duration_seconds: float = 0.0


class IngestResult(CompatBaseModel):
    """导入执行结果。"""

    version: str
    collection: str
    input_files: List[str] = Field(default_factory=list)
    started_at: datetime
    finished_at: datetime
    summary: IngestSummary
    errors: List[IngestError] = Field(default_factory=list)


def validate_required_fields(record: dict, source_file: str, line_no: int) -> None:
    """校验关键字段，失败时抛出含文件与行号的错误。"""

    required_fields = ("title", "chapter", "content", "version", "source_file")
    for field in required_fields:
        value = record.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError(
                f"{source_file}:{line_no} missing required field '{field}'"
            )
