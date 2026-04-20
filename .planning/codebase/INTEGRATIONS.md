# External Integrations

**Analysis Date:** 2026-04-20

## APIs & External Services

**LLM Inference Services:**
- Alibaba DashScope (Qwen) - 云端聊天推理接口
  - SDK/Client: `httpx`（`bid_tool_agents/backend/app/tools/llm/api/qwen.py`）
  - Auth: `ALI_API_KEY`
- Private Qwen (OpenAI-compatible endpoint) - 私有化聊天与向量接口
  - SDK/Client: `httpx`（`bid_tool_agents/backend/app/tools/llm/private/qwen_private.py`）
  - Auth: `PRIVATE_API_KEY`（地址来自 `PRIVATE_QWEN_URL`）
- Private DeepSeek (OpenAI-compatible endpoint) - 私有化聊天与向量接口
  - SDK/Client: `httpx`（`bid_tool_agents/backend/app/tools/llm/private/deepseek.py`）
  - Auth: `PRIVATE_API_KEY`（地址来自 `DEEPSEEK_URL`）

**Document Parsing Services:**
- Unstructured 云解析（可选）- PDF 分区解析
  - SDK/Client: `unstructured`（`bid_tool_agents/backend/app/tools/document/parser.py`）
  - Auth: 解析器入参 `api_key`
- Local OCR 解析 - 本地 PaddleOCR / PyMuPDF / python-docx
  - SDK/Client: `paddleocr`、`PyMuPDF`、`python-docx`（`bid_tool_agents/backend/app/tools/document/parser.py`）
  - Auth: Not applicable

## Data Storage

**Databases:**
- PostgreSQL
  - Connection: `database.host` / `database.user` / `database.password`
  - Client: SQLAlchemy + `psycopg2-binary` / `asyncpg` in `bid_tool_agents/backend/app/tools/database/postgres.py`
- Qdrant (vector DB)
  - Connection: `vector_db.host` / `vector_db.port`
  - Client: `qdrant-client` in `bid_tool_agents/backend/app/tools/database/qdrant.py`
- Neo4j (graph DB)
  - Connection: `graph_db.host` / `graph_db.user` / `graph_db.password`
  - Client: `neo4j` driver in `bid_tool_agents/backend/app/tools/database/neo4j.py`

**File Storage:**
- Local filesystem only
  - Paths: `storage.upload_dir` / `storage.parsed_dir` / `storage.report_dir` in `bid_tool_agents/backend/app/config.py` and `bid_tool_agents/backend/config/*.yaml`

**Caching:**
- Redis
  - Client: `redis.asyncio` in `bid_tool_agents/backend/app/tools/database/redis.py`
  - Connection: `redis.host` / `redis.password` in `bid_tool_agents/backend/config/*.yaml`

## Authentication & Identity

**Auth Provider:**
- Custom（未接入第三方身份平台）
  - Implementation: 前端本地 token 存储在 `bid_tool_agents/frontend/src/stores/user.ts`
  - API usage: 登录请求发往 `/api/v1/auth/login`（`bid_tool_agents/frontend/src/pages/Login.vue`），后端对应路由未在 `bid_tool_agents/backend/app/api/v1/router.py` 中检测到

## Monitoring & Observability

**Error Tracking:**
- None detected (no Sentry/Datadog/Rollbar integration files or imports detected)

**Logs:**
- File logging path configured by `app.log_file` in `bid_tool_agents/backend/app/config.py` and `bid_tool_agents/backend/config/*.yaml`

## CI/CD & Deployment

**Hosting:**
- Backend: containerized FastAPI/Uvicorn service in `bid_tool_agents/backend/Dockerfile`
- Frontend: Nginx static hosting + reverse proxy in `bid_tool_agents/frontend/Dockerfile` and `bid_tool_agents/frontend/nginx.conf`

**CI Pipeline:**
- Not detected

## Environment Configuration

**Required env vars:**
- `ENV`
- `POSTGRES_HOST`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- `QDRANT_HOST`
- `NEO4J_HOST`, `NEO4J_USER`, `NEO4J_PASSWORD`
- `REDIS_HOST`, `REDIS_PASSWORD`
- `ALI_API_KEY`
- `PRIVATE_QWEN_URL`, `DEEPSEEK_URL`, `PRIVATE_API_KEY`
- `VITE_API_BASE_URL` type declaration exists in `bid_tool_agents/frontend/src/vite-env.d.ts`

**Secrets location:**
- Environment variables via `.env` (loaded in `bid_tool_agents/backend/app/config.py`) and `${...}` interpolation in `bid_tool_agents/backend/config/production.yaml`

## Webhooks & Callbacks

**Incoming:**
- None detected (no webhook endpoint routes identified in `bid_tool_agents/backend/app/api/v1`)

**Outgoing:**
- LLM HTTP POST calls in `bid_tool_agents/backend/app/tools/llm/api/qwen.py`, `bid_tool_agents/backend/app/tools/llm/private/qwen_private.py`, and `bid_tool_agents/backend/app/tools/llm/private/deepseek.py`
- Frontend uploads and deletes files through `/api/v1/files/*` in `bid_tool_agents/frontend/src/components/file/FileUploader.vue` and `bid_tool_agents/frontend/src/pages/Upload.vue`

---

*Integration audit: 2026-04-20*
