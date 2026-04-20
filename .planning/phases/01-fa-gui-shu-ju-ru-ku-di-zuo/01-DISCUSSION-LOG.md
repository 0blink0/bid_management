# Phase 1: 法规数据入库底座 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md.

**Date:** 2026-04-20
**Phase:** 01-fa-gui-shu-ju-ru-ku-di-zuo
**Areas discussed:** 入库数据模型, 切分与向量策略, 幂等重建策略, 导入执行与容错

---

## 入库数据模型

| Option | Description | Selected |
|--------|-------------|----------|
| 只保留最小字段 | 仅基础字段，后续再扩展 | |
| 增加 article_no | 增强法条级追溯 | ✓ |
| 增加完整定位 | article_no + paragraph_no + line_range | |

**User's choice:** 增加 `article_no`

| Option | Description | Selected |
|--------|-------------|----------|
| 稳定哈希 | 基于 title+chapter+content，重建稳定 | ✓ |
| 顺序号 | file-0001 等 | |
| UUID | 简单但不稳定 | |

**User's choice:** `chunk_id` 使用稳定哈希

| Option | Description | Selected |
|--------|-------------|----------|
| 数据集版本 | 版本号代表入库批次 | ✓ |
| 法规修订版本 | 版本号代表法律修订 | |
| 两者并存 | version + law_revision | |

**User's choice:** `version` 采用数据集版本

| Option | Description | Selected |
|--------|-------------|----------|
| 相对路径 | 可迁移可追溯 | ✓ |
| 文件名 | 简短但歧义更高 | |
| 绝对路径 | 环境耦合高 | |

**User's choice:** `source_file` 存相对路径

---

## 切分与向量策略

| Option | Description | Selected |
|--------|-------------|----------|
| 按条切分 | 与数据结构一致 | ✓ |
| 按段切分 | 粒度更细 | |
| 混合切分 | 复杂度更高 | |

**User's choice:** 按条切分

| Option | Description | Selected |
|--------|-------------|----------|
| 不拆分 | 简单但可能超长 | |
| 语义分段 + overlap | 兼顾语义与召回 | ✓ |
| 固定长度硬切 | 快但语义断裂风险 | |

**User's choice:** 超长条目语义分段 + overlap

| Option | Description | Selected |
|--------|-------------|----------|
| 固定 1536 | 与现有封装一致 | ✓ |
| 配置化维度 | 更灵活 | |
| 自动探测 | 实现复杂 | |

**User's choice:** 维度固定 `1536`

| Option | Description | Selected |
|--------|-------------|----------|
| 仅子片段 | 节省空间 | |
| 全文 + 子片段 | 兼顾追溯与展示 | ✓ |
| 仅全文 | 检索粒度不足 | |

**User's choice:** payload 保留全文和子片段

---

## 幂等重建策略

| Option | Description | Selected |
|--------|-------------|----------|
| 删集合后重建 | 最干净、可预测 | ✓ |
| 仅 upsert | 快但可能遗留脏数据 | |
| 版本集合+别名 | 稳定但复杂 | |

**User's choice:** 删集合后全量重建

| Option | Description | Selected |
|--------|-------------|----------|
| force=true 保护 | 降低误操作风险 | ✓ |
| 直接允许重建 | 简化流程 | |
| confirm token | 安全但复杂 | |

**User's choice:** 必须显式 `force=true`

| Option | Description | Selected |
|--------|-------------|----------|
| 固定全量重建 | 规则清晰 | ✓ |
| 按 source_file 局部重建 | 灵活性更高 | |
| 按 chapter 局部重建 | 灵活性更高 | |

**User's choice:** 固定全量重建

| Option | Description | Selected |
|--------|-------------|----------|
| 保存审计记录 | 可追踪每次重建 | ✓ |
| 仅日志 | 结构化不足 | |
| 不审计 | 风险高 | |

**User's choice:** 保存结构化审计记录

---

## 导入执行与容错

| Option | Description | Selected |
|--------|-------------|----------|
| 脚本优先 | 先稳底座 | ✓ |
| API 优先 | 服务化更快 | |
| 同时做 | 范围更大 | |

**User's choice:** 脚本入口优先

| Option | Description | Selected |
|--------|-------------|----------|
| fail-fast | 保证一致性 | ✓ |
| 跳过继续 | 完整性风险 | |
| 失败阈值继续 | 复杂度更高 | |

**User's choice:** fail-fast

| Option | Description | Selected |
|--------|-------------|----------|
| 严格预检 | 提前拦截错误 | ✓ |
| 轻量预检 | 覆盖不足 | |
| 不预检 | 风险高 | |

**User's choice:** 严格预检

| Option | Description | Selected |
|--------|-------------|----------|
| 摘要 + 错误明细 | 可诊断性好 | ✓ |
| 仅摘要 | 细节不足 | |
| 逐条报告 | 过重 | |

**User's choice:** 摘要 + 错误明细

---

## Claude's Discretion

- 语义分段阈值与 overlap 比例的具体参数。
- 审计信息落库或落文件的具体实现方式。

## Deferred Ideas

- API 触发导入（Phase 2）。
- 局部重建能力（后续增强阶段评估）。
