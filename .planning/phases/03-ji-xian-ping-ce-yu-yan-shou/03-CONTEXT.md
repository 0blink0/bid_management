# Phase 3: 基线评测与验收 - Context

**Gathered:** 2026-04-20
**Status:** Ready for planning

<domain>
## Phase Boundary

围绕已落地的法规知识库检索 API，建立最小可复用评测样例集、离线评测执行入口与验收门槛，输出可量化的 Recall@5、MRR、延时基线，并在不达标时给出阻塞结论与修复入口。

</domain>

<decisions>
## Implementation Decisions

### 评测样例集
- **D-01:** 样例来源优先基于现有法规 JSONL 抽样构建，不额外引入新数据源。
- **D-02:** 基线样本量定为 30 条，先建立可执行闭环。
- **D-03:** 每条样本最小标注结构为 `query + golden_chunk_id`。
- **D-04:** 样例文件放在 `bid_tool_agents/backend/tests/fixtures/knowledge_eval_cases.jsonl`。

### 指标口径
- **D-05:** Recall@5 采用“Top5 中命中任一目标 chunk 记 1”。
- **D-06:** MRR 采用标准定义：首个相关命中的倒数排名。
- **D-07:** 延时输出口径为 `avg + p50 + p95`。
- **D-08:** 评测默认知识库范围固定为 `laws_regulations`。

### 验收门槛
- **D-09:** Recall@5 通过线为 `>= 0.80`。
- **D-10:** MRR 通过线为 `>= 0.60`。
- **D-11:** 延时通过线为 `p95 <= 1500ms`。
- **D-12:** 任一指标未达标即阻塞并产出修复计划（不允许警告即通过）。

### Claude's Discretion
- 评测执行器采用脚本入口还是 pytest 参数化实现，允许在不违背 D-05~D-12 的前提下由规划/执行阶段决定。
- 评测报告输出格式可在 `json/markdown` 间择优，但必须可复用并可追溯到样例版本。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 阶段与需求边界
- `.planning/ROADMAP.md` — Phase 3 目标与成功标准。
- `.planning/REQUIREMENTS.md` — QUAL-01/02/03 约束与追踪。
- `.planning/STATE.md` — 当前阶段状态。

### 既有能力基线
- `.planning/phases/02-fa-gui-zhi-shi-ku-api/02-CONTEXT.md` — API 契约与错误模型。
- `.planning/phases/02-fa-gui-zhi-shi-ku-api/02-01-SUMMARY.md` — 查询 API 交付结果。
- `.planning/phases/02-fa-gui-zhi-shi-ku-api/02-02-SUMMARY.md` — 异步重建与任务状态交付结果。
- `bid_tool_agents/backend/app/api/v1/knowledge.py` — 评测目标接口实现。
- `bid_tool_agents/backend/tests/api/test_knowledge_query_api.py` — 现有查询契约测试样例。

### 数据源约束
- `docs/dataset/zhaobiao-toubiao/中华人民共和国招标投标法.jsonl`
- `docs/dataset/zhaobiao-toubiao/中华人民共和国招标投标法实施条例.jsonl`

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- 已有 `POST /api/v1/knowledge/query` 可直接作为评测入口。
- `tests/api/test_knowledge_query_api.py` 已覆盖响应结构、排序和错误语义，可复用断言模式。

### Established Patterns
- 测试体系基于 pytest，适合新增 fixture + 评测 runner。
- 错误模型已统一为 `error_code/message/details/request_id`，可直接纳入 QUAL-03 校验。

### Integration Points
- 新评测样例文件需与现有测试目录组织保持一致（`tests/fixtures`）。
- 评测 runner 需直接调用现有 API 或核心检索链路，并输出 Recall/MRR/Latency 报告。

</code_context>

<specifics>
## Specific Ideas

- 基线阶段先保证“可重复运行 + 指标可解释”，再考虑扩样或引入混合召回对比。
- 评测失败必须进入修复闭环，避免形成“有指标但不驱动质量提升”的空转。

</specifics>

<deferred>
## Deferred Ideas

- 多知识库类型并行评测（本阶段固定 `laws_regulations`）。
- 更复杂样本标注（多 gold、人工语义等价集合）放后续增强。

</deferred>

---

*Phase: 03-ji-xian-ping-ce-yu-yan-shou*
*Context gathered: 2026-04-20*
