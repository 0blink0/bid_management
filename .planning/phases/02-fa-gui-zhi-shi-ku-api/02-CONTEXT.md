# Phase 2: 法规知识库 API - Context

**Gathered:** 2026-04-20
**Status:** Ready for planning

<domain>
## Phase Boundary

交付可被 Agent 直接调用的法规知识库 API，覆盖法规入库/重建触发、语义检索、错误可诊断响应，并默认围绕 `laws_regulations` 运行。

</domain>

<decisions>
## Implementation Decisions

### API 契约
- **D-01:** 入库触发采用 `POST /knowledge/ingest/rebuild`，使用显式重建语义。
- **D-02:** 检索采用 `POST /knowledge/query`，请求体承载 `query/knowledge_type/limit`。
- **D-03:** 检索响应采用固定结构：`items[] + total + took_ms + trace`。
- **D-04:** 命中条目元数据最小必带：`title/chapter/source_file/chunk_id/version/score`。

### 检索行为
- **D-05:** `knowledge_type` 缺省时默认 `laws_regulations`。
- **D-06:** `limit` 默认 10，最大 50；超出上限自动截断。
- **D-07:** 命中结果按 `score` 降序，返回浮点分值。

### 错误模型
- **D-08:** 请求参数校验失败使用 HTTP 422。
- **D-09:** 下游依赖失败（向量库/Embedding 等）使用 HTTP 503，返回 `retryable=true`。
- **D-10:** 错误响应结构统一为 `error_code/message/details/request_id`。

### 执行模式
- **D-11:** 入库/重建接口采用异步任务模型，返回 `task_id`。
- **D-12:** 任务状态查询接口采用 `GET /knowledge/tasks/{task_id}`。

### Claude's Discretion
- `trace` 字段的详细内容（如耗时分项、召回来源标记）可在实现阶段按现有日志体系落地。
- 异步任务的落地介质（内存、Redis、数据库）由实现阶段按现有栈复用模式确定。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 阶段与需求边界
- `.planning/ROADMAP.md` — Phase 2 的目标、验收标准与范围边界。
- `.planning/REQUIREMENTS.md` — KAPI-01~04 的定义与追踪关系。
- `.planning/PROJECT.md` — 数据源、命名、可追溯等全局约束。
- `.planning/STATE.md` — 当前阶段与里程碑状态。

### 上一阶段实现与可复用能力
- `.planning/phases/01-fa-gui-shu-ju-ru-ku-di-zuo/01-CONTEXT.md` — 已锁定的数据模型、幂等重建和审计决策。
- `bid_tool_agents/backend/app/domain/knowledge_ingest/` — Phase 1 已落地的入库领域能力（loader/chunker/writer/audit）。

### API 与配置接入点
- `bid_tool_agents/backend/app/api/v1/knowledge.py` — Phase 2 的主要接口实现入口（当前为 TODO 骨架）。
- `bid_tool_agents/backend/app/tools/database/qdrant.py` — 检索/写入底层能力与集合操作封装。
- `bid_tool_agents/backend/app/config.py` — 向量库配置入口（collection 默认值需与 `laws_regulations` 对齐策略评估）。

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `knowledge.py` 已有 `query/types/add/delete` 路由骨架与 Pydantic 请求模型，可直接扩展为 Phase 2 契约。
- `knowledge_ingest.writer.rebuild_laws_collection` 已可作为异步任务执行目标。
- `qdrant.py` 提供 `search/upsert/create/delete_collection`，可复用为 API 后端能力。

### Established Patterns
- 后端接口采用 FastAPI + Pydantic；错误优先通过 HTTP 状态码表达。
- 配置通过 `get_settings()` 获取，便于统一注入 `knowledge_type` 默认值与上限策略。

### Integration Points
- `POST /knowledge/ingest/rebuild` 需要编排 `knowledge_ingest` 模块并记录任务状态。
- `POST /knowledge/query` 需要串联 embedding 与 qdrant search，再映射为标准返回结构。
- `GET /knowledge/tasks/{task_id}` 需要统一任务状态模型，供 Agent 轮询调用。

</code_context>

<specifics>
## Specific Ideas

- API 契约优先保证 Agent 稳定调用，不追求一次覆盖所有知识库类型的复杂能力。
- 错误返回必须可诊断，避免仅返回通用失败文案。

</specifics>

<deferred>
## Deferred Ideas

- 多知识库“全类型默认搜索”能力（本阶段先固定默认 `laws_regulations`）。
- 复杂重排或业务加权排序（本阶段仅按 score 降序）。

</deferred>

---

*Phase: 02-fa-gui-zhi-shi-ku-api*
*Context gathered: 2026-04-20*
