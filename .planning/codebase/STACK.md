# Technology Stack

**Analysis Date:** 2026-04-20

## Languages

**Primary:**
- Python (>=3.10) - backend API、Agent、数据库与文档处理，位于 `bid_tool_agents/backend/app`，版本约束在 `bid_tool_agents/backend/pyproject.toml`
- TypeScript (5.3.x) - 前端应用与类型系统，位于 `bid_tool_agents/frontend/src`，版本在 `bid_tool_agents/frontend/package.json`

**Secondary:**
- JavaScript (ESM) - 前端构建脚本与运行命令，位于 `bid_tool_agents/frontend/package.json`
- YAML - 多环境配置（dev/test/prod），位于 `bid_tool_agents/backend/config/development.yaml`、`bid_tool_agents/backend/config/testing.yaml`、`bid_tool_agents/backend/config/production.yaml`

## Runtime

**Environment:**
- Python 3.10 容器运行时：`bid_tool_agents/backend/Dockerfile` 使用 `python:3.10-slim`
- Node 20 构建运行时：`bid_tool_agents/frontend/Dockerfile` 使用 `node:20-alpine`
- Nginx 运行时：`bid_tool_agents/frontend/Dockerfile` 使用 `nginx:alpine` 托管前端静态产物

**Package Manager:**
- npm（前端）：`bid_tool_agents/frontend/package.json`
- Poetry + pip（后端 Docker 构建）：`bid_tool_agents/backend/Dockerfile` 中执行 `poetry install`
- Lockfile: 前端 `bid_tool_agents/frontend/package-lock.json` 已存在；后端 Poetry lockfile 未检测到

## Frameworks

**Core:**
- FastAPI (>=0.109.0) - 后端 Web/API 框架，入口 `bid_tool_agents/backend/app/main.py`
- Pydantic v2 + pydantic-settings - 配置与数据模型，`bid_tool_agents/backend/app/config.py`
- LangGraph + LangChain - Agent 编排与 LLM 调度，`bid_tool_agents/backend/pyproject.toml`
- Vue 3 + Pinia + Vue Router - 前端框架、状态与路由，`bid_tool_agents/frontend/package.json`

**Testing:**
- pytest + pytest-asyncio - 后端测试框架，`bid_tool_agents/backend/pytest.ini` 与 `bid_tool_agents/backend/tests/pytest.ini`

**Build/Dev:**
- Vite 5 - 前端 dev/build，`bid_tool_agents/frontend/package.json`
- vue-tsc - 前端类型检查，`bid_tool_agents/frontend/package.json`
- Uvicorn - 后端 ASGI 服务启动，`bid_tool_agents/backend/Dockerfile`

## Key Dependencies

**Critical:**
- `sqlalchemy` + `psycopg2-binary` + `asyncpg` - 关系型持久化，`bid_tool_agents/backend/app/tools/database/postgres.py`
- `qdrant-client` - 向量检索存储，`bid_tool_agents/backend/app/tools/database/qdrant.py`
- `neo4j` - 图谱存储访问，`bid_tool_agents/backend/app/tools/database/neo4j.py`
- `redis` - 缓存与短期记忆，`bid_tool_agents/backend/app/tools/database/redis.py`
- `httpx` - LLM 外部 HTTP 调用，`bid_tool_agents/backend/app/tools/llm/api/qwen.py` 与 `bid_tool_agents/backend/app/tools/llm/private/*.py`

**Infrastructure:**
- `unstructured`、`paddleocr`、`paddlepaddle`、`PyMuPDF`、`python-docx` - 文档解析/OCR，`bid_tool_agents/backend/app/tools/document/parser.py`
- `naive-ui`、`apexcharts`、`vue3-apexcharts` - 前端 UI 与可视化，`bid_tool_agents/frontend/package.json`
- `axios` - 前端 HTTP 客户端依赖（当前页面代码主要仍使用 `fetch`），`bid_tool_agents/frontend/package.json`

## Configuration

**Environment:**
- 统一配置入口：`bid_tool_agents/backend/app/config.py`，按 `ENV` 读取 YAML，并支持 `.env` 覆盖
- 环境配置文件：`bid_tool_agents/backend/config/development.yaml`、`bid_tool_agents/backend/config/testing.yaml`、`bid_tool_agents/backend/config/production.yaml`
- 前端环境变量类型声明：`bid_tool_agents/frontend/src/vite-env.d.ts`

**Build:**
- 前端容器与 Nginx：`bid_tool_agents/frontend/Dockerfile`、`bid_tool_agents/frontend/nginx.conf`
- 后端容器：`bid_tool_agents/backend/Dockerfile`
- 多服务编排：`bid_tool_agents/docker-compose.yaml`

## Platform Requirements

**Development:**
- 本地/容器需要 PostgreSQL、Redis、Qdrant、Neo4j 服务，连接字段在 `bid_tool_agents/backend/config/development.yaml`
- 前端默认对接 `/api/v1` 接口（页面代码示例：`bid_tool_agents/frontend/src/pages/Upload.vue`）

**Production:**
- 后端：FastAPI + Uvicorn（端口 8000），`bid_tool_agents/backend/Dockerfile`
- 前端：Vite 构建后由 Nginx 托管（端口 3000），`bid_tool_agents/frontend/Dockerfile`
- 基础设施：`bid_tool_agents/docker-compose.yaml` 编排 PostgreSQL/Redis/Qdrant/Neo4j/前后端

---

*Stack analysis: 2026-04-20*
