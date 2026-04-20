---
phase: 03-ji-xian-ping-ce-yu-yan-shou
plan: 02
subsystem: testing
tags: [acceptance-gate, baseline-runner, error-contract, quality]
requires:
  - phase: 03-ji-xian-ping-ce-yu-yan-shou
    provides: baseline_eval core and 30 eval cases
provides:
  - 可执行基线评测脚本与阈值阻塞闸门
  - 阈值阻塞与退出码回归测试
  - API 异常语义回归增强（QUAL-03）
affects: [release-gate, quality-baseline]
tech-stack:
  added: []
  patterns: [hard-fail-gate, structured-failure-report]
key-files:
  created:
    - bid_tool_agents/backend/app/scripts/evaluate_knowledge_baseline.py
    - bid_tool_agents/backend/tests/knowledge_eval/test_baseline_acceptance_gate.py
  modified:
    - bid_tool_agents/backend/app/domain/knowledge_eval/baseline_eval.py
    - bid_tool_agents/backend/tests/api/test_knowledge_query_api.py
key-decisions:
  - "任一阈值不达标或出现依赖异常均 blocked=true 且返回非0退出码。"
  - "报告中仅输出 failure_reason/request_id 等可诊断字段，避免泄露内部细节。"
patterns-established:
  - "离线评测脚本输出结构化 JSON 报告，包含阈值对比与 remediation。"
  - "异常路径保持阻塞优先，不吞错通过。"
requirements-completed: [QUAL-02, QUAL-03]
duration: 40min
completed: 2026-04-20
---

# Phase 3 Plan 02: 验收闸门与错误语义 Summary

**上线可执行的基线验收闸门脚本，严格执行 Recall/MRR/Latency 阈值并在异常场景下阻塞发布。**

## Performance

- **Duration:** 40 min
- **Started:** 2026-04-20T16:50:00Z
- **Completed:** 2026-04-20T17:30:00Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- 新增 `evaluate_knowledge_baseline.py`，可执行30样例评测并输出结构化报告。
- 实现硬闸门：Recall>=0.80、MRR>=0.60、p95<=1500ms，未达标即 `blocked` + 非0退出码。
- 增强 API/评测异常语义回归，确保 `error_code/message/details/request_id` 与 failure 聚合可诊断。

## Task Commits

1. **Task 1: 实现基线评测执行脚本与阻塞闸门** - `11edeb1` (feat)
2. **Task 2: 补强 QUAL-03 错误语义验收与异常数据场景** - `ab70b5a` (fix)

## Files Created/Modified
- `bid_tool_agents/backend/app/scripts/evaluate_knowledge_baseline.py` - 评测入口、阈值闸门、报告输出与退出码。
- `bid_tool_agents/backend/tests/knowledge_eval/test_baseline_acceptance_gate.py` - 阈值阻塞、failure_reason、malformed case 回归。
- `bid_tool_agents/backend/app/domain/knowledge_eval/baseline_eval.py` - 保留异常 request_id 到评测结果。
- `bid_tool_agents/backend/tests/api/test_knowledge_query_api.py` - 强化错误契约断言。

## Decisions Made
- 选择 JSON 结构化报告格式，便于后续 CI 与闸门解析。
- 对 dependency error 场景默认 blocked，确保“阻塞优先、错误显式”。

## Deviations from Plan
None - plan executed exactly as written.

## Threat Flags
None.

## Known Stubs
None.

## Issues Encountered
- `gsd-sdk` 不可用导致无法调用自动 state handlers，改为手工同步 `.planning` 文档状态。

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Phase 3 验收闸门能力已完整，可作为后续阶段的发布前硬门槛。
- QUAL-02/03 均具备自动化回归覆盖。

## Self-Check: PASSED
- Summary 文件已创建。
- 任务提交 `11edeb1`、`ab70b5a` 可在 git log 查询。

---
*Phase: 03-ji-xian-ping-ce-yu-yan-shou*
*Completed: 2026-04-20*
