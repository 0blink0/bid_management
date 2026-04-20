# Phase 1: 法规数据入库底座 - Context

**Gathered:** 2026-04-20
**Status:** Ready for planning

<domain>
## Phase Boundary

构建可重建、可追溯的法规数据入库底座：从 `docs/dataset/zhaobiao-toubiao` 不标记版 JSONL 解析法规条目，标准化后写入 `laws_regulations` 向量集合，并确保重复执行可控。

</domain>

<decisions>
## Implementation Decisions

### 入库数据模型
- **D-01:** 在基础字段之外新增 `article_no`（条号）以增强法条级追溯能力。
- **D-02:** `chunk_id` 采用稳定哈希（基于 `title + chapter + content`），保证跨次重建稳定可复现。
- **D-03:** `version` 采用“数据集批次版本”语义（例如 `2026-04-20`），用于重建批次治理。
- **D-04:** `source_file` 存储仓库相对路径，而非绝对路径。

### 切分与向量策略
- **D-05:** 基础切分粒度按“条”处理，与当前 JSONL 结构保持一致。
- **D-06:** 对超长法条采用语义分段 + overlap，而非硬切。
- **D-07:** 向量维度当前固定为 `1536`，与现有 Qdrant 封装默认值一致。
- **D-08:** payload 同时保留“原文全文 + 子片段文本”，兼顾检索与溯源展示。

### 幂等重建策略
- **D-09:** 重建采用“删集合后全量重建”作为主策略，确保结果干净且可预测。
- **D-10:** 重建操作必须显式 `force=true` 才允许执行。
- **D-11:** Phase 1 固定全量重建 `laws_regulations`，不做 chapter/source 级局部重建。
- **D-12:** 记录结构化重建审计信息（时间、输入文件、条目数、版本）。

### 导入执行与容错
- **D-13:** Phase 1 先提供脚本入口，API 触发放在后续 Phase 2 落地。
- **D-14:** 导入失败策略为 fail-fast：单条解析失败即终止本次导入。
- **D-15:** 入库前执行严格预检（JSON 解析 + 必填字段校验），不通过不入库。
- **D-16:** 导入结果输出“摘要 + 错误明细”。

### Claude's Discretion
- 语义分段时的具体 overlap 数值和分段阈值（在不违背 D-06 前提下由实现阶段确定）。
- 审计记录的落地介质（本地文件、数据库表或任务日志）与字段扩展。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 需求与阶段边界
- `.planning/ROADMAP.md` — Phase 1 目标、验收标准与范围边界。
- `.planning/REQUIREMENTS.md` — INGEST-01~04 的需求定义与追踪关系。
- `.planning/PROJECT.md` — 项目约束（不标记版 JSONL、命名对齐、可追溯要求）。
- `.planning/STATE.md` — 当前里程碑状态与当前阶段焦点。

### 数据源规范
- `docs/dataset/zhaobiao-toubiao/README.md` — 数据集说明与标记版/不标记版差异。
- `docs/dataset/zhaobiao-toubiao/中华人民共和国招标投标法.jsonl` — 主法规原始数据样本。
- `docs/dataset/zhaobiao-toubiao/中华人民共和国招标投标法实施条例.jsonl` — 实施条例原始数据样本。

### 现有代码约束
- `bid_tool_agents/backend/app/api/v1/knowledge.py` — 已定义 `laws_regulations` 知识库类型，知识库 API 尚为 TODO。
- `bid_tool_agents/backend/app/tools/database/qdrant.py` — 现有集合创建、upsert、search 封装与默认向量维度。
- `bid_tool_agents/backend/app/config.py` — 当前默认集合名为 `bid_documents`，后续实现需与 `laws_regulations` 对齐。

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `bid_tool_agents/backend/app/tools/database/qdrant.py`：已有 `create_collection`、`upsert`、`search`、`delete` 能力，可直接复用为入库底座。
- `bid_tool_agents/backend/app/config.py`：已有 `vector_db` 配置对象，可承载 `collection_name` 与 `vector_size`。

### Established Patterns
- 后端 API 层普遍以 Pydantic 模型定义输入输出；知识库 API 已有路由骨架但实现未完成。
- 数据库/中间件连接采用“初始化 + 全局获取”模式（如 `init_qdrant` / `get_qdrant`）。

### Integration Points
- Phase 1 入库脚本可先直连 `qdrant.py`；Phase 2 再通过 `api/v1/knowledge.py` 暴露服务化入口。
- `VectorDBConfig.collection_name` 当前默认值与路线图目标不一致，是落地阶段必须对齐的关键接点。

</code_context>

<specifics>
## Specific Ideas

- 数据追溯优先级高于最小存储成本：保留全文与切片双字段，便于后续审查解释。
- 幂等策略优先“确定性与可审计”，而非最小写入开销。

</specifics>

<deferred>
## Deferred Ideas

- API 触发导入任务（属于 Phase 2：法规知识库 API）。
- 局部重建（按 `source_file/chapter`）能力，后续可作为增强项评估。

</deferred>

---

*Phase: 01-fa-gui-shu-ju-ru-ku-di-zuo*
*Context gathered: 2026-04-20*
