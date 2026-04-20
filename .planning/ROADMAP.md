# ROADMAP: 智能招投标审查平台（法律法规知识库专项）

## Summary

- Phases: 3
- v1 requirements mapped: 11/11
- Scope: 法律法规知识库构建 + API 服务化 + 基础评测

## Phase 1: 法规数据入库底座

**Goal:** 完成不标记版法规数据到 `laws_regulations` 的标准化、可重建入库能力。  
**UI hint:** no

**Requirements:**
- INGEST-01
- INGEST-02
- INGEST-03
- INGEST-04

**Success Criteria:**
1. 可从 `docs/dataset/zhaobiao-toubiao` 的不标记版 JSONL 成功解析法规条目
2. 向量集合命名与知识库类型对齐（`laws_regulations`）
3. 每条入库数据具备追溯字段（title/chapter/source/chunk/version）
4. 多次重建不会导致不可控重复

**Execution Progress:**
- Plan `01-01`: Completed (`.planning/phases/01-fa-gui-shu-ju-ru-ku-di-zuo/01-01-SUMMARY.md`)
- Plan `01-02`: Completed (`.planning/phases/01-fa-gui-shu-ju-ru-ku-di-zuo/01-02-SUMMARY.md`)

## Phase 2: 法规知识库 API

**Goal:** 提供可被 Agent 直接调用的法规知识库入库与检索 API。  
**UI hint:** no

**Requirements:**
- KAPI-01
- KAPI-02
- KAPI-03
- KAPI-04

**Success Criteria:**
1. API 可触发导入或重建任务
2. API 可执行语义检索并支持 knowledge type 过滤
3. API 返回命中分数与追溯元数据
4. 错误场景有可诊断响应

**Plans:** 2 plans

Plans:
- [x] 02-01-PLAN.md — 固化检索契约（默认类型、limit 截断、统一错误）并完成 KAPI-02/03/04 回归
- [x] 02-02-PLAN.md — 交付异步重建任务触发与状态查询 API，完成 KAPI-01 回归

**Execution Progress:**
- Plan `02-01`: Completed (`.planning/phases/02-fa-gui-zhi-shi-ku-api/02-01-SUMMARY.md`)
- Plan `02-02`: Completed (`.planning/phases/02-fa-gui-zhi-shi-ku-api/02-02-SUMMARY.md`)

## Phase 3: 基线评测与验收

**Goal:** 建立法规检索能力的可量化验收基线。  
**UI hint:** no

**Requirements:**
- QUAL-01
- QUAL-02
- QUAL-03

**Success Criteria:**
1. 具备最小评测样例集与评测执行入口
2. 能输出 Recall@5、MRR 与延时数据
3. 形成可复用验收结论，支撑后续 RAG/图谱扩展

**Plans:** 2 plans

Plans:
- [x] 03-01-PLAN.md — 交付 30 条评测样例与 Recall@5/MRR/Latency 统计器，固化 QUAL-01/02 基线口径
- [x] 03-02-PLAN.md — 落地阈值阻塞验收闸门与错误语义回归，确保 QUAL-02/03 未达标即阻塞

---

## Requirement Mapping Table

| Requirement | Phase |
|-------------|-------|
| INGEST-01 | Phase 1 |
| INGEST-02 | Phase 1 |
| INGEST-03 | Phase 1 |
| INGEST-04 | Phase 1 |
| KAPI-01 | Phase 2 |
| KAPI-02 | Phase 2 |
| KAPI-03 | Phase 2 |
| KAPI-04 | Phase 2 |
| QUAL-01 | Phase 3 |
| QUAL-02 | Phase 3 |
| QUAL-03 | Phase 3 |
