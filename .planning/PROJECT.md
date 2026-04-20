# 智能招投标审查平台（法律法规知识库专项）

## What This Is

本项目是智能招投标审查平台的一期专项子目标：基于 `docs/dataset/zhaobiao-toubiao` 中的法律法规数据，构建可检索、可追溯、可版本化的 `laws_regulations` 知识库能力。  
本期交付聚焦知识库构建与 API 能力，不包含完整生成式问答链路。

## Core Value

在招投标审查场景下，系统能够稳定返回“准确且可定位到法条原文”的法规检索结果。

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] 以不标记版 JSONL 为唯一权威入库源，完成 `laws_regulations` 标准化入库
- [ ] 提供知识库 API（入库/重建/检索）并命名与技术栈规范对齐
- [ ] 检索结果包含可追溯元数据（法名、章节、来源文件、chunk_id）
- [ ] 建立基础评测与验收口径（Recall、引用完整、响应时延）

### Out of Scope

- 完整生成式 RAG 问答链路（答案生成、拒答策略、重排编排）— 本期先完成可复用检索基础
- 知识图谱构建与图谱融合检索 — 后续阶段增量扩展

## Context

- 现有后端技术栈为 FastAPI + Qdrant + Neo4j，知识库类型中已定义 `laws_regulations`
- 数据集位于 `docs/dataset/zhaobiao-toubiao`，包含《招标投标法》与《实施条例》两份不标记版 JSONL
- 标记版文件仅在行尾添加 `&&&&`，不作为本期权威入库源

## Constraints

- **Data Source**: 必须使用不标记版 JSONL — 保证每行可直接 JSON 解析
- **Naming**: 集合与接口命名需对齐既有技术栈与知识库类型 — 降低后续集成成本
- **Architecture**: 本期以“知识库层 + API”交付为边界 — 避免提前耦合完整 RAG 编排
- **Traceability**: 返回结果必须可追溯到法规原文位置 — 支持审查解释与人工复核

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 使用不标记版 JSONL 作为入库源 | 数据是合法 JSONL，解析稳定，避免尾部标记污染 | ✓ Good |
| 本期包含知识库 API | 需要为 Agent 调用提供服务化入口 | ✓ Good |
| 命名对齐 `laws_regulations` 技术栈约定 | 与现有知识库类型和架构文档一致 | ✓ Good |
| 本期不交付完整生成式 RAG | 先做稳固检索底座，降低重构风险 | ✓ Good |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? -> Move to Out of Scope with reason
2. Requirements validated? -> Move to Validated with phase reference
3. New requirements emerged? -> Add to Active
4. Decisions to log? -> Add to Key Decisions
5. "What This Is" still accurate? -> Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check - still the right priority?
3. Audit Out of Scope - reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-20 after initialization*
