---
phase: 03-ji-xian-ping-ce-yu-yan-shou
plan: 01
subsystem: testing
tags: [baseline-eval, recall, mrr, latency, laws-regulations]
requires:
  - phase: 02-fa-gui-zhi-shi-ku-api
    provides: /api/v1/knowledge/query contract and error model
provides:
  - 30条固定评测样例（query + golden_chunk_id）
  - 评测核心（load/evaluate/summarize）
  - QUAL-01/02 指标回归测试
affects: [phase-3-gate, quality-acceptance]
tech-stack:
  added: []
  patterns: [jsonl-eval-fixture, deterministic-offline-metrics]
key-files:
  created:
    - bid_tool_agents/backend/tests/fixtures/knowledge_eval_cases.jsonl
    - bid_tool_agents/backend/app/domain/knowledge_eval/baseline_eval.py
    - bid_tool_agents/backend/tests/knowledge_eval/test_baseline_eval_metrics.py
  modified: []
key-decisions:
  - "样例全部由现有法规 JSONL 经既有 loader 生成稳定 chunk_id，避免外部数据漂移。"
  - "评测口径固定为 Recall@5、MRR、Latency(avg/p50/p95)，并由单测锁定。"
patterns-established:
  - "评测加载阶段 schema fail-fast：缺 query/golden_chunk_id 直接报错。"
  - "单条评测失败不吞错，保留 failure_reason 供后续闸门汇总。"
requirements-completed: [QUAL-01, QUAL-02]
duration: 45min
completed: 2026-04-20
---

# Phase 3 Plan 01: 基线评测样例与指标核心 Summary

**交付30条可复用法规评测样例与可复现的 Recall@5/MRR/Latency 统计核心，为验收闸门提供稳定输入。**

## Performance

- **Duration:** 45 min
- **Started:** 2026-04-20T16:05:00Z
- **Completed:** 2026-04-20T16:50:00Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- 新建 `knowledge_eval_cases.jsonl`，固定30条样例，字段严格为 `query/golden_chunk_id`。
- 新建 `baseline_eval.py`，实现 `load_eval_cases/evaluate_cases/summarize_metrics`。
- 新建 `test_baseline_eval_metrics.py`，覆盖样例约束、Recall@5、MRR、Latency 口径与边界。

## Task Commits

1. **Task 1: 构建 30 条固定评测样例集** - `277eeb5` (feat)
2. **Task 2: 实现 Recall@5/MRR/Latency 统计器** - `e620472` (feat)

## Files Created/Modified
- `bid_tool_agents/backend/tests/fixtures/knowledge_eval_cases.jsonl` - 30条固定基线样例。
- `bid_tool_agents/backend/app/domain/knowledge_eval/baseline_eval.py` - 样例加载、逐条评测、指标汇总。
- `bid_tool_agents/backend/tests/knowledge_eval/test_baseline_eval_metrics.py` - 指标与样例约束测试。

## Decisions Made
- 使用现有 `knowledge_ingest.loader` 生成稳定 `chunk_id` 来源，保证样例可追溯。
- 默认评测知识库类型固定 `laws_regulations`，与 Phase 2 API 契约一致。

## Deviations from Plan
None - plan executed exactly as written.

## Issues Encountered
- `gsd-sdk` 在当前环境不可用（命令不存在），因此改为手动更新 `.planning` 状态文件。

## Known Stubs
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- 已具备可复用离线评测样例与指标核心，可直接接入阈值闸门。
- QUAL-01/02 已由自动化测试覆盖。

## Self-Check: PASSED
- Summary 文件已创建。
- 任务提交 `277eeb5`、`e620472` 可在 git log 查询。

---
*Phase: 03-ji-xian-ping-ce-yu-yan-shou*
*Completed: 2026-04-20*
