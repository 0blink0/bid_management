"""
API路由聚合
"""
from fastapi import APIRouter

from .agents import router as agents_router
from .files import router as files_router
from .knowledge import router as knowledge_router

router = APIRouter()

router.include_router(agents_router, prefix="/agents", tags=["Agent"])
router.include_router(files_router, prefix="/files", tags=["Files"])
router.include_router(knowledge_router, prefix="/knowledge", tags=["Knowledge"])
