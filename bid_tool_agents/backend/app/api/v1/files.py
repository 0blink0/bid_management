"""
文件上传接口
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import uuid
from datetime import datetime

from app.config import get_settings

router = APIRouter()

settings = get_settings()


class FileInfo(BaseModel):
    """文件信息"""
    id: str
    name: str
    size: int
    type: str
    upload_time: datetime
    status: str


class UploadResponse(BaseModel):
    """上传响应"""
    success: bool
    file_id: str
    file_name: str
    message: Optional[str] = None


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """上传文件"""
    # 检查文件大小
    file_content = await file.read()
    if len(file_content) > settings.storage.max_file_size:
        raise HTTPException(status_code=400, detail="File too large")

    # 检查文件类型
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in settings.storage.allowed_extensions:
        raise HTTPException(status_code=400, detail="File type not allowed")

    # 保存文件
    file_id = str(uuid.uuid4())
    file_path = os.path.join(settings.storage.upload_dir, file_id + ext)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file_content)

    return UploadResponse(
        success=True,
        file_id=file_id,
        file_name=file.filename
    )


@router.get("/list")
async def list_files() -> List[FileInfo]:
    """列出已上传文件"""
    # TODO: 实现文件列表查询
    return []


@router.delete("/{file_id}")
async def delete_file(file_id: str):
    """删除文件"""
    # TODO: 实现文件删除
    return {"success": True, "message": f"File {file_id} deleted"}
