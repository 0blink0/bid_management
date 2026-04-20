# Phase 3: 基线评测与验收 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-20
**Phase:** 03-基线评测与验收
**Areas discussed:** 评测样例集, 指标口径, 验收门槛

---

## 评测样例集

| Option | Description | Selected |
|--------|-------------|----------|
| 直接基于现有法规 JSONL 抽样构建 | 快速落地基线 | ✓ |
| 手工整理问答对 | 质量高但慢 | |
| 混合抽样+人工修订 | 折中方案 | |

| Option | Description | Selected |
|--------|-------------|----------|
| 30 条样本 | 轻量起步 | ✓ |
| 50 条样本 | 稳定性更好 | |
| 100 条样本 | 更全面但投入大 | |

| Option | Description | Selected |
|--------|-------------|----------|
| `query + golden_chunk_id` | 直接适配 Recall/MRR | ✓ |
| `query + 标题/章节` | 粒度较粗 | |
| `query + 多个可接受答案` | 标注成本更高 | |

| Option | Description | Selected |
|--------|-------------|----------|
| `backend/tests/fixtures/knowledge_eval_cases.jsonl` | 便于测试与评测复用 | ✓ |
| `docs/dataset/eval/...` | 偏文档化 | |
| 两处都放 | 维护成本更高 | |

---

## 指标口径

| Option | Description | Selected |
|--------|-------------|----------|
| Recall@5: Top5 命中任一目标即 1 | 标准检索召回口径 | ✓ |
| 仅 rank1 命中计 1 | 过严 | |
| 位置加权 | 更复杂 | |

| Option | Description | Selected |
|--------|-------------|----------|
| 标准 MRR（首个相关倒数排名） | 经典定义 | ✓ |
| 多相关项平均倒数 | 变体 | |
| 仅完全 chunk 匹配 | 过严 | |

| Option | Description | Selected |
|--------|-------------|----------|
| 延时输出 avg + p50 + p95 | 平衡可读性与稳定性 | ✓ |
| 仅 avg | 信息不足 | |
| 全分位（含 p99） | 可后续增强 | |

| Option | Description | Selected |
|--------|-------------|----------|
| 默认固定 `laws_regulations` | 与本期范围一致 | ✓ |
| CLI 传参 | 后续可扩展 | |
| 默认全类型 | 超出当前范围 | |

---

## 验收门槛

| Option | Description | Selected |
|--------|-------------|----------|
| Recall@5 >= 0.80 | 基线推荐阈值 | ✓ |
| Recall@5 >= 0.70 | 较宽松 | |
| Recall@5 >= 0.90 | 较严格 | |

| Option | Description | Selected |
|--------|-------------|----------|
| MRR >= 0.60 | 基线推荐阈值 | ✓ |
| MRR >= 0.50 | 较宽松 | |
| MRR >= 0.70 | 较严格 | |

| Option | Description | Selected |
|--------|-------------|----------|
| p95 <= 1500ms | 基线推荐阈值 | ✓ |
| p95 <= 1000ms | 更严格 | |
| p95 <= 2000ms | 更宽松 | |

| Option | Description | Selected |
|--------|-------------|----------|
| 未达标即阻塞并修复 | 强约束闭环 | ✓ |
| 仅告警 | 不足以驱动质量 | |
| 满足 2/3 即通过 | 风险较高 | |

---

## Claude's Discretion

- 评测执行入口是单脚本还是 pytest 包装，由计划阶段在不改变指标口径的前提下确定。

## Deferred Ideas

- 扩展到多知识库并行评测
- 引入更复杂的多 gold 标注与语义等价标注
