"""
智能招投标审查平台 - FastAPI入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.api.v1.router import router as api_router
from app.tools.database.qdrant import init_qdrant


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    settings = get_settings()
    # 启动时初始化
    print(f"Starting {settings.app.app_name}...")
    print(f"Environment: {settings.ENV}")
    try:
        qdrant = init_qdrant(settings.vector_db.url, settings.vector_db.port)
        qdrant.client.get_collections()
        print("Qdrant initialized.")
    except Exception as exc:  # noqa: BLE001
        print(f"Qdrant init warning: {exc}")
    yield
    # 关闭时清理
    print("Shutting down...")


def create_app() -> FastAPI:
    """创建FastAPI应用"""
    settings = get_settings()

    app = FastAPI(
        title=settings.app.app_name,
        description="智能招投标审查平台 API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )

    # CORS配置
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.app.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册路由
    app.include_router(api_router, prefix=settings.app.api_prefix)

    return app


app = create_app()


@app.get("/")
async def root():
    """根路径"""
    return {"message": "智能招投标审查平台 API", "version": "0.1.0"}


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy"}
